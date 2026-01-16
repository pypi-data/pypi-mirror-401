from temporalio import activity

from letta.services.webhook_service import WebhookService


@activity.defn(name="send_step_complete_webhook")
async def send_step_complete_webhook(step_id: str) -> bool:
    """
    Send webhook notification when a step completes.

    This activity sends a POST request to the configured webhook URL
    with the step ID. It uses the STEP_COMPLETE_WEBHOOK and STEP_COMPLETE_KEY
    environment variables for configuration.

    Args:
        step_id: The ID of the completed step

    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    webhook_service = WebhookService()
    return await webhook_service.notify_step_complete(step_id)
