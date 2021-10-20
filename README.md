# Vue3 Django MySQL

## Setting up and running the backend

### Prerequisites

- [Python 3](https://docs.python.org/3/)
- Pip 3
- Virtualenv


### Go to the backend

```
cd ./django/
```

### Create & activate virtual environment

```
python3 -m venv /venv/
source ./venv/bin/activate
```

For more information on virtualenv, visit the [offical site](https://docs.python.org/3/library/venv.html).

### Install project dependencies

Verify that your virtual environment is activated.
The command line should have "(venv)" at the far left.

```
pip install -r requirements.txt

```


#### Create file .env

Go into the .env file and modify:

```

SECRET_KEY = <YOUR SECRET KEY>
NAME_DB = <YOUR NAME DB>
USERNAME_DB = <YOUR USERNAME>
PASSWORD_DB = <YOUR PASSWORD>
HOST_DB = <YOUR HOST DATABASE>

```

<span style="color: green"> - Note : The database here is MySQL </span>


### Prepare Django database

```
python manage.py makemigrations
python manage.py migrate
```

### Launch server

```
python manage.py runserver
```

The backend is thus exposed at localhost:8000

## Setting up and running the frontend

### Prerequisites

- [Node](https://nodejs.org/en/)

### Go to the frontend

```
cd ../vue/
```

### Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

