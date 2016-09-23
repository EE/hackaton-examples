from teryt import client
from datetime import datetime

if __name__ == '__main__':
    state_date = datetime.now()
    for wojewodztwo in client.service.PobierzListeWojewodztw(state_date)['JednostkaTerytorialna']:
        print('%s %s' % (wojewodztwo['NAZWA_DOD'], wojewodztwo['NAZWA']))
        for powiat in client.service.PobierzListePowiatow(wojewodztwo['WOJ'], state_date)['JednostkaTerytorialna']:
            print('\t%s %s' % (powiat['NAZWA_DOD'], powiat['NAZWA']))
            for gmina in client.service.PobierzListeGmin(wojewodztwo['WOJ'], powiat['POW'], state_date)['JednostkaTerytorialna']:
                print('\t\t%s %s' % (gmina['NAZWA_DOD'], gmina['NAZWA']))
