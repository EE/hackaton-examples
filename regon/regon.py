import zeep
from lxml import etree
import requests_toolbelt.multipart
import xmltodict
import json

WSDLFILE = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl.xsd'
APIKEY = 'abcde12345abcde12345'


# change namespace of header tag
class HeaderNamespacePlugin(zeep.Plugin):
    def egress(self, envelope, http_headers, operation, binding_options):
        header = envelope[0]
        header_contents = list(header)
        new_header = etree.Element("{http://www.w3.org/2003/05/soap-envelope}Header")
        new_header.extend(header_contents)
        envelope.replace(header, new_header)
        return envelope, http_headers


# handle multipart response
class MultipartTransport(zeep.Transport):
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)

        multipart = requests_toolbelt.multipart.decoder.MultipartDecoder.from_response(response)
        if len(multipart.parts) != 1:
            raise RuntimeError('expected exactly one part')
        part = multipart.parts[0]

        setattr(part, 'status_code', response.status_code)
        part.headers = {**response.headers, **part.headers}

        return multipart.parts[0]


def maybe_fmap(f, arg):
    return None if arg is None else f(arg)

def pprint(data):
    print(json.dumps(data, indent=4, sort_keys=True))

def parse(xml_string):
    return xmltodict.parse(xml_string, force_list=('dane',))


client = zeep.Client(WSDLFILE, plugins=[HeaderNamespacePlugin()], transport=MultipartTransport())
session = client.service.Zaloguj(APIKEY)
client.transport.session.headers['sid'] = session
print('session', session)

pprint({
    name: client.service.GetValue(name)
    for name in ['StanDanych', 'KomunikatKod', 'KomunikatTresc', 'StatusSesji', 'StatusUslugi', 'KomunikatUslugi']
})

regon = '147415997' # lab EE
pprint(parse(client.service.DaneSzukaj({'Regon': regon})))
pprint({
    name: maybe_fmap(parse, client.service.DanePobierzPelnyRaport(regon, name))
    for name in [
        'PublDaneRaportFizycznaOsoba',
        'PublDaneRaportDzialalnoscFizycznejCeidg',
        'PublDaneRaportDzialalnoscFizycznejRolnicza',
        'PublDaneRaportDzialalnoscFizycznejPozostala',
        'PublDaneRaportDzialalnoscFizycznejWKrupgn',
        'PublDaneRaportLokalneFizycznej',
        'PublDaneRaportLokalnaFizycznej',
        'PublDaneRaportDzialalnosciFizycznej',
        'PublDaneRaportDzialalnosciLokalnejFizycznej',
        'PublDaneRaportPrawna',
        'PublDaneRaportDzialalnosciPrawnej',
        'PublDaneRaportLokalnePrawnej',
        'PublDaneRaportLokalnaPrawnej',
        'PublDaneRaportDzialalnosciLokalnejPrawnej',
        'PublDaneRaportWspolnicyPrawnej',
        'PublDaneRaportTypJednostki',
    ]
})

client.service.Wyloguj(session)
