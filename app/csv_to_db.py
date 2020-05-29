import pandas as pd


from sqlalchemy import create_engine

# Create an engine
def csv_to_db(dburl='postgresql://madmin:medocare@localhost:5432/medocare',file="/home/dj/WORK (Be Project)/mcarev2/Flask/MedoCare/data/CSV/monthly.csv",tablename="medicineinventorymonthly"):
    engine = create_engine(dburl)
    df=pd.read_csv(file)
    df.to_sql(tablename, engine, if_exists='append', index=False)
    print("Table created", tablename)
    #create user madmin with password 'medocare';