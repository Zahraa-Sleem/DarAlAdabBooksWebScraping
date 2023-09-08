import pandas as pd
import json

# Step 1: Parse the JSON File
with open('Books.json', 'r') as json_file:
    data = json.load(json_file)

# Step 2: Convert JSON Data to DataFrame
df = pd.DataFrame(data)

# Step 3: Export DataFrame to Excel
excel_filename = 'data.xlsx'
df.to_excel(excel_filename, index=False)
print(f"Excel file '{excel_filename}' created successfully.")
