// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;

// Сообщаем Telegram что приложение готово
tg.ready();

// Раскрываем на весь экран
tg.expand();

// Данные о домашках (потом будем загружать с сервера)
const homeworks = {
    "01/23/2026": {
        "dailytask": {
            "vocabulary": "apple, banana, cherry",
            "reading": "B, C, A, D"
        },
        "homework": {
            "workbook": "1-B, 2-A, 3-C, 4-D, 5-A",
            "essay": "Summer is great..."
        }
    },
    "01/22/2026": {
        "dailytask": {
            "listening": "A, B, B, C",
            "vocabulary": "car, house, tree"
        },
        "homework": {
            "workbook": "1-A, 2-C, 3-B"
        }
    },
    "01/21/2026": {
        "dailytask": {
            "reading": "C, A, D, B"
        },
        "homework": {
            "grammar": "1-B, 2-B, 3-A, 4-D"
        }
    }
};

// Получаем отсортированный список дат
const dates = Object.keys(homeworks).sort((a, b) => new Date(b) - new Date(a));
let currentDateIndex = 0;

// Элементы DOM
const currentDateEl = document.getElementById('currentDate');
const cardsContainer = document.getElementById('cardsContainer');
const prevBtn = document.getElementById('prevDate');
const nextBtn = document.getElementById('nextDate');
const copyAllBtn = document.getElementById('copyAllBtn');

// === Рендер карточек ===
function renderCards() {
    const date = dates[currentDateIndex];
    const data = homeworks[date];

    currentDateEl.textContent = `🗓 ${date}`;

    if (!data) {
        cardsContainer.innerHTML = `
            <div class="empty-state">
                <div class="emoji">😢</div>
                <div>No answers for this date</div>
            </div>
        `;
        return;
    }

    let html = '';

    for (const [taskType, tasks] of Object.entries(data)) {
        const emoji = taskType === 'dailytask' ? '📝' : '📚';
        const title = taskType === 'dailytask' ? 'Daily Task' : 'Homework';

        html += `
            <div class="card" data-type="${taskType}">
                <div class="card-header">
                    <div class="card-title">
                        <span class="card-emoji">${emoji}</span>
                        ${title}
                    </div>
                    <button class="copy-btn" onclick="copyCard('${taskType}')">Copy</button>
                </div>
                <div class="card-content">
        `;

        for (const [taskName, answer] of Object.entries(tasks)) {
            html += `
                <div class="task-item">
                    <span class="task-name">${capitalize(taskName)}</span>
                    <span class="task-answer">${answer}</span>
                </div>
            `;
        }

        html += `</div></div>`;
    }

    cardsContainer.innerHTML = html;

    // Обновляем состояние кнопок навигации
    prevBtn.disabled = currentDateIndex >= dates.length - 1;
    nextBtn.disabled = currentDateIndex <= 0;
}

// === Копирование одной карточки ===
function copyCard(taskType) {
    const date = dates[currentDateIndex];
    const tasks = homeworks[date][taskType];

    let text = '';
    for (const [name, answer] of Object.entries(tasks)) {
        text += `${capitalize(name)}: ${answer}\n`;
    }

    copyToClipboard(text);

    // Анимация кнопки
    const btn = document.querySelector(`.card[data-type="${taskType}"] .copy-btn`);
    btn.textContent = '✓ Copied';
    btn.classList.add('copied');

    setTimeout(() => {
        btn.textContent = 'Copy';
        btn.classList.remove('copied');
    }, 1500);

    // Вибрация (если поддерживается)
    tg.HapticFeedback.impactOccurred('light');
}

// === Копирование всего ===
copyAllBtn.addEventListener('click', () => {
    const date = dates[currentDateIndex];
    const data = homeworks[date];

    if (!data) return;

    let text = `📅 ${date}\n\n`;

    for (const [taskType, tasks] of Object.entries(data)) {
        const title = taskType === 'dailytask' ? '📝 Daily Task' : '📚 Homework';
        text += `${title}\n`;

        for (const [name, answer] of Object.entries(tasks)) {
            text += `• ${capitalize(name)}: ${answer}\n`;
        }
        text += '\n';
    }

    copyToClipboard(text);
    showToast('All answers copied! ✓');

    tg.HapticFeedback.notificationOccurred('success');
});

// === Навигация по датам ===
prevBtn.addEventListener('click', () => {
    if (currentDateIndex < dates.length - 1) {
        currentDateIndex++;
        renderCards();
        tg.HapticFeedback.impactOccurred('light');
    }
});

nextBtn.addEventListener('click', () => {
    if (currentDateIndex > 0) {
        currentDateIndex--;
        renderCards();
        tg.HapticFeedback.impactOccurred('light');
    }
});

// === Вспомогательные функции ===
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).catch(() => {
        // Fallback для старых браузеров
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    });
}

function showToast(message) {
    // Создаём toast если его нет
    let toast = document.querySelector('.toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.className = 'toast';
        document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}

// === Инициализация ===
renderCards();

// Показываем приветствие с именем пользователя
if (tg.initDataUnsafe?.user?.first_name) {
    showToast(`Hi, ${tg.initDataUnsafe.user.first_name}! 👋`);
}