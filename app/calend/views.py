from flask import render_template, redirect, request, url_for, flash
from .. import db
import calendar    
from . import calend


@calend.route('/calendar', methods=['GET'])
def show_calendar():
    def create_calendar():    
        aln = calendar.LocaleHTMLCalendar(locale="en_US.UTF-8")
        show =  aln.formatyear(2022)
        return show
    return render_template('calendar/calendar_d.html', create_c = create_calendar)
