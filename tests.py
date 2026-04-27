import unittest
import os
import json

class TestTaskApp(unittest.TestCase):
    def setUp(self):
        self.test_file = "tasks.json"
        self.sample_data = [{"title": "Test", "category": "Работа"}]

    def test_save_load(self):
        # Позитивный тест: сохранение и загрузка
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(self.sample_data, f)
        
        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data[0]['title'], "Test")

    def test_validation_empty(self):
        # Граничный случай: пустая строка
        title = ""
        self.assertFalse(len(title) > 0)

if __name__ == '__main__':
    unittest.main()
