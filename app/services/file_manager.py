#app/services/file_manager.py 

"""   
Added safer file copying and cleanup 
Added safety checks 
"""
from pathlib import Path 
import shutil 
from datetime import datetime 
from app.config import DATA_DIR, OUTPUT_DIR 
from app.services.logger import setup_logger 

logger = setup_logger() 

def save_uploaded_file(file_path):
    """
    Copies uploaded file to DATA_DIR 
    If a file with the same name exists: 
        - Appends a timestamp to prevent overwriting 
    Returns path to the copied file
    """ 
    src = Path(file_path) 
    if not src.exists(): 
        raise FileNotFoundError(f"Source file not found: {src}") 
    
    # Makins sure DATA_DIR exists 
    DATA_DIR.mkdir(parents=True, exist_ok=True) 
    destination = DATA_DIR / src.name 
    
    if destination.exists(): 
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
        destination = DATA_DIR / f"{src.stem}_{timestamp}{src.suffix}" 
        logger.info(f"Destination exists -- Using new name: {destination.name}") 

    shutil.copy2(src, destination) 
    logger.info(f"Copied uploaded file to data/: {destination.name}") 

    return destination 

# Updating cleanup functions 
def _clear_directory_contents(directory: Path): 
    """  
    Deletes all files and folders inside 'directory', but not the directory itself
    (skips logs folder) 
    """
    if not directory.exists(): 
        return 
    for entry in directory.iterdir(): 
        try: 
            if entry.is_file() or entry.is_symlink(): 
                entry.unlink()
            elif entry.is_dir(): 
                shutil.rmtree(entry) 
            logger.debug("Removed: %s", entry) 
        except Exception as e: 
            logger.exception("Failed to remove %s: %s", entry, e)

def cleanup_temp_file(): 
    """  
    Removes all files and folders from DATA_DIR and OUTPUT_DIR (not LOG_DIR) 
    """
    try: 
        _clear_directory_contents(DATA_DIR) 
        _clear_directory_contents(OUTPUT_DIR) 
        logger.info("Temporary data/output cleaned up.") 
    except Exception as e: 
        logger.exception("cleanup_temp_file failed: %s", e) 

# def cleanup_temp_file(): 
#     """   
#     Removing files from DATA_DIR and OUTPUT_DIR 
#     Only removing files (not directories) 
#     Does not remove logs/
#     """
#     for folder in [DATA_DIR, OUTPUT_DIR]: 
#         for file in folder.iterdir(): 
#             try: 
#                 if file.is_file(): 
#                     file.unlink() 
#                     logger.debug(f"Removed temporary files: {file}") 
#             except Exception as e: 
#                 logger.exception(f"Failed to removed {file}: {e}") 
