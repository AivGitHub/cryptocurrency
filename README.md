# Cryptocurrency wallet
Application for working with cryptocurrency.

## Installation
1. Run shell script "install": ```./bin/install``` from the project directory.
2. If django not project is not initialized - initialize it.
3. Add "rest_framework".
"cryptocurrency", ""
"api" to INSTALLED_APPS in project settings.py: 
```
INSTALLED_APPS = [
    ...
    'rest_framework',
    'cryptocurrency',
    'api',
]
```
3. Configure database, for postgreSQL:

```
sudo -u postgres psql
postgres=# create database WALLET_DATABASE;
postgres=# create user WALLET_USER with encrypted password 'WALLET_PASSWORD';
postgres=# grant all privileges on database WALLET_DATABASE to WALLET_USER;
```
4. Configure settings.py for connection to database, for postgreSQL:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'WALLET_DATABASE',
        'USER': 'WALLET_USER',
        'PASSWORD': 'WALLET_PASSWORD',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
If you need tests you should alter role createdb to WALLET_USER.

```
        'TEST': {
            'NAME': 'TEST_WALLET_DATABASE',
        },
```

If you don't want to use PostgreSQL delete "psycopg2-binary==2.9.2" from requirements.txt
5. Migrate application "cryptocurrency" and
install fixtures: ```./manage.py loaddata cryptocurrency/fixtures/coins.json```
6. Add to "path('api/', include('api.urls'))" to "urlpatterns" in project urls.py:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```
## Usage
1. Launch the server with the following command from the project directory:
```bash
./bin/runserver
```
2. Now server ready to accept requests:

 ```curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/wallet/ -d "{\"seed\":\"test_seeeeed\", \"symbol\": \"BTC\"}"```

---

```curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/api/wallet/```

3. If you want to add child wallet just add "parent" (seed) to
data in POST request.
You need to know seed of parent wallet because seed is NOT stored in database.

## Information
1. Seed/private key or other private values don't store in database!
2. To add coin you need to add it to 'cryptocurrency/fixtures/coins.json',
./manage.py loaddata cryptocurrency/fixtures/coins.json and modify method 'get_from_seed'
in Wallet class.
## Conclusion

If you have a bug or feature request contact me.
