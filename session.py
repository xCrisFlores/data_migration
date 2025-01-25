#Archivo de la sesion de la base de datos, tiene que existir dicha base antes de poder usar el script
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Base

#parametros de la cadena de conexion, llenar con los respectivos de la maquina
user = ""
password = ""
host = "localhost" #dejar este dato si se estan haciendo pruebas locales
port = "3306" #dejar este dato en caso de usar maria db
database = ""

database_url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()

#validar que existen las tablas
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

#creacion automatica de las tablas si no existen
if not all(table in existing_tables for table in Base.metadata.tables):
    Base.metadata.create_all(engine)
    print("The tables was created")
else:
    print("The tables already exists")

session.close()
