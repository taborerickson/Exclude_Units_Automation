#app/ui/main_window.py 

"""  
Fixed layout, types, and returned dictionary 

MainWindow for UI tool 

Features: 
- Drag & drop or Browse to select the report (.xlsx) 
- Copies the uploaded file into DATA_DIR 
- Processes the file in a background worker to kepe UI responsive
- Disables Browse/Drag actions while processing 
- Shows busy/progress indicator while processing 
- Displays results in a read-only QTableView via PandasModel 
- Shows only user-messages in UI with logging going to logs/
"""
from PySide6.QtWidgets import (
    QMainWindow, QTextEdit, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, 
    QHBoxLayout, QTableView, QProgressDialog
)
from PySide6.QtCore import Qt, QRunnable, Slot, QThreadPool, QObject, Signal 
from pathlib import Path 
from app.services.file_manager import save_uploaded_file 
from app.core.processor import process_report 
from app.services.message_service import success_message, error_message
from app.services.logger import setup_logger 
from app.config import OUTPUT_DIR
from app.utils import PandasModel 
from app import __version__ 
import pandas as pd 
import traceback 

logger = setup_logger() 

# Worker / Signals 
class WorkerSignals(QObject): 
    """  
    Signals used by the background worker 
    - finished: returns the result dictionary on success (process_report()) 
    - error: returns the exception text
    - progress: string messages 
    """
    finished = Signal(object) 
    error = Signal(str) 
    progress = Signal(str) 

class ProcessWorker(QRunnable): 
    """  
    QRunnable that runs process_report in worker thread 
    Takes input_path and pushes signals on finished/error/progress
    """
    def __init__(self, input_path: Path, suggested_output: Path = None): 
        super().__init__() 
        self.input_path = Path(input_path) 
        self.suggested_output = suggested_output 
        self.signals = WorkerSignals() 

    @Slot()
    def run(self): 
        try: 
            self.signals.progress.emit("Starting processing...") 
            # Calling core processing function 
            result = process_report(self.input_path, self.suggested_output) 
            self.signals.finished.emit(result) 
        except Exception as e: 
            # Logging full traceback to the logger 
            tb = traceback.format_exc() 
            logger.error("Processing thread error:\n" + tb) 
            # Short UI message 
            self.signals.error.emit(str(e)) 

