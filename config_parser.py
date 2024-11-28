import argparse
import json
import re
import sys


def parse_dictionary(lines):
    """Парсит словарь, ограниченный ключевыми словами `begin` и `end`."""
    result = {}
    index = 0

    while index < len(lines):
        line = lines[index].strip()

        if not line:
            index += 1
            continue

        if line == "end":
            return result, index + 1

        constant_pattern = r'(\w+)\s*:=\s*(.+)'
        match = re.match(constant_pattern, line)

        if match:
            key, value = match.groups()
            value = value.strip()

            if value == "begin":
                nested_dict, consumed = parse_dictionary(lines[index + 1:])
                result[key] = nested_dict
                index += consumed
            elif value.startswith("({") and value.endswith("})"):
                array_values = re.findall(r'\d+', value)
                result[key] = list(map(int, array_values))
            elif value.startswith('"') and value.endswith('"'):
                result[key] = value[1:-1]
            elif value.isdigit():
                result[key] = int(value)
            else:
                raise ValueError(f"Некорректный формат строки: {line}")
        else:
            raise ValueError(f"Некорректный формат строки: {line}")

        index += 1

    return result, index


def parse_config_file(file_path):
    """Парсит файл конфигурации и возвращает результат в виде словаря."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    result = {}
    try:
        index = 0
        while index < len(lines):
            line = lines[index].strip()

            if not line or line.startswith("#"):
                index += 1
                continue

            if line == "begin":
                root_dict, consumed = parse_dictionary(lines[index + 1:])
                result["root"] = root_dict
                index += consumed
                continue

            if line == "end":
                # Игнорируем верхнеуровневые строки "end"
                index += 1
                continue

            constant_pattern = r'(\w+)\s*:=\s*(.+)'
            match = re.match(constant_pattern, line)

            if match:
                key, value = match.groups()
                value = value.strip()

                if value.startswith('"') and value.endswith('"'):
                    result[key] = value[1:-1]
                elif value.isdigit():
                    result[key] = int(value)
                elif value == "begin":
                    nested_dict, consumed = parse_dictionary(lines[index + 1:])
                    result[key] = nested_dict
                    index += consumed
                else:
                    raise ValueError(f"Некорректный формат строки: {line}")
            else:
                raise ValueError(f"Некорректный формат строки: {line}")

            index += 1

    except ValueError as e:
        print(f"Ошибка при разборе конфигурации: {e}", file=sys.stderr)

    return result



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер конфигурационных файлов.")
    parser.add_argument("--input", required=True, help="Путь к файлу конфигурации.")
    args = parser.parse_args()

    config = parse_config_file(args.input)
    print(json.dumps(config, indent=4, ensure_ascii=False))
