import logging
import shutil
import time

import pandas as pd
import requests
from requests_futures.sessions import FuturesSession


class Namara:
    def __init__(self, api_key, debug=False, host='https://api.namara.io', api_version='v0'):
        self.api_key = api_key
        self.debug = debug
        self.host = host
        self.api_version = api_version
        self.base_path = '{0}/{1}'.format(self.host, self.api_version)
        self.headers = {'Content-Type': 'application/json', 'X-API-Key': api_key}
    
    def export(self, dataset_id, organization_id, options=None, output_format='url', output_file=None):
        url = self.get_url(f'/data_sets/{dataset_id}/data/export?geometry_format=wkt&organization_id={organization_id}')
        while True: 
            response = self.__session.get(url, params=options, headers=self.headers).result().json()
            if self.debug: 
                logging.debug('Response Object: ' + response)
            if 'message' in response and response['message'] == 'Exported':
                if output_format == 'url': 
                    return response['url']
                elif output_format == 'dataframe': 
                    list_of_chunks = [] 
                    for chunk in pd.read_csv(response['url'], chunksize=100):
                        list_of_chunks.append(chunk)
                    return pd.concat(list_of_chunks)
                elif output_format == 'csv': 
                    with requests.get(response['url'], stream=True) as r:
                        shutil.copyfileobj(r.raw, output_file)
                    return
                else: 
                    raise Exception('`output_format` param must be "csv", "dataframe", or "url" (default)')
            elif 'message' in response and response['message'] == 'Failed':
                raise Exception(f"Could not export dataset {dataset_id}")
            elif 'message' in response and response['message'] == 'Pending': 
                time.sleep(5) 
            else: 
                raise Exception(response['error']) 
 
    def get_project_items(self, organization, project, options=None, callback=None, output_format='json'):
        if not organization:
            raise ValueError('organization id is required')
        if not project:
            raise ValueError('project id is required')

        url = self.get_url('/organizations/{0}/projects/{1}/data_sets'.format(organization, project))

        if callback is None:
            response = self.__session.get(url, params=options, headers=self.headers).result()
            if self.debug: 
                logging.debug('REQUEST URL: ' + response.url)
            response.data = self.__extract_datasets(response.json()) if response.ok else response.json()
            if output_format is 'json': 
                return response.data 
            elif output_format is 'dataframe': 
                df = pd.DataFrame(response.data)
                return df
            else: 
                raise ValueError('`output_format` param must be "json" or "dataframe"')
            return response

        def response_hook(response, *args, **kwargs):
            if self.debug: 
                logging.debug('REQUEST URL: ' + response.url)
            response.data = response.json()
            if output_format is 'json': 
                callback(response.data)
            elif output_format is 'dataframe': 
                df = pd.DataFrame(response.data)
                callback(df)
            else: 
                raise ValueError('`output_format` param must be "json" or "dataframe"')

        self.__session.get(url, params=options, headers=self.headers, hooks={
            'response': response_hook
        })

    def get(self, dataset, version, options=None, callback=None, output_format=None):
        if output_format is None: 
            output_format = 'json'

        path = '/data_sets/{0}/data/{1}'.format(dataset, version)
        if self.is_aggregation(options):
            path = '{0}/aggregation'.format(path)

        url = self.get_url(path)

        if callback is None:
            response = self.__session.get(url, params=options, headers=self.headers).result().json()
            if self.debug: 
                logging.debug('REQUEST URL: ' + response.url)
            if output_format is 'json': 
                return response
            elif output_format is 'dataframe': 
                return pd.DataFrame(response)
            else: 
                raise ValueError('`output_format` param must be "json" or "dataframe"')

        def response_hook(response, *args, **kwargs):
            if self.debug: 
                logging.debug('REQUEST URL: ' + response.url)
            response.data = response.json()
            if output_format is 'json': 
                callback(response.data)
            elif output_format is 'dataframe': 
                df = pd.DataFrame(response.data)
                callback(df)
            else: 
                raise ValueError('`output_format` param must be "json" or "dataframe"')

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
