from PyQt6 import QtWidgets, QtCore
from Summarizer import summarize
from MainWindow import Ui_MainWindow
from database import Database
import markdown

class SummarizerWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)

    def __init__(self, url, scope, language, api_key):
        super().__init__()
        self.url = url
        self.scope = scope
        self.language = language
        self.api_key = api_key

    def run(self):
        try:
            result = summarize(self.url, self.scope, self.language, self.api_key)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class Youtube_summarizer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()

        # Load saved API key
        saved_key = self.db.get_api_key("google_api_key")
        if saved_key:
            self.ui.apiKeyLineEdit.setText(saved_key)

        self.ui.pushButton.clicked.connect(self.handle_summarize)
        self.ui.saveButton.clicked.connect(self.handle_save_api_key)

    def handle_save_api_key(self):
        api_key = self.ui.apiKeyLineEdit.text()
        if api_key:
            self.db.add_entry("google_api_key", api_key)
            QtWidgets.QMessageBox.information(self, "Success", "API Key saved successfully!")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter an API Key.")

    def handle_summarize(self):
        url = self.ui.lineEdit.text()
        scope = self.ui.levelOfDetailComboBox.currentText()
        language = self.ui.languageComboBox.currentText()
        api_key = self.ui.apiKeyLineEdit.text()

        if not api_key:
            self.ui.textBrowser.setText("Error: Please enter a Google API Key.")
            return

        self.show_loading()
        
        self.worker = SummarizerWorker(url, scope, language, api_key)
        self.worker.finished.connect(self.handle_result)
        self.worker.error.connect(self.handle_error)
        self.worker.finished.connect(self.hide_loading)
        self.worker.error.connect(self.hide_loading)
        self.worker.start()

    def show_loading(self):
        self.ui.pushButton.setEnabled(False)
        self.ui.textBrowser.setText("Loading summary... Please wait.")
        # Optional: You could add a more visual loading indicator here if needed

    def hide_loading(self):
        self.ui.pushButton.setEnabled(True)

    def handle_result(self, result):
        html_result = markdown.markdown(result)
        self.ui.textBrowser.setHtml(html_result)

    def handle_error(self, error_msg):
        self.ui.textBrowser.setText(f"Error: {error_msg}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    youtube_summarizer = Youtube_summarizer()
    youtube_summarizer.show()
    sys.exit(app.exec())