from flask import Flask, redirect, render_template  # , request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/news', methods=['GET', 'POST'])
def news():
    form = AddNewsForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('add_news.html', title='N', form=form)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret_key'
    app.run(port=8080, host='127.0.0.1')
