# How to set up a development environment

Clone the repository

    cd
    git clone https://github.com/lesglaneurs/lesglaneurs.git

Install the system dependencies

    sudo apt-get install libjpeg-dev

Create and activate a virtual environment

    sudo pip install virtualenv
    cd virtualenvs
    virtualenv lesglaneurs
    . lesglaneurs/bin/activate
    . activate

Set up the project itself (let us assume your name is John Doe):

    cd ~/lesglaneurs
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser --username=johndoe --email=johndoe@gmail.com

Run the server:

    python manage.py runserver --settings=lesglaneurs.settings.dev

To check that the server is running, open your brower at the URL http://127.0.0.1:8000/local/admin/
