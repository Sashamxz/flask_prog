import calendar   
from flask import render_template
from . import calend
from datetime import date


# take date now
def date_now():
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    return today


# settings calendar
def create_calendar():    
    aln = calendar.LocaleHTMLCalendar(locale="C.UTF-8")
    show = aln.formatyear(2022)
    return show


# showcalendar with date today
@calend.route('/calendar', methods=['GET'])
def show_calendar():
    calendarq = create_calendar
    dateq = date_now()
    return render_template('calendar/calendar_d.html', calendarq=calendarq, dateq=dateq)
