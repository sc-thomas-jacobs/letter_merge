
# Functions
def log_message(filepath: str, message: str) -> None:
    try:
        with open(filepath, 'a') as log_file:
            log_file.write(message + '\n')
    except Exception as e:
        print(f"Error writing to log file: {e}")
        
        
def log_error(filepath: str, error_message: str) -> None:
    log_message(filepath, f"ERROR: {error_message}")
    
def log_info(filepath: str, info_message: str) -> None:
    log_message(filepath, f"INFO: {info_message}")
    
def log_warning(filepath: str, warning_message: str) -> None:
    log_message(filepath, f"WARNING: {warning_message}")
    
def clear_log(filepath: str) -> None:
    try:
        with open(filepath, 'w') as log_file:
            log_file.write('')
    except Exception as e:
        print(f"Error clearing log file: {e}")