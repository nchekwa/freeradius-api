import sqlite3
from datetime import datetime

from freeradius import Repositories
from freeradius.database import init_db
from freeradius.models import RadAcct
from pytest import fixture

#
# Each test will depend on repositories instance.
#


@fixture
def repositories():
    db_path = "test_raddb.sqlite"
    init_db(db_path)
    db_session = sqlite3.connect(db_path)
    try:
        yield Repositories(db_session)
    except:
        db_session.rollback()
        raise
    else:
        db_session.commit()
    finally:
        db_session.close()


def insert_radacct_record(db_session, **kwargs):
    """Helper function to insert a radacct record directly into the database."""
    defaults = {
        "acctsessionid": "session123",
        "acctuniqueid": "unique123",
        "username": "testuser",
        "realm": "",
        "nasipaddress": "192.168.1.1",
        "nasportid": None,
        "nasporttype": None,
        "acctstarttime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "acctupdatetime": None,
        "acctstoptime": None,
        "acctinterval": None,
        "acctsessiontime": 3600,
        "acctauthentic": None,
        "connectinfo_start": None,
        "connectinfo_stop": None,
        "acctinputoctets": 1000,
        "acctoutputoctets": 2000,
        "calledstationid": "",
        "callingstationid": "",
        "acctterminatecause": "",
        "servicetype": None,
        "framedprotocol": None,
        "framedipaddress": "10.0.0.1",
        "framedipv6address": "",
        "framedipv6prefix": "",
        "framedinterfaceid": "",
        "delegatedipv6prefix": "",
        "class": None,
    }
    defaults.update(kwargs)
    
    columns = ", ".join(defaults.keys())
    placeholders = ", ".join(["?" for _ in defaults])
    sql = f"INSERT INTO radacct ({columns}) VALUES ({placeholders})"
    
    cursor = db_session.cursor()
    cursor.execute(sql, tuple(defaults.values()))
    return cursor.lastrowid


def test_radacct_find_by_username_empty(repositories):
    """Test finding sessions for a user with no records."""
    sessions = repositories.radacct.find_by_username("nonexistent-user")
    assert sessions == []


def test_radacct_find_by_username(repositories):
    """Test finding sessions for a user with records."""
    db_session = repositories.radacct.db_session
    
    # Insert test records
    insert_radacct_record(db_session, username="testuser", acctuniqueid="unique1", acctsessionid="session1")
    insert_radacct_record(db_session, username="testuser", acctuniqueid="unique2", acctsessionid="session2")
    insert_radacct_record(db_session, username="otheruser", acctuniqueid="unique3", acctsessionid="session3")
    db_session.commit()
    
    # Find sessions for testuser
    sessions = repositories.radacct.find_by_username("testuser")
    assert len(sessions) == 2
    assert all(isinstance(s, RadAcct) for s in sessions)
    assert all(s.username == "testuser" for s in sessions)
    
    # Find sessions for otheruser
    sessions = repositories.radacct.find_by_username("otheruser")
    assert len(sessions) == 1
    assert sessions[0].username == "otheruser"


def test_radacct_find_by_username_with_limit(repositories):
    """Test finding sessions with limit parameter."""
    db_session = repositories.radacct.db_session
    
    # Insert multiple test records
    for i in range(10):
        insert_radacct_record(
            db_session, 
            username="limituser", 
            acctuniqueid=f"limit_unique{i}", 
            acctsessionid=f"limit_session{i}"
        )
    db_session.commit()
    
    # Find with limit
    sessions = repositories.radacct.find_by_username("limituser", limit=5)
    assert len(sessions) == 5


def test_radacct_find_by_username_with_offset(repositories):
    """Test finding sessions with offset parameter."""
    db_session = repositories.radacct.db_session
    
    # Insert multiple test records
    for i in range(10):
        insert_radacct_record(
            db_session, 
            username="offsetuser", 
            acctuniqueid=f"offset_unique{i}", 
            acctsessionid=f"offset_session{i}"
        )
    db_session.commit()
    
    # Find with offset
    all_sessions = repositories.radacct.find_by_username("offsetuser", limit=None)
    offset_sessions = repositories.radacct.find_by_username("offsetuser", limit=5, offset=3)
    
    assert len(all_sessions) == 10
    assert len(offset_sessions) == 5


def test_radacct_count_by_username(repositories):
    """Test counting sessions for a user."""
    db_session = repositories.radacct.db_session
    
    # Insert test records
    for i in range(5):
        insert_radacct_record(
            db_session, 
            username="countuser", 
            acctuniqueid=f"count_unique{i}", 
            acctsessionid=f"count_session{i}"
        )
    db_session.commit()
    
    count = repositories.radacct.count_by_username("countuser")
    assert count == 5
    
    # Count for non-existent user
    count = repositories.radacct.count_by_username("nonexistent")
    assert count == 0


def test_radacct_model_fields(repositories):
    """Test that RadAcct model contains all expected fields."""
    db_session = repositories.radacct.db_session
    
    start_time = "2024-01-15 10:30:00"
    insert_radacct_record(
        db_session,
        username="fielduser",
        acctuniqueid="field_unique",
        acctsessionid="field_session",
        nasipaddress="192.168.1.100",
        acctstarttime=start_time,
        acctsessiontime=7200,
        acctinputoctets=5000,
        acctoutputoctets=10000,
        framedipaddress="10.0.0.50",
        acctterminatecause="User-Request",
    )
    db_session.commit()
    
    sessions = repositories.radacct.find_by_username("fielduser")
    assert len(sessions) == 1
    
    session = sessions[0]
    assert session.username == "fielduser"
    assert session.acctuniqueid == "field_unique"
    assert session.acctsessionid == "field_session"
    assert session.nasipaddress == "192.168.1.100"
    assert session.acctsessiontime == 7200
    assert session.acctinputoctets == 5000
    assert session.acctoutputoctets == 10000
    assert session.framedipaddress == "10.0.0.50"
    assert session.acctterminatecause == "User-Request"
