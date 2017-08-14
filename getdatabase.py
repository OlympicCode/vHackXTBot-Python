import requests
import json
import datetime
import logging
logger = logging.getLogger(__name__)


class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


def main():
    s = requests.session()

    database = s.get("https://vhack.olympiccode.ga/database/getdata.php")
    database = json.loads(database.text)
    # sort = max(database['data'], key=lambda ev: ev[i][3])
    # lines = sorted(database['data'], key=lambda k=database: k['data'][0][2], reverse=True)
    # print sort

    results = [x for x in database['data']]
    data = sorted(results, key=lambda x: x[2])

    logger.info("{:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2}".format("IP".rjust(15),
                                                                   "Username".rjust(15),
                                                                   "Money".rjust(15),
                                                                   "IPSP".rjust(15),
                                                                   "Firewall".rjust(15),
                                                                   "Antivirus".rjust(15),
                                                                   "Add Date".rjust(15)))
    # list_argent = []
    # list_ip = []
    list_total = {}
    list_total = Dictlist()
    d = datetime.date.today()
    day = '{:02d}'.format(d.day)
    month = '{:02d}'.format(d.month)
    year = d.year

    for i, data2 in enumerate(data):
        if "unknown" not in data2[1] and str(year) + "-" + str(month) + "-" + str(day) in data2[6]:
            """print ("{:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2}".format(
                                                              str(data2[0]).rjust(15),
                                                              str(data2[1]).rjust(15),
                                                              str(data2[2]).rjust(15),
                                                              str(data2[3]).rjust(15),
                                                              str(data2[4]).rjust(15),
                                                              str(data2[5]).rjust(15),
                                                              str(data2[6]).rjust(15)))"""
            list_total["ip"] = data2[0], data2[1], data2[2], data2[3], data2[4], data2[5], data2[6]

    results = [x for x in list_total["ip"]]
    data = sorted(results, key=lambda x: int(x[2]), reverse=True)

    for i, data2 in enumerate(data):
        logger.info("{:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2}".format(
                    str(data2[0]).rjust(15),
                    str(data2[1]).rjust(15),
                    str(data2[2]).rjust(15),
                    str(data2[3]).rjust(15),
                    str(data2[4]).rjust(15),
                    str(data2[5]).rjust(15),
                    str(data2[6]).rjust(15)))


if __name__ == "__main__":
    main()
