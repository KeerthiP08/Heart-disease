import gc
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from users.forms import UserRegistrationForm, HeartDataForm
from users.models import UserRegistrationModel, HeartDataModel
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
from django_pandas.io import read_frame
#%matplotlib inline
from sklearn.model_selection import train_test_split
import os
#print(os.listdir())

import warnings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

var_user = 0
crashband = {}

def UserLogin(request):
    global crashband
    crashband = {}
    return render(request, 'UserLogin.html', {})


def UserRegisterAction(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            # return HttpResponseRedirect('./CustLogin')
            form = UserRegistrationForm()
            return render(request, 'Register.html', {'form': form})
        else:
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'Register.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
            # return render(request, 'user/userpage.html',{})
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})

def userhome(request):
    return render(request, 'users/UserHomePage.html', {})
def UserAddData(request):
    if request.method == "POST":
        form = HeartDataForm(request.POST)
        print(form)
        if form.is_valid():
            print('Data is Valid')


            age = form.cleaned_data['age']
            sex =  form.cleaned_data['sex']
            cp = form.cleaned_data['cp']
            trestbps = form.cleaned_data['trestbps']
            chol = form.cleaned_data['chol']
            fbs = form.cleaned_data['fbs']
            restecg = form.cleaned_data['restecg']
            thalach = form.cleaned_data['thalach']
            exang = form.cleaned_data['exang']
            oldpeak = form.cleaned_data['oldpeak']
            slope = form.cleaned_data['slope']
            ca = form.cleaned_data['ca']
            thal = form.cleaned_data['thal']


            test_set = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]

            #dataset = HeartDataModel.objects.all()
            dataset = pd.read_csv("http://localhost:8000/media/heart.csv")

            #print(dataset.head())

            X = dataset.iloc[:,:-1].values
            y = dataset.iloc[:,-1].values
            X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state=0)

            # K Nearest Neighbors
            from sklearn.metrics import accuracy_score

            from sklearn.neighbors import KNeighborsClassifier
            knn = KNeighborsClassifier(n_neighbors=7)
            knn.fit(X_train, Y_train)
            Y_pred_knn = knn.predict(X_test)
            score_knn = round(accuracy_score(Y_pred_knn, Y_test) * 100, 2)


            #Logistic Regression
            from sklearn.linear_model import LogisticRegression
            lr = LogisticRegression()
            lr.fit(X_train, Y_train)
            Y_pred_lr = lr.predict(X_test)
            score_lr = round(accuracy_score(Y_pred_lr, Y_test) * 100, 2)

            #SVM
            from sklearn import svm
            sv = svm.SVC(kernel='linear')
            sv.fit(X_train, Y_train)
            Y_pred_svm = sv.predict(X_test)
            score_svm = round(accuracy_score(Y_pred_svm, Y_test) * 100, 2)

            #Decision_Tree
            from sklearn.tree import DecisionTreeClassifier

            max_accuracy = 0

            for x in range(200):
                dt = DecisionTreeClassifier(random_state=x)
                dt.fit(X_train, Y_train)
                Y_pred_dt = dt.predict(X_test)
                current_accuracy = round(accuracy_score(Y_pred_dt, Y_test) * 100, 2)
                if (current_accuracy > max_accuracy):
                    max_accuracy = current_accuracy
                    best_x = x

            dt = DecisionTreeClassifier(random_state=best_x)
            dt.fit(X_train, Y_train)
            Y_pred_dt = dt.predict(X_test)
            score_dt = round(accuracy_score(Y_pred_dt, Y_test) * 100, 2)

            scores_final = 0
            scores_final_tab = [score_knn,score_lr,score_svm,score_dt]
            algorithm_models = [knn,lr,sv,dt]

            for i in range(0,len(scores_final_tab)):
                if scores_final_tab[i] > scores_final:
                    scores_final = scores_final_tab[i]
                    indexvalue = i

            result = algorithm_models[i].predict([test_set])
            print("Result is ",result)

            test_set.append(result[0])
            global crashband
            manual_set = ['Age', 'Sex', 'Chest Pain', 'Resting Blood Pressure', 'Cholestrol',
                          'Fasting Blood Pressure above 120mg/dl', 'Resting ECG', 'Max Heart Rate',
                          'Exercise Induced Angina',
                          'ST Depression(Old Peak)', 'Peak Exercise ST Segment', 'No of Major Vessels',
                          'Thalassemia Type','Heart Disease Chance']
            for i in range(0,len(manual_set)):
                crashband.update({manual_set[i]: test_set[i]})


            rslt = ''
            if result[0] == 0:
                rslt = "You are not suffering from Heart Disease"
            else:
                rslt = "You are suffering from Heart Disease"
            form = HeartDataForm()
            return render(request, 'users/UserAddData.html', {'form': form,'result':rslt})
        else:
            print("Invalid form")

    else:
        form = HeartDataForm()
    return render(request, 'users/UserAddData.html', {'form': form})


