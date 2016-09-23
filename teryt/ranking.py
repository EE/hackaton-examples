from teryt import client
from pprint import pprint

if __name__ == '__main__':
    pprint({
        name: len(client.service.WyszukajUlice(name, None, None)['Ulica'])
        for name in [
            'adama mickiewicza',
            'juliusza słowackiego',
            'leopolda staffa',
            'wisławy szymborskiej',
            'henryka sienkiewicza',
            'stanisława lema',
            'jana brzechwy',
        ]
    })
