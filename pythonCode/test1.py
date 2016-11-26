import time

# today = datetime.date.today()
# text = '{today.year}/{today.month}/{today.day}'.format(today = today)
# text= today.strftime('%m/%d/%y')
# # print(text)

# now = datetime.datetime.now()
# date_text = now.strftime('%H:%M:%S.%f')
date_text = time.strftime('%c')
print date_text	
