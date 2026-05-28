import asyncio
from typing import Annotated
from fastapi import Depends
from app.core import settings
from app.data import Key
from app.features.authentication.entities import KeyChannel
from app.ports import TelegramPortDep


class SendUserKeyService:
    def __init__(self, telegram_port: TelegramPortDep):
        self.__telegram_port = telegram_port

    async def handle(self, key: Key) -> None:
        app_env = settings.ENVIRONMENT
        message = f"Your {app_env} key is: `{key.value}`"

        tasks = []
        if KeyChannel.TELEGRAM.value in key.channels and key.telegram_chat_id:
            tasks.append(
                self.__telegram_port.send_message(key.telegram_chat_id, message)
            )

        await asyncio.gather(*tasks)


SendUserKeyServiceDep = Annotated[SendUserKeyService, Depends()]
