import os
from dotenv import load_dotenv
from freeradius.settings import RadTables


load_dotenv()

# Uncomment the appropriate line matching the DB-API 2.0 (PEP 249) compliant driver to use
# Default: MySQL
# Other options: "psycopg", "psycopg2", "pymysql", "pysqlite3", "sqlite3"
DB_DRIVER = os.getenv("DB_DRIVER", "mysql.connector")

# Database connection settings
if DB_DRIVER in ["mysql.connector", "pymysql"]:
    DB_NAME = os.getenv("DB_NAME", "raddb")
    DB_USER = os.getenv("DB_USER", "raduser")
    DB_PASS = os.getenv("DB_PASS", "radpass")
    DB_HOST = os.getenv("DB_HOST", "mydb")
    DB_PORT = os.getenv("DB_PORT", 3306)
elif DB_DRIVER in ["sqlite3", "pysqlite3"]:
    DB_NAME = os.getenv("DB_NAME", "raddb")
    DB_USER = ""
    DB_PASS = ""
    DB_HOST = ""
    DB_PORT = None
elif DB_DRIVER in ["psycopg", "psycopg2"]:
    DB_NAME = os.getenv("DB_NAME", "raddb")
    DB_USER = os.getenv("DB_USER", "raduser")
    DB_PASS = os.getenv("DB_PASS", "radpass")
    DB_HOST = os.getenv("DB_HOST", "pgdb")
    DB_PORT = 5432
else:
    DB_NAME = os.getenv("DB_NAME", "raddb")
    DB_USER = os.getenv("DB_USER", "raduser")
    DB_PASS = os.getenv("DB_PASS", "radpass")
    DB_HOST = os.getenv("DB_HOST", "mydb")
    DB_PORT = os.getenv("DB_PORT")

# Database table settings
ITEMS_PER_PAGE = int(os.getenv("ITEMS_PER_PAGE", 100))

# API_URL will be used to set the "Location" header field
# after a resource has been created (POST) as per RFC 7231
# and the "Link" header field (pagination) as per RFC 8288
API_BASE_URL = os.getenv("API_URL", "http://0.0.0.0:8000")
API_URL = f"{API_BASE_URL}/api/v1"


RAD_TABLES = RadTables()
