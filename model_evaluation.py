from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import numpy as np


def model_evaluation(train_data, test_data):
    # classifier = DecisionTreeClassifier(class_weight = 'balanced')
    # classifier = RandomForestClassifier(n_estimators=100)
    # classifier = svm.SVC(kernel='linear', C=1)
    classifier = LogisticRegression(solver='lbfgs')
    # classifier = LinearRegression()
    classifier.fit(train_data[:, 1:-1].astype(int), train_data[:, -1].astype(int))
    predictions = classifier.predict(test_data[:, 1:-1].astype(int))

    # # For linear regression model
    # predictions = abs(predictions)
    # linear_regression_threshold = 0.5
    # predictions = np.rint(predictions).astype(int)


    actual_labels = test_data[:, -1].astype(int)
    test_data_points = np.column_stack((np.column_stack((test_data[:,0], actual_labels)), predictions))
    false_positives = test_data_points[np.where((test_data_points[:, -1] == '1') & (test_data_points[:, -2] == '0'))]
    print(false_positives)
    precision = metrics.precision_score(test_data[:, -1].astype(int), predictions)
    recall = metrics.recall_score(test_data[:, -1].astype(int), predictions)
    f1_score = metrics.f1_score(test_data[:, -1].astype(int), predictions)

    print()
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1_score)
