import time
import json
import http.client
from dataclasses import dataclass
from typing import Callable, Any, Optional, List, Tuple
from os import getenv


# ---------------------------
# Низкий уровень: Telegram API (чистый Python)
# ---------------------------

class TelegramAPI:
    HOST = "api.telegram.org"

    def __init__(self, token: str):
        if not token:
            raise ValueError("Не найден BOT_TOKEN (переменная окружения).")
        self.token = token

    def запрос(self, метод: str, данные: Optional[dict] = None) -> dict:
        conn = http.client.HTTPSConnection(self.HOST)

        headers = {"Content-Type": "application/json"}
        body = json.dumps(данные).encode("utf-8") if данные else None

        conn.request(
            "POST",
            f"/bot{self.token}/{метод}",
            body=body,
            headers=headers
        )

        resp = conn.getresponse()
        raw = resp.read().decode("utf-8")
        conn.close()

        # Telegram всегда отвечает JSON-строкой
        return json.loads(raw)

    def получить_обновления(self, offset: Optional[int], timeout: int = 30) -> dict:
        данные = {"timeout": timeout}
        if offset is not None:
            данные["offset"] = offset
        return self.запрос("getUpdates", данные)

    def отправить_сообщение(self, chat_id: int, text: str) -> dict:
        return self.запрос("sendMessage", {"chat_id": chat_id, "text": text})


# ---------------------------
# Типы (объекты события)
# ---------------------------

@dataclass
class Сообщение:
    api: TelegramAPI
    chat_id: int
    text: str

    def ответ(self, text: str) -> None:
        self.api.отправить_сообщение(self.chat_id, text)


# ---------------------------
# Фильтры (условия)
# ---------------------------

class Команда:
    """Команда('старт') сработает на '/старт' и '/старт@BotName' (без сложных аргументов)."""

    def __init__(self, name: str):
        self.name = name.lstrip("/").strip()

    def подходит(self, msg: Сообщение) -> bool:
        t = (msg.text or "").strip()
        if not t.startswith("/"):
            return False
        first = t.split()[0]                  # '/start' or '/start@name'
        cmd = first[1:].split("@")[0].lower() # 'start'
        return cmd == self.name.lower()


class Текст:
    """Текст('привет') сработает на 'привет' (регистр не важен, пробелы по краям игнорируются)."""

    def __init__(self, value: str):
        self.value = value.strip().lower()

    def подходит(self, msg: Сообщение) -> bool:
        return (msg.text or "").strip().lower() == self.value


# ---------------------------
# Русграмм: Бот/Диспетчер
# ---------------------------

Handler = Callable[[Сообщение], Any]
Rule = Tuple[Callable[[Сообщение], bool], Handler]


class Русграмм:
    """
    Мини-фреймворк:
      - регистрируем обработчики: @бот.сообщение(Команда(...)) / @бот.сообщение(Текст(...))
      - запускаем: бот.запуск()
    """

    def __init__(self, token: Optional[str] = None):
        token = token or getenv("BOT_TOKEN")
        self.api = TelegramAPI(token)
        self._rules: List[Rule] = []

    def сообщение(self, фильтр: Optional[object] = None):
        """
        Декоратор регистрации:
          @бот.сообщение(Команда("start"))
          async/обычная функция - не важно (мы вызовем как обычную)
        """
        def decorator(func: Handler) -> Handler:
            if фильтр is None:
                predicate = lambda msg: True
            else:
                # ожидаем у фильтра метод "подходит"
                if not hasattr(фильтр, "подходит"):
                    raise TypeError("Фильтр должен иметь метод подходит(msg).")
                predicate = lambda msg: фильтр.подходит(msg)

            self._rules.append((predicate, func))
            return func

        return decorator

    def _обработать(self, msg: Сообщение) -> None:
        for predicate, handler in self._rules:
            if predicate(msg):
                handler(msg)
                return  # один матч — один обработчик (как простой роутинг)

    def запуск(self, pause: float = 0.5) -> None:
        offset: Optional[int] = None
        print("Русграмм запущен...")

        while True:
            updates = self.api.получить_обновления(offset=offset, timeout=30)

            for upd in updates.get("result", []):
                offset = upd["update_id"] + 1

                message = upd.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                msg = Сообщение(api=self.api, chat_id=chat_id, text=text)
                self._обработать(msg)

            time.sleep(pause)
