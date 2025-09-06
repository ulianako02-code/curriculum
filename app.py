from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, date, timedelta
from parser import fetch_schedule  # Импортируем функцию парсера


app = Flask(__name__)

# Главная страница с календарем
@app.route('/')
def index():
    return render_template('index.html')

# API-маршрут для получения расписания на конкретную дату
@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    # Получаем дату из запроса (например, /api/schedule?date=2025-09-06)
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Parameter "date" (YYYY-MM-DD) is required'}), 400

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # ЗАПУСКАЕМ ПАРСЕР ДЛЯ ПОЛУЧЕНИЯ СВЕЖИХ ДАННЫХ ПРИ КАЖДОМ ЗАПРОСЕ
    print(f"Запуск парсера для получения актуальных данных...")
    fresh_data = fetch_schedule()  # Эта функция возвращает расписание

    # Фильтруем занятия на выбранный день
    schedule_for_date = []
    for record in fresh_data.get('records', []):
        # Дата в записи хранится в поле 'datestr' в формате "DD.MM.YYYY"
        record_date_str = record.get('datestr')
        if not record_date_str:
            continue
        try:
            # Конвертируем дату из строки "DD.MM.YYYY" в объект date
            record_date = datetime.strptime(record_date_str, '%d.%m.%Y').date()
        except ValueError:
            continue

        if record_date == selected_date:
            # Форматируем запись для фронтенда
            formatted_record = {
                'time': record.get('ptime', ''),
                'subject': record.get('D2', ''),
                'type': record.get('LessonType', ''),
                'auditorium': record.get('A2', ''),
                'teacher': record.get('prs', ''),
                'date': record_date_str
            }
            schedule_for_date.append(formatted_record)

    return jsonify(schedule_for_date)

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
