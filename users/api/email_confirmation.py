from fastapi import APIRouter
from pydantic import EmailStr

from common.smtp_server import send_email_confirmation_code

email_router = APIRouter(prefix="/email", tags=["Work with Emails"])


@email_router.post("/get-code-for-email-confirm")
async def get_code_for_email_confirm(receiver_email_address: EmailStr):
    send_email_confirmation_code(receiver_email_address)
    # TODO: add this code to redis

@email_router.post("/confirm-email-with-code")
async def confirm_email_with_code(confirmation_code: str):
    # compare input code with code in redis
    ...
