import pickle
from sklearn import metrics

with open("test-trained-model.pickle", 'rb') as f:
    model = pickle.load(f)
    predicted = model.predict(train_test["X_test_np"])
    print(metrics.classification_report(train_test["y_test_np"], predicted))
    print(metrics.confusion_matrix(train_test["y_test_np"], predicted))