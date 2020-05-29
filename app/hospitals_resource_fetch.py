import pandas as  pd 

def hospitals_resource_fetch(hname='Kamla Nehru Hospital', file='data/CSV/hospitals_infrastructure.csv'):
    df= pd.read_csv(file)
    data=df.loc[df['Hospital Name']==hname]
    return data