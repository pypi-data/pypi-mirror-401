import os
import unittest
from io import BytesIO
from pathlib import Path
from openpyxl import load_workbook

from loadmemory.excel import ExcelHandler


class ExcelHandlerTest(unittest.TestCase):
    def setUp(self):
        self.file_path = Path(__file__).resolve().parent / 'test.xlsx'
        self.output_path = Path(__file__).resolve().parent / 'test_output.xlsx'
        self.output_data = [
            {"username": "测试用户1", "age": 28, "email": "test1@example.com"},
            {"username": "测试用户2", "age": 30, "email": "test2@example.com"},
        ]
        self.read_fields_map = {
            "姓名": "username",
            "年龄": "age",
            "邮箱": "email",
        }
        self.write_fields_map = {v: k for k, v in self.read_fields_map.items()}

    def tearDown(self):
        if self.output_path.exists():
            os.remove(self.output_path)

    def test_excel_read_file(self):
        result = ExcelHandler.read_from_file(self.file_path, self.read_fields_map, row_offset=1)
        self.assertEqual(len(result[0]), len(self.read_fields_map))
        self.assertEqual(len(result), 1)

    def test_excel_read_object(self):
        with open(self.file_path, 'rb') as f:
            result = ExcelHandler.read_from_object(f, self.read_fields_map, row_offset=1)
            self.assertEqual(len(result[0]), len(self.read_fields_map))
            self.assertEqual(len(result), 1)

    def test_excel_write_stream(self):
        ExcelHandler.write_to_file(self.output_data, self.output_path, self.write_fields_map)
        self.assertTrue(self.output_path.exists())

    def test_excel_write_object(self):
        content = ExcelHandler.write_to_object(self.output_data, self.write_fields_map)
        wb = load_workbook(BytesIO(content))
        self.assertEqual(type(wb.active.title), str)
