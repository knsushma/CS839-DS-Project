import re
import numpy as np


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

    return dataFrames


path = "Data/Records/101.txt"
F = open(path,'r')
named_entity = []
unnamed_entity = []

complete_data = F.read()
words = complete_data.split()
words = [word.strip(" .,;:()") for word in words]
for index, word in enumerate(words):
    if "location" in word:
        #try to take complete location info
        location = re.sub('<[^>]*>', '', word)
        named_entity.append([index,location])
    else:
        # Reduce the unneccesary words, skip them from saving it in unnamed_entity
        unnamed_entity.append([index, word])

positive_entity_feature_set = formFeatureSet(words, named_entity)
negative_entity_feature_set = formFeatureSet(words, unnamed_entity)

dataSet = formDataSetMatrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity)
print(dataSet)





