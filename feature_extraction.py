import numpy as np

neg_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
                'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
                'under',"about","upon","these","those","this","that","i","they","them","january","february", "march",
                "april", "may", "june", "july", "august", "september", "october", "november", "december", "monday",
                "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# previous positive words
prev_pos_words = ["in", "at", "near", "to", "from", "country of origin", "across"]
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

def extract_feature_set(words, entity_set):
    feature_frame = []
    for index, entity in enumerate(entity_set):
        feature_set = []

        # Skip the word in these scenarios:
        # Place name is always capitalized. If the first character is lower case
        # if the word is in negative words
        # if the word ends with 'an'.
        # TODO - Need to whitelist places ending with 'an'
        # if words[index][0].islower() or words[index].lower() in neg_words or words[index][-2:] == 'an':
        #     continue

        #Check for previous positive word
        if  index > 0 and any(word.split(" ") == words[index-len(word.split(" ")):index] for word in prev_pos_words):
            feature_set.append(1)
        else:
            feature_set.append(0)

        #Check for previous positive word
#        if  index > 0 and any(word.split(" ") == words[index-len(word.split(" ")):index].lower() \
#                                                                        for word in prev_pos_ci_words):
#            featureSet.append(1)
#        else:
#            featureSet.append(0)

        # Check for post positive word
        if index < len(words)-1 and any(word.split(" ") == words[index+1:index+len(word.split(" "))+1] for word in post_pos_words):
            feature_set.append(1)
        else:
            feature_set.append(0)

        # Check for prev and post positive word - TODO

        #Check for previous negative word exception
        if index > 0 and any(word.split(" ") == words[index-len(word.split(" ")):index] for word in post_neg_words):
            feature_set.append(0)
        else:
            feature_set.append(1)

        #Check for post negative word exception
        if index < len(words)-1 and any(word.split(" ") == words[index+1:index+len(word.split(" "))+1] for word in post_neg_words):
            feature_set.append(0)
        else:
            feature_set.append(1)

        # More features to be added here
        # TODO

        feature_frame.append(feature_set)

    return feature_frame