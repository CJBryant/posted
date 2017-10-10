# Posted - A News Aggregator
Posted is a news aggregation app built using the Django web framework.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Set working directory to app root
```
$ cd /path/to/posted-app/
```

Set up and activate a virtual environment called `venv` in the current folder
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

Install the required packages in virtual environment
```
$ pip install -r requirements.txt
```

Set up the database
```
$ python manage.py makemigrations
$ python manage.py migrate
```

Load data into database
```
$ python manage.py shell < setup_data.py
```

 Set up the server and create an admin account
```
$ python manage.py createsuperuser
$ python manage.py runserver
```

In another shell window, set up the article maintenance to run periodically
```
$ cd /path/to/posted-app/
$ source venv/bin/activate
$ python manage.py shell < get_articles.py
```

## Viewing Posted in the Browser
To view Posted as a user, go to [127.0.0.1:8000](http://127.0.0.1:8000/)

To view the Posted admin page, go to [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Exiting
To close Posted, Ctrl-C both shell windows. This will need to be done twice for the `article_maintenance` window.
Exit Python by running `quit()`.
Then to exit the virtual environment, run `deactivate` in each shell window.
