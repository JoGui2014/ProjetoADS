from flask import Flask, request, render_template, jsonify
from AppGUI import AppGUI

app = Flask(__name)

@app.route('/')
def index():
    return render_template('homePage.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        uploaded_file = request.files['file']
        if uploaded_file:
            app_gui = AppGUI()  # Crie uma instância de AppGUI
            app_gui.csv_to_json(uploaded_file)  # Chame a função json_to_csv
            return 'Conversion successful'
        else:
            return 'No file selected'
    except Exception as e:
        return 'Error converting file: ' + str(e)

if __name__ == '__main__':
    app.run(debug=True)