from typing import Any, Optional, Dict
import logging

from .storage import StorageBase, State

logger = logging.getLogger(__name__)


class FSMContext:
    """
    Контекст конечного автомата состояний
    """

    def __init__(
            self,
            storage: StorageBase,
            user_id: str,
            workspace_id: str,
            chat_id: Optional[str] = None,
    ):
        """
        Инициализация

        :param storage: хранилище
        :param user_id: id участника
        :param workspace_id: id workspace
        :param chat_id: id чата
        """

        self.storage = storage
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.chat_id = chat_id
        self._state_key = f"fsm:{workspace_id}:{user_id}"

    def get_state(
            self,
    ) -> Optional[State]:
        """
        Получение текущего состояния

        :return: состояние
        """

        state_data = self.storage.get(self._state_key)
        if state_data:
            return State.from_dict(state_data)

        return None

    def set_state(
            self,
            _state: Optional[str],
    ) -> None:
        """
        Установка состояния

        :param _state: состояние
        :return: None
        """

        current = self.get_state()
        if current:
            current.state = _state
            current.chat_id = self.chat_id
        else:
            current = State(
                user_id=self.user_id, workspace_id=self.workspace_id,
                chat_id=self.chat_id, state=_state,
            )

        # ttl - 24 часа
        self.storage.set(self._state_key, current.to_dict(), ttl=86400)

    def set_data(
            self,
            **kwargs,
    ) -> None:
        """
        Установка данных состояния

        :param kwargs: данные
        :return: None
        """

        current = self.get_state()
        if not current:
            current = State(
                user_id=self.user_id,
                workspace_id=self.workspace_id,
                chat_id=self.chat_id,
                state=None,
            )

        current.update_data(**kwargs)
        current.chat_id = self.chat_id
        self.storage.set(self._state_key, current.to_dict(), ttl=86400)

    def get_data(
            self,
    ) -> Dict[str, Any]:
        """
        Получение данных состояния

        :return: данные
        """

        current = self.get_state()

        return current.data if current else {}

    def update_data(
            self,
            **kwargs,
    ) -> None:
        """
        Обновление данных состояния

        :param kwargs: данные
        :return: None
        """

        current = self.get_state()
        if not current:
            current = State(
                user_id=self.user_id,
                workspace_id=self.workspace_id,
                chat_id=self.chat_id,
                state=None,
            )

        current.update_data(**kwargs)
        current.chat_id = self.chat_id
        self.storage.set(self._state_key, current.to_dict(), ttl=86400)

    def get(
            self,
            key: str,
            default: Any = None,
    ) -> Any:
        """
        Получение конкретного значения из данных

        :param key: ключ
        :param default: дефолтное значение
        :return: значение
        """

        current = self.get_state()

        return current.get(key, default) if current else default

    def clear(
            self,
    ) -> None:
        """
        Очистка состояния и данных

        :return: None
        """

        current = self.get_state()
        if current:
            current.clear()
            current.chat_id = self.chat_id
            self.storage.set(self._state_key, current.to_dict(), ttl=3600)
        else:
            self.storage.delete(self._state_key)

    def finish(
            self,
    ) -> None:
        """
        Завершение состояния

        :return: None
        """

        self.storage.delete(self._state_key)


class Storage:
    """
    Класс для работы с хранилищем
    """

    def __init__(
            self,
            storage: StorageBase,
    ):
        """
        Инициализация

        :param storage: хранилище
        """

        self.storage = storage

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

        self.storage.set(f"user_data:{workspace_id}:{user_id}:{key}", value, ttl)

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

        return self.storage.get(f"user_data:{workspace_id}:{user_id}:{key}", default)

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

        self.storage.delete(f"user_data:{workspace_id}:{user_id}:{key}")

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

        self.storage.set(f"chat_data:{workspace_id}:{chat_id}:{key}", value, ttl)

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

        return self.storage.get(f"chat_data:{workspace_id}:{chat_id}:{key}", default)

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

        self.storage.delete(f"chat_data:{workspace_id}:{chat_id}:{key}")

    def set_global_data(
            self,
            key: str,
            value: Any,
            ttl: Optional[int] = None,
    ) -> None:
        """
        Установка глобальных данных

        :param key: ключ
        :param value: значение
        :param ttl: ttl
        :return: None
        """

        self.storage.set(f"global:{key}", value, ttl)

    def get_global_data(
            self,
            key: str,
            default: Any = None,
    ) -> Any:
        """
        Получение глобальных данных

        :param key: ключ
        :param default: дефолтное значение
        :return: значение
        """

        return self.storage.get(f"global:{key}", default)

    def delete_global_data(
            self,
            key: str,
    ) -> None:
        """
        Удаление глобальных данных

        :param key: ключ
        :return: None
        """

        self.storage.delete(f"global:{key}")


def state(
        state_name: str,
):
    """
    Декоратор для обработчиков состояний FSM

    :param state_name: состояние
    """

    def decorator(func):
        func._fsm_state = state_name
        return func

    return decorator
