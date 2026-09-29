from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASEURL="mysql+pymysql://root:Venu410%40@localhost/new_data"

engine=create_engine(DATABASEURL)

sessionlocal=sessionmaker(bind=engine)

def get_session():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()