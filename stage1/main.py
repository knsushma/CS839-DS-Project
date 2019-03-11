from stage1.named_entity_extraction import form_feature_dataframe
from stage1.model_training import predict_accuracy_on_diff_classifiers
from stage1.model_evaluation import model_evaluation
import glob


def named_entity_extraciton_on_train_test_dataset():

    #files =  os.listdir("dataset/trainig_dataset/")
    print("Information Extraction using training and test dataset", "\n")
    training_files = glob.glob("./dataset/training_dataset/*.txt")
    test_files = glob.glob("./dataset/test_dataset/*.txt")

    training_dataframe = form_feature_dataframe(training_files)
    test_dataframe = form_feature_dataframe(test_files)

    # print("Traning dataset labelled entities: ", training_dataframe[numpy.where(training_dataframe[:, -1] == '1')].shape[0])
    # print("Test dataset labelled entities: ", test_dataframe[numpy.where(test_dataframe[:, -1] == '1')].shape[0])

    predict_accuracy_on_diff_classifiers(training_dataframe)
    model_evaluation(training_dataframe, test_dataframe)


# Used for fixing feature extraction rules on traning dataset (spliting traing dataset into P & Q dataset)
def named_entity_extraciton_on_training_dataset():
    print("Information Extraction using only training dataset", "\n")
    training_files = glob.glob("./dataset/P/*.txt")
    test_files = glob.glob("./dataset/Q/*.txt")

    training_dataframe = form_feature_dataframe(training_files)
    test_dataframe = form_feature_dataframe(test_files)

    predict_accuracy_on_diff_classifiers(training_dataframe)
    model_evaluation(training_dataframe, test_dataframe)


if __name__ == '__main__':
    named_entity_extraciton_on_train_test_dataset()
    #named_entity_extraciton_on_training_dataset()

