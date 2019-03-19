from flask import Flask, redirect, render_template, session  # , request
from flask_bootstrap import Bootstrap
from DataBase import DB, NewsModel, UserModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


app = Flask(__name__)
bootstrap = Bootstrap(app)
db = DB()


@app.route('/')
def start_screen():
    return redirect("/registration")

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
    exists = user_model.exists(user_name, password)
    if exists[0]:
        user_model.insert(user_name, password)
        exists = user_model.exists(user_name, password)
        session['username'] = user_name
        session['user_id'] = exists[1]
        return redirect("/news")
    else:
        pass #Error пользователь уже есть


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
    exists = user_model.exists(user_name, password)
    if exists[0]:
        session['username'] = user_name
        session['user_id'] = exists[1]
        return redirect("/news")
    else:
        pass #Error пользователя несуществует

@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')

@app.route('/news', methods=['GET'])
def news():
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection()).get_all()
    return render_template('news.html', news=nm)

@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/news")
    return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'])

@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/news")



if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret_key'
    app.run(port=8080, host='127.0.0.1')
