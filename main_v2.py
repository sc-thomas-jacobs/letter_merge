import pandas as pd
from mailmerge import MailMerge
from pathlib import Path
import re
from typing import List, Dict, Any


# Functions:
def load_excel_data(file_path: Path) -> pd.DataFrame:
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        raise

def sanitize_filename(name: str) -> str:
    return re.sub(r'[^\w\- ]', '_', name)

def generate_documents(data: pd.DataFrame, template_path: Path, grouping_column: str) -> None:
    
    group_identifiers: List[str] = data[grouping_column].dropna().unique().tolist()

    for group_name in group_identifiers:
        group_data: pd.DataFrame = data[data[grouping_column] == group_name]
        merge_records: List[Dict[str, Any]] = group_data.to_dict(orient='records')
        safe_group_name: str = sanitize_filename(str(group_name))

        try:
            with MailMerge(template_path,remove_empty_tables=False,auto_update_fields_on_open="no",keep_fields="none",enable_experimental=False) as document:
                
                document.merge_templates(merge_records, separator='page_break')
                
                output_filename: str = f"{safe_group_name}_Output.docx"
                
                document.write(output_filename)
                
                print(f"Generated document: {output_filename}")
                
                
        except Exception as e:
            print(f"Error generating document for {group_name}: {e}")


# Main Execution:
if __name__ == "__main__":
    excel_file_path: Path = Path("Data.xlsx")
    word_template_path: Path = Path("TEACHER SALARY ASSESSMENT FORM.docx")
    grouping_column: str = "School"

    teacher_data: pd.DataFrame = load_excel_data(excel_file_path)
    generate_documents(teacher_data, word_template_path, grouping_column)
