# Read Me

Python 3.6

```#python
pip install -r requirements.txt
```

Setup virtualenv with virtualenvwrapper

```bash
pip install virtualenv
pip install virtualenvwrapper
```

setup folder for virtualenv through env variables

```bash
export WORKON_HOME=$HOME/.virtualenvs
```

```#bash
workon twitterapi3.6
```

create .env file with twitter api credentials

```#bash
consumer_api_key=''
consumer_api_secret_key=''
```

flask setup

```#bash
set FLASK_APP=app
set FLASK_ENV=development
flask run
```
