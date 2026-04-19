import openpyxl
from pathlib import Path

xlsx_path = Path("obsidian_tier_rules_spec.xlsx")
wb = openpyxl.load_workbook(xlsx_path, data_only=True)
sheet = wb["tier_rules_master"]

headers = [cell.value for cell in sheet[1]]
print("Headers in tier_rules_master:", headers)

# Print first data row to see values
first_row = [cell.value for cell in sheet[2]]
print("First row data:", first_row)
