# warehouse_management_system

add .env file:
DATABASE_URL=<ypur DB URL>
BASE_URL=<your base URL>


add virtual enviarement:
python -m venv venv
venv\Scripts\activate

insatll packages:
pip install -r requirements.txt

migarte files:
flask db init

if make any changes in tables:
flask db migrate
flask db upgrade

run app:
python run.py

to run tests:
pytest