from datetime import datetime, timedelta
import pytz
import dateparser

articletime = dateparser.parse("MAR 07 2021")
print(articletime)

sgtime = datetime.now()
sgtimezone = pytz.timezone('Asia/Kuala_Lumpur')
sgtime = sgtimezone.localize(sgtime)
print(sgtime)

if articletime > sgtime:
    print('articletime>sgtime')
    articletime = articletime - timedelta(days=1)
else:
    print('articletime<sgtime')

print('final article time: ' + str(articletime))




# timestamp = datetime.strptime("Mar 3 2021 6:04 PM", "%b %d %Y %I:%M %p")
#
# timezone = pytz.timezone('US/Eastern')
# timestamp = timezone.localize(timestamp)
# print(timestamp)
# print(timestamp.tzinfo)
#
# timestamp = timestamp.astimezone(pytz.utc)
#
# print(timestamp)
# print(timestamp.tzinfo)


