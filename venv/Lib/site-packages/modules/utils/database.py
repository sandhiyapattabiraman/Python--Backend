from sqlmodel import create_engine, SQLModel, Session


database_url = "sqlite:///database.db"
engine = create_engine(database_url,connect_args={"check_same_thread":False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    


    
__all__ =["engine","Session"]