import calendar


def show_calendar():
    a = calendar.LocaleHTMLCalendar(locale="en_US.UTF-8")
    with open('calendar_d.html', 'w') as g:
        print(a.formatyear(2021, width=4), file=g)