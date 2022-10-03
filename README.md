# Authentication Service Backend

![CI](https://github.com/israelabraham/authentication-service-be/actions/workflows/django.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-authentication-service.svg)](https://badge.fury.io/py/django-authentication-service)

A django rest authentication service backend that handles storage of users account and authentication of their identities.

## Endpoints

The following have been unit tested and ready to use:

- Register
- Login (JWT)
- Login (Refresh JWT)
- Request Email
- Verify Email (Uid & Token)
- Logout
- Change Password
- Reset Password
- Reset Password Complete
- Suspend User
- *Google OAuth (In Progress)*

## API Schema

Download and Import the [schema](api-schemas.yaml) to your favourite API testing tool (postman, insomnia, etc) to get the endpoints and expected payload.

## Requirements

- Python (3.8, 3.9.*)
- Django (2.2, 3.0, 3.1, 3.2, 4.*)

## Quick Start

### Pip Installation

1). Install using `pip`:

```python
    pip install django-authentication-service
```

2). Add `authentication_service` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = [
        ...
        "authentication_service",
    ]
```

Make sure that you have `djangorestframework`, `djangorestframework-simplejwt` and `drf-yasg` installed in your apps.

```python
    INSTALLED_APPS = [
        # django installed apps
        ...
        # already added to installed_apps
        "rest_framework",
        "rest_framework.authtoken",
        "rest_framework_simplejwt",

        # this will help document the apis using either swagger or redoc
        "drf_yasg",

        # new line
        "authentication_service",
    ]
```

3). Configure the `AUTH_USER_MODEL` in the setting:

```python
AUTH_USER_MODEL = "authentication_service.AccountUser"
```

4). Register the account user model to the admin; if you don't want to - set it to False:

```python
REGISTER_USER_MODEL = True # this will show the user model on the django admin
```

5). In order to use the pre-built email templates, you'd have to include the name of your site (or product name) and the contact email:

```python
AUTHENTICATION_SERVICE = {
    "site_name": "Authentication Service",
    "contact_email": "contact@authentication-service.com"
}
```

6). Include the `authentication_service` URLs in your project urls.py:

```python
    path('auth/', include('authentication_service.urls')),
```

7). Run ``python manage.py migrate`` to create new migrations based on the changes on the model.

8). Start the development server:

```python
python manage.py runserver 8080
```

### Docker Installation

To get the service up and running, follow the steps below:

1). Run the commands below in your terminal:

```bash
git clone git@github.com:israelabraham/authentication-service-be.git
```

2). Change directory to authentication-service-be:

```bash
cd authentication-service-be
```

3). Rename the `.env.template` file to `.env` and update the values.

4). Build and run the service with:

```bash
docker-compose up --build
```

The service will build and run on port `8080`.

## Documentation & Support

If you find a code smell, or bad practice(s) anywhere while exploring through the codebase - kindly create an issue stating what it is; or fix the code smell, bad practice or whatever it is you found. As the saying goes, multiple heads are better than one. *winks*

## License

*Disclaimer:* Everything you see here is open and free to use as long as you comply with the [license](https://github.com/israelabraham/authentication-service-be/blob/main/LICENSE.txt). There are no hidden charges. We promise to do our best to fix bugs and improve the code quality.
