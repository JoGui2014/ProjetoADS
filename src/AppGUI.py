import sys
import json
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QButtonGroup, QMessageBox, QFileDialog

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


        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_button_clicked)
        layout.addWidget(self.convert_button)

        self.centralWidget().setLayout(layout)

    def convert_button_clicked(self):
        input_file_or_url = self.input_file_text.text()
        option = 2

        if ".csv" in input_file_or_url:
            option = 1


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
                csv_data = json_data[0].keys()  # Extract the field names

                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

                if file_path:
                    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
                        csv_writer = csv.DictWriter(csv_file, csv_data)
                        csv_writer.writeheader()
                        csv_writer.writerows(json_data)
                    QMessageBox.information(self, "Success", "Successfully converted to: " + file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", "Error converting JSON to CSV: " + str(e))

            # def json_to_csv(self, input_file_or_url):
    #     try:
    #         with self.get_input_stream(input_file_or_url) as input_stream:
    #             json_data = json.load(input_stream)
    #
    #             if isinstance(json_data, list) and len(json_data) > 0:
    #                 # Assuming the CSV header order is preserved in JSON data
    #                 fieldnames = json_data[0].keys()
    #
    #                 # Double-check if fieldnames contain "null" and remove it if present
    #                 if "null" in fieldnames:
    #                     fieldnames.remove("null")
    #
    #                 options = QFileDialog.Options()
    #                 file_path, _ = QFileDialog.getSaveFileName(
    #                     self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
    #
    #                 if file_path:
    #                     with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
    #                         csv_writer = csv.DictWriter(csv_file, fieldnames)
    #                         csv_writer.writeheader()
    #                         csv_writer.writerows(json_data)
    #
    #                     QMessageBox.information(self, "Success", "Successfully converted to: " + file_path)
    #                 else:
    #                     QMessageBox.information(self, "Info", "No file selected for saving.")
    #             else:
    #                 QMessageBox.critical(self, "Error", "Invalid JSON data format.")
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", "Error converting JSON to CSV: " + str(e))

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