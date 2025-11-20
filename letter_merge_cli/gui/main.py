import customtkinter as ctk
import pandas as pd
from filer_picker import FilePicker
from tkinter import messagebox
from pathlib import Path
import letter_merge.core as core
from letter_merge_app import LetterMergeApp

if __name__ == "__main__":
    app = LetterMergeApp()
    app.mainloop()