from PyQt6 import QtWidgets
from Summarizer import summarize
from MainWindow import Ui_MainWindow

class Youtube_summarizer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.handle_summarize)

    def handle_summarize(self):
        url = self.ui.lineEdit.text()
        scope = self.ui.levelOfDetailComboBox.currentText()
        language = self.ui.languageComboBox.currentText()
        try:
            result = summarize(url, scope, language)
            self.ui.textBrowser.setText(result)
        except Exception as e:
            self.ui.textBrowser.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    youtube_summarizer = Youtube_summarizer()
    youtube_summarizer.show()
    sys.exit(app.exec())