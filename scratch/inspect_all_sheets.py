import openpyxl
from pathlib import Path

xlsx_path = Path("obsidian_tier_rules_spec.xlsx")
wb = openpyxl.load_workbook(xlsx_path)

for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    headers = [cell.value for cell in sheet[1]]
    print(f"Sheet '{sheet_name}' headers: {headers}")

wb.close()
