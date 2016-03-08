# DrexelAutoRegister
This is the server portion for https://github.com/mrkybe/DrexelAutoRegister


## Dependencies
- flask (for the server)
- mock (for unit testing)


## Setup
Before running, you will need to have at least `pip v8.0.0` and `virtualenv v14.0.3`.
These are the versions I have and have tested this on.
This was also tested using `python 2.7`.

- [Instructions for installing pip.](https://pip.pypa.io/en/stable/installing/)
- [Instructions for installing virtualenv.](http://virtualenv.readthedocs.org/en/latest/installation.html)

### Installing dependencies
First create the virtualenv where all the dependencies will be isolated.
```sh
$ virtualenv venv
```

Enter the virtualenv
```sh
$ source venv/bin/activate
```

Once in the venv, install dependencies with pip.
```sh
(venv) $ pip install -r requirements.txt
```


## Usage
Most of the usage depends on a client communicating with the end points of the app.
```sh
(venv) $ python app.py
```
This launches a server available at `127.0.0.1:8080`. The host is also made public, so other computers
can access the server at `YOUR_COMPUTER's_IP_ADDRESS:8080`.


### Endpoints

#### /add_user
This end point receives only post requests and adds a user to the database/filesystem.

params:
- id (string)
- email (string)
- crns (json-encoded STRING; not an actual array)

responses:
- JSON STRING in the format `{"code": 200, "message": "Some message."}`
  - `code` is the same as the response code sent back.
  - `message` is a string associated with this code. This can be a success or error message.


#### /register_user
This end point receives only post requests and registers users for a class.

params:
- id (string)
- email (string)
- password (string; this is also encrypted)

**For anyone who stumbles upon this repo, sees `password`, and whines about
security, deal with it. It's not like we're storing credit card numbers.**

responses:
- JSON STRING in the format `{"code": 200, "message": "Some message."}`
  - `code` is the same as the response code sent back.
  - `message` is a string associated with this code. This can be a success or error message.


## Tests
Unit tests to make sure the core functionality stays intact.
```sh
(venv) $ python tests.py
```


## TODO
- Add logic for user login with twil.

