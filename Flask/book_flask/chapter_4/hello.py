from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'string'
bootstrap = Bootstrap(app)
moment = Moment(app)
class NameForm(FlaskForm):
    name = StringField("Enter the Name", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    name =None
    form =NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data =''
    return render_template('index.html',form=form, name=name)


if __name__ == '__main__':
    app.run(debug=True)
