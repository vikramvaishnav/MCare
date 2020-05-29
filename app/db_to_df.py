import pandas as pd


from sqlalchemy import create_engine

# Create an engine
def db_to_df(csv=False,dburl='postgresql://madmin:medocare@localhost:5432/medocare',file="data/CSV/monthly.csv",tablename="medicineinventorymonthly"):
    if csv==False:
       engine = create_engine(dburl)
       query="SELECT * FROM "+tablename
       df=pd.read_sql(query,engine)
    else:
        df= pd.read_csv(file)
    return df
    #create user madmin with password 'medocare';
