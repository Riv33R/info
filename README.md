# 📖 Справочник сотрудников МОУ "ДСШ" № 1
Этот проект представляет собой веб-сервис, предназначенный для удобного хранения и отображения контактной информации сотрудников образовательного учреждения МОУ "ДСШ" № 1.

# 🛠️ Функциональные возможности
Отображение данных: Список сотрудников представлен в табличной форме, содержащей:
ФИО сотрудника
Занимаемую должность
Контактный номер телефона
Быстрые звонки: Возможность совершения звонков прямо из браузера на устройствах, поддерживающих функцию "click-to-call".
Простота использования: Адаптивный и минималистичный интерфейс, удобный как для ПК, так и для мобильных устройств.

# 📂 Структура проекта

```
/
├── static/                # Статические файлы (CSS, JS)
│   ├── script.js          # Скрипты JavaScript
│   └── style.css          # Стили CSS
├── templates/             # Шаблоны HTML
│   └── index.html         # Главная HTML-страница
├── app.py                 # Основной файл приложения на Flask
├── requirements.txt       # Список зависимостей проекта
├── userdata.ps1           # Скрипт PowerShell (для выгрузки данных пользователей из AD)
├── README.md              # Документация проекта
└── .gitignore             # Исключения для Git
```
# 🚀 Установка и запуск
1. Установите зависимости
Убедитесь, что Python установлен на вашем устройстве. Затем выполните:

```
pip install -r requirements.txt
```

# 2. Запустите приложение
Запустите сервер разработки:

```
python app.py
```
# 3. Откройте в браузере
Перейдите по адресу:

```
http://127.0.0.1:5000
```
