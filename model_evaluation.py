from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

def model_evaluation(train_data, test_data):
    classifier = DecisionTreeClassifier(class_weight = 'balanced')
    classifier.fit(train_data[:, 1:-1], train_data[:, -1])
    predictions = classifier.predict(test_data[:, 1:-1])
    precision = metrics.precision_score(test_data[:, -1], predictions)
    recall = metrics.recall_score(test_data[:, -1], predictions)
    f1_score = metrics.f1_score(test_data[:, -1], predictions)
    print(precision)
    print(recall)
    print(f1_score)