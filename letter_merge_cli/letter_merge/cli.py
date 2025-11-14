import argparse
from pathlib import Path
from . import core

def main():
    parser = argparse.ArgumentParser(prog="letter-merge")
    
    # Add the arguments.
    parser.add_argument("--template", required=True, help="Path to the docx template file")
    parser.add_argument("--data", required=True, help="Path to the Excel data file")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--group-by", required=True, help="Column to group by")

    # Parse the arguments.
    args = parser.parse_args()

    # Load data and generate documents.
    data = core.load_excel_data(Path(args.data))
    core.generate_documents(data, Path(args.template), Path(args.output), args.group_by)


if __name__ == "__main__":
    main()