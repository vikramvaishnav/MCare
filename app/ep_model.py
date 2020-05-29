import pandas as pd
import urllib, json
import math
import datetime
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

class Ep_model:
    def __init__(self,district_name='Pune'):
        super().__init__()
        self.district_name= district_name
        self.population={'Pune':3120000,'Mumbai':18400000}
        self.X,self.D,self.R =None,None,None
    def data_fetch(self):
        with urllib.request.urlopen("https://api.covid19india.org/districts_daily.json") as url:
            s = url.read()
            data = json.loads(s)
        data = data['districtsDaily']
        state = 'Maharashtra'
        state_data = data[state]
        date = []
        active = []
        confirmed = []
        deceased = []
        district = []
        recovered =[]
        for (k, v) in state_data.items():
        #  print(k)
            for i in v:
                district.append(k)
                date.append(i['date'])
                active.append(i['active'])
                confirmed.append(i['confirmed'])
                deceased.append(i['deceased'])
                recovered.append(i['recovered'])
            dataset = pd.DataFrame({'district': district,'date': date, 'active': active, 'confirmed': confirmed, 'deceased': deceased, 'recovered': recovered})
        df=dataset.loc[dataset['district']=='Pune']
        # df.sort_values("deceased", inplace = True) 
        # df.drop_duplicates(subset='deceased',inplace=True)
        # df.sort_values("recovered", inplace = True) 
        # df.drop_duplicates(subset='recovered',inplace=True)
        self.df=df
    def data_preprocess(self,X_cml, recovered, death,date):
       
        X_cml=X_cml.reshape((1,-1))[0]
        X_cml=X_cml[X_cml != 0]
        print(X_cml)

    # recovered = cumulative recovered cases
        # print(recovered)
        recovered=recovered.reshape((1,-1))[0]
        recovered=recovered[recovered != 0]
        #recovered=recovered[:-1]
        # death = cumulative deaths
        #death = np.array([2, 3, 3, 3, 4, 6, 9, 18, 25, 41, 56, 80, 106, 132, 170, 213, 259, 304, 361, 425, 491, 564, 637, 723, 812, 909, 1017, 1114, 1368, 1381, 1524, 1666, 1772, 1870, 2006, 2121, 2239, 2348, 2445, 2595, 2666, 2718, 2747, 2791, 2838, 2873, 2915, 2946, 2984, 3015, 3045, 3073, 3100, 3123, 3140, 3162, 3173, 3180, 3194, 3204, 3218, 3231, 3242, 3250, 3253, 3261, 3267, 3276, 3283, 3287, 3293, 3298, 3301, 3306, 3311, 3314, 3321, 3327, 3331, 3335, 3338, 3340, 3340, 3342, 3344], dtype=np.float64)[:-27]
    
        death= death.reshape((1,-1))[0]
        death= death[death!= 0]
        #death=death[:-1]
        print(death)
    # recovered=recovered[len(recovered)-len(date):]
        
        #death=death[len(death)-len(date):]
    #  X_cml= X_cml[len(X_cml)-len(date):]
        if len(recovered)<len(death):
            X_cml= X_cml[len(X_cml)-len(recovered):]
            death=death[len(death)-len(recovered):]
         
            # date=date[len(date)-len(recovered):]
        elif len(death)<len(X_cml):
            
            recovered=recovered[len(recovered)-len(death):]
            X_cml= X_cml[len(X_cml)-len(death):]
            
            # date=date[len(date)-len(death):]
        elif len(X_cml)<len(death): 
            recovered=recovered[len(recovered)-len(X_cml):]

            death=death[len(death)-len(X_cml):]
            # date=date[len(date)-len(X_cml):]
        else:
            pass
        # dates=list(date)
        # base = datetime.datetime.strptime(dates[-1], "%Y-%m-%d")
        return X_cml, recovered, death
    def data_spilt(self,data, orders, start):
        x_train = np.empty((len(data) - start - orders, orders))
        y_train = data[start + orders:]

        for i in range(len(data) - start - orders):
            x_train[i] = data[i + start:start + orders + i]
        return x_train, y_train
    def SIR(self,X_cml, recovered, death, population):
      
        X = X_cml - recovered - death
        R = recovered
        D= death
        print('xrd',X,R,D)
        n = np.array([population] * len(X), dtype=np.float64)

        S = n - X - R
        rho= 1/14

        X_diff = np.array([X[:-1], X[1:]], dtype=np.float64).T
        R_diff = np.array([R[:-1], R[1:]], dtype=np.float64).T
        D_diff= np.array([D[:-1],D[1:]], dtype=np.float64).T
        alpha= (D[1:]-D[:-1])/(rho*X[:-1])
        gamma = (R[1:] - R[:-1]) / (X[:-1]* (1-alpha))
        beta = n[:-1] * (X[1:] - X[:-1] + R[1:] - R[:-1]+ D[1:]- D[:-1]) / (X[:-1] * (n[:-1] - X[:-1] - R[:-1] -D[:-1]))
        R0 = beta / gamma
        
        ########## Parameters for Ridge Regression ##########
        ##### Orders of the two FIR filters in (12), (13) in the paper. #####
        orders_beta = 3
        orders_gamma = 3
        orders_alpha=3

        ##### Select a starting day for the data training in the ridge regression. #####
        start_beta = 1
        start_gamma = 1
        start_alpha=1
        ########## Print Info ##########
        print("\nThe latest transmission rate beta of SIR model:", beta[-1])
        print("The latest recovering rate gamma of SIR model:", gamma[-1])
        print("The latest mortality rate alpha of SIR model:", alpha[-1])
        print("The latest basic reproduction number R0:", R0[-1])

        ########## Ridge Regression ##########
        ##### Split the data to the training set and testing set #####
        x_beta, y_beta = self.data_spilt(beta, orders_beta, start_beta)
        x_gamma, y_gamma = self.data_spilt(gamma, orders_gamma, start_gamma)
        x_alpha,y_alpha= self.data_spilt(alpha, orders_alpha,start_alpha)

        ##### Searching good parameters #####
    #     clf_beta = ridge(x_beta, y_beta)
    #     clf_gamma = ridge(x_gamma, y_gamma)
        print(x_beta,y_beta)

        #### Training and Testing #####
        clf_beta = Ridge(alpha=0.003765, copy_X=True, fit_intercept=False, max_iter=None, normalize=True, random_state=None, solver='auto', tol=1e-08).fit(x_beta, y_beta)
        clf_gamma = Ridge(alpha=0.001675, copy_X=True, fit_intercept=False, max_iter=None,normalize=True, random_state=None, solver='auto', tol=1e-08).fit(x_gamma, y_gamma)
        clf_alpha = Ridge(alpha=0.001675, copy_X=True, fit_intercept=False, max_iter=None,normalize=True, random_state=None, solver='auto', tol=1e-08).fit(x_alpha, y_alpha)

    #     clf_beta= model(x_beta,y_beta)
        
    #     clf_gamma=model(x_gamma,y_gamma)
        beta_hat = clf_beta.predict(x_beta)
    #     beta_hat= clf_beta.predict(np.reshape(x_beta, (x_beta.shape[0], 1, x_beta.shape[1]))) 
    
        gamma_hat = clf_gamma.predict(x_gamma)
        alpha_hat=  clf_alpha.predict(x_alpha)
    #     gamma_hat= clf_gamma.predict(np.reshape(x_gamma, (x_gamma.shape[0], 1, x_gamma.shape[1])))
        
   
        ########## Time-dependent SIR model ##########

        ##### Parameters for the Time-dependent SIR model #####
        stop_X = 0 # stopping criteria
        stop_day = 100 # maximum iteration days (W in the paper)

        day_count = 0
        turning_point = 0

        S_predict = [S[-1]]
        X_predict = [X[-1]]
        R_predict = [R[-1]]
        D_predict= [D[-1]]

        predict_beta = np.array(beta[-orders_beta:]).tolist()
        predict_gamma = np.array(gamma[-orders_gamma:]).tolist()
        predict_alpha=  np.array(alpha[-orders_alpha:]).tolist()
        while (X_predict[-1] >= stop_X) and (day_count <= stop_day):
            if predict_beta[-1] > predict_gamma[-1]:
                turning_point += 1

            next_beta = clf_beta.predict(np.asarray([predict_beta[-orders_beta:]]))[0]
    #         next_beta = clf_beta.predict(np.reshape(np.asarray([predict_beta[-orders_beta:]]),(np.asarray([predict_beta[-orders_beta:]]).shape[0],1,np.asarray([predict_beta[-orders_beta:]]).shape[1])))[0]
            next_gamma = clf_gamma.predict(np.asarray([predict_gamma[-orders_gamma:]]))[0]
    #         next_gamma = clf_gamma.predict(np.reshape(np.asarray([predict_gamma[-orders_gamma:]]),(np.asarray([predict_gamma[-orders_gamma:]]).shape[0],1,np.asarray([predict_gamma[-orders_gamma:]]).shape[1])))[0]
            next_alpha = clf_alpha.predict(np.asarray([predict_alpha[-orders_alpha:]]))[0]
            if next_beta < 0:
                next_beta = 0
            if next_gamma < 0:
                next_gamma = 0
            if next_alpha < 0:
                next_alpha = 0
                

            predict_beta.append(next_beta)
            predict_gamma.append(next_gamma)
            predict_alpha.append(next_alpha)

            next_S = ((-predict_beta[-1] * S_predict[-1] *
                    X_predict[-1]) / n[-1]) + S_predict[-1]
            next_X = ((predict_beta[-1] * S_predict[-1] * X_predict[-1]) /
                    n[-1]) - ((1-predict_alpha[-1])* predict_gamma[-1] * X_predict[-1]) - (predict_alpha[-1] * rho * X_predict[-1]) + X_predict[-1]
            next_R = ((1-predict_alpha[-1])*predict_gamma[-1] * X_predict[-1]) + R_predict[-1]
            next_D= (predict_alpha[-1] *rho * X_predict[-1])+ D_predict[-1]
            S_predict.append(next_S)
            X_predict.append(next_X)
            R_predict.append(next_R)
            D_predict.append(next_D)

            day_count += 1
        print(X,X_predict)
        ########## Print Info ##########
        print('\nConfirmed cases tomorrow:', np.rint(X_predict[1] + R_predict[1]+ D_predict[1]))
        print('Infected persons tomorrow:', np.rint(X_predict[1]))
        print('Recovered persons tomorrow:', np.rint(R_predict[1]))
        print('Death persons tomorrow:', np.rint(D_predict[1]))

        print('\nEnd day:', day_count)
        print('Confirmed cases on the end day:', np.rint(X_predict[-2] + R_predict[-2]))

        print('\nTuring point:', turning_point)

        ########## Plot the time evolution of the time-dependent SIR model ##########
       
        X=list(X)
        X.extend(X_predict[1:])
      
        D= list(D)
        D.extend(D_predict[1:])
        R=list(R)
        R.extend(R_predict[1:])
        print("x",X)
       
        return X_predict, D_predict, R_predict
    def train(self):
        X_cml,recovered,death= self.data_preprocess(self.df.confirmed.values,self.df.recovered.values,self.df.deceased.values,self.df.date.values)
        self.X,self.D,self.R= self.SIR(X_cml, recovered, death, self.population[self.district_name])
        
    def tomorrow_data(self):
        if self.X==None or self.D == None or self.R ==None:
            self.train()
        return self.X[1],self.D[1],self.R[1]
    def today_data(self):
        if self.X==None or self.D == None or self.R ==None:
            self.train()
        return self.X[0],self.D[0],self.R[0]
