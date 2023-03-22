from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, url
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    choice_cf = ['👇🏿', '✘', '☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️']
    choice_wf = ['👇🏿', '✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪']
    choice_pw = ['👇🏿', '✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌']
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location', [DataRequired(), url()])
    open_time = StringField("Open", [DataRequired()])
    close_time = StringField("Close", [DataRequired()])
    coffee_rating = SelectField("Coffee Rating", [DataRequired()], choices=choice_cf)
    wifi_rating = SelectField("Wifi Rating", [DataRequired()], choices=choice_wf)
    power_outlet = SelectField("Power Outlet", [DataRequired()], choices=choice_pw)
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open-closing time, coffee rating, Wi-Fi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        # Exercise:
        # Make the form write a new row into cafe-data.csv
        if form.validate_on_submit():
            with open('Coffee_wifi/cafe-data.csv', 'a', newline='', encoding='utf8') as f:
                new_data = [form.cafe.data.title(), form.location.data, form.open_time.data.upper(),
                            form.close_time.data.upper(),
                            form.coffee_rating.data, form.wifi_rating.data, form.power_outlet.data]
                f.write('\n')
                f.write(",".join(new_data))
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes', methods=['GET', 'POST'])
def cafes():
    with open('Coffee_wifi/cafe-data.csv', 'r', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
