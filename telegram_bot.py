import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import json
from utils import Handler, Request
from aiogram.exceptions import TelegramEntityTooLarge


from secret import KEY
TOKEN = KEY


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!") # type: ignore


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        text = message.text
        assert isinstance(text, str)
        data = json.loads(text.strip())
        request = Request(**data)
        handler = Handler(request)
        res = await handler.request_to_responce()
        await message.answer(json.dumps(res))
    except TypeError:
        await message.answer("TypeError!")
    except ValueError:
        await message.answer('Invalid data! (Expects JSON)')
    except TelegramEntityTooLarge:
        await message.answer('Responce too large!')
    except Exception as e:
        await message.answer(f'ERROR!   {str(e)}')


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())