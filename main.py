from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kfjwnefj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Используем SQLite в качестве базы данных
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(70), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/error')
def error_page():
    return render_template('error.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверяем наличие пользователя в базе данных
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Вход выполнен успешно, редиректим на главную страницу
            return redirect(url_for('index'))
        else:
            # Ошибка входа
            return render_template('error_login.html')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User.query.filter_by(username=username, password=password).first()
        if new_user:
            flash('Ошибка ввода!')
            flash('Такой пользователь уже существует!')
            return redirect(url_for('register'))
        else:
            return redirect(url_for('index'))
    return render_template('register.html')



@app.route('/convert', methods=['POST'])
def convert():
    try:
      rate = float(request.form['rate'])
      amount = float(request.form['amount'])
      try:
       rate / amount == 0
      except ZeroDivisionError:
          return 'Ошибка!'
      dollars = rate / amount
      if str(rate).isalpha() or str(amount).isalpha():
          flash('Строка содержит буквы!')
          return redirect('/')
      if rate > amount:
          return render_template('error_digit.html')
      if rate != 0 and dollars != 0:
        return render_template('result.html', dollars=dollars)
      if rate == 0 or amount == 0:
          flash('Ошибка ввода!')
          return render_template('index.html')
      if rate == 0 and amount == 0:
          flash('Ошибка ввода!')
          return redirect('/')
      else:
        return 'Ошибка ввода!'
    except ValueError or ZeroDivisionError:
        return redirect('/')



if __name__ == '__main__':  
    app.run(debug=True)
