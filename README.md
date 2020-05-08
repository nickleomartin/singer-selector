# singer-selector
A [singer](https://www.singer.io/) extension to programmatically select streams and fields. 

## Setup

``` BASH
virtualenv venv
source venv/bin/activate
python3 -m pip install -e '.[dev]'
```

## Invoke

``` BASH
selector --config tests/config.json --catalog tests/catalog.json > tests/edited_catalog.json
```

## Run Tests

``` BASH
pytest tests/
```
