import os
import sqlite3
from contextlib import closing

from .models import AttributeOpValue, Group, Nas, User, UserGroup
from .repositories import GroupRepository, NasRepository, UserRepository

# Adapted from docker/freeradius-mysql/2-schema.sql for SQLite
SQLITE_SCHEMA = """
DROP TABLE IF EXISTS radcheck;
CREATE TABLE radcheck (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(64) NOT NULL DEFAULT '',
  attribute VARCHAR(64) NOT NULL DEFAULT '',
  op CHAR(2) NOT NULL DEFAULT '==',
  value VARCHAR(253) NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_radcheck_username ON radcheck (username);

DROP TABLE IF EXISTS radgroupcheck;
CREATE TABLE radgroupcheck (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  groupname VARCHAR(64) NOT NULL DEFAULT '',
  attribute VARCHAR(64) NOT NULL DEFAULT '',
  op CHAR(2) NOT NULL DEFAULT '==',
  value VARCHAR(253) NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_radgroupcheck_groupname ON radgroupcheck (groupname);

DROP TABLE IF EXISTS radgroupreply;
CREATE TABLE radgroupreply (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  groupname VARCHAR(64) NOT NULL DEFAULT '',
  attribute VARCHAR(64) NOT NULL DEFAULT '',
  op CHAR(2) NOT NULL DEFAULT '=',
  value VARCHAR(253) NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_radgroupreply_groupname ON radgroupreply (groupname);

DROP TABLE IF EXISTS radreply;
CREATE TABLE radreply (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(64) NOT NULL DEFAULT '',
  attribute VARCHAR(64) NOT NULL DEFAULT '',
  op CHAR(2) NOT NULL DEFAULT '=',
  value VARCHAR(253) NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_radreply_username ON radreply (username);

DROP TABLE IF EXISTS radusergroup;
CREATE TABLE radusergroup (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(64) NOT NULL DEFAULT '',
  groupname VARCHAR(64) NOT NULL DEFAULT '',
  priority INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_radusergroup_username ON radusergroup (username);

DROP TABLE IF EXISTS nas;
CREATE TABLE nas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nasname VARCHAR(128) NOT NULL,
  shortname VARCHAR(32),
  type VARCHAR(30) DEFAULT 'other',
  ports INTEGER,
  secret VARCHAR(60) NOT NULL DEFAULT 'secret',
  server VARCHAR(64),
  community VARCHAR(50),
  description VARCHAR(200) DEFAULT 'RADIUS Client'
);
CREATE INDEX IF NOT EXISTS idx_nas_nasname ON nas (nasname);

DROP TABLE IF EXISTS radhuntgroup;
CREATE TABLE radhuntgroup (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  groupname VARCHAR(64) NOT NULL DEFAULT '',
  nasipaddress VARCHAR(15) NOT NULL DEFAULT '',
  nasportid VARCHAR(15) DEFAULT NULL
);
CREATE INDEX IF NOT EXISTS idx_radhuntgroup_nasipaddress ON radhuntgroup (nasipaddress);

DROP TABLE IF EXISTS radacct;
CREATE TABLE radacct (
  radacctid INTEGER PRIMARY KEY AUTOINCREMENT,
  acctsessionid VARCHAR(64) NOT NULL DEFAULT '',
  acctuniqueid VARCHAR(32) NOT NULL DEFAULT '',
  username VARCHAR(64) NOT NULL DEFAULT '',
  groupname VARCHAR(64) NOT NULL DEFAULT '',
  realm VARCHAR(64) DEFAULT '',
  nasipaddress VARCHAR(15) NOT NULL DEFAULT '',
  nasportid VARCHAR(32) DEFAULT NULL,
  nasporttype VARCHAR(32) DEFAULT NULL,
  acctstarttime DATETIME DEFAULT NULL,
  acctupdatetime DATETIME DEFAULT NULL,
  acctstoptime DATETIME DEFAULT NULL,
  acctinterval INTEGER DEFAULT NULL,
  acctsessiontime INTEGER DEFAULT NULL,
  acctauthentic VARCHAR(32) DEFAULT NULL,
  connectinfo_start VARCHAR(50) DEFAULT NULL,
  connectinfo_stop VARCHAR(50) DEFAULT NULL,
  acctinputoctets BIGINT DEFAULT NULL,
  acctoutputoctets BIGINT DEFAULT NULL,
  calledstationid VARCHAR(50) NOT NULL DEFAULT '',
  callingstationid VARCHAR(50) NOT NULL DEFAULT '',
  acctterminatecause VARCHAR(32) NOT NULL DEFAULT '',
  servicetype VARCHAR(32) DEFAULT NULL,
  framedprotocol VARCHAR(32) DEFAULT NULL,
  framedipaddress VARCHAR(15) NOT NULL DEFAULT '',
  framedipv6address VARCHAR(45) NOT NULL DEFAULT '',
  framedipv6prefix VARCHAR(45) NOT NULL DEFAULT '',
  framedinterfaceid VARCHAR(44) NOT NULL DEFAULT '',
  delegatedipv6prefix VARCHAR(45) NOT NULL DEFAULT '',
  class VARCHAR(64) DEFAULT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_radacct_acctuniqueid ON radacct (acctuniqueid);
CREATE INDEX IF NOT EXISTS idx_radacct_username ON radacct (username);
CREATE INDEX IF NOT EXISTS idx_radacct_acctstarttime ON radacct (acctstarttime);
CREATE INDEX IF NOT EXISTS idx_radacct_nasipaddress ON radacct (nasipaddress);
"""


