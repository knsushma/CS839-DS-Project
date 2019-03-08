import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.model_selection import cross_val_score

def predict_accuracy_on_diff_classifiers(data_set):
    print("Accuracy to be found using diff classifiers")
    cross_validation_fold = 3
    # 1. Decision Tree

    # 2. Random Forest

    # 3. Support Vector Machine
    svm_model = svm.SVC(kernel='linear', C=1)
    cross_validation_accuracy = cross_val_score(svm_model, data_set[:, 1:-1].astype(int), data_set[:, -1].astype(int), cv=cross_validation_fold)
    average_cross_validation_accuracy = np.mean(cross_validation_accuracy)
    print(average_cross_validation_accuracy)

    # 4. Linear Regression
    linear_regression_model = LinearRegression()
    # scikit-learn internally returns negative MSE for Linear Regression
    negative_mse = cross_val_score(linear_regression_model, data_set[:, 1:-1].astype(int), data_set[:, -1].astype(int), cv=cross_validation_fold)
    average_mse = -np.mean(negative_mse)
    average_accuracy = 1-average_mse
    print(average_accuracy)

    # 5. Logistic Regression
    logistic_regression_model = LogisticRegression(solver='lbfgs')
    cross_validation_accuracy = cross_val_score(logistic_regression_model, data_set[:, 1:-1].astype(int),
                                                data_set[:, -1].astype(int), cv=cross_validation_fold)
    average_cross_validation_accuracy = np.mean(cross_validation_accuracy)
    print(average_cross_validation_accuracy)

