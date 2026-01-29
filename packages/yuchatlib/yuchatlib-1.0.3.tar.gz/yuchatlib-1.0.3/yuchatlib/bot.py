from typing import Dict, Any, Callable
from dataclasses import dataclass
from functools import wraps
import traceback
import threading
import inspect
import logging
import sched
import time
import re

from .fsm import FSMContext, Storage as StorageFacade, state as fsm_state_decorator
from .storage import StorageBase, MemoryStorage, RedisStorage
from .yuchat import YuChatAPI
from .classes import *


logger = logging.getLogger(__name__)


@dataclass
class Command:
    """Команда бота"""

    name: str
    description: str
    handler: Callable
    pattern: Optional[str] = None
    require_mention: bool = False


@dataclass
class ScheduledTask:
    """Информация о запланированной задаче"""

    id: str
    interval: float
    get_text: Callable
    workspace_id: str
    chat_id: str
    priority: int = 1
    thread: Optional[threading.Thread] = None
    stop_event: Optional[threading.Event] = None


class MessageScheduler:
    """
    Планировщик сообщений
    """

    def __init__(
            self,
    ):
        """Инициализация"""

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.tasks: Dict[str, ScheduledTask] = {}
        self._lock = threading.Lock()
        self._scheduler_thread: Optional[threading.Thread] = None
        self._stop_scheduler = threading.Event()

    def start(
            self,
    ):
        """Запуск планировщика в отдельном потоке"""

        if self._scheduler_thread and self._scheduler_thread.is_alive():
            return

        self._stop_scheduler.clear()
        self._scheduler_thread = threading.Thread(
            target=self._scheduler_main_loop,
            daemon=True,
            name="MessageSchedulerMain"
        )
        self._scheduler_thread.start()
        logger.info("Message scheduler started.")

    def stop(
            self,
    ):
        """Остановка планировщика"""

        self._stop_scheduler.set()
        self.stop_all()

        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
            self._scheduler_thread = None
        logger.info("Message scheduler stopped.")

    def _scheduler_main_loop(
            self,
    ):
        """Главный цикл планировщика"""

        while not self._stop_scheduler.is_set():
            try:
                # есть ли задачи для выполнения
                with self._lock:
                    if not self.tasks:
                        time.sleep(1)
                        continue

                self.scheduler.run(blocking=False)
                time.sleep(0.1)

            except Exception as e:
                logger.error(f"Error in scheduler main loop: {e}")
                time.sleep(1)

    def _schedule_next(
            self,
            task: ScheduledTask,
            bot,
    ):
        """
        Планирование следующего выполнения

        :param task: задача
        :param bot: объект YuChatBot
        :return: None
        """

        self.scheduler.enter(
            delay=task.interval,
            priority=task.priority,
            action=self._execute_task,
            argument=(task.id, bot),
        )

    def _execute_task(
            self,
            task_id: str,
            bot,
    ):
        """
        Выполнение задачи

        :param task_id: id задачи
        :param bot: объект YuChatBot
        :return: None
        """

        with self._lock:
            if task_id not in self.tasks:
                return

            task = self.tasks[task_id]

            if task.stop_event and task.stop_event.is_set():
                return

            task.last_run = datetime.datetime.now()

        try:
            text = task.get_text()
            bot.send_message(
                workspace_id=task.workspace_id,
                chat_id=task.chat_id,
                markdown=text
            )
            logger.debug(f"Scheduled task {task_id} executed successfully.")
        except Exception as e:
            logger.error(f"Error executing scheduled task {task_id}: {e}.")

        with self._lock:
            if task_id in self.tasks and not task.stop_event.is_set():
                self._schedule_next(task, bot)

    def schedule_messages(
            self,
            task_id: str,
            interval: float,
            get_text: Callable,
            workspace_id: str,
            chat_id: str,
            bot,
            priority: int = 1,
            start_immediately: bool = True,
    ) -> bool:
        """
        Планирование регулярной отправки сообщений

        :return: успешно/ошибка
        """

        with self._lock:
            if task_id in self.tasks:
                logger.warning(f"Task {task_id} already exists.")
                return False

            # создание задачи
            stop_event = threading.Event()
            task = ScheduledTask(
                id=task_id,
                interval=interval,
                get_text=get_text,
                workspace_id=workspace_id,
                chat_id=chat_id,
                priority=priority,
                stop_event=stop_event,
            )

            # сохранение
            self.tasks[task_id] = task

            # первое выполнение
            if start_immediately:
                self.scheduler.enter(
                    delay=0,
                    priority=priority,
                    action=self._execute_task,
                    argument=(task_id, bot)
                )
            else:
                self._schedule_next(task, bot)

            # запуск главного потока планировщика, если еще не запущен
            if not self._scheduler_thread or not self._scheduler_thread.is_alive():
                self.start()

            logger.info(f"Task {task_id} scheduled with interval {interval}s")

            return True

    def stop_task(
            self,
            task_id: str,
    ) -> bool:
        """
        Остановка задачи

        :param task_id: id задачи
        :return: True/False
        """

        with self._lock:
            if task_id not in self.tasks:
                return False

            task = self.tasks[task_id]
            task.stop_event.set()

            for event in self.scheduler.queue:
                if event.argument[0] == task_id:
                    try:
                        self.scheduler.cancel(event)
                    except ValueError:
                        pass

            del self.tasks[task_id]
            logger.info(f"Task {task_id} stopped.")

            return True

    def stop_all(
            self,
    ):
        """Остановка всех задач"""

        with self._lock:
            task_ids = list(self.tasks.keys())
            for task_id in task_ids:
                self.stop_task(task_id)

            for event in list(self.scheduler.queue):
                try:
                    self.scheduler.cancel(event)
                except ValueError:
                    pass


