1. Please create a virtual environment

```$ virtualenv virt```

```$ source virt/bin/activate```

2. Install the packages

```$ pip install -r requirements.txt```

3. migrate the models (Without migrating the app should work, there's only
    django default models)

```$ ./manage.py migrate```

4. Fire up the server

```$ ./manage.py runserver ```

The server can be accesses at 'http://127.0.0.1:8000/'

There are lots of empty files which were automatically created, mainly please look into

`web.forms`, `web.views`, `web.utils`
