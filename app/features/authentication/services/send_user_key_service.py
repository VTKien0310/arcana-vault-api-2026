import asyncio
from typing import Annotated
from fastapi import Depends
from app.data import Key
from app.features.authentication.entities.key_entity import KeyChannel
from app.ports import TelegramPortDep


class SendUserKeyService:
    def __init__(self, telegram_port: TelegramPortDep):
        self.__telegram_port = telegram_port

    async def handle(self, key: Key) -> None:
        tasks = []
        if KeyChannel.TELEGRAM.value in key.channels:
            tasks.append(
                self.__telegram_port.send_message(key.telegram_chat_id, key.value)
            )

        await asyncio.gather(*tasks)


SendUserKeyServiceDep = Annotated[SendUserKeyService, Depends()]
