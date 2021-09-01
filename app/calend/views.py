from flask import render_template, redirect, request, url_for, flash
from .. import db
import calendar    
from . import calend


@calend.route('/date', methods=['GET', 'POST'])
def show_calendar():
    a = calendar.LocaleHTMLCalendar(locale='ru_RU.UTF-8')
    with open('/home/req/github/flask_proj/app/templates/calendar/calendar_d.html', 'w') as html_d:
        print(a.formatyear(2014, width=4), file=html_d)
    return render_template('calendar/calendar_d.html')