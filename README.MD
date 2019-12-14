# Read Me

Python 3.6

Setup virtualenv with virtualenvwrapper

```bash
pip install virtualenv
pip install virtualenvwrapper
```

setup folder for virtualenv through env variables

```bash
export WORKON_HOME=$HOME/.virtualenvs
```

create a virtual env

```bash
mkvirtualenv twitterapi3.6
```

start up virtual env

```#bash
workon twitterapi3.6
```

```#python
pip install -r requirements.txt
```

create .env file with twitter api credentials and fire base admin credential json
currently need json credentials from fire storage

```#bash
consumer_api_key=''
consumer_api_secret_key=''
firebase_credentials_path=''
firebase_credentials_json=''
```

flask setup

```#bash
set FLASK_APP=app
set FLASK_ENV=development
flask run
```

ngrok command

```#bash
ngrok http 5000
```
