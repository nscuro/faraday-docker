# faraday-docker

Docker & Docker Compose setup for [FaradaySEC](https://faradaysec.com/)'s server.  

The aim of this project is to get a working Faraday setup up and running as
quick and reliable as possible. Useful when evaluating if Faraday is of any use to you or not.

Built for Faraday 3.1.1 - most likely works for future versions also.

## Usage

### Install Server

* Adjust the environment variables in [`faraday-server-db.env`](./faraday-server-db.env) and [`faraday-server-app.env`](./faraday-server-app.env) as needed
  * For testing purposes the defaults work just fine
  * The default values are defines in the server's [`Dockerfile`](./images/faraday-server/Dockerfile)
* `git clone https://guthub.com/nscuro/faraday-docker.git`
* `cd faraday-docker`
* `docker-compose up --build -d`

### Install Client

* Install [pipenv](https://github.com/pypa/pipenv)
* `git clone https://github.com/infobyte/faraday`
* `cd faraday`
* `git checkout tags/v3.1.1 -b v3.1.1`
* `pipenv install --two -r requirements.txt`
* `pipenv install -r requirements_extra.txt`
* `pipenv run python faraday.py --gui=no`
  * Confirm with `y` when faraday asks about installing more dependencies
* The first run most likely fails due to the last workspace `untitled` not being accessible
  * Just open `http://127.0.0.1:5985`, login and create a workspace with that name
  * Run `pipenv run python faraday.py --gui=no` again and it should work
