from named_entity_extraction import form_feature_dataframe
from model_training import predict_accuracy_on_diff_classifiers
from model_evaluation import model_evaluation

import glob


def data_extraciton_on_I_J_dataset():
    training_files = glob.glob("Data/I/*.txt")
    test_files = glob.glob("Data/J/*.txt")

    training_dataframe = form_feature_dataframe(training_files)
    test_dataframe = form_feature_dataframe(test_files)

    predict_accuracy_on_diff_classifiers(training_dataframe)
    #model_evaluation(training_dataframe, test_dataframe)


def data_extraciton_on_P_Q_dataset():
    training_files = glob.glob("Data/P/*.txt")
    test_files = glob.glob("Data/Q/*.txt")

    training_dataframe = form_feature_dataframe(training_files)
    test_dataframe = form_feature_dataframe(test_files)

    predict_accuracy_on_diff_classifiers(training_dataframe)
    model_evaluation(training_dataframe, test_dataframe)


if __name__ == '__main__':
    data_extraciton_on_P_Q_dataset()