This is a Product Document describing the work done so far
Authors: Michael Simeone, Shashank Kapoor, Zachary Weiss

To Do:
    1. eb open command currently doesn't work, need to install nltk to elastic beanstalk
    2. our current stop words need to be added to an amazon S3 bucket (cloud storage)
    3. discuss what else needs to be added.

    -------
    1. Page Rank
    2. GUI
    3. user document -> summarize_texts() + display ---- New tab
        index.js
        index.html
        jquery
    -------

Currently:
    1. python manage.py runserver works
        meaning the developer server works

Django principles: (Using Django framework)
    MVC- model view controller
        Provides a way of structuring the project, separates the code
        that's used to process the data from the UI codes
    MTV- model template view
    DRY- Don't repeat yourself
        i.e. Don't write code that does the same


    pre-reqs:
                (*) Can be installed using anaconda @ https://www.anaconda.com/distribution/
        *python (ubuntu 16.10 or newer):
            $ sudo apt-get update
            $ sudo apt-get install python3

        *pip:
            $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            $ python get-pip.py
            upgrade:
            $ pip install -U pip

        NLTK python module: (required from views.py)
            $ sudo pip install -U nltk
            $ sudo pip install -U numpy

            Test:
            $ python
            >> import nltk

        awsebcli: (AKA "eb CLI"--requires python and pip)
            $ pip install awsebcli --upgrade --user

        virtualenv: (requires awsebcli python and pip)
            creates a virtual environment
            $ virtualenv -p pythong 3.7 /tmp/eb_python_app


    Full Tutorials:
        all other prereqs:
            https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/python-development-environment.html

        aws: (contains python3 install info)
            https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html

        Elastic Beanstalk: (contains Django framework install info)
            https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html

    COMMANDS:
    $ python manage.py runserver
        -Runs the Django site locally with manage.py runserver
        This is only a development server NOT to be used later
    $ source ~/eb-virt/bin/activate
        - generates a Django application
    $ eb init <application-name>
        - initialize an elastic beanstalk environment
    $ eb deploy
        - bundles up the contents of the project directory and deploys it to
          the environment
    $ eb open
        - opens the public URL of the website in your default browser


----------------------------------------------------------------------
----------------------------------------------------------------------

/Test/ebdjango (container) info:

manage.py: (template python file)
    utility script that you can run from the cli
    contains functions for running the site

requirements.txt: (template aws file)
    Used to ensure proper language and frameworks are used

----------------------------------------------------------------------
----------------------------------------------------------------------

/Test/ebdjango/ebdjango (application) info:

TEMPLATES/ (directory with html files)

    Url templates need to be placed within :
    /venv/lib/python3.7/site-packages/django/contrib/admin/templates/

    or

    /venv/lib/python3.7/site-packages/django/contrib/auth/templates/
    This means that all files within /edjango/templates/polls
    are not being used correctly

__init__.py: (template python file)
    This file tells python that this is a package allowing all
    of the scripts to be imported as modules

apps.py
    -TBA

models.py
    - place holder for datastuctures

settings.py: (template django/aws file)
    -A file that ensures connection to the correct address along
    with keys for access

summarize.py
    -TBA (shashank)

urls.py: (template django python file)
    -A file that maps urls to specific pages
    i.e. link an "about us" to a specific page

    -When creating a url based on some "request" the name that
    is associated with the url must be passed as a parameter to a
    views.py def (i.e request) in order to be handled properly

views.py: (django python file)
    -A file that renders different webpages based on a request input
    -Uses the django framework for rendering

wsgi.py: (django config file)
    -TBA
