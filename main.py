import mailmerge
import pandas as pd




# Load the data source from an excel file.
data = pd.read_excel('Data.xlsx')

file_breakpoint = "Name"




# Load each of the unique schools from the data.
breakpoints = data[file_breakpoint].unique()


# Load the word template document.
template = 'TEACHER SALARY ASSESSMENT FORM.docx'



    
for breakpoint in breakpoints:
    # Filter data for the current school.
    set = data[data[file_breakpoint] == breakpoint]
    
    # Prepare records for mail merge.
    records = set.to_dict(orient='records')
    
    with mailmerge.MailMerge(template,
        remove_empty_tables=False,
        auto_update_fields_on_open="no",
        keep_fields="none",
        enable_experimental=False) as document:
        # Merge the records into the document.
        document.merge_templates(records, separator='page_break')
    
        document.write(f'{breakpoint}_Output.docx')
        print(f'Generated document for {breakpoint}')