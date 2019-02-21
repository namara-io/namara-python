from requests_futures.sessions import FuturesSession

class Namara:
    def __init__(self, api_key, debug=False, host='https://api.namara.io', api_version='v0'):
        self.api_key = api_key
        self.debug = debug
        self.host = host
        self.api_version = api_version
        self.base_path = '{0}/{1}'.format(self.host, self.api_version)
        self.headers = {'Content-Type': 'application/json', 'X-API-Key': api_key}

    def get_project_items(self, organization, project, options=None, callback=None):
        if not organization:
            raise ValueError('organization id is required')
        if not project:
            raise ValueError('project id is required')

        url = self.get_url('/organizations/{0}/projects/{1}/data_sets'.format(organization, project))

        if callback is None:
            response = self.__session.get(url, params=options, headers=self.headers).result()
            if self.debug: print('REQUEST: ' + response.url)
            response.data = self.__extract_datasets(response.json()) if response.ok else response.json()
            return response

        def response_hook(response, *args, **kwargs):
            if self.debug: print('REQUEST: ' + response.url + '\n\n')
            response.data = self.__extract_datasets(response.json()) if response.ok else response.json()
            callback(response)

        self.__session.get(url, params=options, headers=self.headers, hooks={
            'response': response_hook
        })

    def get(self, dataset, version, options=None, callback=None):
        path = '/data_sets/{0}/data/{1}'.format(dataset, version)
        if self.is_aggregation(options):
            path = '{0}/aggregation'.format(path)

        url = self.get_url(path)

        if callback is None:
            response = self.__session.get(url, params=options, headers=self.headers).result()
            if self.debug: print('REQUEST: ' + response.url + '\n\n')
            response.data = response.json()
            return response

        def response_hook(response, *args, **kwargs):
            if self.debug: print('REQUEST: ' + response.url)
            response.data = response.json()
            callback(response)

        self.__session.get(url, params=options, headers=self.headers, hooks={
            'response': response_hook,
        })

    def get_url(self, path=''):
        return '{0}{1}'.format(self.base_path, path)

    @staticmethod
    def is_aggregation(options):
        return options is not None and 'operation' in options.keys()

    def __extract_latest_version(self, dataset):
        if not dataset:
            return None

        return max(list(map(lambda v: v['identifier'], dataset['versions'])))

    def __extract_datasets(self, data):
        if not data:
            return data

        return list(map(lambda ds: (ds['id'], self.__extract_latest_version(ds)), data['data_sets']))

    __session = FuturesSession(max_workers=4)
