from requests_futures.sessions import FuturesSession

class Namara:
    def __init__(self, api_key, debug=False, host='api.namara.io', api_version='v0'):
        self.api_key = api_key
        self.debug = debug
        self.host = host
        self.api_version = api_version
        self.path = ''
        self.headers = {'Content-Type': 'application/json', 'X-API-Key': api_key}

    def get(self, dataset, version, options=None, callback=None):
        self.path = self.get_path(dataset, version, options)
        if self.debug: print 'REQUEST: ' + self.get_path(dataset, version, options)

        if callback is not None:
            FuturesSession(max_workers=4).get(self.path, params=options, headers=self.headers, background_callback=callback)
        else:
            return FuturesSession(max_workers=4).get(self.path, params=options, headers=self.headers).result().json()

    def get_path(self, dataset, version, options={}):
        return self.get_base_path(dataset, version) + '?api_key=' + self.api_key if not self.is_aggregation(options) else self.get_base_path(dataset, version) + '/aggregation?api_key=' + self.api_key

    def get_base_path(self, dataset, version):
        return 'https://{0}/{1}/data_sets/{2}/data/{3}'.format(self.host, self.api_version, dataset, version)

    @staticmethod
    def is_aggregation(options):
        return options is not None and 'operation' in options.keys()