# Main Window 
class MainWindow(QMainWindow): 
    def __init__(self): 
        super().__init__()
        self.setWindowTitle(f"Exclude Units Report Automation Tool (v{__version__})") 
        self.setMinimumSize(900, 650) 
        # Background thread pool 
        self.threadpool = QThreadPool() 
        logger.info(f"Threadpool with max {self.threadpool.maxThreadCount()} threads created.") 

        """  
        Adding instruction label (replacing status label) 
        """
        self.instruction_label = QLabel(
            "Drag & drop the exported report below\n-or-\nClick 'Browse' to select a file from your local computer"
        )
        # Increasing the font size and centering 
        self.instruction_label.setStyleSheet(
            "font-size:14pt; font-weight:bold; color:#FFFFFF;"
        )
        self.instruction_label.setWordWrap(True) 
        self.instruction_label.setAlignment(Qt.AlignCenter) 

        # Adding primary status label that will update after processing 
        self.status_label = QLabel("Awaiting file...") 
        self.status_label.setStyleSheet("font-size:10pt; color:#DDDDDD;") 
        self.status_label.setWordWrap(True) 
        self.status_label.setAlignment(Qt.AlignCenter) 

        # Adding next steps label (initially hidden) 
        # After a successful run, notifies user that they can run another file 
        self.next_steps_label = QLabel("Note: You can drag another file here or click 'Browse' to process another report.") 
        self.next_steps_label.setStyleSheet("font-size:11pt; color:#4FC3F7;") 
        self.next_steps_label.setWordWrap(True) 
        self.next_steps_label.setAlignment(Qt.AlignCenter) 
        self.next_steps_label.hide() # hidden until processing completes

        # UI: status label and output display 
        # self.status_label = QLabel("Drag & drop report file here, or click Browse.") 
        self.browse_button = QPushButton("Browse...") 
        self.browse_button.clicked.connect(self.on_browse)
    
        # Table view (DataFrame preview) 
        self.table_view = QTableView() 
        self.table_model = PandasModel(pd.DataFrame()) 
        self.table_view.setModel(self.table_model) 
        self.table_view.setSortingEnabled(True) 
        self.table_view.setSelectionBehavior(QTableView.SelectRows) 
        self.table_view.setEditTriggers(QTableView.NoEditTriggers) 

        # Progress diaglog 
        self.progress = None 

        # Layout 
        top_layout = QHBoxLayout() 
        # Left --> instructions & status / Right --> Browse button 
        left_col_layout = QVBoxLayout() 
        left_col_layout.addWidget(self.instruction_label) 
        left_col_layout.addWidget(self.status_label) 
        left_col_layout.addWidget(self.next_steps_label) 
        # Adding the left stacked area and browse button to the top_layout
        top_layout.addLayout(left_col_layout, stretch=1) 
        top_layout.addWidget(self.browse_button, stretch=0) 
        # top_layout.addWidget(self.status_label) 
        # top_layout.addWidget(self.browse_button)

        main_layout = QVBoxLayout() 
        main_layout.addLayout(top_layout) 
        main_layout.addWidget(self.table_view) 

        container = QWidget() 
        container.setLayout(main_layout) 

        # Updating to force UI colors so theme differences don't affect readability when opened
        container.setObjectName("centralWidget") 
        # Adding explicit colors for widgets to the central stylesheet
        container.setStyleSheet("""
            /* Root background */
            QWidget#centralWidget {
                background-color: #2B2B2B;   /* charcoal */
            }

            /* Generic labels: white text */
            QLabel {
                color: #FFFFFF;
            }

            /* Instruction label: slightly larger */
            QLabel[instruction="true"] {
                font-size: 14pt;
                font-weight: bold;
                color: #FFFFFF;
            }

            /* Status label: slightly lighter */
            QLabel[status="true"] {
                font-size: 10pt;
                color: #DDDDDD;
            }

            /* Next-steps label: light blue */
            QLabel[nextsteps="true"] {
                font-size: 11pt;
                color: #4FC3F7;
            }

            /* Browse button - big, bold, high contrast */
            QPushButton#browseButton {
                background-color: #1976D2;
                color: #FFFFFF;
                font-weight: bold;
                font-size: 12pt;
                padding: 10px 18px;
                border-radius: 6px;
                min-width: 120px;
                min-height: 42px;
            }

            /* Browse button hover/pressed */
            QPushButton#browseButton:hover {
                background-color: #3393FF;
            }
            QPushButton#browseButton:pressed {
                background-color: #145A9C;
            }

            /* Table view dark theme */
            QTableView {
                background-color: #333638;
                color: #FFFFFF;
                gridline-color: #555555;
            }
            QHeaderView::section {
                background-color: #424347;
                color: #FFFFFF;
                padding: 4px;
                border: 1px solid #555555;
            }
            """)

        # Applying the attributes that are used by the selectors 
        self.instruction_label.setProperty("instruction", True) 
        self.status_label.setProperty("status", True) 
        self.next_steps_label.setProperty("nextsteps", True) 
        # Setting object name for browse button
        self.browse_button.setObjectName("browseButton") 
        self.browse_button.setMinimumHeight(42) 
        self.browse_button.setMinimumWidth(130) 
        self.setCentralWidget(container)    
        # container.setStyleSheet("background-color:#2B2B2B;")
        # self.setCentralWidget(container) 

        # Cracking processing state 
        self._is_processing = False 

    # Drag and drop 
    def dragEnterEvent(self, event): 
        if event.mimeData().hasUrls(): 
            event.acceptProposedAction()  
        else: 
            event.ignore() 

    def dropEvent(self, event): 
        """  
        Handles a file being dropped into the window
        - Copies to DATA_DIR 
        - Calls processor 
        - Updates UI with messages and preview
        """
        if self._is_processing: 
            self._show_user_message("Processing already in progress. Please Wait.") 
            return 
        
        urls = event.mimeData().urls() 
        if not urls: 
            self._show_user_message("No files dropped.") 
            return 
        
        file_path = Path(urls[0].toLocalFile()) 
        if not file_path.exists(): 
            self._show_user_message("Dropped file not found.") 
            return 
        
        # Enforcing only .xlsx files 
        if file_path.suffix.lower() not in (".xlsx","xlsm",".xls"): 
            self._show_user_message("Please drop an Excel (.xlsx) file.") 
            return 
        
        # Saving file to data/ and starting worker
        try: 
            saved = save_uploaded_file(file_path) 
        except Exception: 
            logger.exception("Failed to save uploaded file.") 
            self._show_user_message("Failed to copy file. Error has been logged.") 
            return 
        
        # Starting the background processing 
        self._start_processing(saved) 

    # Browsing action 
    def on_browse(self): 
        if self._is_processing: 
            self._show_user_message("Processing already in progress.") 
            return 
        windows_filter = "Excel files (*.xlsx *.xlsm *.xls)" 
        fname, _ = QFileDialog.getOpenFileName(self, "Select report", str(Path.home()), windows_filter) 
        if fname: 
            try: 
                saved = save_uploaded_file(Path(fname)) 
            except Exception: 
                logger.exception("Failed to copy selected file.") 
                self._show_user_message("Failed to copy file.") 
                return 
            self._start_processing(saved) 

    # Internal helper functions
    def _start_processing(self, input_path: Path): 
        """  
        Prepares UI state and starts background worker (runs process_report()) 
        Disables Browse button and shows a progress indicator
        """
        self._set_processing_state(True) 
        self._show_progress("Processing report...") 
        # Suggested output filename 
        suggested_output = OUTPUT_DIR / f"exclude_properties_{input_path.stem}.csv" 

        worker = ProcessWorker(input_path, suggested_output)
        worker.signals.progress.connect(lambda s: self._show_user_message(s)) 
        worker.signals.finished.connect(self._on_processing_finished) 
        worker.signals.error.connect(self._on_processing_error)

        # Submitting worker to thread pool 
        self.threadpool.start(worker) 

    def _set_processing_state(self, is_processing: bool): 
        """  
        Enables/disables UI elements while processing 
        Prevents end-user from starting multiple processes/browsing
        """
        self._is_processing = is_processing
        self.browse_button.setEnabled(not is_processing) 

    def _show_progress(self, text: str):
        """  
        Creates and shows progress dialog 
        Using QProgressDialog (without percentage) 
        """
        if self.progress is None: 
            self.progress = QProgressDialog(text, None, 0, 0, self) 
            self.progress.setWindowTitle("Working") 
            self.progress.setWindowModality(Qt.ApplicationModal) 
            self.progress.setCancelButton(None) 
            self.progress.setMinimumDuration(0) 
        self.progress.setLabelText(text) 
        self.progress.show() 

    def _hide_progress(self): 
        if self.progress: 
            self.progress.hide() 
            self.progress.deleteLater() 
            self.progress = None 

    def _show_user_message(self, text: str): 
        """  
        Shows a short status text in the status label 
        """
        self.status_label.setText(text) 

    # Finished / Errors 
    def _on_processing_finished(self, result: dict): 
        """  
        Called when processing is completed (successfully) 
        Updates UI with user message/populates preview table
        """
        self._hide_progress() 
        self._set_processing_state(False) 

        if not result: 
            self._show_user_message("Processing returned no result.") 
            # Keeping instructions and next steps visible for retrying 
            self.next_steps_label.show() 
            return 
        
        # Emphasizing the result message 
        final_msg = result.get("message", success_message()) 
        # Updating the status label text and applying new style 
        self.status_label.setText(final_msg)
        self.status_label.setStyleSheet("font-size:16pt; font-weight:bold; color:#1a8f00;") 
        # Hiding the instruction label (final message is primary message) 
        self.instruction_label.hide() 
        # Showing the next steps for the end-user 
        self.next_steps_label.show() 

        # Result: output_path, flagged_rows, message, preview 
        # self._show_user_message(result.get("message", success_message())) 

        # If output and flagged rows exist: load CSV to DataFrame/preview 
        try: 
            output_path = result.get("output_path") 
            # reading CSV to DataFrame for table display 
            if output_path and Path(output_path).exists(): 
                data = pd.read_csv(output_path) 
                model = PandasModel(data) 
                self.table_view.setModel(model) 
            else: 
                # using text preview if CSV is missing 
                preview_text = result.get("preview", "No preview available.")
                # Converting to DataFrame 
                data_preview = pd.DataFrame({"Preview": preview_text.splitlines()})
                model = PandasModel(data_preview) 
                self.table_view.setModel(model) 
        except Exception: 
            logger.exception("Failed to load output CSV into table view.") 
            self.table_view.setModel(PandasModel(pd.DataFrame({"Preview": ["Failed to render preview."]})))

    def _on_processing_error(self, error_msg: str): 
        """  
        Called when background worker pushes an error 
        """
        self._hide_progress() 
        self._set_processing_state(False) 
        self._show_user_message(error_message()) 
        self.table_view.setModel(PandasModel(pd.DataFrame({"Error": ["Processing failed. Error has been logged."]})))
        # Full error details logged to log files for troubleshooting 


