#app/main.py 

import sys 
from PySide6.QtWidgets import QApplication, QMessageBox  
from app.config import LOG_DIR 
from app.ui.main_window import MainWindow 
from app.services.file_manager import cleanup_temp_file 
from app.services.logger import setup_logger 
from app import __version__ 

# Configuring logger early 
logger = setup_logger() 

# Logging application startup version 
logger.info(f"Starting Report Processing Tool | Version: {__version__}")

# Adding excepthook to log unexpected exceptions 
def handle_uncaught_exception(exc_type, exc_value, exc_tb): 
    """Logging and showing a message for uncaught exceptions"""
    # Avoiding KeyboardInterrupt 
    if issubclass(exc_type, KeyboardInterrupt): 
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return 
    logger.critical("Unhandled exception occured", exc_info=(exc_type, exc_value, exc_tb))
    # Showing a brief message (if GUI available) 
    try: 
        QMessageBox.critical(None, "Unexpected Error", 
                             f"An unexpected error occured. A log has been written to: \n{LOG_DIR}")
    except Exception: 
        print("Unhandled exception occured. Logged at:", LOG_DIR, file=sys.stderr) 

# Registering the hook first 
sys.excepthook = handle_uncaught_exception

def main(): 
    app = QApplication(sys.argv) 
    window = MainWindow() 
    window.show() 
    exit_code = app.exec() 
    # Cleaning up temp files / keeping logs 
    cleanup_temp_file() 
    sys.exit(exit_code) 


if __name__ == "__main__": 
    main() 