class YuChatHandler:
    """
    Базовый класс для обработчиков событий
    """

    def __init__(
            self,
            bot: 'YuChatBot',
    ):
        """Инициализация"""

        self.bot = bot

    def handle(
            self,
            update: Update,
    ) -> None:
        """
        Обработка обновления

        :param update: обновление
        :return: None
        """

        raise NotImplementedError


class MessageHandler(YuChatHandler):
    """
    Обработчик сообщений
    """

    def __init__(
            self,
            bot: 'YuChatBot',
    ):
        """Инициализация"""

        super().__init__(bot)
        self.commands: Dict[str, Command] = {}
        self.message_handlers: List[Callable] = []
        self.state_handlers: Dict[str, Callable] = {}

    def register_command(
            self,
            name: str,
            description: str = "",
            pattern: str = None,
            require_mention: bool = False,
    ):
        """
        Декоратор для регистрации команды

        :param name: название команды
        :param description: описание
        :param pattern: паттерн
        :param require_mention: require_mention
        :return: декоратор
        """

        def decorator(func):
            # обертывание функции, чтобы правильно передавать параметры
            @wraps(func)
            def wrapper(bot, message, args, fsm_context=None):
                # проверка функции
                params = list(inspect.signature(func).parameters.values())
                # функция ожидает fsm_context
                if len(params) >= 4 and params[3].name == 'fsm_context':
                    return func(bot, message, args, fsm_context)
                # функция не ожидает fsm_context
                else:
                    return func(bot, message, args)

            self.commands[name] = Command(
                name=name,
                description=description,
                handler=wrapper,
                pattern=pattern,
                require_mention=require_mention,
            )

            # возвращение оригинальной функции
            return func

        return decorator

    def register_message_handler(
            self,
            func,
    ):
        """
        Декоратор для регистрации обработчика всех сообщений

        :param func: функция
        :return: функция
        """

        @wraps(func)
        def wrapper(bot, message, fsm_context=None):
            params = list(inspect.signature(func).parameters.values())
            if len(params) >= 3 and params[2].name == 'fsm_context':
                return func(bot, message, fsm_context)
            else:
                return func(bot, message)

        self.message_handlers.append(wrapper)

        # возвращение оригинальной функции
        return func

    def register_state_handler(
            self,
            state_name: str,
            func: Callable,
    ):
        """
        Регистрация обработчика состояния FSM

        :param state_name: состояние
        :param func: функция
        :return: None
        """

        # обертка функции для обработки состояния
        @wraps(func)
        def wrapper(bot, message, args, fsm_context):
            params = list(inspect.signature(func).parameters.values())
            if len(params) >= 4 and params[3].name == 'fsm_context':
                return func(bot, message, args, fsm_context)
            else:
                return func(bot, message, args)

        self.state_handlers[state_name] = wrapper

    def handle(
            self,
            update: Update,
    ) -> None:
        """
        Обработка сообщений

        :param update: обновление
        :return: None
        """

        message = update.new_chat_message
        if message:
            chat_id, workspace_id, user_id = message.chat_id, message.workspace_id, message.author
            # контекст FSM
            fsm_context = self.bot.get_fsm_context(
                user_id=user_id,
                workspace_id=workspace_id,
                chat_id=chat_id,
            )
            # текущее состояние пользователя
            current_state = fsm_context.get_state()

            # если есть состояние, вызов обработчика состояния
            if current_state and current_state.state:
                state_handler = self.state_handlers.get(current_state.state)
                if state_handler:
                    try:
                        state_handler(self.bot, message, "", fsm_context)
                        return
                    except Exception as e:
                        logger.error(f"Error in state handler {current_state.state}: {e}")
                        # при ошибке в обработчике состояния очистка состояния
                        fsm_context.clear()

            # иначе проверка команд
            command_processed = self._process_commands(message, chat_id, workspace_id, user_id, fsm_context)

            # если команда не обработана, вызов общих обработчиков
            if not command_processed:
                for handler in self.message_handlers:
                    try:
                        handler(self.bot, message, fsm_context)
                    except Exception as e:
                        logger.error(f"Error in message handler: {e}")

    def _process_commands(
            self,
            message: NewChatMessage,
            chat_id: str,
            workspace_id: str,
            user_id: str,
            fsm_context: FSMContext,
    ) -> bool:
        """
        Обработка команд из сообщения

        :param message: сообщение
        :param chat_id: id чата
        :param workspace_id: id workspace
        :param user_id: id участника
        :param fsm_context: FSMContext
        :return: True/False
        """

        _, _, _ = user_id, chat_id, workspace_id
        text = message.markdown.strip()

        # проверка, начинается ли сообщение с команды
        if text.startswith('/'):
            # извлечение команды и аргументов, удаление /
            parts = text.split(maxsplit=1)
            command_name = parts[0][1:]

            # удаление @mention, если есть
            if '@' in command_name:
                command_name = command_name.split('@')[0]

            args = parts[1] if len(parts) > 1 else ""

            # поиск обработчика
            for cmd_name, cmd in self.commands.items():
                # проверка точного совпадения имени
                if command_name == cmd_name:
                    # проверка паттерна, если есть
                    if cmd.pattern:
                        if not re.match(cmd.pattern, args):
                            continue

                    # выполнение команды
                    try:
                        cmd.handler(self.bot, message, args, fsm_context)
                        return True
                    except Exception as e:
                        logger.error(f"Error executing command {cmd_name}: {e}")
                        return True

        return False


