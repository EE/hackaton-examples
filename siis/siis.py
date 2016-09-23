import requests


class Table:

    def __init__(self, year, name, limit_max=100):
        self.year = year
        self.name = name
        self.limit_max = limit_max

    def get_raw(self, path, *args, **kwargs):
        return self.year.get_raw('tables/%s/%s' % (self.name, path), *args, **kwargs)

    def schema(self):
        return self.get_raw('schema')['data']

    def get(self, filter_string=None, limit=None, offset=0):
        result = []
        while limit == None or len(result) < limit:
            # prepare get parameters
            get_params = {
                'limit': self.limit_max if limit == None else min(self.limit_max, limit - len(result)),
                'offset': offset,
            }
            if filter_string != None:
                get_params['filter'] = filter_string

            # get
            response = self.get_raw('', params=get_params)['data']
            result += response

            # reached end of table
            if len(response) < self.limit_max:
                break

            # next offset
            offset = max(e['id'] for e in response) + 1

        return result[0:limit]


class Year:

    def __init__(self, api, year):
        self.api = api
        self.year = year

        self.tables = {
            table['name']: Table(self, table['name'])
            for table in self.get_raw('tables')['data']
        }

    def get_raw(self, path, *args, **kwargs):
        return self.api.get_raw('years/%d/%s' % (self.year, path), *args, **kwargs)

    def schema(self):
        return {name: table.schema() for name, table in self.tables.items()}


class API:

    def __init__(self, url):
        self.url = url

        self.years = {
            year: Year(self, year)
            for year in self.get_raw('years')['data']
        }

    def get_raw(self, path, *args, **kwargs):
        response = requests.get(self.url + path, *args, **kwargs)
        response.raise_for_status()
        return response.json()

    def schema(self):
        return {year: year_object.schema() for year, year_object in self.years.items()}
