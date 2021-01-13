from flask import Flask, render_template, session, redirect, url_for,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

class NameForm(FlaskForm):
    name = StringField("Enter the Name", validators=[DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'string'
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))
if __name__ == '__main__':
    app.run(debug=True)
