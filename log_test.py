import logging
import os
from datetime import date
# create logger
lgr = logging.getLogger('logger name')
# lgr.setLevel(logging.WARNING) # log all escalated at and above DEBUG
# add a file handler
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()


# dd/mm/YY H:M:S
d1 = now.strftime("%Y-%m-%d_%H-%M-%S")
print(d1)
f_name = 'face_crop_'+d1+'.txt'
fh = logging.FileHandler(f_name)
fh.setLevel(logging.WARNING) # ensure all messages are logged to file

# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s,%(name)s,%(message)s')
fh.setFormatter(frmt)

# add the Handler to the logger
lgr.addHandler(fh)
# You can now start issuing logging statements in your code
lgr.debug('a debug message')
lgr.info('an info message')
lgr.error('An error writen here.')
lgr.critical('Something very critical happened.')
