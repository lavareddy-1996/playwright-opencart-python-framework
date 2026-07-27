import json
import csv
import openpyxl

# Column order used consistently across json/csv/xlsx test data files.
# Keeping this explicit (rather than relying on dict/row insertion order)
# means a reordered or missing column in one file can't silently produce
# misaligned test data.
LOGIN_DATA_FIELDS = ("testName", "email", "password", "expected")


def read_json_data(file_path: str, fields=LOGIN_DATA_FIELDS):
    """
    Reads test data from a JSON file and returns a list of tuples.

    Example JSON structure:
    [
        {"testName": "Valid login", "email": "test1@example.com",
         "password": "abc123", "expected": "success"}
    ]

    Raises FileNotFoundError / ValueError instead of swallowing errors —
    a broken data file should fail the test run loudly (e.g. as a
    parametrize collection error), not silently produce zero test cases
    that make the suite look "green" for having run nothing.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    return [tuple(record[field] for field in fields) for record in json_data]


def read_csv_data(file_path: str, fields=LOGIN_DATA_FIELDS):
    """
    Reads test data from a CSV file and returns a list of tuples.
    CSV file should contain headers matching `fields`.
    """
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [tuple(row[field] for field in fields) for row in reader]


def read_excel_data(file_path: str, sheet_name: str = None, fields=LOGIN_DATA_FIELDS):
    """
    Reads test data from an Excel file and returns a list of tuples.
    Assumes the first row contains headers matching `fields` (in any order).
    """
    workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    try:
        sheet = workbook[sheet_name] if sheet_name else workbook.active
        rows = sheet.iter_rows(values_only=True)
        header = [str(h).strip() for h in next(rows)]
        col_index = {name: idx for idx, name in enumerate(header)}

        data = []
        for row in rows:
            if row is None or all(cell is None for cell in row):
                continue  # skip blank trailing rows
            data.append(tuple(row[col_index[field]] for field in fields))
        return data
    finally:
        workbook.close()
