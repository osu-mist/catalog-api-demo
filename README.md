Catalog API Demo
================

Demo of course catalog related APIs:

1. [Class Search API](https://github.com/osu-mist/class-search-api)
2. [Terms API](https://github.com/osu-mist/terms-api)
3. [Course Subjects API](https://github.com/osu-mist/course-subjects-api)

Installation
------------

This application is implemented with [Django](https://www.djangoproject.com/) framework ([version 1.10.1](https://docs.djangoproject.com/en/1.10/releases/1.10.1/)), so make sure you have installed Django first. You can simply install it with [pip](https://pip.pypa.io/en/latest/):
    
```
pip install Django==1.10.1
```

Configuration
-------------

1. Register your application to use the Class Search API, Course Subjects API, and Terms API at the [OSU Developer Portal](https://developer.oregonstate.edu/).
2. Put your `configuration.json` file which contains `client_id` and `client_secret` in the root folder of this application.

    ```json
    "client_id": "secret",
    "client_secret": "sauce"
    ```

Usage
-----

1. Execute the following commands to run the server:

    ```
    cd catalog_api_demo
    python manage.py runserver
    ```

2. While the server is running locally, visit `http://127.0.0.1:8000/catalog_api_demo/` with your Web browser.
