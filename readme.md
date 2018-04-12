# Nutell'ove

## Features
This app lets a user search for a product and suggests similar healthier products.
The user can then favorite the suggested products (or not) after creating registering to the app or logging in.

## Installation

### Python 3

Install from : https://www.python.org/downloads/  
Preferably choose Python 3.6.3

### Virtualenv and VirtualenvWrapper

```sh
pip install --user virtualenv
pip install --user virtualenvwrapper
```

#### Unix
After the installation it's time to add theses lines in ```~/.profile``` (maybe ```~/.bashrc``` or ```~/.bash_profile```)

```sh
export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
export PROJECT_HOME=~/pyprojects
mkdir -p $PROJECT_HOME
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.x
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source .local/bin/virtualenvwrapper.sh
```

And finally reload this file :

```sh 
source ~/.profile
```

# Requirements
## Installing Postgresql
Go to https://www.postgresql.org/download/ and choose your OS.
On MacOs you can install Homebrew (a packet manager): https://brew.sh/index
and then in a terminal: ```brew install postegresql```

## Running the virtual environment
After the virtual environment is setup, you can then work on it:
```sh
workon {your_env_name}
```

## Installing the dependencies
First change your directory to be in the root django project folder (where manage.py is located): 
```sh
cd nutellove
```

```sh
pip install -r requirements.txt
```
or (Unix only)
```sh
make init
```

## Creating and feeding db
First, in a terminal, run :
```sh
make create_db u={{ YOUR DB USERNAME }} n={{ YOUR DB NAME }}
```

In your Django `settings.py`
```sh DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ YOUR DB NAME }}',
        'USER': '{{ YOUR DB USERNAME }}',
        'PASSWORD': '{{ YOUR DB PASSWORD OR EMPTY ('') }}', 
        'HOST': 'YOUR DB HOST OR EMPTY ('')',
        'PORT': '5432',
    }
}
```

Then run in a terminal :
```sh
make migrate_db
make feed_db
```

## Adding/updating data fetched from OpenFoodFacts
### Updating the constants
You can change the constants used in ```constants.py```.
You can see all the data-fields available at: https://world.openfoodfacts.org/data/data-fields.txt
You can also add categories of products fetched. To know the list of all categories available on OpenFoodFacts, you can go at: https://fr.openfoodfacts.org/categories or https://world.openfoodfacts.org/categories (slow to load).

### Updating the db_file.csv
After you have updated the ```constants.py``` file, you need to download the CSV file at: https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv.
When it is downloaded, move it to the project folder and run ```csv_cleaner.py``` (might take some time depending on the constants you passed).

Then run in a terminal :
```sh
make feed_db
```

You should be all set.

# Running the app
To run the app :
```sh
python manage.py runserver
```
Then go to localhost:8000 or 127.0.0.1:8000, and the app should be launched and usable there.