class ChatMemberHandler(YuChatHandler):
    """
    Обработчик событий участников чата
    """

    def __init__(
            self,
            bot: 'YuChatBot',
    ):
        """Инициализация"""

        super().__init__(bot)
        self.invite_handlers: List[Callable] = []
        self.join_handlers: List[Callable] = []
        self.left_handlers: List[Callable] = []

    def on_invite(
            self,
            func,
    ):
        """
        Декоратор для обработки приглашений

        :param func: функция
        :return: функция
        """

        self.invite_handlers.append(func)

        return func

    def on_join(
            self,
            func,
    ):
        """
        Декоратор для обработки входа в чат

        :param func: функция
        :return: функция
        """

        self.join_handlers.append(func)

        return func

    def on_left(
            self,
            func,
    ):
        """
        Декоратор для обработки выхода из чата

        :param func: функция
        :return: функция
        """

        self.left_handlers.append(func)

        return func

    def handle(
            self,
            update: Update,
    ) -> None:
        """
        Обработка событий участников

        :param update: обновление
        :return: None
        """

        if update.invite_to_chat:
            for handler in self.invite_handlers:
                try:
                    handler(self.bot, update.invite_to_chat)
                except Exception as e:
                    logger.error(f"Error in invite handler: {e}")

        elif update.joined_to_chat:
            for handler in self.join_handlers:
                try:
                    handler(self.bot, update.joined_to_chat)
                except Exception as e:
                    logger.error(f"Error in join handler: {e}")

        elif update.left_from_chat:
            for handler in self.left_handlers:
                try:
                    handler(self.bot, update.left_from_chat)
                except Exception as e:
                    logger.error(f"Error in left handler: {e}")


