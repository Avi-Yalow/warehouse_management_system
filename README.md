# warehouse_management_system

## 1. Environment Setup

Create a `.env` file in the root directory with the following configurations:

```
DATABASE_URL=<ypur DB URL>
BASE_URL=<your base URL>
HOST=<app host>
PORT=<host port>
```


## 2.Virtual Environment

Create and activate a virtual environment:
```
python -m venv venv
venv\Scripts\activate

```

## 3.Installation

Install required packages:
```
pip install -r requirements.txt
```
## 4. Database Migration

migarte files:

```
flask db init

#if making any changes in tables:
flask db migrate
flask db upgrade
```

## Running the Application
run app:
```
python run.py
```

## Testing

to run tests:

```
pytest
```
##  API Documentation

docs for the endpoints:
```
http://<host>:<port>/docs
```