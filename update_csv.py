import json
import pandas as pd
import re
import os

def update_data_in_html(csv_path, html_path):
    if not os.path.exists(csv_path) or not os.path.exists(html_path):
        print("Error: Ensure both the CSV and HTML files exist.")
        return

    # 1. Read CSV and convert to JSON
    df = pd.read_csv(csv_path)
    new_json_data = json.dumps(df.to_dict(orient='records'), separators=(',', ':'))

    # 2. Read the existing HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Use Regex to replace the content between the markers
    # This looks for // DATA_START, then anything until // DATA_END
    pattern = r'(// DATA_START\s+const data = ).*?(;\s+// DATA_END)'
    replacement = f'\\1{new_json_data}\\2'
    
    new_content = re.sub(
        pattern, 
        lambda m: f"{m.group(1)}{new_json_data}{m.group(2)}", 
        content, 
        flags=re.DOTALL
    )

    # 4. Write the updated content back to the same file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Successfully updated data in {html_path}")

if __name__ == "__main__":
    update_data_in_html('parsed_la28_schedule.csv', 'index.html')