# Spam Number API

  This project is a RESTful API built using Django and Django REST Framework. The API is designed to support a mobile app that allows users to register, manage their profiles, report phone numbers as spam, and search for users or contacts by phone number or name.

## Table of Contents

- Setup Instructions

- Running the Project

- API Endpoints

  - Authentication

  - User Profile

  - Contacts

  - Spam Reporting

  - Search

### Setup Instructions

- Prerequisites
  - Python 3.x
  - Django
  - Django REST Framework
  - PostgreSQL (or another relational database supported by Django)
  - pip (Python package manager)

#### Installation Steps
  - Extract Zip File
  - `cd spam-detection-api`
  
#### Create a Virtual Environment:
    
    - `python -m venv venv`
    - `source venv/bin/activate` # On Windows use `venv\Scripts\activate`

#### Install Dependencies:
  - `pip install -r requirements.txt`

### Set Up the Database:
  - Used the local postgresql for setup
  - Configure your database settings in `spam_detection_api/settings.py.`

```
DATABASES = {

     'default': {

         'ENGINE': 'django.db.backends.postgresql',

         'NAME': 'your_database_name',  // Create the table in your database before run server

         'USER': 'user_name',  

         'PASSWORD': 'user_password',

         'HOST': 'localhost',

         'PORT': '5432',
    }
} 
```

#### Apply migrations:
- `python manage.py makemigrations`
- `python manage.py migrate`
 
#### Create a Superuser:
  - `python manage.py createsuperuser`

#### Run the Development Server:
  - `python manage.py runserver`


# Access the API:

The API will be available at http://127.0.0.1:8000/.

- You can use tools like Postman to interact with the API endpoints.
## API Endpoints

## Authentication

1.  Register a New User
```

Endpoint: POST /auth/users/

Body:

{

  "username": "john",

  "password": "strongpassword123",

  "name": "John Doe",

  "phone_number": "1234567890",

  "email": "john@example.com"  // Optional

}
```

2.  Obtain JWT Token

```
Endpoint: POST /auth/jwt/create/

Body:

{

  "username": "john",

  "password": "strongpassword123"

}
```

3. Verify JWT Token

```
Endpoint: POST /auth/jwt/verify/   || POST /auth/jwt/verify_user/

Body:
{
  "token": "<your-token>"
}
```

4. Refresh JWT Token

```
Endpoint: POST /auth/jwt/refresh/

Body:

{
  "refresh": "<your-refresh-token>"
}
```

## User Profile

1. Get User Profile
 - For token makesure the prefix should be JWT
 
```
Endpoint: GET /api/user/profile/

Headers:

Authorization: JWT <your-token>
```

2. Update User Profile

```
Endpoint: PATCH /api/profile/update/

Headers:

Authorization: JWT <your-token>

Body:
{
  "email": "new-email@example.com"
}
```

## Contacts

1. Add a Contact

```
Endpoint: POST /api/contacts/

Headers:

Authorization: JWT <your-token>

Body:

{
  "name": "Jane Doe",
  "phone_number": "0987654321"
}
```

2. List Contacts

```
Endpoint: GET /api/contacts/

Headers:

Authorization: JWT <your-token>
```

3. List Contacts by ID

```
Endpoint: GET /api/contacts/1/

Headers:

Authorization: JWT <your-token>
```

4. Delete Contacts by ID

```
Endpoint: DELETE /api/contacts/1/

Headers:

Authorization: JWT <your-token>
```

5. Update a Contact by ID

```
Endpoint: PATCH /api/contacts/1/

Headers:

Authorization: JWT <your-token>

Body:

{
  "name": "Jane Doe",
  "phone_number": "0987654321"
}
```

## Spam Reporting

1. Mark a Number as Spam

```
Endpoint: POST /api/spam/

Headers:

Authorization: JWT <your-token>

Body:
{
  "phone_number": "0987654321"

}
```

2. Get All Spam

```
Endpoint: GET /api/spam/

Headers:

Authorization: JWT <your-token>
```

2. Get Spam by ID

```
Endpoint: GET /api/spam/1/

Headers:

Authorization: JWT <your-token>
```


3. Delete  Spam by ID

```
Endpoint: DELETE /api/spam/1/

Headers:

Authorization: JWT <your-token>
```

## Search

1. Search by Phone Number

```
Endpoint: GET /api/search/?q=7984094163&search_by=phone_number

Headers:

Authorization: JWT <your-token>

Query Parameters:

phone_number: The phone number to search for.
```

2. Search by Name

```
Endpoint: /api/search/?q=nikunj&search_by=name

Headers:

Authorization: JWT <your-token>

Query Parameters:

name: The name to search for.
```