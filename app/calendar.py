import calendar
def show_calendar():
    caln = calendar.LocaleHTMLCalendar(locale='Russian_Russia')
    with open('calendar.html', 'w') as g:
        print(caln.formatyear(2021, width=4), file=g)