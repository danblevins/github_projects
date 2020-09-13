from flask import Flask, redirect, url_for, render_template, request, json
import pandas as pd
import numpy as np

##SKLearn
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import auc, mean_squared_error, r2_score, accuracy_score, log_loss, classification_report
from sklearn.linear_model import LogisticRegression, LinearRegression, ElasticNet
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

def run_ml(df=None,target=None,type=None,ts=0.2,rs=1,hyper=False):
    if df == 'iris':
        from sklearn.datasets import load_iris
        df = load_iris()
    elif df == 'wine':
        from sklearn.datasets import load_wine
        df = load_wine()
    elif df == 'boston':
        from sklearn.datasets import load_boston
        df = load_boston()
    else:
        from sklearn.datasets import load_diabetes
        df = load_diabetes()

    df = pd.DataFrame(np.c_[df['data'], df['target']],
                columns= np.append(df['feature_names'], ['target']))
    X = df.drop(target,axis=1)
    y = df.target
    result = []

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
        
        for mdl in classifiers:
            temp_result = {}
            if hyper == False:
                mdl.fit(X_train, y_train)
                temp_result['model'] = str(mdl).replace('()','')
                
                pred = mdl.predict(X_test)
                acc = round(accuracy_score(y_test, pred)*100,2)
                temp_result['accuracy'] = acc
                pred = mdl.predict_proba(X_test)
                ll = round(log_loss(y_test, pred),2)
                temp_result['log loss'] = ll

            elif hyper == True:
                if str(mdl) == 'KNeighborsClassifier()':
                    leaf_size = list(range(1,10))
                    n_neighbors = list(range(1,10))
                    p=[1,2]
                    hyperparameters = dict(leaf_size=leaf_size, n_neighbors=n_neighbors, p=p)
                    mdl = GridSearchCV(mdl, hyperparameters, cv=10)
                    best_model = mdl.fit(X_train, y_train)
            result.append(temp_result)

    elif type == 'r':
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts,random_state=rs)
        
        for mdl in regressors:
            temp_result = {}
            if hyper == False:
                mdl.fit(X_train, y_train)
                temp_result['model'] = str(mdl).replace('()','')
                
                pred = mdl.predict(X_test)
                rr = round(r2_score(y_test, pred),2)
                mse = round(mean_squared_error(y_test, pred),2)
                acc = rr
                ll = mse
                temp_result['RR'] = acc
                temp_result['MSE'] = ll

            elif hyper == True:
                if str(mdl) == 'KNeighborsClassifier()':
                    leaf_size = list(range(1,10))
                    n_neighbors = list(range(1,10))
                    p=[1,2]
                    hyperparameters = dict(leaf_size=leaf_size, n_neighbors=n_neighbors, p=p)
                    mdl = GridSearchCV(mdl, hyperparameters, cv=10)
                    best_model = mdl.fit(X_train, y_train)
            result.append(temp_result)

    else:
        print("In the 'run_ml' function please have type=c or type=r.")

    return result, mdl, acc, ll

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

### Web Pages ###
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classification", methods=["GET", "POST"])
def classif():
    result=''
    mdl=''
    acc=''
    ll=''
    if request.method == 'POST':
        if 'Run Iris' in request.form['run']:
            result, mdl, acc, ll = run_ml('iris','target','c')
        elif 'Run Wine' in request.form['run']:
            result, mdl, acc, ll = run_ml('wine','target','c')
        else:
            pass
    else:
        pass
    return render_template("class.html", result=result, mdl=mdl, acc=acc, ll=ll)

@app.route("/regression", methods=["GET", "POST"])
def reg():
    result=''
    mdl=''
    rr=''
    mse=''
    if request.method == 'POST':
        if 'Run Boston' in request.form['run']:
            result, mdl, rr, mse = run_ml('boston','target','r')
        elif 'Run Diabetes' in request.form['run']:
            result, mdl, rr, mse = run_ml('diabetes','target','r')
        else:
            pass
    else:
        pass
    return render_template("reg.html", result=result, mdl=mdl, rr=rr, mse=mse)

@app.route("/nlp")
def nlp():
    return render_template("nlp.html")

if __name__ == '__main__':
    app.run(debug=False)
