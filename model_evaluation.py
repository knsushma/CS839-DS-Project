from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

def model_evaluation(train_data, test_data):
    classifier = DecisionTreeClassifier(class_weight = 'balanced')
    classifier.fit(train_data[:, 1:-1].astype(int), train_data[:, -1].astype(int))
    predictions = classifier.predict(test_data[:, 1:-1].astype(int))
    precision = metrics.precision_score(test_data[:, -1].astype(int), predictions)
    recall = metrics.recall_score(test_data[:, -1].astype(int), predictions)
    f1_score = metrics.f1_score(test_data[:, -1].astype(int), predictions)
    print(precision)
    print(recall)
    print(f1_score)