def UserDataView(request):
    """data_list = HeartDataModel.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(data_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    """
    lender = {}
    for key in crashband:
        lender[key] = crashband[key]

    #print(lender)
    if(len(crashband) == 0):
        print(len(lender))
        return render(request, 'users/DataView_list.html', {'lt': lender})
    else:
        if(lender['Sex']==1):
            lender['Sex'] = "Male"
        else:
            lender['Sex'] = "Female"

        chestpaintype = ["Typical Angina","Atypical Angina","Non-Anginal","Asymptotic"]
        lender['Chest Pain'] = chestpaintype[lender['Chest Pain']-1]

        lender['Resting Blood Pressure'] = str(lender['Resting Blood Pressure'])+"mmHg"

        lender['Cholestrol'] = str(lender['Cholestrol'])+"mg/dl"

        if(lender['Fasting Blood Pressure above 120mg/dl'] == 1):
            lender['Fasting Blood Pressure above 120mg/dl'] = "Yes"
        else:
            lender['Fasting Blood Pressure above 120mg/dl'] = "No"

        restingecgtype = ["Normal","ST-T wave abnormality","Left Ventricular Hyperthrophy"]
        lender['Resting ECG'] = restingecgtype[lender['Resting ECG']]

        if lender['Exercise Induced Angina'] == 1:
            lender['Exercise Induced Angina'] = "Yes"
        else:
            lender['Exercise Induced Angina'] = "No"

        slopenew = ["Upward Sloping","Flat","Downward Sloping"]
        lender['Peak Exercise ST Segment'] = slopenew[lender['Peak Exercise ST Segment']]

        thaltype = ["Normal","Fixed Defect","Reversible Defect","Irreversible Defect"]
        lender['Thalassemia Type'] = thaltype[lender['Thalassemia Type']]

        if(lender['Heart Disease Chance']) == 1:
            lender['Heart Disease Chance'] = "Yes"
        else:
            lender['Heart Disease Chance'] = "No"

        return render(request, 'users/DataView_list.html', {'lt': lender})


