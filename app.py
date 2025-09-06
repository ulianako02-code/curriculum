// Упрощенная версия app.js для тестирования
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded - testing calendar");
    renderWeekCalendar();
    displayTestSchedule();
});

function renderWeekCalendar() {
    const calendar = document.getElementById('weekCalendar');
    if (!calendar) {
        console.error("Calendar element not found!");
        return;
    }
    
    console.log("Rendering calendar...");
    
    const today = new Date();
    const currentDate = today.getDate();
    
    // Создаем дни недели (пн-вс)
    const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
    
    for (let i = 0; i < 7; i++) {
        const dayDate = new Date(today);
        dayDate.setDate(today.getDate() - today.getDay() + 1 + i); // Начинаем с понедельника
        
        const dayElement = document.createElement('div');
        dayElement.className = 'day';
        
        // Определяем класс для стилизации
        if (dayDate.getDate() === currentDate) {
            dayElement.classList.add('current-day');
        } else if (dayDate.getDate() < currentDate) {
            dayElement.classList.add('past-day');
        } else {
            dayElement.classList.add('future-day');
        }
        
        dayElement.innerHTML = `
            <div class="day-number">${dayDate.getDate()}</div>
            <div class="day-name">${dayNames[i]}</div>
        `;
        
        calendar.appendChild(dayElement);
    }
}

function displayTestSchedule() {
    const scheduleContent = document.getElementById('scheduleContent');
    if (!scheduleContent) {
        console.error("Schedule content element not found!");
        return;
    }
    
    // Тестовые данные вместо API
    scheduleContent.innerHTML = `
        <div class="schedule-item">
            <div class="time">9:00-10:30</div>
            <div class="subject">Эконометрика (продвинутый уровень)</div>
            <div class="details teacher">Мирзоян Ашот Гамлетович</div>
            <div class="details auditorium">А205</div>
            <div class="divider"></div>
        </div>
        <div class="schedule-item">
            <div class="time">11:00-12:30</div>
            <div class="subject">Эмпирический анализ отраслевых рынков</div>
            <div class="details teacher">Маркова Ольга Анатольевна, Ионкина Карина Александровна, Морозов Антон Николаевич</div>
            <div class="details auditorium">А405</div>
        </div>
    `;
}

// Обновляем текущую дату
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

// Инициализируем при загрузке
updateCurrentDate();
