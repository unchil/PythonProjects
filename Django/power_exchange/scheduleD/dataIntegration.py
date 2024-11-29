import pandas as pd
from sqlalchemy import create_engine

db_url = 'sqlite:////Volumes/WorkSpace/PythonProjects/power_exchange/db.sqlite3'

engine = create_engine(db_url, echo=False)

with engine.connect() as conn, conn.begin():
    df = pd.read_sql_table("supplydemand_dayfiveminsupplydemand", conn)
    df.to_sql(name='supplydemand_fullsupplydemand', con=engine, if_exists='append', index=False, method='multi')

