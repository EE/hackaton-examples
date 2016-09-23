from __future__ import print_function

from settings import APIKEY

from suds.client import Client
from lxml import etree

WSDLFILE = 'https://datastoretest.ceidg.gov.pl/CEIDG.DataStore/services/DataStoreProvider.svc?wsdl'

# create client
client = Client(WSDLFILE)

# prepare query (registered in Warsaw)
cities = client.factory.create('ns1:ArrayOfstring')
cities.string.append('Warszawa')

# send request
result = client.service.GetMigrationDataExtendedInfo(AuthToken=APIKEY, City=cities)

# parse response xml
root = etree.fromstring(result)

# print first element
print(etree.tostring(root[0], pretty_print=True))

# print emails of active entries
print(root.xpath('InformacjaOWpisie[DaneDodatkowe/Status/text() = "Aktywny"]/DaneKontaktowe/AdresPocztyElektronicznej/text()'))
