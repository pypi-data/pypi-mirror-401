import mimetypes
from pathlib import Path as PathLibPath
from typing import Optional

from temporalio import activity

from letta.agents.temporal.metrics import track_activity_metrics
from letta.agents.temporal.types import UploadFileToFolderParams, UploadFileToFolderResult
from letta.errors import LettaInvalidArgumentError, LettaUnsupportedFileUploadError
from letta.log import get_logger
from letta.schemas.enums import DuplicateFileHandling, FileProcessingStatus
from letta.schemas.file import FileMetadata
from letta.services.file_processor.file_types import (
    get_allowed_media_types,
    get_extension_to_mime_type_map,
)
from letta.utils import safe_create_file_processing_task, safe_create_task, sanitize_filename

logger = get_logger(__name__)


def _resolve_media_type(filename: str, provided_content_type: Optional[str]) -> str:
    """Resolve and validate the media type using same logic as REST handler."""
    allowed_media_types = get_allowed_media_types()

    raw_ct = (provided_content_type or "").strip()
    media_type = raw_ct.split(";", 1)[0].strip().lower() if raw_ct else ""

    if media_type not in allowed_media_types and filename:
        guessed, _ = mimetypes.guess_type(filename)
        media_type = (guessed or "").lower()

        if media_type not in allowed_media_types:
            ext = PathLibPath(filename).suffix.lower()
            ext_map = get_extension_to_mime_type_map()
            media_type = ext_map.get(ext, media_type)

    if media_type not in allowed_media_types:
        raise LettaUnsupportedFileUploadError(
            message=(
                f"Unsupported file type: {media_type or 'unknown'} (filename: {filename}). "
                f"Supported types: PDF, text files (.txt, .md), JSON, and code files (.py, .js, .java, etc.)."
            )
        )

    return media_type


@activity.defn(name="upload_file_to_folder_activity")
@track_activity_metrics
async def upload_file_to_folder_activity(params: UploadFileToFolderParams) -> UploadFileToFolderResult:
    """Temporal activity that mirrors the REST upload_file_to_folder logic end-to-end.

    Executes duplicate handling, creates FileMetadata, schedules file processing,
    and triggers sleeptime ingest. Returns FileMetadata and whether the upload
    was skipped due to duplicate handling.
    """
    # Resolve media type (validates allowed types)
    _ = _resolve_media_type(params.file_name, params.content_type)

    # Lazy import to avoid circular imports during module initialization
    from letta.server.rest_api.app import server as letta_server
    from letta.server.rest_api.routers.v1.folders import (
        load_file_to_source_cloud,
        sleeptime_document_ingest_async,
    )

    server = letta_server

    actor = await server.user_manager.get_actor_or_default_async(actor_id=params.actor_id)

    # Fetch folder (source) and agent states
    folder = await server.source_manager.get_source_by_id(source_id=params.folder_id, actor=actor)

    content = params.content
    file_size_mb = len(content) / (1024 * 1024) if content is not None else 0
    logger.info(f"Temporal upload_file_to_folder_activity: loaded {file_size_mb:.2f} MB into memory, filename: {params.file_name}")

    # Use custom name if provided; otherwise sanitize uploaded filename
    original_filename = params.override_name if params.override_name else sanitize_filename(params.file_name)

    # Duplicate handling
    existing_file = await server.file_manager.get_file_by_original_name_and_source(
        original_filename=original_filename, source_id=params.folder_id, actor=actor
    )

    unique_filename: Optional[str] = None
    skipped = False
    if existing_file:
        if params.duplicate_handling == DuplicateFileHandling.ERROR:
            raise LettaInvalidArgumentError(
                message=f"File '{original_filename}' already exists in folder '{folder.name}'",
                argument_name="duplicate_handling",
            )
        elif params.duplicate_handling == DuplicateFileHandling.SKIP:
            # Return existing metadata and mark skipped
            return UploadFileToFolderResult(file_metadata=existing_file, skipped=True)
        elif params.duplicate_handling == DuplicateFileHandling.REPLACE:
            await server.file_manager.delete_file(file_id=existing_file.id, actor=actor)
            unique_filename = original_filename

    if not unique_filename:
        unique_filename = await server.file_manager.generate_unique_filename(
            original_filename=original_filename, source=folder, organization_id=actor.organization_id
        )

    # Create file metadata
    file_metadata = FileMetadata(
        source_id=params.folder_id,
        file_name=unique_filename,
        original_file_name=original_filename,
        file_path=None,
        file_type=mimetypes.guess_type(original_filename)[0] or params.content_type or "unknown",
        file_size=len(content) if content is not None else None,
        processing_status=FileProcessingStatus.PARSING,
    )
    file_metadata = await server.file_manager.create_file(file_metadata, actor=actor)

    # Gather attached agents
    agent_states = await server.source_manager.list_attached_agents(source_id=params.folder_id, actor=actor)

    # Schedule cloud file processing (parsing + embedding)
    logger.info("Temporal: scheduling cloud-based file processing task...")
    safe_create_file_processing_task(
        load_file_to_source_cloud(
            server,
            agent_states,
            content,
            params.folder_id,
            actor,
            folder.embedding_config,
            file_metadata,
        ),
        file_metadata=file_metadata,
        server=server,
        actor=actor,
        logger=logger,
        label="file_processor.process",
    )

    # Trigger sleeptime ingest in background for any subscribed agents
    safe_create_task(
        sleeptime_document_ingest_async(server, params.folder_id, actor),
        label="sleeptime_document_ingest_async",
    )

    return UploadFileToFolderResult(file_metadata=file_metadata, skipped=skipped)
