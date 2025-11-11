import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
import pandas as pd
from mailmerge import MailMerge
import re
from typing import List, Dict, Any



# Functions:
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




class MailMergeApp:
    
    # Constructor:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Mail Merge Generator")

        # Variables
        self.data_file_path: Path | None = None
        self.template_file_path: Path | None = None
        self.output_directory: Path | None = None
        self.grouping_column: tk.StringVar = tk.StringVar()

        # UI Elements
        self.create_widgets()


    # Methods:
    def create_widgets(self) -> None:
        # Data file selector
        tk.Label(self.root, text="Select Data File:").grid(row=0, column=0, sticky="w")
        tk.Button(self.root, text="Browse", command=self.select_data_file).grid(row=0, column=1)

        # Template file selector
        tk.Label(self.root, text="Select Template File:").grid(row=1, column=0, sticky="w")
        tk.Button(self.root, text="Browse", command=self.select_template_file).grid(row=1, column=1)

        # Output folder selector
        tk.Label(self.root, text="Select Output Folder:").grid(row=2, column=0, sticky="w")
        tk.Button(self.root, text="Browse", command=self.select_output_folder).grid(row=2, column=1)

        # Grouping column dropdown
        tk.Label(self.root, text="Grouping Column:").grid(row=3, column=0, sticky="w")
        self.grouping_dropdown = ttk.Combobox(self.root, textvariable=self.grouping_column, state="readonly")
        self.grouping_dropdown.grid(row=3, column=1)

        # Run button
        tk.Button(self.root, text="Run Mail Merge", command=self.run_mail_merge).grid(row=4, column=0, columnspan=2, pady=10)

    def select_data_file(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.data_file_path = Path(file_path)
            self.load_columns()

    def select_template_file(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if file_path:
            self.template_file_path = Path(file_path)

    def select_output_folder(self) -> None:
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_directory = Path(folder_path)

    def load_columns(self) -> None:
        try:
            df = pd.read_excel(self.data_file_path)
            columns = df.columns.tolist()
            self.grouping_dropdown["values"] = columns
            if columns:
                self.grouping_column.set(columns[0])
        except Exception as e:
            print(f"Error loading columns: {e}")

    def run_mail_merge(self) -> None:
        # You can fill in the logic here
        print("Running mail merge...")
        print(f"Data file: {self.data_file_path}")
        print(f"Template file: {self.template_file_path}")
        print(f"Output folder: {self.output_directory}")
        print(f"Grouping column: {self.grouping_column.get()}")
        
        
        teacher_data: pd.DataFrame = load_excel_data(self.data_file_path)
        generate_documents(teacher_data, self.template_file_path, self.grouping_column.get())


# Main Execution:
if __name__ == "__main__":
    root = tk.Tk()
    app = MailMergeApp(root)
    root.mainloop()
