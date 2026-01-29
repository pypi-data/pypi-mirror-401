import re
import sys
from pathlib import Path


# Мини-словарь замен: из "русского" → в Python
ЗАМЕНЫ = {
    r"\bиз\b": "from",
    r"\bимпорт\b": "import",
    r"\bкак\b": "as",

    r"\bфун\b": "def",
    r"\bкласс\b": "class",

    r"\bесли\b": "if",
    r"\bиначе\b": "else",
    r"\bдля\b": "for",
    r"\bв\b": "in",
    r"\bпока\b": "while",

    r"\bвернуть\b": "return",
    r"\bпродолжить\b": "continue",
    r"\bпрервать\b": "break",

    # спец-замены для главного блока
    r"__имя__": "__name__",
    r"__главный__": "__main__",
}


def перевести(текст: str) -> str:
    out = текст
    for шаблон, замена in ЗАМЕНЫ.items():
        out = re.sub(шаблон, замена, out)
    return out


def запустить(путь_к_файлу: str) -> None:
    src_path = Path(путь_к_файлу).resolve()
    исходник = src_path.read_text(encoding="utf-8")

    python_code = перевести(исходник)

    compiled = compile(python_code, str(src_path), "exec")
    env = {"__name__": "__main__", "__file__": str(src_path)}
    exec(compiled, env, env)


def найти_главный_файл() -> str:
    """Ищет главный файл в порядке приоритета:
    1. главный.рус
    2. главный.рус  
    3. любой .рус файл (первый найденный)
    """
    current_dir = Path(".")
    
    # Приоритетные файлы
    приоритетные = ["главный.рус", "главный.рус"]
    for файл in приоритетные:
        путь = current_dir / файл
        if путь.exists():
            return str(путь)
    
    # Любой .рус файл
    русские_файлы = list(current_dir.glob("*.рус"))
    if русские_файлы:
        return str(русские_файлы[0])
    
    return None


def main():
    # Если передан аргумент - используем его
    if len(sys.argv) > 1:
        файл = sys.argv[1]
    else:
        # Ищем автоматически
        файл = найти_главный_файл()
        if not файл:
            print("Ошибка: не найден .рус файл")
            print("Использование: русграмм [файл.рус]")
            print("Или создайте один из файлов: главный.рус, главный.рус")
            sys.exit(1)
    
    print(f"Запускаю: {файл}")
    запустить(файл)


if __name__ == "__main__":
    main()
