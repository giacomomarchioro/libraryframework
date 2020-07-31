import sqlalchemy as db
import os
from datetime import datetime
# Create the database or access it.
if "movements.sqlite" not in os.listdir(os.getcwd()):
    engine = db.create_engine('sqlite:///movements.sqlite')
    connection = engine.connect()
    metadata = db.MetaData()

    # this table store the movements of the objects (manuscripts, books etc. etc.)
    emp = db.Table('movimentazioni', metadata,
                db.Column('Time_stamp', db.DateTime()),
                db.Column('ID_bene', db.Integer()),
                db.Column('stanza', db.Integer()),
                db.Column('operatore', db.Integer()),
                db.Column('destinazione', db.Integer()),
                db.Column('motivo', db.Integer()),
                db.Column('peso', db.Integer()),
                )
    metadata.create_all(engine) #  Creates the table

else:
    print("Database already created.")