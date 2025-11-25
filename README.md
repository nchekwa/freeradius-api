[![python](https://img.shields.io/badge/python-3.10+-success.svg)](https://devguide.python.org/versions)
[![license](https://img.shields.io/badge/license-MIT-success.svg)](https://opensource.org/licenses/MIT)

* [What is this project?](#what-is-this-project)
* [Quick demo](#quick-demo)
* [HOWTO](#howto)
  * [Using Docker](#using-docker)
  * [Using a venv](#using-a-venv)
* [Configuration](#configuration)
* [Keyset pagination](#keyset-pagination)
* [API authentication](#api-authentication)

# What is this project?

A Python REST API on top of the FreeRADIUS database for automation purposes.

* It provides an [object-oriented view](src/freeradius/models) of the database schema.
* It implements logic to ensure data consistency.
* It works with **MySQL**, **MariaDB**, **PostgreSQL** and **SQLite** using DB-API 2.0 compliant drivers.

# Quick demo

## Get NASes, users, groups, and huntgroups

Number of results is limited to `100` by default.

```sh
curl -X 'GET' http://localhost:8000/api/v1/nas
#> 200 OK
[
    {"nasname": "3.3.3.3", "shortname": "my-super-nas", "secret": "my-super-secret"},
    {"nasname": "4.4.4.4", "shortname": "my-other-nas", "secret": "my-other-secret"}
]
```
```sh
curl -X 'GET' http://localhost:8000/api/v1/users
#> 200 OK
[
    {
        "username": "alice@adsl",
        "checks": [{"attribute": "Cleartext-Password", "op": ":=", "value": "alice-pass"}],
        "replies": [
            {"attribute": "Framed-IP-Address", "op": ":=", "value": "10.0.0.2"},
            {"attribute": "Framed-Route", "op": "+=", "value": "192.168.1.0/24"}
        ],
        "groups": [{"groupname": "100m", "priority": 1}]
    },
    {
        "username": "bob",
        "checks": [{"attribute": "Cleartext-Password", "op": ":=", "value": "bob-pass"}],
        "replies": [
            {"attribute": "Framed-IP-Address", "op": ":=", "value": "10.0.0.1"}
        ],
        "groups": [{"groupname": "100m", "priority": 1}]
    }
]
```
```sh
curl -X 'GET' http://localhost:8000/api/v1/groups
#> 200 OK
[
    {
        "groupname": "100m",
        "checks": [],
        "replies": [{"attribute": "Filter-Id", "op": ":=", "value": "100m"}],
        "users": [
            {"username": "bob", "priority": 1},
            {"username": "alice@adsl", "priority": 1}
        ]
    }
]
```
```sh
curl -X 'GET' http://localhost:8000/api/v1/huntgroups
#> 200 OK
[
    {
        "groupname": "ap-group",
        "nas_ip_address": "192.168.1.10",
        "nas_port_id": "ap-01"
    }
]
```

## Get specific resources

```sh
curl -X 'GET' http://localhost:8000/api/v1/nas/3.3.3.3
```
```sh
curl -X 'GET' http://localhost:8000/api/v1/users/eve
```
```sh
curl -X 'GET' http://localhost:8000/api/v1/groups/100m
```

## Create resources

```sh
curl -X 'POST' \
  'http://localhost:8000/api/v1/nas' \
  -H 'Content-Type: application/json' \
  -d '{
  "nasname": "5.5.5.5",
  "shortname": "my-nas",
  "secret": "my-secret"
}'
```

## Patch resources

The update strategy follows [RFC 7396](https://datatracker.ietf.org/doc/html/rfc7396) (JSON Merge Patch) guidelines:
* Omitted fields are not modified.
* `None` value means removal.
* **A list field can only be overwritten (replaced).**

```sh
curl -X 'PATCH' \
  'http://localhost:8000/api/v1/nas/5.5.5.5' \
  -H 'Content-Type: application/json' \
  -d '{
  "secret": "new-secret"
}'
```

## Delete resources

```sh
curl -X 'DELETE' http://localhost:8000/api/v1/nas/5.5.5.5
```

# HOWTO

**An instance of the FreeRADIUS server is NOT needed for testing.** The focus is on the FreeRADIUS database. As long as you have one (or a Docker container for it), the API can run.

## Using Docker

The project includes a Docker setup for easy testing.

```bash
git clone https://github.com/angely-dev/freeradius-api.git
cd freeradius-api/docker
docker compose up -d --build
```

Then go to: http://localhost:8000/docs

## Using a venv

1. **Get the project:**

```bash
git clone https://github.com/angely-dev/freeradius-api.git
cd freeradius-api
```

2. **Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

Copy the example environment file and edit it to match your database settings.

```bash
cd src
cp .env.example .env
nano .env
```

Set `DB_DRIVER`, `DB_HOST`, `DB_USER`, `DB_PASS`, etc.

5. **Run the API:**

```bash
uvicorn api:app --reload
```

Then go to: http://localhost:8000/docs

# Configuration

Configuration is managed via environment variables (or a `.env` file in the `src` directory).

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_DRIVER` | Database driver (`mysql.connector`, `psycopg`, `sqlite3`, etc.) | `mysql.connector` |
| `DB_HOST` | Database host | `mydb` |
| `DB_PORT` | Database port | `3306` |
| `DB_NAME` | Database name | `raddb` |
| `DB_USER` | Database user | `raduser` |
| `DB_PASS` | Database password | `radpass` |
| `ITEMS_PER_PAGE` | Pagination limit | `100` |
| `API_URL` | Base URL for Link headers | `http://0.0.0.0:8000` |
| `X_API_KEY` | API Key(s) for authentication | `None` |

# Keyset pagination

Results are paginated using Keyset pagination (aka `WHERE` + `LIMIT`).

Pagination is done through HTTP response headers (as per [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288)). The `Link` header contains the URL for the next page.

```bash
$ curl -X 'GET' -i http://localhost:8000/api/v1/users
HTTP/1.1 200 OK
link: <http://localhost:8000/api/v1/users?from_username=acb>; rel="next"
...
```

# API authentication

Authentication can be enabled by setting the `X_API_KEY` environment variable.

1. **Set the key in `.env`:**
   ```bash
   X_API_KEY=my-secret-key
   ```
   Or for multiple keys:
   ```bash
   X_API_KEY=key1,key2,key3
   ```

2. **Make authenticated requests:**

   ```bash
   curl -X 'GET' -H 'X-API-Key: my-secret-key' http://localhost:8000/api/v1/users
   ```

The header name can be customized via `X_API_KEY_HEADER`.
