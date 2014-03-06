Getting a dev server to work
----------------------------

Prepare a virtual environment:

+ sudo apt-get install virtualenv
+ mkdir ~/cnq
+ cd ~/cnq
+ virtualenv cnqvenv
+ source cnqvenv/bin/activate
+ pip install django

Get the Carnique site and prepare a test database:

+ git clone https://github.com/joostvunderink/carnique_site.git
+ cd carnique_site
+ export DJANGO_SETTINGS_MODULE=carnique.settings.dev
+ export PYTHONPATH=.
+ python manage.py syncdb

Edit carnique/settings/dev.py and change the bottom part to:

    TEMPLATE_DIRS = (
        '/home/<username>/cnq/carnique_site/carnique/templates',
    )

Then run the server, for example:

+ python manage.py runserver
+ python manage.py runserver 192.168.42.1:8123


