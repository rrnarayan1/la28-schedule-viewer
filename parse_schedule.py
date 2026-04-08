import pdfplumber
import pandas as pd

def parse_olympic_schedule(pdf_path, output_csv_path):
    print(f"Parsing '{pdf_path}'...")
    all_rows = []
    
    # Open the PDF using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extract the table from the current page
            table = page.extract_table()
            
            if table:
                all_rows.extend(table)
            else:
                print(f"No table found on page {page_num}.")

    if not all_rows:
        print("Failed to extract any tables from the PDF.")
        return

    print(len(all_rows))
    all_rows = all_rows[1:]

    # Convert the extracted list of lists into a pandas DataFrame
    df = pd.DataFrame(all_rows)
    header_idx = 0

    # Set the columns and drop the rows before the actual data starts
    df.columns = df.iloc[header_idx]
    df = df.iloc[header_idx + 1:].copy()

    # Drop any completely empty rows
    df.dropna(how='all', inplace=True)

    # Drop non-valid rows
    df = df.dropna(subset=['Date'])
    df = df.drop_duplicates()

    # Clean up newline characters within cells (common in PDF extraction)
    # This prevents cells with multiple lines from breaking the CSV layout
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('\n', ' ', regex=False).str.strip()

    # Define the exact headers you requested
    requested_columns = [
        'Sport', 
        'Zone', 
        'Session Code', 
        'Date', 
        'Games Day', 
        'Session Description', 
        'Start Time', 
        'End Time'
    ]

    # Filter the DataFrame to only include the requested columns
    # We use a list comprehension to ensure we don't throw an error if a column is slightly misspelled in the PDF
    final_cols = [col for col in requested_columns if col in df.columns]
    
    if len(final_cols) < len(requested_columns):
        missing = set(requested_columns) - set(final_cols)
        print(f"Warning: Could not find the following requested columns in the PDF: {missing}")

    df_final = df[final_cols]

    # Export to CSV
    df_final.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Success! Data parsed and saved to '{output_csv_path}'.")

if __name__ == "__main__":
    # Specify the input PDF and the desired output CSV name
    INPUT_PDF = "LA28OlympicGamesCompetitionScheduleByEventV3.0.pdf"
    OUTPUT_CSV = "parsed_la28_Schedule.csv"
    
    parse_olympic_schedule(INPUT_PDF, OUTPUT_CSV)