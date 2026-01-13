import pytest
import sqlalchemy as sa

@pytest.fixture()
def database(tmp_path):
    from ostryalis import Database
    return Database(cfg=lambda _key: str(tmp_path))

def test_attach_before(database):
    database.attach('extra')
    with database.use_session() as session:
        result = [row[1] for row in session.execute(sa.text("PRAGMA database_list"))]
        assert result == ['main', 'extra']

def test_attach_after(database):
    with database.use_session() as session:
        database.attach('extra')
        result = [row[1] for row in session.execute(sa.text("PRAGMA database_list"))]
        assert result == ['main', 'extra']
