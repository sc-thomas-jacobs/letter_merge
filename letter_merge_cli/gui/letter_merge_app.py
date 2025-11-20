import customtkinter as ctk
import pandas as pd
from filer_picker import FilePicker
from tkinter import messagebox
from pathlib import Path
import letter_merge.core as core


# Constants:
APPEARANCE_MODE: str = "dark"
COLOR_THEME: str = "dark"
APPLICATION_TITLE: str = "Letter Merge V0.1"

APPLICATION_WIDTH: int = 700
APPLICATION_HEIGHT: int = 500
APPLICATION_SIZE: str = f"{APPLICATION_WIDTH}x{APPLICATION_HEIGHT}"


# CustomTkinter configuration.
ctk.set_appearance_mode(APPEARANCE_MODE)
#ctk.set_default_color_theme(COLOR_T#HEME)


class LetterMergeApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        # Instance fields.
        self.data: pd.DataFrame = pd.DataFrame()
        
        # Window configuration.
        self.title(APPLICATION_TITLE)
        self.geometry(APPLICATION_SIZE)

        # Heading
        heading = ctk.CTkLabel(self, text=APPLICATION_TITLE, font=ctk.CTkFont(size=24, weight="bold"))
        heading.pack(pady=15)

        # Main content frame (left column layout)
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # File Pickers stacked vertically
        self.data_picker = FilePicker(content_frame, "Data Source (Excel)", picker_type="file",
                                      filetypes=[("Excel Files", "*.xlsx *.xls")])
        self.data_picker.pack(pady=8, fill="x", expand=True)

        self.template_picker = FilePicker(content_frame, "Template (Word DOCX)", picker_type="file",
                                          filetypes=[("Word Documents", "*.docx")])
        self.template_picker.pack(pady=8, fill="x", expand=True)

        self.output_picker = FilePicker(content_frame, "Output Directory", picker_type="directory")
        self.output_picker.pack(pady=8, fill="x", expand=True)

        # Grouping Type Row
        group_frame = ctk.CTkFrame(content_frame)
        group_frame.pack(side="left", expand=True, pady=5)

        # Label above dropdown
        self.group_label = ctk.CTkLabel(group_frame, text="Grouping Column")
        self.group_label.grid(row=0, column=0, sticky="ew", padx=5)

        self.group_dropdown = ctk.CTkOptionMenu(group_frame, values=[])
        self.group_dropdown.grid(row=1, column=0, sticky="ew", padx=5)

        # Standard Name Row
        name_frame = ctk.CTkFrame(content_frame)
        name_frame.pack(side="left", expand=True, pady=5)

        # Label above entry
        self.name_label = ctk.CTkLabel(name_frame, text="Filename Prefix")
        self.name_label.grid(row=0, column=0, sticky="ew", padx=5)

        self.name_entry = ctk.CTkEntry(name_frame, width=300, placeholder_text="e.g. letter_merge_schools")
        self.name_entry.grid(row=1, column=0, sticky="ew", padx=5)

        # Make both frames expand horizontally
        group_frame.grid_columnconfigure(0, weight=1)
        name_frame.grid_columnconfigure(0, weight=1)


        # Run Button (large, bottom)
        self.run_button = ctk.CTkButton(self, text="Run Merge", width=200, height=50, font=ctk.CTkFont(size=16),command=self.run_logic)
        self.run_button.pack(pady=20)

        # Hook Excel picker to update dropdown
        self.data_picker.button.configure(command=self.browse_data)


    # Methods.
    def browse_data(self) -> None:
        self.data_picker.browse()
        excel_path = self.data_picker.get()
        if excel_path:
            # Update the grouping options.
            self.update_grouping_options(excel_path)
            
    def update_grouping_options(self, excel_path) -> None:
        try:
            df = pd.read_excel(excel_path, nrows=0)  # read headers only
            columns = list(df.columns)
            if columns:
                self.group_dropdown.configure(values=columns)
                self.group_dropdown.set(columns[0])
            else:
                messagebox.showerror("Error", "No columns found in Excel file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read Excel file:\n{e}")

    def run_logic(self) -> None:
        try:
            # Load the data frame.
            self.data = core.load_excel_data(Path(self.data_picker.get()))
            
            core.generate_documents(self.data, Path(self.template_picker.get()), Path(self.output_picker.get()), self.group_dropdown.get(), self.name_entry.get())
            messagebox.showinfo("Success", "Letter merge completed successfully!")
        except Exception as exception:
            messagebox.showerror("Error", f"Letter merge failed:\n{exception}")
