from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import numpy as np

def model_evaluation(train_data, test_data):
    classifier = DecisionTreeClassifier(class_weight = 'balanced')
    classifier.fit(train_data[:, 1:-1].astype(int), train_data[:, -1].astype(int))
    predictions = classifier.predict(test_data[:, 1:-1].astype(int))
    #actual_labels = test_data[np.where(test_data[:, -1].astype(int) == 1)]
    actual_labels = test_data[:, -1].astype(int)
    mismatches = np.column_stack((np.column_stack((test_data[:,0], actual_labels)), predictions))
    false_positives = mismatches[np.where((mismatches[:, -1] == '1') & (mismatches[:, -2] == '0'))]
    print(false_positives)
    precision = metrics.precision_score(test_data[:, -1].astype(int), predictions)
    recall = metrics.recall_score(test_data[:, -1].astype(int), predictions)
    f1_score = metrics.f1_score(test_data[:, -1].astype(int), predictions)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1_score)