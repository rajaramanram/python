#output get_day,get_month
from datetime import *
import datetime
from datetime import datetime
get_today=date.today()
#print(get_today)
import calendar
get_day= calendar.day_name[get_today.weekday()]
#print(get_day)
#for month
currentMonth = datetime.now().month
#print(currentMonth)
get_month=calendar.month_name[currentMonth]
#print(get_month)
currentDate=datetime.now().day
#print(currentDate)
currentYear=datetime.now().year
#print(currentYear)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
#print(current_time)
'''
import iso8601
import dateutil.parser
from pytz import timezone

fmt = '%Y-%m-%d %H:%M:%S %Z'
ist =  timezone('Asia/Kolkata')

str = '2017-07-30T10:00:00+05:30'
d = iso8601.parse_date(str).astimezone(ist)
print(d.strftime(fmt))

d = dateutil.parser.parse(str).astimezone(ist)
print(d.strftime(fmt))'''
total_date_time=get_day[:3]+' '+get_month[:3]+' '+str(currentDate)+' '+str(current_time)+' '+'IST'+' '+str(currentYear)
#print(total_date_time)
