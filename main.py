from named_entity_extraction import form_feature_dataframe
from model_training import predict_accuracy_on_diff_classifiers
from model_evaluation import model_evaluation

import os


training_files = os.listdir("Data/I")
test_files = os.listdir("Data/J")

training_dataframe = form_feature_dataframe("Data/I/", training_files)
test_dataframe = form_feature_dataframe("Data/J/", test_files)


predict_accuracy_on_diff_classifiers(training_dataframe)
model_evaluation(training_dataframe, test_dataframe)