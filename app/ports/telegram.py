from typing import Annotated
import httpx
from fastapi import Depends
from app.core import settings


class TelegramPort:
    def __init__(self):
        self.__bot_endpoint = (
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"
        )

    async def send_message(self, chat_id: str, text: str) -> bool:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                f"{self.__bot_endpoint}/sendMessage",
                json={"chat_id": chat_id, "text": text},
            )

            return response.json()["ok"]


TelegramPortDep = Annotated[TelegramPort, Depends()]
