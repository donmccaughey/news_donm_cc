from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', now=datetime.now())


@app.template_filter()
def format_date_time(value: datetime) -> str:
    return value.strftime('%Y-%m-%d %H:%M:%S')