def init_test_data(connection):
    """
    Populates the database with initial test data.
    """
    user_repo = UserRepository(connection)
    group_repo = GroupRepository(connection)
    nas_repo = NasRepository(connection)

    # Add some NASes
    n1 = Nas(nasname="3.3.3.3", shortname="my-super-nas", secret="my-super-secret")
    n2 = Nas(nasname="4.4.4.4", shortname="my-other-nas", secret="my-other-secret")
    if not nas_repo.exists(n1.nasname) and not nas_repo.exists(n2.nasname):
        nas_repo.add(n1)
        nas_repo.add(n2)

    # Add some groups
    g1 = Group(
        groupname="100m",
        replies=[AttributeOpValue(attribute="Filter-Id", op=":=", value="100m")],
    )
    g2 = Group(
        groupname="200m",
        replies=[AttributeOpValue(attribute="Filter-Id", op=":=", value="200m")],
    )
    if not group_repo.exists(g1.groupname) and not group_repo.exists(g2.groupname):
        group_repo.add(g1)
        group_repo.add(g2)

    # Add some users
    u1 = User(
        username="bob",
        groups=[UserGroup(groupname=g1.groupname)],
        checks=[
            AttributeOpValue(attribute="Cleartext-Password", op=":=", value="bob-pass")
        ],
        replies=[
            AttributeOpValue(attribute="Framed-IP-Address", op=":=", value="10.0.0.1"),
            AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.1.0/24"),
            AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.2.0/24"),
            AttributeOpValue(attribute="Huawei-Vpn-Instance", op=":=", value="bob-vrf"),
        ],
    )
    u2 = User(
        username="alice@adsl",
        groups=[UserGroup(groupname=g1.groupname)],
        checks=[
            AttributeOpValue(attribute="Cleartext-Password", op=":=", value="alice-pass")
        ],
        replies=[
            AttributeOpValue(attribute="Framed-IP-Address", op=":=", value="10.0.0.2"),
            AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.1.0/24"),
            AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.2.0/24"),
            AttributeOpValue(
                attribute="Huawei-Vpn-Instance", op=":=", value="alice-vrf"
            ),
        ],
    )
    u3 = User(
        username="eve",
        groups=[
            UserGroup(groupname=g1.groupname, priority=1),
            UserGroup(groupname=g2.groupname, priority=2),
        ],
        checks=[
            AttributeOpValue(attribute="Cleartext-Password", op=":=", value="eve-pass")
        ],
        replies=[
            AttributeOpValue(attribute="Framed-IP-Address", op=":=", value="10.0.0.3"),
            AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.1.0/24"),
            AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.2.0/24"),
            AttributeOpValue(attribute="Huawei-Vpn-Instance", op=":=", value="eve-vrf"),
        ],
    )
    u4 = User(
        username="oscar@wil.de",
        checks=[
            AttributeOpValue(attribute="Cleartext-Password", op=":=", value="oscar-pass")
        ],
        replies=[
            AttributeOpValue(attribute="Framed-IP-Address", op=":=", value="10.0.0.4"),
            AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.1.0/24"),
            AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.2.0/24"),
            AttributeOpValue(
                attribute="Huawei-Vpn-Instance", op=":=", value="oscar-vrf"
            ),
        ],
    )
    if (
        not user_repo.exists(u1.username)
        and not user_repo.exists(u2.username)
        and not user_repo.exists(u3.username)
        and not user_repo.exists(u4.username)
        and group_repo.exists(g1.groupname)
        and group_repo.exists(g2.groupname)
    ):
        user_repo.add(u1)
        user_repo.add(u2)
        user_repo.add(u3)
        user_repo.add(u4)


def init_db(db_path: str = "raddb.sqlite"):
    """
    Initializes the SQLite database with the required schema.
    This function drops existing tables and recreates them.
    """
    with closing(sqlite3.connect(db_path)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.executescript(SQLITE_SCHEMA)
        connection.commit()


def cleanup_db(db_path: str = "raddb.sqlite"):
    """
    Removes the database file.
    """
    if os.path.exists(db_path):
        os.remove(db_path)

