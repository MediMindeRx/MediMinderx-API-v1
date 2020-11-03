[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

# MediMindeRx API
  
![logo](https://imgur.com/olxejeK)</br>

* Jordan Shryock
  * [Github](https://github.com/jordy1611) 
  * [LinkedIn](https://www.linkedin.com/in/jordan-shryock-6a48b9113/)

* Kathy Bui
  * [Github](https://github.com/kathybui732) 
  * [LinkedIn](https://www.linkedin.com/kathytbui/)

* Kwibe Merci
  * [Github](https://github.com/jkwibe) 
  * [LinkedIn](https://www.linkedin.com/kwibe-merci/)


## Abstract
Never forget your medical supplies again! This mobile app serves to track reminders for medical supplies and notify the user at a given time. 

The MediMinderx_BE is the backend application used by all of MediMinderx's applications. The application builds out RESTful API endpoints for full crud functionality for users and their reminders.

The most difficult and rewarding thing about building this application was picking up a brand new tech stack. We were able to learn python and develop this application in flask in a matter of 14 days. 

## Set up 
Follow the steps below to get this database up and running on your local environment:

### Prerequisites
* PostgreSQL installed 
  * [Homebrew Install](https://formulae.brew.sh/formula/postgresql)
  * [Browser Install](https://www.postgresql.org/download/)

* Postico Installed 
  * [Homebrew Install](https://formulae.brew.sh/cask/postico)
  * [Browser Install](https://eggerapps.at/postico/)

* Python3 Installed
  * [Homebrew Install](https://formulae.brew.sh/formula/python@3.8)
  * [Browser Install](https://www.python.org/downloads/)


### Installation
* Clone down this repo
  1. `git clone git@github.com:MediMindeRx/MediMindeRx-API-v1.git`
  1. `cd` into directory `MediMindeRx-API-v1`

* Initialize database for first time with
  1. `python3 -m venv env`
  1. `source env/bin/activate`
  1. `pip3 install -r requirements.txt`
  1. `createdb mediminderx`
  1. `export DATABASE_URL==postgresql://<YOUR USERNAME>:<YOUR PASSWORD>@localhost:5432/mediminderx`
  1. `python migrate.py db init (this creates a db, so make sure you don’t have one already in postico)`
  1. `python migrate.py db migrate`
  1. `python migrate.py db upgrade`
  1. `python run.py` to start the server
  
* How to run test suite
  1. `createdb mediminderx_test`
  1. `export DATABASE_URL==postgresql://<YOUR USERNAME>:<YOUR PASSWORD>@localhost:5432/mediminderx_test`
  1. `python migrate.py db upgrade`
  1. `pytest`


## Tech Stack 
- Python3
- Flask
- PostgreSQL
- Postico
- Testing Software
- Testing Software

### Future Extentensions
- Option to send texts to family members via Twilio api
- Users can find all the nearest emergency centers (i.e. hostpitals, police stations)
- Users can get notifications based off heart rate or step count sourced off health application such as thorugh fitbit or apple's health app

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/MediMindeRx/MediMindeRx-Mobile.svg?style=flat-square
[contributors-url]: https://github.com/MediMindeRx/MediMindeRx-Mobile/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/MediMindeRx/MediMindeRx-Mobile.svg?style=flat-square
[forks-url]: https://github.com/MediMindeRx/MediMindeRx-Mobile/network/members
[stars-shield]: https://img.shields.io/github/stars/MediMindeRx/MediMindeRx-Mobile.svg?style=flat-square
[stars-url]: https://github.com/MediMindeRx/MediMindeRx-Mobile/stargazers
[issues-shield]: https://img.shields.io/github/issues/MediMindeRx/MediMindeRx-Mobile.svg?style=flat-square
[issues-url]: https://github.com/MediMindeRx/MediMindeRx-Mobile/issues


## Endpoints

### POST `https://mediminderx-api.herokuapp.com/api/v1/users`

Body:
`json {"name": "John"}`

Response:
```json {
{
  "data": {
      "type": "users",
      "id": 1,
      "attributes": {
          "name": "John"
      }
  }
}
```


### GET `https://mediminderx-api.herokuapp.com/api/v1/users/1`

Response:
```json {
{
  "data": [
      {
          "type": "users",
          "id": 1,
          "attributes": {
              "name": "John"
          }
      }
  ]
}
```


### GET `https://mediminderx-api.herokuapp.com/api/v1/users`

Response:
```json {
{
  "data": [
      {
          "type": "users",
          "id": 1,
          "attributes": {
              "name": "John"
          }
      },
      {
          "type": "users",
          "id": 2,
          "attributes": {
              "name": "Jane"
          }
      }
  ]
}
```


### PUT `https://mediminderx-api.herokuapp.com/api/v1/users`

Body:
```json {
{
  "name": "Jake",
  "id": "1"
}
```

Response:
```json {}
{
  "data": {
      "type": "users",
      "attributes": {
          "name": "Jake"
      },
      "id": 1
  }
}
```


### DELETE `https://mediminderx-api.herokuapp.com/api/v1/users`

Body:
```json{}
{
  "id": "1"
}
```

Response:
```json{}
{
  "message": "User has been successfully deleted"
}
```


### POST `https://mediminderx-api.herokuapp.com/api/v1/reminders`

Body:
```json{}
{
  "user_id": "1",
  "title": "Soccer Practice",
  "supplies": "inhaler",
  "show_supplies": "false"
}
```

Response:
```json{}
{
  "data": {
    "type": "reminders",
    "id": 3,
    "attributes": {
        "user_id": 1,
        "location_reminder": null,
        "creation_date": "2020-10-26T20:17:36.207302",
        "schedule_reminder": null,
        "supplies": "inhaler",
        "show_supplies": false,
        "title": "Soccer Practice"
    }
  }
}
```


### PUT `https://mediminderx-api.herokuapp.com/api/v1/reminders`

Body:
```json{}
{
  "id": "1",
  "title": "Dance Practice",
  "supplies": "inhaler",
  "show_supplies": "false"
}
```

Response:
```json{}
{
  "data": {
    "type": "reminders",
    "attributes": {
        "supplies": "inhaler",
        "user_id": 1,
        "show_supplies": false,
        "location_reminder": null,
        "title": "Dance Practice",
        "creation_date": "2020-10-26T20:17:36.207302",
        "schedule_reminder": null
    },
    "id": 3
  }
}
```


### DELETE `https://mediminderx-api.herokuapp.com/api/v1/reminders`

Body:
`{ "id": "3" }`

Response:
```json{}
{
  "message": "Reminder successfully deleted"
}
```


### GET `https://mediminderx-api.herokuapp.com/api/v1/users/1/reminders`

Response:
```json{}
{
  "data": [
    {
      "type": "reminders",
      "id": 4,
      "attributes": {
        "supplies": "inhaler",
        "title": "Soccer Practice",
        "location_reminder": null,
        "schedule_reminder": {
          "data": {
            "type": "schedule",
            "id": 6,
            "attributes": {
              "days": "Tuesday, Wednesday",
              "unix_time": "1603767106",
              "creation_date": "2020-10-26T20:54:48.401702",
              "repeating": false
              "times": "10:30"
            }
          }
        },
        "creation_date": "2020-10-26T20:46:35.589353",
        "user_id": 1,
        "show_supplies": false
      }
    },
    {
      "type": "reminders",
      "id": 5,
      "attributes": {
        "supplies": "Knee Brace",
        "title": "Hockey Game",
        "location_reminder": {
            "data": {
                "type": "location",
                "id": 5,
                "attributes": {
                    "location_name": "Home",
                    "longitude": "-77.0364",
                    "address": "123 Address Lane"
                    "creation_date": "2020-10-26T20:56:33.014708",
                    "latitude": "38.8951"
                }
            }
        },
        "schedule_reminder": null,
        "creation_date": "2020-10-26T20:47:04.818274",
        "user_id": 1,
        "show_supplies": false
      }
    }
  ]
}
```


### POST `https://mediminderx-api.herokuapp.com/api/v1/schedules`

Body:
```json{}
{
  "reminder_id": "1",
  "schedule_name": "Soccer reminder",
  "unix_time": "1603767106",
  "repeating": "false",
  "days": "Tuesday, Wednesday",
  "times": "10:30"
}
```

Response:
```json{}
{
  "data": {
    "type": "schedule",
    "attributes": {
    "id": 6,
      "days": "Tuesday, Wednesday",
      "unix_time": "1603767106",
      "schedule_name": "Schedule 1",
      "repeating": false
      "creation_date": "2020-10-26T20:54:48.401702",
      "times": "10:30"
    }
  }
}
```


### POST `https://mediminderx-api.herokuapp.com/api/v1/users/1/locations`

Body:
```json{}
{
  "reminder_id": "5",
  "location_name": "Home",
  "latitude": "38.8951",
  "longitude": "-77.0364",
  "address": "123 Address Lane"
}
```

Response:
```json{}
{
"data": {
    "type": "location",
    "id": 5,
    "attributes": {
      "location_name": "Home",
      "longitude": "-77.0364",
      "creation_date": "2020-10-26T20:56:33.014708",
      "latitude": "38.8951",
      "address": "123 Address Lane"
    }
  }
}
```
