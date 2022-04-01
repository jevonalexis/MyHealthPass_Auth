# MyHealthPass_Auth

## Description

Authentication and authorization library for MYHealthPass.

## Features
- User Login 
- User Registration
- User lockout
- Rate limiting by request signature (user agent + cookies + client ip) to prevent brute force attack

### Configurable

- App session length
- Password complexity policy 
  - Min length
  - Max length
  - Uppercase required
  - Lowercase required
  - Number required
  - Special characters to be considered

- User lockout policy 
  - number of failed login attempts
- Rate limiting lockout policy 
  - Number of login attempts
  - Timespan in which the attempts must be made before lockout
  - Lock out / cool down period

## Requirements

- Python 3.7+
- Redis client
- A remote or local database connection


## Set up

- Fork this repo
- pip install *requirements.txt*
- configure *app/policy_config.py*
- create a copy of *config_template.py* named *config.py* and configure it
- execute `python run.py`

## Usage

### Routes

| Route       | Methods     |   Params/Body           |   Description                         |
| :---        |    :----:   |     :----             |     :----                            |
| /register   | POST       |{"email" : "", "password" : "", "firstname": "", "lastname": "" }| Creates a new user with the given details|
| /login   | POST        |{"email" : "", "password" : ""}|Logs in unlocked if username found in db and password is correct|
| /logout   | GET        |       |Logs out user|
| /unlock_user   | POST        |{"email" : ""}|*Returns a link with a unique token that expires|
| /check_token   | GET, POST        |token="", email=""      |** Checks token and email address and unlocks user if valid, returns error message otherwise |

\
&ast; = Send to user's email address in real world\
&ast; &ast; = Redirect to password reset page in real world


### UnitTest

From project top level directory run `python -m unittest discover -s .\tests\Validator\ -p "test_*.py"`