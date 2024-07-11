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