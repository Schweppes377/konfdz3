import unittest
import os
from config_parser import parse_config_file, parse_dictionary


class TestConfigParser(unittest.TestCase):

    def create_temp_file(self, content):
        """Создает временный файл с содержимым для тестов."""
        temp_file_path = "temp_config.txt"
        with open(temp_file_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(content)
        return temp_file_path

    def tearDown(self):
        """Удаляет временный файл после тестов."""
        if os.path.exists("temp_config.txt"):
            os.remove("temp_config.txt")

    def test_parse_config_file_simple(self):
        """Тест простого файла конфигурации."""
        content = """
        name := "TestName"
        value := 123
        """
        file_path = self.create_temp_file(content)
        expected = {"name": "TestName", "value": 123}
        result = parse_config_file(file_path)
        self.assertEqual(result, expected)

    def test_parse_config_file_with_nested_dict(self):
        """Тест файла с вложенным словарем."""
        content = """
        name := "TestName"
        begin
            key1 := "Value1"
            key2 := begin
                nested_key := 42
            end
        end
        """
        file_path = self.create_temp_file(content)
        expected = {
            "name": "TestName",
            "root": {
                "key1": "Value1",
                "key2": {
                    "nested_key": 42
                }
            }
        }
        result = parse_config_file(file_path)
        self.assertEqual(result, expected)

    def test_parse_dictionary(self):
        """Тест функции parse_dictionary отдельно."""
        lines = [
            "key1 := 123",
            "key2 := begin",
            "  nested_key := \"Value\"",
            "end",
            "key3 := ({1, 2, 3})"
        ]
        expected = {
            "key1": 123,
            "key2": {"nested_key": "Value"},
            "key3": [1, 2, 3]
        }
        result, _ = parse_dictionary(lines)
        self.assertEqual(result, expected)

    def test_parse_dictionary_with_extra_end(self):
        """Тест parse_dictionary с лишним `end`."""
        lines = [
            "key1 := \"Value\"",
            "end"
        ]
        expected = {"key1": "Value"}
        result, index = parse_dictionary(lines)
        self.assertEqual(result, expected)
        self.assertEqual(index, 2)


if __name__ == "__main__":
    unittest.main()
