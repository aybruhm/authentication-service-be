# Authentication Service Backend

A django (rest) authentication service that handles storage of users and authentication of their identities.

## Quick start

1. Add "authentication_service" to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
        ...
        'authentication_service',
    ]
    ```

2. Include the authentication_service URLconf in your project urls.py like this::

    path('auth/', include('authentication_service.urls')),

3. Run ``python manage.py migrate`` to create the authentication_service models.

4. Start the development server.

5. Visit ```http://127.0.0.1:8000/auth/```
