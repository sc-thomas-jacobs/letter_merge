import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# Reusable path selector widget
class PathSelector(ttk.Frame):
    def __init__(self, parent, label_text, file_type, callback):
        super().__init__(parent)
        self.file_type = file_type
        self.callback = callback
        self.path_var = tk.StringVar()

        # Label
        label = tk.Label(self, text=label_text, font=("Segoe UI", 9, "bold"),
                         bg="#000000", fg="white", anchor="w")
        label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))

        # Frame for entry and button
        self.section_frame = tk.Frame(self, bg="#FFFFFF", bd=1, relief="solid")
        self.section_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.section_frame.columnconfigure(0, weight=1)
        self.section_frame.columnconfigure(1, weight=0)

        # Entry field (left side)
        self.entry = tk.Entry(self.section_frame, textvariable=self.path_var,
                              font=("Segoe UI", 10), state="readonly",
                              relief="flat", bg="white")
        self.entry.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=8)

        # Browse button (right side)
        browse_btn = tk.Button(self.section_frame, text="Browse", command=self.browse,
                               bg="#000000", fg="white", font=("Segoe UI", 10),
                               relief="flat", padx=10)
        browse_btn.grid(row=0, column=1, padx=(5, 10), pady=8)

    def browse(self):
        if self.file_type == "file":
            path = filedialog.askopenfilename()
        elif self.file_type == "folder":
            path = filedialog.askdirectory()
        else:
            path = None

        if path:
            self.path_var.set(path)
            self.callback(Path(path))

    def get_path(self):
        return Path(self.path_var.get()) if self.path_var.get() else None


# Main App
class MailMergeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Schools Choice Mail Merge")
        self.root.geometry("600x400")
        self.root.configure(bg="#000000")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.data_path = None
        self.template_path = None
        self.output_path = None

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#FFFFFF")
        style.configure("TLabel", background="#FFFFFF", foreground="white", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="black", background="#FFFFFF")

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20, style="TFrame")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Schools Choice Mail Merge", style="Header.TLabel").grid(row=0, column=0, pady=(0, 20), sticky="n")

        # Path selectors
        self.data_selector = PathSelector(frame, "Select Data File", "file", self.set_data_path)
        self.data_selector.grid(row=1, column=0, sticky="ew", pady=5)

        self.template_selector = PathSelector(frame, "Select Template File", "file", self.set_template_path)
        self.template_selector.grid(row=2, column=0, sticky="ew", pady=5)

        self.output_selector = PathSelector(frame, "Select Output Folder", "folder", self.set_output_path)
        self.output_selector.grid(row=3, column=0, sticky="ew", pady=5)

        # Run button
        run_btn = tk.Button(frame, text="Run Mail Merge", command=self.run_mail_merge,
                            bg="#1B4F72", fg="white", font=("Segoe UI", 10, "bold"),
                            relief="flat", padx=10)
        run_btn.grid(row=4, column=0, pady=30)

    def set_data_path(self, path: Path):
        self.data_path = path

    def set_template_path(self, path: Path):
        self.template_path = path

    def set_output_path(self, path: Path):
        self.output_path = path

    def run_mail_merge(self):
        if not all([self.data_path, self.template_path, self.output_path]):
            messagebox.showerror("Missing Information", "Please select all required paths.")
            return

        # Placeholder for your mail merge logic
        messagebox.showinfo("Success", f"Mail merge initiated!\n\nData: {self.data_path}\nTemplate: {self.template_path}\nOutput: {self.output_path}")


# Launch
if __name__ == "__main__":
    root = tk.Tk()
    app = MailMergeUI(root)
    root.mainloop()
