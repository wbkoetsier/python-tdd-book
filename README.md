# Test-driven development with Python
Following the book in print (5th edition) and [online](https://www.obeythetestinggoat.com/).

## Requirements
Python: 3.6+

`pip freeze`:
```
Django==1.11.16
pkg-resources==0.0.0
pytz==2018.7
selenium==3.141.0
urllib3==1.24.1
```

Geckodriver: 0.23.0 (anywhere on the path) with Firefox 63.0. Or visit https://github.com/mozilla/geckodriver/releases.

[(Vanilla) Bootstrap 3.3.4](https://github.com/twbs/bootstrap/releases/download/v3.3.4/bootstrap-3.3.4-dist.zip).

## Run
`python manage.py runserver`

## Test
`python manage.py test functional_tests`

`python manage.py test lists`
