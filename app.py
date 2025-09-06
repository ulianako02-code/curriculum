// Основные функции приложения
console.log("App.js loaded successfully!");
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    initializeApp();
});

async function initializeApp() {
    try {
        // Устанавливаем текущую дату
        updateCurrentDate();
        
        // Инициализируем календарь
        renderWeekCalendar();
        
        // Загружаем расписание
        await loadSchedule();
        
        // Добавляем обработчики событий
        setupEventListeners();
        
    } catch (error) {
        console.error('Ошибка инициализации:', error);
        showError('Ошибка при загрузке приложения');
    }
}

function updateCurrentDate() {
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    document.getElementById('currentDate').textContent = now.toLocaleDateString('ru-RU', options);
}

function renderWeekCalendar() {
    const calendar = document.getElementById('weekCalendar');
    if (!calendar) {
        console.error("Calendar element not found!");
        return;
    }
    
    console.log("Rendering calendar...");
    calendar.innerHTML = '<div class="day"><div class="day-number">6</div><div class="day-name">Ср</div></div>';
}

function createDayElement(date, currentDate) {
    const day = document.createElement('div');
    day.className = 'day';
    
    const dayNumber = date.getDate();
    const dayNames = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
    const dayName = dayNames[date.getDay()];
    
    // Определяем класс для стилизации
    if (dayNumber === currentDate) {
        day.classList.add('current-day');
    } else if (dayNumber < currentDate) {
        day.classList.add('past-day');
    } else {
        day.classList.add('future-day');
    }
    
    day.innerHTML = `
        <div class="day-number">${dayNumber}</div>
        <div class="day-name">${dayName}</div>
    `;
    
    // Добавляем обработчик клика
    day.addEventListener('click', () => {
        selectDate(date);
    });
    
    return day;
}

async function loadSchedule() {
    try {
        showLoading();
        
        // Проверяем кэш
        const now = Date.now();
        if (!scheduleData || !lastFetchTime || (now - lastFetchTime) > CONFIG.CACHE_DURATION) {
            await fetchScheduleData();
        }
        
        displayScheduleForDate(new Date());
        
    } catch (error) {
        console.error('Ошибка загрузки расписания:', error);
        showError('Ошибка при загрузке расписания. Проверьте соединение или попробуйте позже.');
    }
}

async function fetchScheduleData() {
    try {
        const formData = new URLSearchParams();
        for (const key in CONFIG.REQUEST_BODY) {
            formData.append(key, CONFIG.REQUEST_BODY[key]);
        }
        
        const response = await fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: CONFIG.REQUEST_HEADERS,
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        scheduleData = await response.json();
        lastFetchTime = Date.now();
        
    } catch (error) {
        console.error('Ошибка получения данных:', error);
        throw error;
    }
}

function displayScheduleForDate(date) {
    const scheduleContent = document.getElementById('scheduleContent');
    const scheduleTitle = document.getElementById('scheduleTitle');
    
    if (!scheduleData || !scheduleData.records) {
        scheduleContent.innerHTML = '<div class="error-message">Данные расписания не получены</div>';
        return;
    }
    
    const dateStr = date.toLocaleDateString('ru-RU');
    scheduleTitle.textContent = `Расписание на ${dateStr}`;
    
    const daySchedule = scheduleData.records.filter(record => {
        const recordDate = parseDate(record.r2);
        return recordDate && recordDate.toDateString() === date.toDateString();
    });
    
    if (daySchedule.length === 0) {
        scheduleContent.innerHTML = `
            <div class="no-classes">
                <h3>Занятий нет 🎉</h3>
                <p>На ${dateStr} занятий не запланировано</p>
            </div>
        `;
        return;
    }
    
    let scheduleHTML = '';
    daySchedule.forEach((lesson, index) => {
        scheduleHTML += `
            <div class="schedule-item">
                <div class="time">${lesson.ptime || 'Время не указано'}</div>
                <div class="subject">${lesson.D2 || 'Предмет не указан'}</div>
                <div class="details teacher">${lesson.prs || 'Преподаватель не указан'}</div>
                <div class="details auditorium">${lesson.A2 || 'Аудитория не указана'}</div>
                <div class="details type">${lesson.LessonType || 'Тип не указан'}</div>
                ${index < daySchedule.length - 1 ? '<div class="divider"></div>' : ''}
            </div>
        `;
    });
    
    scheduleContent.innerHTML = scheduleHTML;
}

function parseDate(dateString) {
    try {
        if (dateString && dateString.startsWith('/Date(')) {
            const timestamp = parseInt(dateString.slice(6, -2));
            return new Date(timestamp);
        }
        return null;
    } catch (error) {
        console.error('Ошибка парсинга даты:', error);
        return null;
    }
}

function selectDate(date) {
    // Обновляем выделение в календаре
    document.querySelectorAll('.day').forEach(dayEl => {
        dayEl.classList.remove('current-day');
    });
    
    // Добавляем выделение выбранной дате
    const dayNumber = date.getDate();
    document.querySelectorAll('.day-number').forEach(el => {
        if (parseInt(el.textContent) === dayNumber) {
            el.parentElement.classList.add('current-day');
        }
    });
    
    // Показываем расписание для выбранной даты
    displayScheduleForDate(date);
}

function showLoading() {
    document.getElementById('scheduleContent').innerHTML = `
        <div class="loading">Загрузка расписания</div>
    `;
}

function showError(message) {
    document.getElementById('scheduleContent').innerHTML = `
        <div class="error-message">
            <h3>Ошибка</h3>
            <p>${message}</p>
            <button onclick="location.reload()" style="
                background: #8b0000;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
            ">Попробовать снова</button>
        </div>
    `;
}

function setupEventListeners() {
    // Обработчик для кнопки обновления
    document.getElementById('refreshBtn').addEventListener('click', async () => {
        scheduleData = null;
        lastFetchTime = null;
        await loadSchedule();
    });
    
    // Обработчик для обновления расписания при изменении даты
    const todayBtn = document.querySelector('.current-day');
    if (todayBtn) {
        todayBtn.addEventListener('dblclick', () => {
            const today = new Date();
            updateCurrentDate();
            renderWeekCalendar();
            displayScheduleForDate(today);
        });
    }
}

// Глобальные функции для использования в HTML
window.refreshSchedule = async function() {
    scheduleData = null;
    lastFetchTime = null;
    await loadSchedule();
};
