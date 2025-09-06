from flask import Flask, render_template, jsonify
import json
from datetime import datetime, date
import parser  # Импортируйте ваш модуль с парсером здесь

app = Flask(__name__)

# Маршрут для главной страницы
@app.route('/')
def index():
    # Запустите парсер для обновления данных (можно с ограничением по частоте)
    # parser.fetch_schedule()  # Раскомментируйте, если хотите обновлять при каждом входе
    return render_template('index.html')

# API-маршрут для получения расписания на конкретную дату
@app.route('/api/schedule/<date_str>')
def get_schedule(date_str):
    try:
        # Парсим дату из URL
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Загружаем данные из JSON-файла, который создает парсер
    try:
        with open('data/schedule.json', 'r', encoding='utf-8') as f:
            all_schedules = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'Schedule data not found.'}), 404

    # Преобразуем даты в строки для сравнения и фильтруем занятия на выбранный день
    schedule_for_date = []
    for record in all_schedules.get('records', []):
        # Предположим, что дата хранится в поле 'datestr' в формате "DD.MM.YYYY"
        record_date_str = record.get('datestr')
        if not record_date_str:
            continue
        try:
            record_date = datetime.strptime(record_date_str, '%d.%m.%Y').date()
        except ValueError:
            continue

        if record_date == selected_date:
            schedule_for_date.append(record)

    return jsonify(schedule_for_date)

if __name__ == '__main__':
    app.run(debug=True)  # Запускаем сервер в режиме отладки
