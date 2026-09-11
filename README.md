# Nano Django

Right from you start a [Django project](https://docs.djangoproject.com/en/6.1/) there are many files involved to define the different aspects of the project. In many respects this is good but for beginners it can be a little intimidating knowing how to navigate the files. 

[Nano Django](https://docs.nanodjango.dev/en/latest/) takes a different approach, you can define a Django project in a single file, using views, models and admin. If you subsquently decide you would prefer to use the conventional Django structure Nano Django provides a tool to automatically convert your Nano Django project to a full Django project.

## Resources

 - [Project Home](https://nanodjango.dev)
 - [Docs](https://docs.nanodjango.dev/en/latest/)
 - [Repos](https://github.com/radiac/nanodjango)

## Environmental Variables
Environmental Variables are configured using [direnv](https://direnv.net/). The real config file is not committed but `.envrc.sample` shows the structure of the necessary file.

## Initialization 

The default means of starting a nano django app, defined in app.py, is ...

```
nanodjango run app.py
```

... the first time that is run a superuser is created with a default userid/password. The default userid and/or password can be overridden.

```
nanodjango run --pass='not-this-one' app.py
```

You can arrange to be prompted by using the arguments without values ...

```
nanodjango run --pass app.py # prompts for the superuser password
```

Alternatively you can supply the password to be used via an environment value `DJANGO_SUPERUSER_PASSWORD` ...

```
DJANGO_SUPERUSER_PASSWORD='not-this-one' nanodjango run app.py
```






