#!/usr/bin/env python3
"""
The purpose of ml.py is to quickly spin up supervised machine learning algorithms for faster training and tuning.

:: Functions ::
    run_ml(df=None,target=None,type=None,ts=0.2,rs=1,hyper=False)
        - df: The dataframe that is cleaned and ready for machine learning
        - target: The target variable in the dataframe
        - type: 'c' or 'r'. Denotes whether you want to run classification or regression models on the data
        - ts: The train_test_split test size
        - rs: The random state
        - In development: hyper: Boolean. If you want the function to perform hyperparameter tuning, set to True. Default is False
    #Examples: run_ml(iris,'target','c'), run_ml(wine,'target','c'), run_ml(boston,'target','r'), run_ml(diab,'target','r')  

Author(s): Dan Blevins
"""

#import training, pipeline, metrics, etc.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import auc, mean_squared_error, r2_score, accuracy_score, log_loss, classification_report

#import algos
from sklearn.linear_model import LogisticRegression, LinearRegression, ElasticNet
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

#import test data if desired
from sklearn.datasets import load_iris, load_boston, load_wine, load_diabetes
iris = load_iris()
boston = load_boston()
wine = load_wine()
diab = load_diabetes()
#classification test data
iris = pd.DataFrame(np.c_[iris['data'], iris['target']],
                    columns= np.append(iris['feature_names'], ['target']))
wine = pd.DataFrame(np.c_[wine['data'], wine['target']],
                    columns= np.append(wine['feature_names'], ['target']))  
#regression test data
boston = pd.DataFrame(np.c_[boston['data'], boston['target']],
                    columns= np.append(boston['feature_names'], ['target']))                                      
diab = pd.DataFrame(np.c_[diab['data'], diab['target']],
                    columns= np.append(diab['feature_names'], ['target']))                    


def run_ml(df=None,target=None,type=None,ts=0.2,rs=1,hyper=False):
    X = df.drop(target,axis=1)
    y = df.target

    classifiers = [
    KNeighborsClassifier(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    GradientBoostingClassifier(),
    MultinomialNB(),
    GaussianNB()]

    regressors = [
    KNeighborsRegressor(),
    LinearRegression(),
    ElasticNet(),
    RandomForestRegressor(),
    GradientBoostingRegressor(),
    DecisionTreeRegressor()]

    #This function scores the desired machine learning algorithm.
    if type == 'c':
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts,random_state=rs,stratify=y)
        
        for clf in classifiers:
            if hyper == False:
                #pipeline = make_pipeline(preprocessing.StandardScaler(), clf)
                clf.fit(X_train, y_train)
                print("="*30)
                print(clf)
                print('##### Results #####')
                
                pred = clf.predict(X_test)
                acc = accuracy_score(y_test, pred)
                print("Accuracy: {:.4%}".format(acc))
                pred = clf.predict_proba(X_test)
                ll = log_loss(y_test, pred)
                print("Log Loss: {}".format(ll))

            elif hyper == True:
                print("="*30)
                print(clf)
                print('##### Results #####')
                if str(clf) == 'KNeighborsClassifier()':
                    leaf_size = list(range(1,10))
                    n_neighbors = list(range(1,10))
                    p=[1,2]
                    hyperparameters = dict(leaf_size=leaf_size, n_neighbors=n_neighbors, p=p)
                    clf = GridSearchCV(clf, hyperparameters, cv=10)
                    best_model = clf.fit(X_train, y_train)
                    print('Best leaf_size:', best_model.best_estimator_.get_params()['leaf_size'])
                    print('Best p:', best_model.best_estimator_.get_params()['p'])
                    print('Best n_neighbors:', best_model.best_estimator_.get_params()['n_neighbors'])
        print("="*30)

    elif type == 'r':
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts,random_state=rs)
        
        for reg in regressors:
            reg.fit(X_train, y_train)
            print("="*30)
            print(reg)
            print('##### Results #####')
            
            pred = reg.predict(X_test)
            rr = r2_score(y_test, pred)
            mse = mean_squared_error(y_test, pred)
            print("R2: {:.4%}".format(rr))
            print("MSE: {:.4%}".format(mse))
        print("="*30)

    else:
        print("In the 'run_ml' function please have type=c or type=r.")