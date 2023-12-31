import sys
import json
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, \
    QRadioButton, QButtonGroup, QMessageBox, QFileDialog


class AppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calendar Tools")
        self.setFixedSize(400, 250)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()

        self.input_label = QLabel("Input File/URL:", self)
        self.layout.addWidget(self.input_label)

        self.input_file_text = QLineEdit(self)
        self.layout.addWidget(self.input_file_text)

        self.button_group = QButtonGroup(self)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_button_clicked)
        self.layout.addWidget(self.convert_button)

        #Inês
        self.over_population_button = QPushButton("Aulas em Sobrelotação", self)
        self.over_population_button.clicked.connect(self.over_population_button_clicked)
        self.layout.addWidget(self.over_population_button)

        self.centralWidget().setLayout(self.layout)

    def convert_button_clicked(self, input_file_or_url):
        #input_file_or_url = self.input_file_text.text()
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

                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Save JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)

                if file_path:
                    self.save_file(file_path, json_data)
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

    #Inês
    def over_population_button_clicked(self):
        input_file = self.input_file_text.text()

        if ".json" in input_file:
            input_file = self.json_to_csv(self, input_file)

        try:
            with self.get_input_stream(input_file) as input_stream:
                csv_data = input_stream.read().decode("utf-8")
                csv_data = [line.split(';') for line in csv_data.split('\n') if line]  # Convert CSV string to a list of lists

                if csv_data:
                    header_row = csv_data[0]
                    lotacao_index = -1  # Initialize with an invalid index
                    inscritos_index = -1  # Initialize with an invalid index

                    # Find the index of the columns dynamically
                    for index, column_name in enumerate(header_row):
                        if "Lotação" in column_name:
                            lotacao_index = index
                        if "Inscritos no turno" in column_name:
                            inscritos_index = index

                    if lotacao_index != -1 and inscritos_index != -1:
                        # Valid columns found, proceed with checking for overpopulation

                        with open("overpopulated_classes.csv", "w", newline="", encoding="utf-8") as csv_file:
                            csv_writer = csv.writer(csv_file)

                            # Write the header row to the output file
                            csv_writer.writerow(header_row)

                            for row in csv_data[1:]:
                                try:
                                    lotacao = int(row[lotacao_index])
                                    inscritos = int(row[inscritos_index])
                                    if isinstance(lotacao, int) and isinstance(inscritos, int):
                                        if inscritos > lotacao:
                                            print(row)
                                            csv_writer.writerow(row)
                                except ValueError as e:
                                    pass
                        csv_file.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", "Error showing Over Population: " + str(e))

        # Display a message indicating the process is complete
        QMessageBox.information(self, "Overpopulation Classes", "Overpopulated classes have been saved to 'overpopulated_classes.csv'.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppGUI()
    ex.show()
    sys.exit(app.exec_())
