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


### PATCH `https://mediminderx-api.herokuapp.com/api/v1/users`

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
          "id": 2,
          "attributes": {
              "title": "Dance Practice",
              "show_supplies": false,
              "creation_date": "2020-10-27T21:39:28.399831",
              "user_id": 3,
              "supplies": "inhaler"
          }
      }
  }
```


### PATCH `https://mediminderx-api.herokuapp.com/api/v1/reminders`

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
  "repeating": "false"
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