class YuChatBot(YuChatAPI):
    """
    Клиент YuChat
    """

    def __init__(
            self,
            token: str,
            base_url: str = "https://yuchat.ai",
            polling_interval: int = 5,
            timeout: int = 30,
            storage: Optional[StorageBase] = None,
            redis_config: Optional[Dict[str, Any]] = None,
            skip_updates: bool = False,
    ):
        """
        Инициализация

        :param token: Bearer токен для авторизации
        :param base_url: базовый URL API
        :param polling_interval: интервал опроса в секундах
        :param timeout: таймаут запроса long polling
        :param storage: хранилище
        :param redis_config: конфигурация Redis
        :param skip_updates: пропуск обновлений
        """

        super().__init__(token, base_url)

        self.polling_interval = polling_interval
        self.timeout = timeout
        self._polling_thread: Optional[threading.Thread] = None
        self._stop_polling = threading.Event()
        self._last_update_id = 0
        self.skip_updates = skip_updates

        # инициализация хранилища
        if storage:
            self.storage = storage
        elif redis_config:
            self.storage = RedisStorage(**redis_config)
        else:
            self.storage = MemoryStorage()

        self.storage_facade = StorageFacade(self.storage)

        # инициализация обработчиков
        self.message_handler = MessageHandler(self)
        self.chat_member_handler = ChatMemberHandler(self)

        # список всех обработчиков
        self._handlers = [
            self.message_handler,
            self.chat_member_handler,
        ]

        # дополнительные кастомные обработчики
        self._custom_handlers: List[Callable] = []

        # планировщик отправки сообщений
        self.scheduler = MessageScheduler()

    def __enter__(
            self,
    ):

        self.start_polling(skip_updates=self.skip_updates)

        return self

    def __exit__(
            self,
            exc_type,
            exc_val,
            exc_tb,
    ):

        self.stop_polling()

    def schedule_message(
            self,
            task_id: str,
            interval: float,
            workspace_id: str,
            chat_id: str,
            get_text: Callable,
            priority: int = 1,
    ) -> bool:
        """
        Регулярная отправка сообщений

        :param task_id: идентификатор задачи
        :param interval: интервал в секундах между сообщениями
        :param get_text: функция, возвращающая markdown сообщения
        :param workspace_id: id workspace
        :param chat_id: id чата
        :param priority: приоритет
        :return: успешно/ошибка
        """

        return self.scheduler.schedule_messages(
            task_id=task_id,
            interval=interval,
            get_text=get_text,
            workspace_id=workspace_id,
            chat_id=chat_id,
            priority=priority,
            bot=self,
        )

    def get_fsm_context(
            self,
            user_id: str,
            workspace_id: str,
            chat_id: Optional[str] = None,
    ) -> FSMContext:
        """
        Получение контекста FSM для пользователя

        :param user_id: <UNK> id участника
        :param workspace_id: id workspace
        :param chat_id: id чата
        :return: FSMContext
        """

        return FSMContext(
            storage=self.storage,
            user_id=user_id,
            workspace_id=workspace_id,
            chat_id=chat_id,
        )

    def register_handler(
            self,
            handler: Callable,
    ):
        """
        Регистрация кастомного обработчика

        :param handler: handler
        :return: handler
        """

        self._custom_handlers.append(handler)

        # автоматическая регистрация state handlers
        if hasattr(handler, '_fsm_state'):
            self.message_handler.register_state_handler(
                handler._fsm_state,
                handler,
            )

        return handler

    def command(
            self,
            name: str,
            description: str = "",
            pattern: str = None,
            require_mention: bool = False,
    ):
        """
        Декоратор для регистрации команды

        :param name: <UNK> имя команды
        :param description: описание
        :param pattern: паттерн
        :param require_mention: require_mention
        :return: функция
        """

        return self.message_handler.register_command(name, description, pattern, require_mention)

    def message(
            self,
            func,
    ):
        """
        Декоратор для регистрации обработчика сообщений

        :param func: функция
        :return: функция
        """

        return self.message_handler.register_message_handler(func)

    def state_handler(
            self,
            state_name: str,
    ):
        """
        Декоратор для регистрации обработчика состояния FSM

        :param state_name: состояние
        :return: декоратор
        """

        def decorator(func):
            # использование декоратора из fsm модуля
            decorated_func = fsm_state_decorator(state_name)(func)
            # регистрация в обработчике
            self.message_handler.register_state_handler(state_name, decorated_func)
            return decorated_func

        return decorator

    def on_invite(
            self,
            func,
    ):
        """
        Декоратор для обработки приглашений

        :param func: функция
        :return: декоратор
        """

        return self.chat_member_handler.on_invite(func)

    def on_join(
            self,
            func,
    ):
        """
        Декоратор для обработки входа в чат

        :param func: функция
        :return: декоратор
        """

        return self.chat_member_handler.on_join(func)

    def on_left(
            self,
            func,
    ):
        """
        Декоратор для обработки выхода из чата

        :param func: функция
        :return: декоратор
        """

        return self.chat_member_handler.on_left(func)

    def set_user_data(
            self,
            user_id: str,
            workspace_id: str,
            key: str,
            value: Any,
            ttl: Optional[int] = None,
    ) -> None:
        """
        Установка данных пользователя

        :param user_id: id пользователя
        :param workspace_id: id workspace
        :param key: ключ
        :param value: значение
        :param ttl: ttl
        :return: None
        """

        self.storage_facade.set_user_data(user_id, workspace_id, key, value, ttl)

    def get_user_data(
            self,
            user_id: str,
            workspace_id: str,
            key: str,
            default: Any = None,
    ) -> Any:
        """
        Получение данных пользователя

        :param user_id: id пользователя
        :param workspace_id: id workspace
        :param key: ключ
        :param default: дефолтное значение
        :return: данные
        """

        return self.storage_facade.get_user_data(user_id, workspace_id, key, default)

    def delete_user_data(
            self,
            user_id: str,
            workspace_id: str,
            key: str,
    ) -> None:
        """
        Удаление данных пользователя

        :param user_id: id пользователя
        :param workspace_id: id workspace
        :param key: ключ
        :return: None
        """

        self.storage_facade.delete_user_data(user_id, workspace_id, key)

    def set_chat_data(
            self,
            chat_id: str,
            workspace_id: str,
            key: str,
            value: Any,
            ttl: Optional[int] = None,
    ) -> None:
        """
        Установка данных чата

        :param chat_id: id чата
        :param workspace_id: id workspace
        :param key: ключ
        :param value: значение
        :param ttl: ttl
        :return: None
        """

        self.storage_facade.set_chat_data(chat_id, workspace_id, key, value, ttl)

    def get_chat_data(
            self,
            chat_id: str,
            workspace_id: str,
            key: str,
            default: Any = None,
    ) -> Any:
        """
        Получение данных чата

        :param chat_id: id чата
        :param workspace_id: id workspace
        :param key: ключ
        :param default: дефолтное значение
        :return: данные
        """

        return self.storage_facade.get_chat_data(chat_id, workspace_id, key, default)

    def delete_chat_data(
            self,
            chat_id: str,
            workspace_id: str,
            key: str,
    ) -> None:
        """
        Удаление данных чата

        :param chat_id: id чата
        :param workspace_id: id workspace
        :param key: ключ
        :return: None
        """

        self.storage_facade.delete_chat_data(chat_id, workspace_id, key)

    def start_polling(
            self,
            skip_updates: bool = False,
    ):
        """
        Запуск long polling в отдельном потоке

        :param skip_updates: пропуск обновлений
        """

        if self._polling_thread and self._polling_thread.is_alive():
            raise RuntimeError("Polling already running!")

        self._stop_polling.clear()
        self._polling_thread = threading.Thread(
            target=self._polling_loop,
            daemon=True,
            name="YuChatPolling",
            args=(skip_updates,),
        )
        self._polling_thread.start()
        logger.info("Long polling started")

    def stop_polling(
            self,
    ):
        """Остановка long polling"""

        self._stop_polling.set()
        if self._polling_thread:
            self._polling_thread.join(timeout=10)
            self._polling_thread = None
        logger.info("Long polling stopped.")

    def _polling_loop(
            self,
            skip_updates: bool = False,
    ):
        """
        Цикл long polling

        :param skip_updates: пропуск обновлений
        """

        logger.info(f"Starting polling with interval {self.polling_interval}s.")

        if skip_updates:
            updates = self.get_updates().updates
            if updates:
                self._last_update_id = max(update.update_id for update in updates)

        while not self._stop_polling.is_set():
            try:
                updates_response = self.get_updates(
                    offset=self._last_update_id + 1 if self._last_update_id else None,
                    limit=100,
                )
                logger.debug(f"Got updates: {updates_response}.")

                if updates_response.updates:
                    for update in updates_response.updates:
                        self._process_update(update)
                        self._last_update_id = update.update_id

                # если обновлений не было, ожидание перед следующим запросом
                else:
                    time.sleep(self.polling_interval)

            except Exception as e:
                logger.error(f"Unexpected error in polling: {e}")
                time.sleep(self.polling_interval)

    def _process_update(
            self,
            update: Update,
    ):
        """
        Обработка одного обновления

        :param update: обновление
        :return: None
        """

        try:
            logger.info(f"Received update {update.update_id}.")

            # обработка через все обработчики
            for handler in self._handlers:
                handler.handle(update)

            # вызов кастомных обработчиков
            for custom_handler in self._custom_handlers:
                try:
                    custom_handler(self, update)
                except Exception as e:
                    logger.error(f"Error in custom handler: {e}")

        except Exception as e:
            logger.error(f"Error processing update {update.update_id}: {e}. {traceback.format_exc()}")

    def reply(
            self,
            message: NewChatMessage,
            text: str,
            **kwargs,
    ) -> SendChatMessageResponse:
        """
        Ответ на сообщение

        :param message: исходное сообщение
        :param text: текст ответа
        :param kwargs: дополнительные параметры
        :return: SendChatMessageResponse
        """

        return self.send_message(
            workspace_id=message.workspace_id,
            chat_id=message.chat_id,
            markdown=text,
            reply_to=message.message_id,
            **kwargs,
        )

    def get_help_text(
            self,
    ) -> str:
        """
        Генерация текста помощи со списком команд

        :return: список команд
        """

        if not self.message_handler.commands:
            return "No commands available"

        help_lines = ["Available commands:", ""]
        for cmd_name, cmd in self.message_handler.commands.items():
            help_lines.append(f"`/{cmd_name}` - {cmd.description}")

        return "\n".join(help_lines)

    def get_commands_list(
            self,
    ) -> Dict[str, Command]:
        """
        Получение списка зарегистрированных команд

        :return: словарь с командами
        """

        return self.message_handler.commands.copy()
