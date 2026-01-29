from typing import Any, Optional, Dict, List
from abc import ABC, abstractmethod
import logging
import fnmatch
import pickle
import redis
import json
import time

logger = logging.getLogger(__name__)


class StorageBase(ABC):
    """
    Абстрактное хранилище
    """

    @abstractmethod
    def get(
            self,
            key: str,
            default: Any = None,
    ) -> Any:
        """Получение значение по ключу"""

        pass

    @abstractmethod
    def set(
            self,
            key: str,
            value: Any,
            ttl: Optional[int] = None,
    ) -> None:
        """Установка значения"""

        pass

    @abstractmethod
    def delete(
            self,
            key: str,
    ) -> None:
        """Удаление ключа"""

        pass

    @abstractmethod
    def exists(
            self,
            key: str,
    ) -> bool:
        """Проверка существования ключа"""

        pass

    @abstractmethod
    def keys(
            self,
            pattern: str,
    ) -> List[str]:
        """Получение ключей по шаблону"""

        pass

    @abstractmethod
    def clear(
            self,
    ) -> None:
        """Очистка хранилища"""

        pass


class MemoryStorage(StorageBase):
    """Хранилище в памяти"""

    def __init__(
            self,
    ):
        """Инициализация"""

        self._data, self._ttl = {}, {}

    def get(
            self,
            key: str,
            default: Any = None,
    ) -> Any:
        """
        Получение значения по ключу

        :param key: ключ
        :param default: значение по умолчанию
        :return: данные
        """

        self._check_ttl(key)

        return self._data.get(key, default)

    def set(
            self,
            key: str,
            value: Any,
            ttl: Optional[int] = None,
    ) -> None:
        """
        Установка значения

        :param key: ключ
        :param value: значение
        :param ttl: ttl
        :return: None
        """

        self._data[key] = value
        if ttl:
            self._ttl[key] = time.time() + ttl

    def delete(
            self,
            key: str,
    ) -> None:
        """
        Удаление ключа

        :param key: ключ
        :return: None
        """

        self._check_ttl(key)
        self._data.pop(key, None)
        self._ttl.pop(key, None)

    def exists(
            self,
            key: str,
    ) -> bool:
        """
        Проверка существования ключа

        :param key: ключ
        :return: True/False
        """

        self._check_ttl(key)

        return key in self._data

    def keys(
            self,
            pattern: str,
    ) -> List[str]:
        """
        Получение ключей по шаблону

        :param pattern: паттерн
        :return: список ключей
        """

        self._clean_expired()

        return [k for k in self._data.keys() if fnmatch.fnmatch(k, pattern)]

    def clear(
            self,
    ) -> None:
        """Очистка хранилища"""

        self._data.clear()
        self._ttl.clear()

    def _check_ttl(
            self,
            key: str,
    ) -> None:
        """
        Проверка TTL ключа

        :param key: ключ
        :return: None
        """

        if key in self._ttl:
            if time.time() > self._ttl[key]:
                del self._data[key]
                del self._ttl[key]

    def _clean_expired(
            self,
    ) -> None:
        """Очистка просроченных ключей"""

        current = time.time()
        expired = [k for k, exp in self._ttl.items() if current > exp]
        for key in expired:
            del self._data[key]
            del self._ttl[key]


