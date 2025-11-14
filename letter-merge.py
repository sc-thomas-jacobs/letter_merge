import argparse
from pathlib import Path
import pandas as pd
from mailmerge import MailMerge
from typing import List, Dict, Any
import re

def load_excel_data(file_path: Path) -> pd.DataFrame | Exception:
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



def run_letter_merge(template_path: str, data_path: str, output_path: str, group_by: str) -> None:
    teacher_data: pd.DataFrame = load_excel_data(data_path)
    generate_documents(teacher_data, template_path)



def main():
    parser = argparse.ArgumentParser(prog="letter-merge")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run the mail merge")
    run_parser.add_argument("--template", required=True, help="Path to the docx template file")
    run_parser.add_argument("--data", required=True, help="Path to the excel data file")
    run_parser.add_argument("--output", required=True, help="Output directory")

    args = parser.parse_args()

    if args.command == "run":
        run_letter_merge(args.template, args.data, args.output)

if __name__ == "__main__":
    main()