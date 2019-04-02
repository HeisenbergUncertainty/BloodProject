from flask import Flask, redirect, render_template, session, request, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm, SelfForm, AddNewsForm
from DataBase import DB, NewsModel, UserModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'no_secret_key'
bootstrap = Bootstrap(app)
db = DB()


@app.route('/')
def nothing():
    return redirect("/logout")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.user_name
    password = form.password
    self = render_template('login.html', title='Авторизация', form=form)

    if request.method == 'GET':
        return self

    elif request.method == 'POST':
        if not (request.form.get('user_name') and request.form.get('password')):
            return self
            # make error введите данные

        else:
            user_model = UserModel(db.get_connection())
            exists = user_model.exists(user_name, password)
            if exists[0]:
                session['user_name'] = user_name
                session['user_id'] = exists[1]
                return redirect("/news")

            else:
                return self
                # make error нет пользователя


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    user_name = form.user_name
    password = form.password
    self = render_template('registration.html', title='Регистрация', form=form)

    if request.method == 'GET':
        return self

    elif request.method == 'POST':

        if not (request.form.get('user_name') and request.form.get('password')):
            return self
            # make error введите данные

        else:
            user_model = UserModel(db.get_connection())
            exists = user_model.exists(user_name, password)

            if exists[0]:
                return self  # make error пользователь уже есть

            else:
                user_model.insert(user_name, password)
                exists = user_model.exists(user_name, password)
                session['user_name'] = user_name
                session['user_id'] = exists[1]
                return redirect("/news")


@app.route('/<int:user_id>', methods=['GET', 'POST'])
def self(user_id):
    if 'user_name' not in session:
        return redirect('/login')

    form = SelfForm()
    isopen = form.isopen #&&&&&&&&&&&&&&&&&&&

    # news = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('self.html', user_name=session['user_name'],
                           user_id=session['user_id'], form=form,
                           avatar=url_for('static',
                                          filename='img/zero_avatar.jpg'))


@app.route('/news', methods=['GET'])
def news():
    if 'user_name' not in session:
        return redirect('/login')
    news = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('news.html', user_name=session['user_name'],
                           user_id=session['user_id'], news=news)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'user_name' not in session:
        return redirect('/login')

    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new = NewsModel(db.get_connection())
        new.insert(title, content, session['user_id'])
        return redirect("/news")

    return render_template('add_news.html', title='Добавление новости',
                           form=form, user_name=session['user_name'],
                           user_id=session['user_id'])


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'user_name' not in session:
        return redirect('/login')
    new = NewsModel(db.get_connection())
    new.delete(news_id)
    return redirect("/news")


@app.route('/logout')
def logout():
    session.pop('user_name', 0)
    session.pop('user_id', 0)
    return redirect('/login')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
