import json
from pprint import pprint
from datetime import datetime, timedelta
from pytz import timezone
import pytz
def main():
    with open('example_2.json') as json_data:
        d = json.load(json_data)
        pprint(d)

    print(int(d['quiz']['maths']['q1']['options'][0])+int(d['quiz']['maths']['q1']['options'][2]));

    #create time zone
    eastern = timezone('US/Eastern');
    print(eastern.zone);
    #set local time
    fmt = '%Y-%m-%d %H:%M:%S %Z%z';
    loc_dt = eastern.localize(datetime(2002, 10, 27, 6, 0, 0))
    print(loc_dt.strftime(fmt))
    #based on local time calculate time in Amsterdam
    ams_dt = loc_dt.astimezone(timezone('Europe/Amsterdam'))
    print(ams_dt.strftime(fmt))

    utc = pytz.utc;
    utc_dt = datetime(2002, 10, 27, 12, 0, 0, tzinfo=utc)
    loc_dt = utc_dt.astimezone(timezone('Australia/NSW'))
    print(loc_dt.strftime(fmt))
if __name__ == '__main__':
  main()