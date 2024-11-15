from flask import Flask, render_template, request

import pandas as pd

csvfile = "path to your data.csv"

app = Flask(__name__)

@app.route('/')
def index():
    # Чтение данных из CSV файла при каждом запросе
    csv_file_path = csvfile  # Путь к вашему CSV-файлу
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    
    # Преобразуем данные в список словарей для передачи в шаблон
    records = df.to_dict(orient='records')

    return render_template('index.html', records=records)

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=4000, debug=False)

