from flask import Flask, render_template, request, send_from_directory
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import EqualTo, DataRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from functools import wraps
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf import FlaskForm
import csv
import os



csvfile = "data.csv"
usersdb = "users.csv"
logondb = "logon.csv"

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, role="user"):
        self.id = id
        self.role = role

@app.route('/', methods=["GET", "POST"])
def index():

    return render_template('index.html')

@app.route('/manual', methods=["GET", "POST"])
def manual():

    return render_template('manual.html')

@app.route('/files/<path:filename>')
def files(filename):
    return send_from_directory('files', filename)

@app.route('/spravka', methods=["GET", "POST"])
def spravka():
    # Чтение данных из CSV файла при каждом запросе
    csv_file_path = csvfile  # Путь к вашему CSV-файлу
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    
    # Преобразуем данные в список словарей для передачи в шаблон
    records = df.to_dict(orient='records')

    return render_template('spravka.html', records=records)

@login_manager.user_loader
def load_user(user_id):
    try:
        with open(usersdb, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["username"] == user_id:
                    return User(id=row["username"], role=row["role"])
    except FileNotFoundError:
        pass
    return None

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Register")

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return redirect(url_for('login'))  # Перенаправляем на страницу входа
        return func(*args, **kwargs)
    return decorated_view
	
def read_csv_data(filepath, search_term):
    results = []
    try:
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (
                    search_term.lower() in row.get("UserName", "").lower()
                    or search_term.lower() in row.get("ComputerName", "").lower()
                ):
                    # Convert LogonTime string to datetime object
                    logon_time = datetime.strptime(row["LogonTime"], "%y-%m-%d %H:%M")
                    # Format the datetime object to the desired format
                    row["LogonTime"] = logon_time.strftime("%d.%m.%Y %H:%M")
                    results.append(row)
            # Sort results by datetime objects in LogonTime
            results.sort(
                key=lambda x: datetime.strptime(x["LogonTime"], "%d.%m.%Y %H:%M"),
                reverse=True,
            )
    except FileNotFoundError:
        results = [{"Error": "File not found or cannot be accessed"}]
    except ValueError as e:
        print(f"Error converting date and time: {e}")

    return results

# Сохраняем пароль в файле как хэш, используя generate_password_hash
def save_user_credentials(username, password, role="user"):
    hashed_password = generate_password_hash(password)
    with open(usersdb, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, hashed_password, role])

# Проверяем правильность пароля, используя check_password_hash
def verify_user_credentials(username, password):
    with open(usersdb, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == username:
                return check_password_hash(row[1], password)
    return False

@app.route("/register", methods=["GET", "POST"])
@login_required
@admin_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = "user"  # По умолчанию создаем пользователя с ролью "user"
        save_user_credentials(username, password, role)
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Проверка пользователя и пароля с использованием хэша
        if verify_user_credentials(username, password):
            user = User(username)
            login_user(user)
            return redirect(url_for("index"))
    
    return render_template("login.html", form=form)

@app.route("/users", methods=["GET"])
@login_required
@admin_required
def users():
    user_list = []
    try:
        with open(usersdb, newline="") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=["username", "password", "role"])
            user_list = [(row["username"], row["role"]) for row in reader]  # Извлекаем только имя и роль
    except FileNotFoundError:
        user_list = []
    return render_template("users.html", users=user_list)

@app.route("/change_role/<username>", methods=["POST"])
@login_required
@admin_required
def change_role(username):
    new_role = request.form.get("role")
    if new_role not in ["admin", "user"]:  # Ограничиваем список ролей
        return "Недопустимая роль", 400

    users = []
    try:
        with open(usersdb, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username:
                    row[2] = new_role  # Изменяем роль
                users.append(row)
    except FileNotFoundError:
        return "Файл пользователей не найден", 404

    # Перезаписываем файл с обновлённой ролью
    with open(usersdb, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(users)

    return redirect(url_for("users"))

@app.route("/delete_user/<username>", methods=["POST"])
@login_required
@login_required
def delete_user(username):
    users = []
    try:
        with open(usersdb, newline="") as csvfile:
            reader = csv.reader(csvfile)
            users = [row for row in reader if row[0] != username]  # Убираем пользователя из списка
    except FileNotFoundError:
        pass

    # Сохраняем обновленный список пользователей
    with open(usersdb, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(users)

    return redirect(url_for("users"))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/logs", methods=["GET", "POST"])
@login_required
@admin_required
def logs():
    results = []
    if request.method == "POST":
        username_or_pcname = request.form["search"]
        # Replace the following path with the path to your file
        filepath = logondb
        results = read_csv_data(filepath, username_or_pcname)
    return render_template("logs.html", results=results)

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=4000, debug=False)

