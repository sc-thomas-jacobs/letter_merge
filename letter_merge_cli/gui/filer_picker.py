import customtkinter as ctk
from tkinter import filedialog

class FilePicker(ctk.CTkFrame):
    """
    A custom file or directory picker component for CustomTkinter.

    Args:
        master (_type_): _description_
        label_text (str): _description_
    """
    
    
    # Initialisation.
    def __init__(self, master, label_text: str, picker_type: str ="file", filetypes=None, **kwargs):
        super().__init__(master, **kwargs)

        # Label at the top
        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Entry expands horizontally
        self.entry = ctk.CTkEntry(self)
        self.entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # Button stays fixed
        self.button = ctk.CTkButton(self, text="Browse", command=self.browse)
        self.button.grid(row=1, column=1, padx=5, pady=5)

        # Make column 0 expand
        self.grid_columnconfigure(0, weight=1)

        # Config.
        self.picker_type = picker_type  # "file" or "directory"
        self.filetypes = filetypes if filetypes else [("All files", "*.*")]


    # Methods.
    def browse(self) -> None:
        """
        Open a file or directory dialog and set the selected path in the entry.
        
        Returns:
            None
        """
        
        
        if self.picker_type == "file":
            path = filedialog.askopenfilename(filetypes=self.filetypes)
        else:
            path = filedialog.askdirectory()

        if path:
            self.entry.delete(0, "end")
            self.entry.insert(0, path)

    def get(self) -> str:
        return self.entry.get()
