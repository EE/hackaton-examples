import requests
import math


class Table:

    def __init__(self, url, limit_max=1000):
        self.url = url
        self.limit_max = limit_max

    def get_raw(self, query={}, sort=None, page=None, perPage=None):
        params = query.copy()
        if sort != None:
            params['sort'] = sort
        if page != None:
            params['page'] = page
        if perPage != None:
            params['perPage'] = perPage
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        return response.json()

    def get(self, query={}, sort=None, limit=None):
        if limit == None:
            results = []
            page = 1
            while True:
                result = self.get_raw(query, sort, page, self.limit_max)
                results.extend(result['data'])
                if result['returnedRows'] != self.limit_max:
                    break
                page += 1
            return results

        elif limit > self.limit_max:
            results = []
            for page in range(math.ceil(limit/self.limit_max)):
                result = self.get_raw(query, sort, page + 1, self.limit_max)
                results.extend(result['data'])
                if result['returnedRows'] != self.limit_max:
                    break
            return results[:limit]

        else:
            return self.get_raw(query, sort, 1, limit)['data']


class API:

    def __init__(self, url):
        self.url = url
        self.tables = {
            k.replace('_url', ''): Table(v)
            for k, v in requests.get(self.url).json()['urls'].items()
        }
