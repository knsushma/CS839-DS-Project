import re
from stage1.feature_extraction import *
from stage1.model_evaluation import *
from itertools import islice
import nltk


unigram_disposable_words = ["I", "He", "She", "They", "Those", "The", "Mr", "Ms", "Mrs", "January", "February", "March", "April", "May", "June", "July", "August",
                            "September", "October", "November", "December", "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Sept", "Oct", "Nov", "Dec", "Sunday",
                            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Good", "Christmas", "New", "Eastern", "President", "Twitter", "Facebook",
                            "Google", "Instagram", "Bloomberg", "Volkswagen", "Trump", "Ivanka", "Donald", "Takata", "Minister", "Government", "Oscar", "Democrats", "Planet",
                            "Earth", "King", "University", "south", "north", "east", "west", "eastern", "western", "southern", "northern", "continental", "central", "upper",
                            "lower", "southeastern", "southwestern", "northeastern", "northwestern", "Southeast", "Southwest", "Northeast", "NorthWest", "mainland", "contemporary",
                            "Air", "Congress", "CBS", "KFC", "Gov", "Senator", "Election", "Skype", "Sony"]

bigram_disposable_words = ["New Year", "New Year's", "Prime Minister", "Vice President", "according to", "Election Day"]


def form_feature_dataframe(files_list):

    dataframe = []
    # Read each document and extract information for model training
    for file_name in files_list:
        document = open(file_name, 'r', encoding="utf8")
        complete_data = document.read()
        words = complete_data.split()
        words = [word.strip(" .;:()") for word in words]
        iter_words = iter(enumerate(words))

        labeled_entity = []
        unlabeled_entity = []

        # Reading the document word by word
        for index, word in iter_words:
            word = re.sub("\'s", "", word)
            word = re.sub("\’s", "", word)
            word = word.strip(",")
            if "location" in word:
                # Save the labeled entities to create featire dataframe for model training
                if word.count("location") == 2:
                    location = re.sub('<[^>]*>', '', word)
                    labeled_entity.append([index,location, 1])
                else:
                    #
                    labeled_data = " ".join(words[index:])
                    matched_data = re.match('<[^>]*>[a-z A-Z\s*]*</[^>]*>', labeled_data)
                    if matched_data:
                        len_of_word_matched = len(matched_data[0].split(" "))
                        labeled_entity.append([index, re.sub('<[^>]*>', '', matched_data[0]), len_of_word_matched])
                        next(islice(iter_words, len_of_word_matched-1, len_of_word_matched-1), None)
            else:
                # Reduce the unneccesary words, skip them from saving it in unlabeled_entity
                if (has_bigram_disposable_words(words, index)):
                    next(islice(iter_words, 2 , 2 ), None)
                else:
                    if word and word[0].isupper() and word.lower() not in [X.lower() for X in unigram_disposable_words] and not (any(ch.isdigit() for ch in word)) and not is_word_a_verb(word) and not is_word_preposition(word):
                        unlabeled_entity.append([index, word, 1])

        positive_entity_feature_set = extract_feature_set(words, {en[0]:en[1:] for en in labeled_entity})
        negative_entity_feature_set = extract_feature_set(words, {en[0]:en[1:] for en in unlabeled_entity})

        dataset = form_dataset_matrix(positive_entity_feature_set, negative_entity_feature_set, labeled_entity, unlabeled_entity)
        dataframe.extend(dataset)
    return np.array(dataframe)


def form_dataset_matrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity):
    data_frame = []
    for index in range(0,len(named_entity)):
        data_frame.append(([named_entity[index][1]] + positive_entity_feature_set[index] + [1]))
    for index in range(0,len(unnamed_entity)):
        data_frame.append(([unnamed_entity[index][1]] + negative_entity_feature_set[index] + [0]))
    #data_frame = np.array(data_frame)

    return data_frame

def has_bigram_disposable_words(words, index):
    if (is_index_not_out_of_bound(index, 1, len(words)) and
            (" ".join([words[index], words[index+1]])).lower() in [X.lower() for X in bigram_disposable_words] ):
        return True
    else:
        return False


def is_word_a_verb(word):
    if(wordnet.synsets(word)):
        w = wordnet.synsets(word)[0].pos()
        if (w == "v"):
            return 1
        else:
            return 0
    else:
        return 0


def is_word_preposition(word):
    if(nltk.pos_tag([word])):
        w =  nltk.pos_tag([word])[0][1]
        if (w == "IN"):
            return 1
        else:
            return 0
    else:
        return 0