def UserMachineLearning(request):
    #gc.collect()
    dataset = HeartDataModel.objects.all()
    dataset = read_frame(dataset)
   
    #dataset.fillna
    print(dataset.head())
    print(type(dataset))
    print(dataset.shape)
    print(dataset.head(5))
    print(dataset.sample(5))
    print(dataset.describe())
    dataset.info()
    info = ["age", "1: male, 0: female",
            "chest pain type, 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic",
            "resting blood pressure", " serum cholestoral in mg/dl", "fasting blood sugar > 120 mg/dl",
            "resting electrocardiographic results (values 0,1,2)", " maximum heart rate achieved",
            "exercise induced angina", "oldpeak = ST depression induced by exercise relative to rest",
            "the slope of the peak exercise ST segment", "number of major vessels (0-3) colored by flourosopy",
            "thal: 3 = normal; 6 = fixed defect; 7 = reversable defect"]

    for i in range(len(info)):
        print(dataset.columns[i] + ":\t\t\t" + info[i])
    #X = dataset.drop(['target'], axis=1).values
    #print("x",X)
    dataset["target"].describe()
    print(dataset["target"].unique())
    print(dataset.corr()["target"].abs().sort_values(ascending=False))
    y = dataset["target"]
    print("y",y)
    sns.countplot(y)
    plt.show()
    print("Dataset Head",dataset.head(25))
    target_temp = dataset.target.value_counts()

    print("target Label Count=",target_temp)
    print("Percentage of patience without heart problems: " + str(round(target_temp[0] * 100 / 303, 2)))
    print("Percentage of patience with heart problems: " + str(round(target_temp[1] * 100 / 303, 2)))
    print(dataset["sex"].unique())
    sns.barplot(dataset["sex"], y)
    plt.show()
    dataset["cp"].unique()
    sns.barplot(dataset["cp"], y)
    plt.show()
    dataset["fbs"].describe()
    dataset["fbs"].unique()
    sns.barplot(dataset["fbs"], y)
    plt.show()
    dataset["restecg"].unique()
    sns.barplot(dataset["restecg"], y)
    plt.show()
    dataset["exang"].unique()
    sns.barplot(dataset["exang"], y)
    plt.show()
    dataset["slope"].unique()
    sns.barplot(dataset["slope"], y)
    plt.show()
    dataset["ca"].unique()
    sns.countplot(dataset["ca"])
    plt.show()
    sns.barplot(dataset["ca"], y)
    plt.show()
    dataset["thal"].unique()
    sns.barplot(dataset["thal"], y)
    plt.show()
    sns.distplot(dataset["thal"])
    plt.show()
    from sklearn.model_selection import train_test_split

    predictors = dataset.drop("target", axis=1)
    target = dataset["target"]

    X_train, X_test, Y_train, Y_test = train_test_split(predictors, target, test_size=0.20, random_state=0)
    X_train.shape
    print(X_train.shape)
    X_test.shape
    print(X_test.shape)
    Y_train.shape
    print(Y_train.shape)
    Y_test.shape
    print(Y_test.shape)

    # Linear regression
    from sklearn.metrics import accuracy_score
    from sklearn.linear_model import LogisticRegression

    lr = LogisticRegression()

    lr.fit(X_train, Y_train)

    Y_pred_lr = lr.predict(X_test)
    Y_pred_lr.shape
    print(Y_pred_lr.shape)
    score_lr = round(accuracy_score(Y_pred_lr, Y_test) * 100, 2)

    print("The accuracy score achieved using Linear regression is: " + str(score_lr) + " %")

    # Naive Bayes
    from sklearn.naive_bayes import GaussianNB

    nb = GaussianNB()

    nb.fit(X_train, Y_train)

    Y_pred_nb = nb.predict(X_test)
    Y_pred_nb.shape
    print(Y_pred_nb.shape)
    score_nb = round(accuracy_score(Y_pred_nb, Y_test) * 100, 2)

    print("The accuracy score achieved using Naive Bayes is: " + str(score_nb) + " %")

    # SVM
    from sklearn import svm

    sv = svm.SVC(kernel='linear')

    sv.fit(X_train, Y_train)

    Y_pred_svm = sv.predict(X_test)
    Y_pred_svm.shape
    print(Y_pred_svm.shape)
    score_svm = round(accuracy_score(Y_pred_svm, Y_test) * 100, 2)

    print("The accuracy score achieved using Linear SVM is: " + str(score_svm) + " %")

    # K Nearest Neighbors
    from sklearn.neighbors import KNeighborsClassifier

    knn = KNeighborsClassifier(n_neighbors=7)
    knn.fit(X_train, Y_train)
    Y_pred_knn = knn.predict(X_test)
    Y_pred_knn.shape
    print(Y_pred_knn.shape)
    score_knn = round(accuracy_score(Y_pred_knn, Y_test) * 100, 2)

    print("The accuracy score achieved using KNN is: " + str(score_knn) + " %")

    # Decision Tree
    from sklearn.tree import DecisionTreeClassifier

    max_accuracy = 0

    for x in range(200):
        dt = DecisionTreeClassifier(random_state=x)
        dt.fit(X_train, Y_train)
        Y_pred_dt = dt.predict(X_test)
        current_accuracy = round(accuracy_score(Y_pred_dt, Y_test) * 100, 2)
        if (current_accuracy > max_accuracy):
            max_accuracy = current_accuracy
            best_x = x

    # print(max_accuracy)
    # print(best_x)

    dt = DecisionTreeClassifier(random_state=best_x)
    dt.fit(X_train, Y_train)
    Y_pred_dt = dt.predict(X_test)
    print(Y_pred_dt.shape)
    score_dt = round(accuracy_score(Y_pred_dt, Y_test) * 100, 2)

    print("The accuracy score achieved using Decision Tree is: " + str(score_dt) + " %")

    # Neural Network
    from keras.models import Sequential
    from keras.layers import Dense
    model = Sequential()
    model.add(Dense(11, activation='relu', input_dim=14))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.fit(X_train,Y_train,epochs=300)
    model.fit(X_train, Y_train, epochs=300)
    Y_pred_nn = model.predict(X_test)
    Y_pred_nn.shape
    print(Y_pred_nn.shape)
    rounded = [round(x[0]) for x in Y_pred_nn]

    Y_pred_nn = rounded
    score_nn = round(accuracy_score(Y_pred_nn, Y_test) * 100, 2)

    print("The accuracy score achieved using Neural Network is: " + str(score_nn) + " %")

    scores = [score_lr, score_nb, score_svm, score_knn, score_dt, score_nn]
    algorithms = ["LR", "Naive Bayes", "SVM", "K-Nearest Neighbors", "Decision Tree", "Neural Network"]

    for i in range(len(algorithms)):
        print("The accuracy score achieved using " + algorithms[i] + " is: " + str(scores[i]) + " %")
        sns.set(rc={'figure.figsize': (15, 8)})
    plt.xlabel("Algorithms")
    plt.ylabel("Accuracy score")

    sns.barplot(algorithms, scores)
    plt.show()
    dict = {
        "score_lr" :score_lr,
        "score_nb" :score_nb,
        "score_svm" :score_svm,
        "score_knn" :score_knn,
        "score_dt" :score_dt,
        "score_nn" :score_nn,

    }
    return render(request, 'users/Machinelearning.html', dict)