# OLD: 

# # Main Window 
# class MainWindow(QMainWindow): 
#     def __init__(self): 
#         super().__init__()
#         self.setWindowTitle("Exclude Units Report Automation Tool")  
#         self.setAcceptDrops(True) 
#         # UI: status label and output display 
#         self.status_label = QLabel("Drag and drop a report file here") 
#         self.output_display = QTextEdit() 
#         self.output_display.setReadOnly(True) 
#         # Adding browse button (in case end-user prefers it) 
#         self.browse_button = QPushButton("Browse...") 
#         self.browse_button.clicked.connect(self.on_browse) 

#         layout = QBoxLayout() 
#         layout.addWidget(self.status_label) 
#         layout.addWidget(self.output_display) 

#         container = QWidget() 
#         container.setLayout(layout) 
#         self.setCentralWidget(container) 

#     def dragEnterEvent(self, event): 
#         if event.mimeData().hasUrls(): 
#             event.accept() 
#         else: 
#             event.ignore() 

#     def dropEvent(self, event): 
#         """  
#         Handles a file being dropped into the window
#         - Copies to DATA_DIR 
#         - Calls processor 
#         - Updates UI with messages and preview
#         """
#         try: 
#             file_path = Path(event.mimeData().urls()[0].toLocalFile()) 
#             self.status_label.setText("Copying file...") 
#             input_file = save_uploaded_file(file_path) 

#             self.status_label.setText("Processing... please wait") 
#             # Suggested output name for CSV file 
#             suggested_output = OUTPUT_DIR / f"processed_report_{input_file.name}.csv" 

#             result = process_report(input_file, suggested_output) 

#             # Result: dictionary showing user-friendly message and preview
#             self.output_display.setText(result.get("message", success_message())) 
#             self.output_display.setPlainText(result.get("preview", "No preview available.")) 

#         except Exception as e: 
#             logger.exception("Processing Failed.") 
#             # Only showing user-facing error message
#             self.status_label.setText(error_message()) 
#             self.output_display.setPlainText("An error occurred whole processing the file. Error has been logged.")
