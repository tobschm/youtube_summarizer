from PyQt6 import QtWidgets
from Summarizer import summarize
from MainWindow import Ui_MainWindow
from database import Database

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

        try:
            result = summarize(url, scope, language, api_key)
            self.ui.textBrowser.setText(result)
        except Exception as e:
            self.ui.textBrowser.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    youtube_summarizer = Youtube_summarizer()
    youtube_summarizer.show()
    sys.exit(app.exec())