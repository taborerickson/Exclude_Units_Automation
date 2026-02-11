#app/services/logger.py 

"""  
Added handling to prevent duplicate handlers 
"""
import logging 
from logging.handlers import RotatingFileHandler 
from app.config import LOG_DIR 
from app import __version__ 
from datetime import datetime 

def setup_logger(): 
    """  
    Uses rotating file handler with timestamped filename to separate logger runs 
    Prevents duplicated handlers if it is called repeatedly
    """
    logger = logging.getLogger("report_tool") 
    if logger.handlers: 
        # Already configured -- returns existing logger 
        return logger
    
    logger.setLevel(logging.DEBUG) 

    # Console handler (INFO Level) 
    console_handler = logging.StreamHandler() 
    console_handler.setLevel(logging.INFO) 
    ch_formatter = logging.Formatter(
        f"%(asctime)s | v{__version__} | %(levelname)s | %(message)s"
    )
    console_handler.setFormatter(ch_formatter) 
    logger.addHandler(console_handler) 

    # Rotating file handler (DEBUG) 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    logfile = LOG_DIR / f"app_{timestamp}.log" 
    handler = RotatingFileHandler(
        logfile, 
        maxBytes=5_000_000, 
        backupCount=5, 
        encoding="utf-8" 
    )
    handler.setLevel(logging.DEBUG) 
    formatter = logging.Formatter(
        f"%(asctime)s | v{__version__} | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter) 
    logger.addHandler(handler) 

    # Reducing verbose of third-party libraries 
    logging.getLogger("openpyxl").setLevel(logging.WARNING) 
    logging.getLogger("pandas").setLevel(logging.WARNING) 

    # logging logger initialization with current version 
    logger.info(f"Logger initialized | Version: {__version__}")

    return logger 
