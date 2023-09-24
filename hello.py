from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'B0btheskinnylob'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your utoronto email?', validators=[Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email_response')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you have changed your name!')
        if old_email is not None and old_name != form.email.data:
            flash('looks like you have changed you email!')
        session['name'] = form.name.data
        if(re.match("^[a-zA-Z_.+-@]+utoronto+", form.email.data)):
            session['email_response'] = "Your email is " + form.email.data
        else:
            session['email_response'] = "Please use your UofT email address"
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email_response'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_erro(e):
    return render_template('500.html'), 500