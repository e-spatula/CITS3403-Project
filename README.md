# Polly

This is a project submission for Agile Web development at the University of Western Australia by David Adams and Eddie Atkinson.

The idea of this app was to allow people and organisations to more easily organise events by voting on times and dates to possibly run events.
Users will be able to create Polls and vote on them as well as view results of various polls.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Social Choice Mechanism
This application uses a simple first past the post voting system. Only logged in users can vote and users can only vote once.
The poll creator has the option to limit the number of options individual users can vote for. 

### Prerequisites

A minimum of python 3.7 is required to run this project

on linux:

```
$ sudo apt-get install python3.6
```

on mac:

```
$ brew install python3
```

on windows go to the python website and download the installer

### Installing

To set up the virtual environment open the root directory of the project in a terminal and type: 
```
$ python3 -m venv flask
$ source flask/bin/activate
$ pip install -r requirements.txt
```


## Running the tests

Open the root directory for the project in a terminal window and enter the command:

```
python -m unittest discover
```
To run the automated tests.

**Ensure that the virtual environment is not active when you run the automated tests, it will give you an error.**



## Deployment



To run this server locally assuming correct installation set the environment variables by opening a terminal at the root directory of the project and entering:

```
$ export FLASK_APP=polly.py
```
**If you are the marker for this assignment we will have submitted a .env file with the submission for this assignment, please place that in the root directory of the project.**

If you are not the marker you will need to provide the following environment variables:

```
$ export MAIL_PASSWORD = <our-mail-server-password>
$ export ADMIN_PIN = <whatever-admin-pin-you-want-to-set>

```
Then enter:
```
$ flask run
```
## Dummy Accounts

**For the maker's attention**

There are some dummy accounts available for use with the following credentials:

Username: Eddie
Password: eddie

This user has admin privileges

Username: NewUser
Password: newuser

This user does not have admin privileges

## Dependencies

* alembic==1.0.10
* asn1crypto==0.24.0
* astroid==1.6.0
* Babel==2.6.0
* backports.functools-lru-cache==1.4
* blinker==1.4
* certifi==2019.3.9
* chardet==3.0.4
* Click==7.0
* configparser==3.5.0
* coverage==4.5.3
* cryptography==2.1.4
* dateparser==0.7.1
* decorator==4.4.0
* enum34==1.1.6
* Flask==1.0.3
* Flask-Babel==0.12.2
* Flask-Login==0.4.1
* Flask-Mail==0.9.1
* Flask-Migrate==2.4.0
* Flask-Moment==0.7.0
* Flask-OpenID==1.2.5
* Flask-ReCaptcha==0.4.2
* Flask-SQLAlchemy==2.4.0
* Flask-WhooshAlchemy==0.56
* Flask-WTF==0.14.2
* flipflop==1.0
* futures==3.1.1
* guess-language==0.2
* html-testRunner==1.2
* idna==2.8
* infinity==1.4
* intervals==0.8.1
* ipaddress==1.0.17
* isort==4.3.4
* itsdangerous==1.1.0
* Jinja2==2.10.1
* keyring==10.6.0
* keyrings.alt==3.0
* lazy-object-proxy==1.3.1
* logilab-common==1.4.1
* Mako==1.0.10
* MarkupSafe==1.1.1
* mccabe==0.6.1
* numpy==1.16.2
* pbr==5.1.3
* pycrypto==2.6.1
* pygobject==3.32.1
* PyJWT==1.7.1
* pylint==1.8.3
* python-dateutil==2.8.0
* python-dotenv==0.10.2
* python-editor==1.0.4
* python-openid==2.2.5
* pytz==2019.1
* pyxdg==0.25
* regex==2019.4.14
* requests==2.22.0
* SecretStorage==2.3.1
* singledispatch==3.4.0.3
* six==1.12.0
* SQLAlchemy==1.3.3
* sqlalchemy-migrate==0.12.0
* sqlparse==0.3.0
* Tempita==0.5.2
* typing==3.6.6
* tzlocal==1.5.1
* urllib3==1.25.2
* validators==0.12.6
* virtualenv==16.4.3
* Werkzeug==0.15.4
* Whoosh==2.7.4
* wrapt==1.9.0
* WTForms==2.2.1
* WTForms-Components==0.10.4


## Built With

* [flask](http://flask.pocoo.org/) - The web framework used
* [python](https://www.python.org/) - Dependency and Package Management
* [CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout) - Front end styling


## Authors

* **Eddie Atkinson**
* **David Adams**
 

## Acknowledgments

* Css tricks for never failing to find something that worked
* Eddie for putting up with David
* Coders for Causes for letting us take over the club room for hours on end
