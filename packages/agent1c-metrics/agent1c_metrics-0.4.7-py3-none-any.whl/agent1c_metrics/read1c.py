import json, re

class ParseJSONException(json.JSONDecodeError):
    def __init__(self, original_text, message="Unable to parse 1c data"):
        self.original_text = original_text
        self.message = message
        super().__init__(self.message)

def lts(lst_file):

    print(f"Reading LST file: {lst_file}")

    content = ''
    with open(lst_file,encoding='utf-8') as cfg:
        # 1. Убираем лишние символы и нормализуем скобки
        content = cfg.read().replace("\r\n",'\n').replace('\n','').replace('\uFEFF','').replace('\n', '')
    
    # Сохраняем оригинал для отладки
    str_original = content

    # Специальный хак: 1С файлы — это последовательность структур {..}{..}
    # Чтобы сделать это валидным JSON-массивом, добавим запятые между ними
    content = content.replace('}{', '},{')
    content = f'[{content}]' # Оборачиваем всё в общие скобки

    # Заменяем фигурные скобки на квадратные
    content = content.replace('{', '[').replace('}', ']')

    # 2. Оборачиваем UUID в кавычки (если они еще не в них)
    # Ищем паттерн UUID, который окружен либо скобкой, либо запятой
    uuid_pattern = r'(?<=[,\[])([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})'
    content = re.sub(uuid_pattern, r'"\1"', content)
    
    # Убираем двойные кавычки, если UUID уже был в кавычках (чтобы не вышло """uuid""")
    # Но сначала нужно защитить пустые строки
    content = re.sub(r'(?<=[,\[])""(?=[,\]])', '"__EMPTY__"', content)
    content = content.replace('""', '\\"')
    
    # 3. Оборачиваем длинные числа-даты 1С (например, 00010101000000)
    # Ищем последовательности цифр, начинающиеся с нуля, которые не в кавычках
    content = re.sub(r'(?<=[,\[])(0\d+)(?=[,\]])', r'"\1"', content)

    # 4. Исправляем пути Windows (обратные слеши)
    # В JSON обратный слеш должен быть экранирован \\
    # Но проще всего временно заменить их на прямой слеш или экранировать
    #content = content.replace('\\', '/')
    content = re.sub(r'(?<!\\)\\(?![\\"])', r'\\\\', content)
    content = re.sub(r'\\(?!\\)"(?=[,\]])', r'\\\\"', content)
    #content = re.sub(r'\\(?!\\)', r'\\\\', content)
    
    """     .replace('{','[').replace('}',']')
    print("Original string:",str_original)
    str_original = re.sub(r"([0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12})",wrap_by_quotes,str_original)
    str_original = re.sub(r"[^,\[](\"\")",replace_double_quotes,str_original)
    str_original = re.sub(r",(0\d+)",wrap_by_quotes,str_original)
    str_original = re.sub(r"(\\)[^\"]",wrap_backslash,str_original)
    print(str_original) """

    try:
        data = json.loads(content)
    except json.decoder.JSONDecodeError as e:
        print(f"Original string:\n{str_original}")
        print(f"Final string:\n{content}")
        print(f"Ошибка в позиции {e.pos}: {e.msg}")
        # Вывод проблемного участка для отладки
        start = max(0, e.pos - 40)
        end = min(len(content), e.pos + 40)
        print(f"Контекст: {content[start:end]}")
        print(f"          {' ' * (e.pos - start)}^")
        raise
        raise ParseJSONException(str_original)

    return data

def wrap_by_quotes(match_obj):
    environment = match_obj.group()
    value = match_obj.group(1)
    replacement = environment.replace(value,f'"{value}"')
    if value is not None:
        return replacement

def wrap_backslash(match_obj):
    environment = match_obj.group()
    value = match_obj.group(1)
    replacement = environment.replace(value,f'\\\\')
    if value is not None:
        return replacement

def replace_double_quotes(match_obj):
    value = match_obj.group()
    if value is not None:
        return value.replace('""','\\"')