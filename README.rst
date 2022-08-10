==========================
Account Service Backend
==========================
Account service is a Django app responsible for handling authentication for loopscentral.

Quick start
-----------

1. Add "account_service" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'account_service',
    ]

2. Include the account_service URLconf in your project urls.py like this::

    path('auth/', include('account_service.urls')),

3. Run ``python manage.py migrate`` to create the account_service models.

4. Start the development server.

5. Visit http://127.0.0.1:8000/auth/