# YuChat Bot Library

Python библиотека для создания ботов для корпоративного мессенджера [YuChat](https://www.yuchat.ai).

## Особенности

- Полная поддержка API YuChat
- Long Polling для получения обновлений
- FSM система состояний
- Поддержка Redis для хранения данных
- Обработка команд (команды начинающиеся с `/`)
- Встроенные декораторы для обработчиков
- Валидация данных через Pydantic
- Поддержка webhook

## Установка

```bash
pip install yuchatlib
```

## Быстрый старт

```python
import logging
import time

from yuchatlib import YuChatBot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot = YuChatBot(
    token="your_token",
    base_url="base_url",
    polling_interval=2,
    storage=None,
)


@bot.command(name="start", description="Начать работу с ботом")
def start_command(_bot, message, args):
    """Команда /start без fsm_context"""

    _bot.reply(
        message=message,
        text="👋 Привет! Я бот с поддержкой FSM.\n\n"
             "Доступные команды:\n"
             "• /survey - начать опрос\n"
             "• /data - посмотреть сохраненные данные\n"
             "• /clear - очистить состояние\n"
             "• /help - справка",
    )


@bot.command(name="survey", description="Пройти опрос")
def survey_command(_bot, message, args, fsm_context):
    """Начало опроса с fsm_context"""

    fsm_context.set_state("WAITING_FOR_NAME")
    _bot.reply(
        message=message,
        text="📝 Отлично! Начнем опрос.\n\nКак вас зовут?",
    )


@bot.state_handler("WAITING_FOR_NAME")
def waiting_for_name(_bot, message, args, fsm_context):
    """Обработка имени"""

    name = message.markdown.strip()
    fsm_context.set_data(name=name)
    fsm_context.set_state("WAITING_FOR_AGE")

    _bot.reply(
        message=message,
        text=f"Приятно познакомиться, {name}! Сколько вам лет?",
    )


@bot.state_handler("WAITING_FOR_AGE")
def waiting_for_age(_bot, message, args, fsm_context):
    """Обработка возраста"""

    try:
        age = int(message.markdown.strip())
        if age < 0 or age > 150:
            raise ValueError
    except ValueError:
        _bot.reply(message=message, text="Пожалуйста, введите корректный возраст (число от 0 до 150).")
        return

    fsm_context.update_data(age=age)
    fsm_context.set_state("WAITING_FOR_CITY")

    _bot.reply(
        message=message,
        text="Отлично! Из какого вы города?",
    )


@bot.state_handler("WAITING_FOR_CITY")
def waiting_for_city(_bot, message, args, fsm_context):
    """Обработка города"""

    city = message.markdown.strip()
    # получение данных из контекста
    name, age = fsm_context.get("name", "Неизвестно"), fsm_context.get("age", "Неизвестно")

    # сохранение в общее хранилище
    _bot.set_user_data(
        user_id=message.author,
        workspace_id=message.workspace_id,
        key="survey_results",
        value={
            "name": name,
            "age": age,
            "city": city,
            "completed_at": time.time(),
        }
    )
    fsm_context.finish()

    _bot.reply(
        message=message,
        text=f"✅ Спасибо за участие в опросе!\n\n"
             f"Ваши данные:\n"
             f"• Имя: {name}\n"
             f"• Возраст: {age}\n"
             f"• Город: {city}\n\n"
             f"Данные сохранены!",
    )


if __name__ == "__main__":
    with bot:
        while True:
            time.sleep(1)

```
