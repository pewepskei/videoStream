## Notes added regarding v2
## Clone the Repository

```
git clone git@github.com:pewepskei/videoStream.git
```

## Easier way to run 

Then bring up the app
```
docker-compose up -d --build
```

or

```
docker compose build
```
```
docker compose up
```

You can also perform the migration by:
```
docker-compose exec web python manage.py migrate
```

or 

```
docker compose exec web python manage.py migrate
```

## Manual Method


Create virtualenv and activate it:

```bash
virtualenv -p python3.10 venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r videoStream/requirements.txt
```

## Version 2
Major addition:
- Added Redis as message broker
- Added Celery as Async Task Executor
- Allowed multiple video input
- Added folder `/test_files` containing sample files for ease of testing
- Currently only the uploading task is delegated to celery

To check celery logs use this command
```
docker logs -f celery
```

## Version 1
Created branch for version 1 called `v1`

Some Features:
- Create and Manage own Profile or Account
- Add, Edit, Delete and View videos uploaded
- Added a comment feature
- Profiles are custom URLs

NOTE: I haven't setup the email server yet, so the verification link will actually be posted in the console

Day 0: Create a working framework with a working CRUD method

Day 1: Created Comments and Profiles database, barely functional but looks good to me

Day 2: Added some styling

Day 3: Comments mechanism and Populate the website