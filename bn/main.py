from bn import Endpoint
from settings import HOST

import requests
from datetime import datetime, timedelta
from collections import defaultdict
import dateutil.parser
import dateutil.tz
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pprint import pprint

api = Endpoint(HOST)
now = datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc())
back = timedelta(days=3)

# gather data
activity = defaultdict(lambda: 0)
for entry in api.get(created_date=(now - back, now)):
    date = dateutil.parser.parse(entry['createdDate']).replace(minute=0, second=0, microsecond=0)
    activity[date] += 1

pprint(activity)

ax = plt.subplot(111)

# plot
ax.bar(*zip(*activity.items()), width=1/24)

# configure x axis
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S'))
ax.xaxis.set_label_text('date')

ax.yaxis.set_label_text('records created')

plt.show()
