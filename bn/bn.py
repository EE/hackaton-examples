import requests


class Endpoint:

    def __init__(self, url, limit_max=100, data_key=None):
        if data_key == None:
            data_key = url.split('/')[-1]

        self.url = url
        self.limit_max = limit_max
        self.data_key = data_key

    def get_raw(self, id=None, since_id=None, kind=None, limit=None, created_date=None, updated_date=None):
        params = {}
        if id != None:
            params['id'] = ','.join(map(str, id))
        if since_id != None:
            params['sinceId'] = str(since_id)
        if kind != None:
            params['kind'] = kind
        if limit != None:
            params['limit'] = str(limit)
        if created_date != None:
            params['createdDate'] = ','.join([e.isoformat() for e in created_date])
        if updated_date != None:
            params['updatedDate'] = ','.join([e.isoformat() for e in updated_date])
        response = requests.get(self.url + '.json', params=params)
        response.raise_for_status()
        return response.json()

    def get(self, limit=None, since_id=0, **kwargs):
        data = []
        while limit == None or len(data) <= limit:

            if limit == None:
                limit_single = self.limit_max
            else:
                limit_single = min(self.limit_max, limit - len(data))

            response = self.get_raw(since_id=since_id, limit=limit_single, **kwargs)[self.data_key]
            data.extend(response)

            since_id = max([since_id] + [e['id'] for e in response]) + 1

            if len(response) < limit_single:
                break

        return data if limit == None else data[:limit]
