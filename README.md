# AIRLINES (August 2022)

This is an application that allows you to assess offered airplanes. It calculates maximum minutes a plane can fly based on its characteristics.

## How to run
---
```bash
# Running under production closed (not really tho) env.
cd proj
docker-compose up

# Running for development purposes.
cd proj
docker-compose -f docker-compose.dev.yml up
```

## Structure
---
In my mind I had the following criteria or deviations from the test task:
- Each plane must have a series (1-M)
- Depending on series, plane gets its `fuel_tank_capacity` (based on predefined formulas)

I found it more realistic and more extendable. It allows us to have multiple planes with the same tank capacity, but different people capacity.

- I created a Plane abstract model.

It allows us to have military and cargo planes. They are all, well, planes and share this or that common traits. Again, extendability, DRY and stuff!

- There's a plane_reader module, that implements factory pattern.

Having this we can easily (relatively :)) add assessing from excel or word files.

## How to use
---
Head to the root api page: http://localhost:8000/api/v1/. From there you're good to go creating series and airplanes.

There's an option to create multiple series and planes all at once (as was stated in the task, allowing user an input for 10 planes). Head to the http://localhost:8000/api/v1/planes/many/ url. From there you're expected to send json data.

Example:
```python
[
    {"series_code": 1, "series_name": "One", "capacity": 1},
    {"series_code": 2, "series_name": "Two", "capacity": 20},
    {"series_code": 3, "series_name": "Three", "capacity": 30},
    {"series_code": 4, "series_name": "Four", "capacity": 4},
    {"series_code": 5, "series_name": "Five", "capacity": 50},
    {"series_code": 6, "series_name": "Sex", "capacity": 60},
    {"series_code": 7, "series_name": "Seven", "capacity": 7},
    {"series_code": 8, "series_name": "Eight", "capacity": 80},
    {"series_code": 9, "series_name": "Nine", "capacity": 9},
    {"series_code": 10, "series_name": "Ten", "capacity": 100}
]
```

## Testing
---
There's 95% test coverage. Tests can be run with:
```bash
# Entering the docker container
docker exec -it <container_name/id> /bin/bash

# Running test
coverage run --source='.' manage.py test # to run tests
coverage html # to get the coverage reports
```
