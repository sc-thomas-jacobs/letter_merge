from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docxcompose.composer import Composer
from docx.shared import Mm
from io import BytesIO
import utils


def load_excel_data(file_path: Path) -> pd.DataFrame | Exception:
    """
    Loads Excel data from the specified file path.

    Args:
        file_path (Path): Path to the Excel file.

    Raises:
        RuntimeError: If loading the Excel file fails.

    Returns:
        pd.DataFrame | Exception: DataFrame containing the Excel data or an Exception if loading fails.
    """
    
    
    try:
        return pd.read_excel(file_path)
    except Exception as exception:
        raise RuntimeError(f"Failed to load Excel data from {file_path}: {exception}")


def generate_documents(data, template_path, output_path, grouping_column) -> None | Exception:
    """
    Generates documents by merging data into a Word template, grouped by a specified column.

    Args:
        data (_type_): Data to merge into the template.
        template_path (_type_): Path to the Word template.
        output_path (_type_): Path to save the generated documents.
        grouping_column (_type_): Column name to group data by.

    Raises:
        RuntimeError: If document generation fails for any group.
        RuntimeError: If template loading fails.
        RuntimeError: If rendering a record fails.

    Returns:
        None | Exception: None if successful, or an Exception if an error occurs.
    """
    
    
    # For each unique group in the grouping column.
    for group_name in data[grouping_column].unique():
        # Filter data for the current group.
        group_data = data[data[grouping_column] == group_name]

        try:
            base_doc = Document(template_path)
            composer = Composer(base_doc)
        except Exception as e:
            # Log and raise error if template loading fails.
            raise RuntimeError(f"Failed to load template for group {group_name}: {e}")

        # Process each record in the group.
        for idx, record in enumerate(group_data.itertuples(index=False)):
            try:
                # Render the document for the current record.
                doc = DocxTemplate(template_path)
                
                # Prepare context for rendering.
                context = record._asdict()
                context["group_name"] = group_name
                doc.render(context)

                # Save rendered document to a BytesIO buffer to avoid file I/O.
                buf = BytesIO()
                doc.save(buf)
                buf.seek(0)

                temp_doc = Document(buf)
                
                # If this is the first record, initialize the composer with the base document.
                if idx == 0:
                    base_doc = temp_doc
                    composer = Composer(base_doc)
                # Otherwise, append the rendered document.
                else:
                    composer.append(temp_doc)
            
            except Exception as e:
                # Log and raise error if rendering fails.
                raise RuntimeError(f"Failed to render record {record} in group {group_name}: {e}")

        try:
            output_filename = output_path / f"letter_{group_name}.docx"
            composer.save(output_filename)
        except Exception as e:
            # Log and raise error if saving fails.
            raise RuntimeError(f"Failed to save output for group {group_name}: {e}")


# Constants
DATA_FILE = Path(r"C:\Users\Thomas.Jacobs\OneDrive - Vertas Group Limited\Documents\Projects\Letter Merge V2\SAF Data Source.xlsx")
TEMPLATE_FILE = Path(r"C:\Users\Thomas.Jacobs\OneDrive - Vertas Group Limited\Documents\Projects\Letter Merge V2\NEW TEMPLATE.docx")
OUTPUT_DIR = Path(r"C:\Users\Thomas.Jacobs\OneDrive - Vertas Group Limited\Documents\Projects\Letter Merge V2")
GROUPING_COLUMN = "SCHOOL"

# Run pipeline
data_frame: pd.DataFrame = load_excel_data(DATA_FILE)
generate_documents(data_frame, TEMPLATE_FILE, OUTPUT_DIR, GROUPING_COLUMN)
