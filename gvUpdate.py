import greenview, os.path, logging
from datetime import datetime
import json

class DateRecord(object):
    """represents a file on disk with a simple list of dates"""
    def __init__(self, fileName, max_len=None):
        """read file into data array"""
        self.max_len = max_len
        self.format = "%d/%m/%Y %H:%M:%S"
        self.filename = fileName
        self.data = []
        if os.path.exists(self.filename):
            from csv import reader as rdr
            with open(self.filename, 'r') as date_file:
                reader = rdr(date_file)
                for row in reader:
                    self.data.append(datetime.strptime(row[0], self.format))

    def updateFile(self, date):
        """Add a date to the end of the array and write all back to file"""
        from csv import writer as wtr
        self.data.append(date)
        if self.max_len is not None:
            while len(self.data) > self.max_len:
                self.data = self.data[1:]
            
        with open(self.filename, 'w') as date_file:
            writer = wtr(date_file)
            for record in self.data:
                writer.writerow([datetime.strftime(record, self.format)])

    def latestDownload(self):
        """return the latest date downloaded"""
        try:
            return self.data[-1]
        except IndexError:
            return None

def maintain(root, meter_id):
    dateFile = os.path.join(root, 'date_%04i.csv' % meter_id)
    ws = greenview.WebService()
    dr = DateRecord(dateFile, max_len=1)
    latest_in_file = dr.latestDownload()
    latest_on_server = ws.GraemeLatestReadingDate(meter_id).datetime
    if not latest_in_file or (latest_in_file < latest_on_server):
        logging.info('downloading meter %04i' % meter_id)
        w = ws.GraemeLatestWeek(meter_id)
        lw = w.data()
        profile_root = os.path.join(os.path.dirname(__file__), 'profiles')
        profile_file = os.path.join(profile_root, 'profile_%04i.json' % int(meter_id))
        with open(profile_file, 'r') as f:
            p = json.load(f)
        result = {
            'upper': [p[lw['datetime'][i].strftime("%a%H%M")]['upper'] for i in range(len(lw['value']))],
            'lower': [p[lw['datetime'][i].strftime("%a%H%M")]['lower'] for i in range(len(lw['value']))],
            'time_id': [lw['datetime'][i].strftime("%a%H%M") for i in range(len(lw['value']))],
            'value': list(lw['value']),
            'datetime': [lw['datetime'][i].strftime("%m/%d/%Y %H:%M:%S") for i in range(len(lw['value']))]
        }
        chart_file = os.path.join(root, 'chart_%04i.json' % int(meter_id))
        with open(chart_file, 'w') as f:
            json.dump(result, f)
        dr.updateFile(latest_on_server)
        logging.debug('meter %04i download complete' % meter_id)
    else:
        logging.info('meter %04i already downloaded (%s)' % (meter_id, latest_in_file))

def main(root):
    try:
        logging.debug('Starting update')
        for meter_id in [213, 69, 111, 15, 490]:
            logging.debug('Maintaining meter %04i' % meter_id)
            maintain(root, meter_id)
    except greenview.ServerError, e:
        logging.warning('<==============================Server problem==============================')    
        logging.warning(e)#I know this will happen sometimes so its just a warning
    except Exception, e:
        logging.error('<==============================Unexpected error==============================')
        logging.error(e)
        raise
    finally:
        logging.debug('Update complete')
    
if __name__ == "__main__":    
    root = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(root): os.makedirs(root)
    logFile = os.path.join(root, 'update.log')
    logging.basicConfig(filename=logFile, level=logging.WARNING, format='%(levelname)s: %(asctime)s %(message)s')
    main(root)
