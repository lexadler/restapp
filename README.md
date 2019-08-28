# RestApp

REST API for PostgreSQL with Flask and pipeline as a code for Jenkins.

## Requirements:

1. Docker CE and Docker Compose must be installed on the host.

## Deployment:

1. Run `sudo docker-compose up -d` from the project folder. This will create instances of PostreSQL, Jenkins and RestApp as docker containers.
2. To build a pipeline in Jenkins install GitHub Integration Plugin
3. Create a pipeline with *Pipeline script from SCM* definition and `https://github.com/lexadler/restapp.git` as a Git repository.
4. You can use Github hook trigger by adding webhook to your forked repo and using it's URL within a pipeline to run unit tests after each commit.

You can access your RestApp, PostgreSQL and Jenkins instances at localhost on ports 5000, 5432 and 8080 respectively.

## Usage:

There are five basic APIs available to use while containers is running. Each can be tested with curl, Postman or another tool.

### Returns list with all users from the database for testing purposes.
**Request:** GET /users
**Response code:** 200 OK
**curl**: `curl -XGET 'localhost:5000/users'`

### Saves the given user's name and date of birth in the database. 

**Request:** POST /hello/<username> {“dateOfBirth": "YYYY-MM-DD" }
**Response code:** 201 Created or 409 Conflict if user already exists.
**Response message:** *New user '<username>' was added successfully.*
**curl**: `curl -XPOST -H 'Content-Type: application/json' -d '{"dateOfBirth":"YYYY-MM-DD"}' 'localhost:5000/hello/<username>'`

### Saves/updates the given user's name and date of birth in the database.

**Request:** PUT /hello/<username> {“dateOfBirth": "YYYY-MM-DD" }
**Response code:** 204 No Content or 201 Created if user doesn't exist.
**curl**: `curl -XPUT -H 'Content-Type: application/json' -d '{"dateOfBirth":"YYYY-MM-DD"}' 'localhost:5000/hello/<username>'`

*Note:*
<username> must contains only letters. 
YYYY-MM-DD must be a date before the today date.

### Returns hello birthday message for the given user.
**Request:** GET /hello/<username>
**Response code:** 200 OK or 404 Not Found if user doesn't exist.
**Response messages:** 
* If username's birthday is in N days: *Hello, <username>! Your birthday is in N day(s)*
* If username's birthday is today: *Hello, <username>! Happy birthday!*
**curl**: `curl -XGET -H 'localhost:5000/hello/<username>'`

### Deletes the given user from the database.
**Request:** DELETE /hello/<username>
**Response code:** 200 OK or 404 Not Found if user doesn't exist.
**Response messages:** *User <username> was deleted successfully.*
**curl**: `curl -XDELETE 'localhost:5000/hello/<username>'`

Have fun!
