# Cryptocurrency wallet
Application for working with cryptocurrency.

## Installation
1. Run shell script "install": ```./bin/install``` from the project directory.
2. Add "rest_framework". "cryptocurrency" and "api" to INSTALLED_APPS in project settings.py: 
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
If you don't want to use PostgreSQL delete requirement from requirements.txt
5. Add to "path('api/', include('api.urls'))" to "urlpatterns" in project urls.py:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```
## Usage
Launch the server with the following command from the project directory:
```bash
./bin/runserver
```
## Conclusion

If you have a bug or feature request contact me.
