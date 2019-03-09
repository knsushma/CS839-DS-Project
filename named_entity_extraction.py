import re
from feature_extraction import *
from model_training import *
from itertools import islice


def form_dataset_matrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity):
    data_frame = []
    for index in range(0,len(named_entity)):
        data_frame.append(([named_entity[index][1]] + positive_entity_feature_set[index] + [1]))
    for index in range(0,len(unnamed_entity)):
        data_frame.append(([unnamed_entity[index][1]] + negative_entity_feature_set[index] + [0]))
    #data_frame = np.array(data_frame)

    return data_frame

disposable_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
                    'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
                    'under',"about","upon","these","those","this","that","i","they","them"]


training_dataframe = []
for file_prefix in range(101,230):

    filePath = "Data/Records/" + str(file_prefix) + ".txt"
    document = open(filePath, 'r')

    named_entity = []
    unnamed_entity = []

    complete_data = document.read()
    words = complete_data.split()
    words = [word.strip(" .,;:()") for word in words]
    iter_words = iter(enumerate(words))
    for index, word in iter_words:
        if "location" in word:
            if word.count("location") == 2:
                location = re.sub('<[^>]*>', '', word)
                named_entity.append([index,location])
            else:
                labeled_data = " ".join(words[index:])
                matched_data = re.match('<[^>]*>[a-z A-Z\s*]*</[^>]*>', labeled_data)
                if matched_data:
                    named_entity.append([index, re.sub('<[^>]*>', '', matched_data[0])])
                    len_of_word_matched = len(matched_data[0].split(" "))
                    next(islice(iter_words, len_of_word_matched-1, len_of_word_matched-1), None)
        else:
            # Reduce the unneccesary words, skip them from saving it in unnamed_entity
            if word and word[0].isupper() and word.lower() not in disposable_words and not (any(ch.isdigit() for ch in word)):
                unnamed_entity.append([index, word])

    positive_entity_feature_set = extract_feature_set(words, named_entity)
    negative_entity_feature_set = extract_feature_set(words, unnamed_entity)

    dataset = form_dataset_matrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity)
    training_dataframe.extend(dataset)
    print(np.array(dataset))
check = np.array(training_dataframe)
print(check[np.where(check[:,-1] == '1')])
predict_accuracy_on_diff_classifiers(np.array(training_dataframe))

