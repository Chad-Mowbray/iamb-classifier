from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import svm
from sklearn.neural_network import MLPClassifier
import pickle
from sklearn import metrics
import os



def tune_params(train_test=None, m=ComplementNB):
    parameters = [
    {'alpha': [.01,.1,.5,1,1.5,2, 2.5,3,4]},
    ]
    filepath = os.path.join(os.path.dirname(__file__), "train_test_data.pickle")
    for m in [ComplementNB,GaussianNB,MultinomialNB,RandomForestClassifier,GradientBoostingClassifier]:
        with open(filepath, "rb") as f:
            train_test = pickle.load(f)

        model = m()
        if m in [GaussianNB,RandomForestClassifier, GradientBoostingClassifier]:
            clf = model
            clf.fit(train_test["X_train_np"], train_test["y_train_np"])
        else:
            clf = GridSearchCV(model, parameters)
            clf.fit(train_test["X_train_np"], train_test["y_train_np"])
            print(clf.best_params_)
        
        with open(f"{m.__name__}-test-model.pickle", 'wb') as f:
            pickle.dump(clf, f)

        predicted = clf.predict(train_test["X_test_np"])
        print(metrics.classification_report(train_test["y_test_np"], predicted))
        print(metrics.confusion_matrix(train_test["y_test_np"], predicted))
        print(metrics.accuracy_score(train_test["y_test_np"], predicted))
        print("Accuracy on training set: {:.3f}".format(clf.score(train_test["X_train_np"], train_test["y_train_np"])))
        print("Accuracy on test set: {:.3f}".format(clf.score(train_test["X_test_np"], train_test["y_test_np"])))
        print("*"*80)