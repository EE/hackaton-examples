import zeep
import zeep.wsse.username

WSDLFILE = 'https://uslugaterytws1test.stat.gov.pl/wsdl/terytws1.wsdl'
USERNAME = 'TestPubliczny'
PASSWORD = '1234abcd'

client = zeep.Client(WSDLFILE, wsse=zeep.wsse.username.UsernameToken(USERNAME, PASSWORD))

if not client.service.CzyZalogowany():
    raise RuntimeError('CzyZalogowany() == False')
