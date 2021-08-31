import calendar
def show_calendar():
    caln = calendar.LocaleHTMLCalendar(locale='Russian_Russia')
    calendarq=caln.formatmonth(2021)