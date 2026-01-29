from app.utils.di import create_backlog_context
from app.utils.ultils import update_issue_description_handler


async def update_issue_description(
    issue_key: str,
    description: str,
):
    """
    Update the description of a Backlog issue.

    Args:
        issue_key (str): The key or ID of the Backlog issue to update.
        description (str): The new description content for the issue.
    """
    try:
        if not issue_key:
            raise ValueError("Please provide an issue key.")
        if not description:
            raise ValueError("Please provide a description.")

        ctx = create_backlog_context()
        result = await update_issue_description_handler(
            backlog_domain=ctx.backlog_domain,
            api_key=ctx.api_key,
            issue_key=issue_key,
            description=description,
        )
        return result
    except Exception as e:
        raise e