class RedisStorage(StorageBase):
    """
    Redis хранилище
    """

    def __init__(
            self,
            host: str = 'localhost',
            port: int = 6379,
            db: int = 0,
            password: Optional[str] = None,
            prefix: str = "yuchat:",
            decode_responses: bool = False,
            **kwargs,
    ):
        """
        Инициализация

        :param host: Redis хост
        :param port: Redis порт
        :param db: номер базы данных
        :param password: пароль Redis
        :param prefix: префикс для всех ключей
        :param decode_responses: декодировать ответы в строки
        """

        self._prefix = prefix
        self._redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses,
            **kwargs,
        )

        try:
            self._redis.ping()
            logger.info(f"Redis '{host}:{port}' OK.")
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            raise

    def _make_key(
            self,
            key: str,
    ) -> str:
        """
        Добавление префикса к ключу

        :param key: ключ
        :return: ключ с префиксом
        """

        return f"{self._prefix}{key}"

    def get(
            self,
            key: str,
            default: Any = None,
    ) -> Any:
        """
        Получение значения по ключу

        :param key: ключ
        :param default: дефолтное значение
        :return: данные
        """

        full_key = self._make_key(key)
        value = self._redis.get(full_key)

        if value is None:
            return default

        try:
            value: str
            return json.loads(value)
        except Exception as e:
            _ = e
            try:
                value: bytes
                return pickle.loads(value)
            except Exception as e:
                _ = e
                return value

    def set(
            self,
            key: str,
            value: Any,
            ttl: Optional[int] = None,
    ) -> None:
        """
        Установка значения ключа

        :param key: ключ
        :param value: значение
        :param ttl: ttl
        :return: None
        """

        full_key = self._make_key(key)

        try:
            if isinstance(value, (dict, list, tuple, int, float, str, bool, type(None))):
                serialized = json.dumps(value, ensure_ascii=False)
            else:
                serialized = pickle.dumps(value)

            if ttl:
                self._redis.setex(full_key, ttl, serialized)
            else:
                self._redis.set(full_key, serialized)

        except Exception as e:
            logger.error(f"Redis save data error: {e}")
            raise e

    def delete(
            self,
            key: str,
    ) -> None:
        """
        Удаление ключа

        :param key: ключ
        :return: None
        """

        self._redis.delete(self._make_key(key))

    def exists(
            self,
            key: str,
    ) -> bool:
        """
        Проверка существования ключа

        :param key: ключ
        :return: True/False
        """

        return bool(self._redis.exists(self._make_key(key)))

    def keys(
            self,
            pattern: str,
    ) -> List[str]:
        """
        Получение ключей по шаблону

        :param pattern: паттерн
        :return: список ключей
        """

        full_pattern = self._make_key(pattern)
        keys = self._redis.keys(full_pattern)

        # удаление префиксов
        prefix_len = len(self._prefix)
        return [key.decode() if isinstance(key, bytes) else key[prefix_len:] for key in keys]

    def clear(
            self,
    ) -> None:
        """Очистка хранилища (только ключи с префиксом)"""

        keys: List[str] = self._redis.keys(f"{self._prefix}*")
        if keys:
            self._redis.delete(*keys)


class State:
    """
    Хранение состояния пользователя
    """

    def __init__(
            self,
            user_id: str,
            workspace_id: str,
            chat_id: Optional[str] = None,
            state: Optional[str] = None,
            data: Optional[Dict[str, Any]] = None,
    ):
        """Инициализация"""

        self.user_id = user_id
        self.workspace_id = workspace_id
        self.chat_id = chat_id
        self.state = state
        self.data = data or {}

    def to_dict(
            self,
    ) -> Dict[str, Any]:
        """
        Конвертирование в словарь
        """

        return {
            "user_id": self.user_id,
            "workspace_id": self.workspace_id,
            "chat_id": self.chat_id,
            "state": self.state,
            "data": self.data,
        }

    @classmethod
    def from_dict(
            cls,
            data: Dict[str, Any],
    ) -> 'State':
        """
        Создание объекта из словаря
        """

        return cls(
            user_id=data.get("user_id"),
            workspace_id=data.get("workspace_id"),
            chat_id=data.get("chat_id"),
            state=data.get("state"),
            data=data.get("data", {}),
        )

    def update_data(
            self,
            **kwargs,
    ) -> None:
        """
        Обновление состояния
        """

        self.data.update(kwargs)

    def get(
            self,
            key: str,
            default: Any = None,
    ) -> Any:
        """
        Получение состояния
        """

        return self.data.get(key, default)

    def clear(
            self,
    ) -> None:
        """
        Очистка состояния
        """

        self.state, self.data = None, {}
