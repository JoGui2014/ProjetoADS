import sys
import json
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QButtonGroup, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt

class AppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calendar Tools")
        self.setFixedSize(400, 250)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.input_label = QLabel("Input File/URL:", self)
        layout.addWidget(self.input_label)

        self.input_file_text = QLineEdit(self)
        layout.addWidget(self.input_file_text)

        self.button_group = QButtonGroup(self)

        self.csv_to_json_radio = QRadioButton("CSV to JSON", self)
        self.csv_to_json_radio.setChecked(True)
        layout.addWidget(self.csv_to_json_radio)
        self.button_group.addButton(self.csv_to_json_radio)

        self.json_to_csv_radio = QRadioButton("JSON to CSV", self)
        layout.addWidget(self.json_to_csv_radio)
        self.button_group.addButton(self.json_to_csv_radio)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_button_clicked)
        layout.addWidget(self.convert_button)

        self.centralWidget().setLayout(layout)

    def convert_button_clicked(self):
        option = 1 if self.csv_to_json_radio.isChecked() else 2
        input_file_or_url = self.input_file_text.text()

        try:
            if option == 1:
                self.csv_to_json(input_file_or_url)
            elif option == 2:
                self.json_to_csv(input_file_or_url)
            else:
                raise ValueError("Invalid option: " + option)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        sys.exit()

    def csv_to_json(self, input_file_or_url):
        try:
            with self.get_input_stream(input_file_or_url) as input_stream:
                csv_data = input_stream.read().decode("utf-8")
                json_data = json.dumps(list(csv.DictReader(csv_data.splitlines())))
                self.save_file("JSON", json_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", "Error converting CSV to JSON: " + str(e))

    def json_to_csv(self, input_file_or_url):
        try:
            with self.get_input_stream(input_file_or_url) as input_stream:
                json_data = json.load(input_stream)
                csv_data = csv.DictWriter(sys.stdout, json_data[0].keys())
                csv_data.writeheader()
                csv_data.writerows(json_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", "Error converting JSON to CSV: " + str(e))

    def get_input_stream(self, input_file_or_url):
        if input_file_or_url.startswith("http") or input_file_or_url.startswith("https"):
            from urllib.request import urlopen
            return urlopen(input_file_or_url)
        else:
            return open(input_file_or_url, "rb")

    def save_file(self, file_type, content):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save " + file_type + " File", "", "", options=options)
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                QMessageBox.information(self, "Success", "Successfully converted to: " + file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", "Error saving file: " + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppGUI()
    ex.show()
    sys.exit(app.exec_())