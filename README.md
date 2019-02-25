Namara
======

The official python client for the Namara data collaboration service. [namara.io](https://namara.io)

## Installation

```bash
pip install namara
```

## Usage

### Instantiation

You need a valid API key in order to access Namara (you can find it in your My Account details on namara.io).

```python
from namara import Namara

namara = Namara({YOUR_API_KEY})
```

Available keyword arguments when initializing:
- `api_key` (required)
- `host` (optional, default: `'https://api.namara.io'`)
- `api_version` (optional, default: `'v0'`)
- `debug` (optional, default: `False`)


### Getting Data

To make a basic request to the Namara API you can call `get` on your instantiated object and pass it the ID of the dataset you want and the ID of the version of the data set:

Synchronous:

```python
response = namara.get('5885fce0-92c4-4acb-960f-82ce5a0a4650', 'en-1')
```

Asynchronous:

```python
def cb(response):
  #...

namara.get('5885fce0-92c4-4acb-960f-82ce5a0a4650', 'en-1', options=None, callback=cb)
```

To inspect the response:
```python
response.data # dataset data as JSON array of objects
response.status_code # http status, 200 if successful
response.url # api endpoint used to retrieve the response
```

Without a third `options` argument passed, `get` will return response data with the Namara default offset (0) and limit (250) applied. To specify options, you can pass an options argument:

```python
options = {
  'offset': 0,
  'limit': 150
};

namara.get('5885fce0-92c4-4acb-960f-82ce5a0a4650', 'en-1', options)
```

Available keyword arguments for `get` method:
- `dataset` (required, data set id)
- `version` (required, data set version)
- `options` (optional)
- `callback` (optional)

### Options

All [Namara data options](https://namara.io/#/api) are supported.

**Organization and Project options**
In order to access a data set within the context of your Namara organization and/or project the following options are required. These options will allow you to access data that requires a subscription in order to use the full data set.

```python
options = {
  'organizationId': '...',
  'projectId': '...'
}
```

**Query options**

```python
options = {
  'select': 'market_nam,website',
  'where': 'town = "Toronto" AND nearby(geometry, 43.6, -79.4, 10km)',
  'offset': '0',
  'limit': '20'
}
```

**Aggregation options**
Only one aggregation option can be specified in a request, in the case of this example, all options are illustrated, but passing more than one in the options object will throw an error.

```python
options = {
  'operation': 'sum(p0)',
  'operation': 'avg(p0)',
  'operation': 'min(p0)',
  'operation': 'max(p0)',
  'operation': 'count(*)',
  'operation': 'geocluster(p3, 10)',
  'operation': 'geobounds(p3)'
}
```

### Running Tests

From command line:

```
python -m unittest test_namara
```

### License

Apache License, Version 2.0
