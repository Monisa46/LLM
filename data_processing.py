import pandas as pd

def load_and_clean(file):
    """
    Safely load a CSV or Excel file and clean it for display.
    - Keeps all rows that have at least one valid value.
    - Strips extra spaces from column names.
    - Supports CSVs with commas, semicolons, or tabs.
    - Supports Excel files (.xlsx, .xls)
    """

    # Try reading as CSV with common delimiters
    try:
        df = pd.read_csv(file, encoding="utf-8", sep=",")
    except pd.errors.ParserError:
        try:
            df = pd.read_csv(file, encoding="utf-8", sep=";")
        except pd.errors.ParserError:
            try:
                df = pd.read_csv(file, encoding="utf-8", sep="\t")
            except Exception:
                # If not CSV, try Excel
                try:
                    df = pd.read_excel(file)
                except Exception as e:
                    raise ValueError(f"Cannot read the uploaded file: {e}")

    # Strip extra spaces from column names
    df.columns = df.columns.str.strip()

    # Drop only completely empty rows
    df = df.dropna(how='all')

    # Optionally, reset index
    df.reset_index(drop=True, inplace=True)

    return df

