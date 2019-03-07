import re
import numpy as np
import string


def formFeatureSet(words, entitySet):
    featureFrame = np.array([])
    for index, entity in enumerate(entitySet):
        featureSet = []

        #Check for previous word to be "in" or "at"
        if  index >= 1 and any(specificWord == words[index-1] for specificWord in ["in", "at", "near"]):
            featureSet.append(1)
        else:
            featureSet.append(0)

        #Check for next word exception
        if index < len(words)-1 and any(specificWord == words[index+1] for specificWord in ["University", "Police department"]):
            featureSet.append(0)
        else:
            featureSet.append(1)

        # More features to be added here
        # TODO

        if (featureFrame.shape[0] == 0):
            featureFrame = np.hstack((featureFrame, featureSet))
        else:
            featureFrame = np.vstack((featureFrame, featureSet))

    return featureFrame.astype(int)


def formDataSetMatrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity):
    dataFrames = []
    for index in range(0,len(named_entity)):
        dataFrames.append([named_entity[index][1]] + positive_entity_feature_set[index].tolist() + [1])

    for index in range(0,len(unnamed_entity)):
        dataFrames.append([unnamed_entity[index][1]] + negative_entity_feature_set[index].tolist() + [0])

    dataFrames = np.array(dataFrames)
    # dataFrames[:, [1,2,3]] = dataFrames[:, [1,2,3]].astype(int)

    return dataFrames


def predict_accuracy_on_diff_classifiers(dataset):
    print("Accuracy to be found using diff classifiers")
    # TODO


disposable_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
                    'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
                    'under',"about","upon","these","those","this","that","i","they","them"]


for file_prefix in range(101,111):

    filePath = "Data/Records/" + str(file_prefix) + ".txt"
    document = open(filePath, 'r')

    named_entity = []
    unnamed_entity = []

    complete_data = document.read()
    words = complete_data.split()
    words = [word.strip(" .,;:()") for word in words]
    for index, word in enumerate(words):
        if "location" in word:
            if word.count(word) == 2:
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

    positive_entity_feature_set = formFeatureSet(words, named_entity)
    negative_entity_feature_set = formFeatureSet(words, unnamed_entity)

    dataset = formDataSetMatrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity)
    print(dataset)
    predict_accuracy_on_diff_classifiers(dataset)





