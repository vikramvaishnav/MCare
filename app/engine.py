from keras.models import Sequential, model_from_json
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Bidirectional

from sklearn.preprocessing import MinMaxScaler
import numpy as np
import datetime
from dateutil.relativedelta import *
import pandas as pd
import math


'''
Date Generalization remaining
'''
def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        end_ix = i + n_steps
        if end_ix > len(sequence)-1:
            break
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)
class LSTM_Model:
    def __init__(self,df,model_path='/home/dj/WORK (Be Project)/mcarev2/Flask/flask-argon-dashboard/data/'):
        self.df=df
        self.model_path=model_path
        
    def train(self):
        
        df=self.df
        size = int(len(df))
        n_steps=1
        n_features = 1
        r=[i for i in df.columns if i!='datum']
        for x in r:
          
            X=df[x].values
            scaler = MinMaxScaler(feature_range = (0, 1))
            X=scaler.fit_transform(X.reshape(-1, 1))
            X_train,y_train=split_sequence(X[:-1], n_steps)
            X_test= X[-1]
            X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], n_features))
            model = Sequential()

            model.add(LSTM(100, activation='relu', input_shape=(n_steps, n_features)))
        #     model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(n_steps, n_features)))
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mse')
            model.fit(X_train, y_train, epochs=400, verbose=0)
            model_json=model.to_json()
            with open(self.model_path+"/model_"+x+"_.json","w") as json_file:
                json_file.write(model_json)
            model.save_weights(self.model_path+"/model_"+x+"_weights.h5")
            
    def predict(self,months_weeks=5):
        df=self.df
        size = int(len(df))
        n_steps=1
        n_features = 1
       
        numrows=4
        numcols=2


        # warnings.filterwarnings("ignore")
        medpred=[]
        lastdate=list(df['datum'])[-1]
        r=[i for i in df.columns if i!='datum']
        dates=[]
        date=datetime.datetime.strptime(lastdate,'%Y-%m-%d')
        dates.append(str(date.strftime('%Y-%m-%d')))
        for i in range(months_weeks-1):
            date=datetime.datetime.strptime(lastdate,'%Y-%m-%d')+relativedelta(months=i+1)
            dates.append(str(date.strftime('%Y-%m-%d')))
        for x in r:
            X=df[x].values
            scaler = MinMaxScaler(feature_range = (0, 1))
            X=scaler.fit_transform(X.reshape(-1, 1))
            X_test= X[-1]
            X_test = X_test.reshape((len(X_test), n_steps, n_features))
            json_file= open(self.model_path+"/model_"+x+"_.json","r")
            model_json=json_file.read()
            model=model_from_json(model_json)
            model.load_weights(self.model_path+'/model_'+x+'_weights.h5')
            predictions=[]
            prediction = model.predict(X_test, verbose=0)
            prediction = scaler.inverse_transform(prediction)
            predictions.append(int(prediction))

            for i in range(months_weeks-1):
                prediction = model.predict(scaler.transform(np.array(predictions[-1]).reshape(-1,1)).reshape(1,n_steps,n_features), verbose=0)
            #y_test=scaler.inverse_transform(y_test)

                prediction = scaler.inverse_transform(prediction)
                predictions.append(float(int(prediction)))
            medpred.append({x:predictions})
        return dates,medpred
    
    def predict_week(self,months_weeks=5):
        df=self.df
        size = int(len(df))
        n_steps=1
        n_features = 1
       
        numrows=4
        numcols=2


        # warnings.filterwarnings("ignore")
        medpred=[]
        lastdate=list(df['datum'])[-1]
        r=[i for i in df.columns if i!='datum']
        dates=[]
        date=datetime.datetime.strptime(lastdate,'%m/%d/%Y')
        dates.append(str(date.strftime('%Y-%m-%d')))
        for i in range(months_weeks-1):
            date=datetime.datetime.strptime(lastdate,'%m/%d/%Y')+datetime.timedelta(weeks=i+1)
            dates.append(str(date.strftime('%Y-%m-%d')))
        for x in r:
            X=df[x].values
            scaler = MinMaxScaler(feature_range = (0, 1))
            X=scaler.fit_transform(X.reshape(-1, 1))
            X_test= X[-1]
            X_test = X_test.reshape((len(X_test), n_steps, n_features))
            json_file= open(self.model_path+"/model_"+x+"_.json","r")
            model_json=json_file.read()
            model=model_from_json(model_json)
            model.load_weights(self.model_path+'/model_'+x+'_weights.h5')
            predictions=[]
            prediction = model.predict(X_test, verbose=0)
            prediction = scaler.inverse_transform(prediction)
            predictions.append(int(prediction))

            for i in range(months_weeks-1):
                prediction = model.predict(scaler.transform(np.array(predictions[-1]).reshape(-1,1)).reshape(1,n_steps,n_features), verbose=0)
            #y_test=scaler.inverse_transform(y_test)

                prediction = scaler.inverse_transform(prediction)
                predictions.append(float(int(prediction)))
            medpred.append({x:predictions})
        return dates,medpred