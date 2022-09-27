import os
from pathlib import Path
from setuptools import setup, find_packages
 

README=Path("README.md").read_text(encoding="utf-8")
 
# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
 
setup(
    name = 'django-authentication-service',
    version = '0.0.1',
    packages = find_packages(),
    include_package_data = True,
    license = 'MIT License',
    description = '🔐 Handles storage of users and authentication of their identities.',
    long_description = README,
    long_description_content_type='text/markdown',
    keywords=[
        'authentication', 
        'django auth', 
        'auth service',
        'authenticaton service'
    ],
    url = 'https://github.com/israelabraham/authentication-service-be',
    author = 'Abram',
    author_email = 'israelvictory87@gmail.com',
    classifiers =[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires=">=3.8",
    install_requires=[
        "django>=2.2",
        "djangorestframework",
        "djangorestframework-simplejwt",
        "rest-api-payload",
        "drf-yasg",
        "httpx"
    ],
)

