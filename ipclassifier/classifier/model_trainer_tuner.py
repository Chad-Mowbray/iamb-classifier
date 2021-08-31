from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import ComplementNB


def tune_params(train_test, m=ComplementNB):
    parameters = [
    {'alpha': [1,1.5,2, 2.5,3,4]},
    ]

    model = m()
    clf = GridSearchCV(model, parameters)
    clf.fit(train_test["X_train_np"], train_test["y_train_np"])
    print(clf.best_params_)