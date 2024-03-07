see requirements.txt for used packages

Postgres sql is used for datase see models.py for the database tables 



The tool is mainly divided into three different scraper:
1. scraper for main category
2. recursive scraper for all subcategories ( delivers all leaf subcategories)
3. Scrapes though all the subcategories and adds asins found both pages 
4. goes through all the asinsand saves seller info if found


To Deploy the project:
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

All the database infos are saved in environment variables
The cookies info is found in .env file as well 

to deploy the django applicatio : python manage.py runserver
to migrate the databae : python manage.py make migrations
                         python manage.py migrate
