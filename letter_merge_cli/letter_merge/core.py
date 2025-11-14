from pathlib import Path
import pandas as pd
from mailmerge import MailMerge
from typing import List, Dict, Any
from . import utils

def load_excel_data(file_path: Path) -> pd.DataFrame:
    return pd.read_excel(file_path)

def generate_documents(data: pd.DataFrame, template_path: Path, output_path: Path, grouping_column: str) -> None:
    group_identifiers = data[grouping_column].dropna().unique().tolist()
    for group_name in group_identifiers:
        group_data = data[data[grouping_column] == group_name]
        merge_records = group_data.to_dict(orient='records')
        safe_group_name = utils.sanitize_filename(str(group_name))
        output_filename = output_path / f"{safe_group_name}_Output.docx"
        with MailMerge(template_path) as document:
            document.merge_templates(merge_records, separator='page_break')
            document.write(output_filename)
