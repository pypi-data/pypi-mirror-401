__all__ = ['search']

import sqlalchemy as sa
from .database import database

def search(q=None, session=None):
    with database.use_session(session) as session:
        rows = session.execute(
            sa.text('''
                SELECT
                    *
                FROM
                    object
                LIMIT
                    100
            ''')
        )
        for row in rows:
            yield dict(row._mapping)
