import re
import numpy as np

neg_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
                'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
                'under',"about","upon","these","those","this","that","i","they","them","january","february", "march",
                "april", "may", "june", "july", "august", "september", "october", "november", "december", "monday",
                "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# previous positive words
prev_pos_words = ["in", "at", "near", "to", "from", "country of origin"]
# case independent previous positive words
# prev_pos_ci_words = ["east", "eastern", "west", "western", "south", "southern", "north", "northern"]
# post positive words
post_pos_words = ["City", "County"]
# case independent post positive words
post_pos_ci_words = []

# previous negative words
prev_neg_words = ["University of", "College of"]
# case independent previous negative words
prev_neg_ci_words = []
# post negative words
post_neg_words = ["University", "Police department"]
# case independent post negative words
post_neg_ci_words = []


def formFeatureSet(words, entitySet):
    featureFrame = np.array([])
    for index, entity in enumerate(entitySet):
        featureSet = []

        # Skip the word in these scenarios:
        # Place name is always capitalized. If the first character is lower case
        # if the word is in negative words
        # if the word ends with 'an'.
        # TODO - Need to whitelist places ending with 'an'
        if words[index][0].islower() or words[index].lower() in neg_words or words[index][-2:] == 'an':
            continue

        #Check for previous positive word
        if  index > 0 and any(word.split(" ") == words[index-len(word.split(" ")):index] \
                                                                        for word in prev_pos_words):
            featureSet.append(1)
        else:
            featureSet.append(0)

        #Check for previous positive word
#        if  index > 0 and any(word.split(" ") == words[index-len(word.split(" ")):index].lower() \
#                                                                        for word in prev_pos_ci_words):
#            featureSet.append(1)
#        else:
#            featureSet.append(0)

        # Check for post positive word
        if index < len(words)-1 and \
            any(word.split(" ") == words[index+1:index+len(word.split(" "))+1] for word in post_pos_words):
            featureSet.append(1)
        else:
            featureSet.append(0)

        # Check for prev and post positive word - TODO

        #Check for previous negative word exception
        if index > 0 and \
            any(word.split(" ") == words[index-len(word.split(" ")):index] for word in post_neg_words):
            featureSet.append(0)
        else:
            featureSet.append(1)

        #Check for post negative word exception
        if index < len(words)-1 and \
            any(word.split(" ") == words[index+1:index+len(word.split(" "))+1] for word in post_neg_words):
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

    return dataFrames


def predict_accuracy_on_diff_classifiers(dataset):
    print("Accuracy to be found using diff classifiers")
    # TODO


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

dataset = formDataSetMatrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity)
predict_accuracy_on_diff_classifiers(dataset)





