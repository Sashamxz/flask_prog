from flask import render_template, redirect, request, url_for, flash
from .. import db
import calendar    
from . import calend
from datetime import date




def date_now():
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    return today



# @calend.route('/calendar', methods=['GET'])
def create_calendar():    
    aln = calendar.LocaleHTMLCalendar(locale="C.UTF-8")
    show =  aln.formatyear(2022)
    return show



@calend.route('/calendar', methods=['GET'])
def show_calendar():
    calendarq = create_calendar
    dateq = date_now()
    return render_template('calendar/calendar_d.html', calendarq=calendarq, dateq= dateq)

