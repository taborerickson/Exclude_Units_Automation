#app/main.py 

import sys 
from PySide6.QtWidgets import QApplication 
from app.ui.main_window import MainWindow 
from app.services.file_manager import cleanup_temp_file 
from app.services.logger import setup_logger 
from app import __version__ 

# Configuring logger early 
logger = setup_logger() 

# Logging application startup version 
logger.info(f"Starting Report Processing Tool | Version: {__version__}")

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