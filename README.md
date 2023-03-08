# Django Image
This is a Django REST Framework API that allows users to upload and retrieve images, with different capabilities depending on the user's account tier.  
<br>

## Prerequisites
This project requires Docker and Docker Compose to be installed on your local machine.

<li>Docker  
<li>Docker Compose  
<br><br>


## Running the Project
### To run the project, first navigate to the project directory:

```sh
cd images
```
Then, start the project using Docker Compose:

```sh
docker-compose up
```
This will start the Django server and the PostgreSQL database. You can access the API at http://localhost:8000.
<br><br>

## Running Tests
### To run the tests, use the following command:

```sh
docker-compose run --rm app sh -c "python manage.py test"
```
This will run the test suite.  
<br>

## API Endpoints
### The API provides the following endpoints:

```
POST /api/images/ - upload a new image
GET /api/images/{id}/ - retrieve an individual image by ID
GET /api/images/ - list all images
GET /api/images/{id}/thumbnail/?size={size} - retrieve a thumbnail image at a specific size
GET /api/account-tiers/ - list all account tiers
GET /api/account-tiers/{id}/ - retrieve an individual account tier by ID
```
<br>

## Authentication
The API requires authentication for all endpoints except for listing account tiers. To authenticate, include an Authorization header with a valid JWT token:

```
Authorization: Bearer <JWT Token>
```
You can obtain a JWT token by sending a POST request to the /api/token/ endpoint with valid credentials. For example:


```sh
curl -X POST -H "Content-Type: application/json" -d '{"username": "your-username", "password": "your-password"}' http://localhost:8000/api/token/
```
This will return a JSON object containing an access token and a refresh token:

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
Include the access token in the Authorization header for subsequent requests.  
<br>


## Built With
<li> Django - Python web framework  
<li> Django REST Framework - Web API framework for Django  
<li> Pillow - Python imaging library  
<li> psycopg2 - PostgreSQL adapter for Python  
<li> PyJWT - JSON Web Token implementation in Python  
<br><br>

## Task Completion Time
3 hours