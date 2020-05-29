import pandas as pd 
def map_to_df(file='data/map/hospitals.csv',loc='Pune City'):
    
    df=pd.read_csv(file)
    
    df=df.loc[df['Taluka_Name']==loc]
    latitude= list(df.latitude)
    longitude=list(df.longitude)

    hnames=list(df['Health Facility Name'])
    
    return hnames,latitude, longitude