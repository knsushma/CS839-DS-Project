import re
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.model_selection import cross_val_score
import itertools


def form_feature_set(words, entity_set):
    feature_frame = np.array([])
    for index, entity in enumerate(entity_set):
        feature_set = []

        #Check for previous word to be "in" or "at"
        if  index >= 1 and any(specific_word == words[index-1] for specific_word in ["in", "at", "near"]):
            feature_set.append(1)
        else:
            feature_set.append(0)

        #Check for next word exception
        if index < len(words)-1 and any(specific_word == words[index+1] for specific_word in ["University", "Police department"]):
            feature_set.append(0)
        else:
            feature_set.append(1)

        # More features to be added here
        # TODO

        if (feature_frame.shape[0] == 0):
            feature_frame = np.hstack((feature_frame, feature_set))
        else:
            feature_frame = np.vstack((feature_frame, feature_set))

    return feature_frame.astype(int)


def form_dataset_matrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity):
    data_frame = []
    for index in range(0,len(named_entity)):
        print([named_entity[index][1]] + positive_entity_feature_set[index].tolist() + [1])
        data_frame.append(([named_entity[index][1]] + positive_entity_feature_set[index].tolist() + [1]))

    for index in range(0,len(unnamed_entity)):
        data_frame.append(([unnamed_entity[index][1]] + negative_entity_feature_set[index].tolist() + [0]))

    data_frame = np.array(data_frame)
    # data_frame[:, [1,2,3]] = data_frame[:, [1,2,3]].astype(int)

    return data_frame


def predict_accuracy_on_diff_classifiers(data_set):
    print("Accuracy to be found using diff classifiers")
    cross_validation_fold = 3
    # 1. Decision Tree

    # 2. Random Forest

    # 3. Support Vector Machine
    svm_model = svm.SVC(kernel='linear', C=1)
    cross_validation_accuracy = cross_val_score(svm_model, data_set[:, 1:-1].astype(int),
                                                data_set[:, -1].astype(int), cv=cross_validation_fold)
    average_cross_validation_accuracy = np.mean(cross_validation_accuracy)
    print(average_cross_validation_accuracy)

    # 4. Linear Regression
    linear_regression_model = LinearRegression()
    # scikit-learn internally returns negative MSE for Linear Regression
    negative_mse = cross_val_score(linear_regression_model, data_set[:, 1:-1].astype(int),
                                   data_set[:, -1].astype(int), cv=cross_validation_fold)
    average_mse = -np.mean(negative_mse)
    average_accuracy = 1-average_mse
    print(average_accuracy)

    # 5. Logistic Regression
    logistic_regression_model = LogisticRegression(solver='lbfgs')
    cross_validation_accuracy = cross_val_score(logistic_regression_model, data_set[:, 1:-1].astype(int),
                                                data_set[:, -1].astype(int), cv=cross_validation_fold)
    average_cross_validation_accuracy = np.mean(cross_validation_accuracy)
    print(average_cross_validation_accuracy)


disposable_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
                    'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
                    'under',"about","upon","these","those","this","that","i","they","them"]


for file_prefix in range(101,102):

    filePath = "Data/Records/" + str(file_prefix) + ".txt"
    document = open(filePath, 'r')

    named_entity = []
    unnamed_entity = []

    complete_data = document.read()
    words = complete_data.split()
    words = [word.strip(" .,;:()") for word in words]
    for index, word in enumerate(words):
        if "location" in word:
            if word.count("location") == 2:
                location = re.sub('<[^>]*>', '', word)
                named_entity.append([index,location])
            else:
                labeled_data = complete_data[index:]
                matched_data = re.match('<[^>]*> [a-z A-Z\s*]*</[^>]*>', labeled_data)
                if matched_data:
                    named_entity.append(re.sub('<[^>]*>', '', matched_data[0]))
        else:
            # Reduce the unneccesary words, skip them from saving it in unnamed_entity
            if word[0].isupper() and word.lower() not in disposable_words and not (any(ch.isdigit() for ch in word)):
                unnamed_entity.append([index, word])

    positive_entity_feature_set = form_feature_set(words, named_entity)
    negative_entity_feature_set = form_feature_set(words, unnamed_entity)

    dataset = form_dataset_matrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity)
    print(dataset)
    predict_accuracy_on_diff_classifiers(dataset)
