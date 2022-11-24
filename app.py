from datetime import datetime
import logging
import asyncio
from configparser import ConfigParser

from aiogram import Bot, Dispatcher, executor

# Логгер не обязателен, нужен для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Берем данные из config.ini
config = ConfigParser()
config.read('config.ini')
BOT_TOKEN = config['API']['BOT_TOKEN']
CHAT_ID = config['API']['CHAT_ID']
MESSAGE = config['API']['MESSAGE']
HOURS = int(config['API']['HOURS'])
MINUTES = int(config['API']['MINUTES'])

# Инициализируем бота и диспетчера(для работы с апи)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def get_weekday_message_send() -> list[int]:
    """Возвращает список дней недели, в которые нужно отправлять сообщение
    Данные берутся из config.ini"""
    weekdays = []
    count = 0
    config_weekdays = config['WEEKDAYS']
    for _, value in config_weekdays.items():
        if value == 'True':
            weekdays.append(count)
        count += 1
    return weekdays


async def send_message(chat_id: str, message: str, hours: int, minutes: int, weekdays: list[int]) -> None:
    """Отправляет сообщение в чат в каждые hours часов и minutes минут"""
    current_time = datetime.now()
    if (current_time.weekday() in weekdays):
        if (current_time.hour == hours and current_time.minute == minutes):
            await bot.send_message(chat_id, message)
            logger.info(f'Отправка сообщения: "{message}" в {current_time}')
            await asyncio.sleep(86400)
        else:
            await asyncio.sleep(60)
    else:
        await asyncio.sleep(3600)


def main():
    while True:
        executor.start(dp, send_message(CHAT_ID, MESSAGE, HOURS, MINUTES, get_weekday_message_send()))


if __name__ == '__main__':
    main()
