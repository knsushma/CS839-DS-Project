import numpy as np
# import enchant
# import nltk
from nltk.corpus import wordnet

neg_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
                'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
                'under',"about","upon","these","those","this","that","i","they","them","january","february", "march",
                "april", "may", "june", "july", "august", "september", "october", "november", "december", "monday",
                "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

#nltk.download('wordnet', '/Users/sushmakn/env/data-extraction/lib/python3.7/site-packages/nltk_data')


def extract_feature_set(words, entity_set):
    corpus_length = len(words)
    feature_frame = []
    for index, entity in entity_set.items():
        feature_set = []

        # if(is_english_word(entity)):
        #     feature_set.append(1)
        # else:
        #     feature_set.append(0)

        if (is_index_not_out_of_bound(index, entity[1], corpus_length)):
            #print(words[index-1], words[index], words[index:])
            #F1
            feature_set.append(is_previous_word_strong_preposition_for_entity_recognition(words[index-1], words[index+1]))

            # F2
            feature_set.append(is_previous_word_weak_preposition_for_entity_recognition(words[index-1]))

            # F3
            if (is_index_not_out_of_bound(index-1, entity[1], corpus_length)):
                feature_set.append(is_previous_to_previous_word_preposition_for_entity_recognition(words[index - 2], words[index - 1]))
            else:
                feature_set.append(0)

            #F4
            feature_set.append(is_previous_word_for_entity_recognition(words[index-1]))

            # F5
            feature_set.append(is_previous_word_ending_with_comma( words[index - 1]))

            # F6
            if (is_index_not_out_of_bound(index-1, entity[1], corpus_length)):
                feature_set.append(is_previous_word_location_with_AND_OR(words[index - 1], words[index - 2]))
            else:
                feature_set.append(0)

            # F7
            if (is_index_not_out_of_bound(index, entity[1], corpus_length)):
                feature_set.append(is_previous_two_words_preposition_and_THE(words[index - 1], words[index - 2], entity[0]))
            else:
                feature_set.append(0)

            # F8
            feature_set.append(is_next_word_for_entity_recognition(words[index + 1]))
        else:
            feature_set.extend([0,0,0,0,0,0,0,0])

        #Negative Cases
        if (is_index_not_out_of_bound(index, entity[1], corpus_length)):

            #F9
            feature_set.append(is_next_word_verb(words[index+1]))

            #feature_set.append(is_next_word_verb(words[index - 1]))

            # F10
            feature_set.append(is_word_ending_with_non_entity_recognition( words[index]))


            feature_set.append(is_prev_word_for_non_entity_recognition_for_name_prefixes(words[index-1]))

            # F11
            if (is_index_not_out_of_bound(index-1, entity[1], corpus_length)):
                feature_set.append(is_previous_two_words_for_non_entity_recognotion(words[index - 1], words[index - 2]))
            else:
                feature_set.append(1)

            # F12
            feature_set.append(is_next_word_for_non_entity_recognition(words[index + 1]))

            # F13
            feature_set.append(is_next_word_for_non_entity_recognition_specifics(words[index + 1]))

        else:
            feature_set.extend([1,1,1,1,1,1])


        feature_frame.append(feature_set)

    return feature_frame



def is_index_not_out_of_bound(current_index, word_length, length_of_corpus):
    if(current_index > 0 and current_index+word_length < length_of_corpus):
        return True
    else:
        return False

#Features for Positivity
# def is_english_word(word):
#     en_lang = enchant.Dict("en_US")
#     if (en_lang.check(str(word))):
#         return True
#     else:
#         return False

entity_recognition_strong_prepositions = ["in", "of", "at", "near", "to", "from", "across", "outside", "on", "around", "inside"]
def is_previous_word_strong_preposition_for_entity_recognition(prev, next):
    # next and (all(entity != next for entity in non_entity_recognition_in_next_word)) and
    if ( next and (all(entity != next for entity in non_entity_recognition_in_next_word)) and
            prev and any(prev == entity for entity in entity_recognition_strong_prepositions)):
        return 1
    else:
        return 0

entity_recognition_weak_prepositions = ["with", "as", "through", "outside", "throughout", "into", "leave", "like", "about"]
def is_previous_word_weak_preposition_for_entity_recognition(prev):
    if (prev and any(prev == entity for entity in entity_recognition_weak_prepositions)):
        return 1
    else:
        return 0

entity_recognition_specifics = ["south", "north", "east", "west", "eastern" ,"western", "southern", "northern", "continental", "central", "upper", "lower", "southeastern", "southwestern", "northeastern", "northwestern", "mainland", "contemporary", "southeast", "southwest", "northeast", "northwest"]
def is_previous_word_for_entity_recognition(prev):
    if (prev and any(prev.lower() == word for word in entity_recognition_specifics)):
        return 1
    else:
        return 0

entity_recognition_prepositions_in_pre_pre_word = ["in", "of", "at", "near", "to", "from", "across", "outside", "on", "around"]
entity_recognition_prepositions_in_pre_word = ["a", "an", "new"] + entity_recognition_specifics
def is_previous_to_previous_word_preposition_for_entity_recognition(prev_prev, prev):
    # prev and any(prev == entity for entity in entity_recognition_prepositions_in_pre_word) and
    if (prev and any(prev.lower() == entity for entity in entity_recognition_prepositions_in_pre_word) and
            prev_prev and any(prev_prev == entity for entity in entity_recognition_prepositions_in_pre_pre_word)):
        return 1
    else:
        return 0


def is_previous_word_ending_with_comma(prev):
    if (prev and prev[-1] == "," and "location>" in prev):
        return 1
    else:
        return 0

def is_previous_word_location_with_AND_OR(prev, prev_prev):
    if (prev and (prev.lower() == "and" or prev.lower == "or") and prev_prev and ("location>" in prev_prev)):
        return 1
    else:
        return 0

entity_recognition_prepositions_in_prev_prev_word = ["and", "in", "of", "at", "for", "with", "around", "from", "across", "like"]
country_list = ["United", "Czech Republic", "Philippines", "U.S.", "U. S.", "U.K.", "New York", "United Arab Emirates"]
def is_previous_two_words_preposition_and_THE(prev, prev_prev, word):
    if (prev and prev.lower() == "the" and prev_prev and
            any(prev_prev.lower() == prep for prep in entity_recognition_prepositions_in_prev_prev_word) and any(country in word for country in country_list) ):
        return 1
    else:
        return 0

entity_recognition_in_next_word= ["native", "city", "state"]
def is_next_word_for_entity_recognition(word):
    if(word and any(entity == word for entity in entity_recognition_in_next_word)):
        return 1
    else:
        return 0

#Features for negativity
def is_next_word_verb(word):
    #print(word, wordnet.synsets(word))
    if(wordnet.synsets(word)):
        w = wordnet.synsets(word)[0].pos()
        if (w == "v"):
            return 0
        else:
            return 1
    else:
        return 1

def is_prev_word_verb(word):
    if(wordnet.synsets(word)):
        w = wordnet.synsets(word)[0].pos()
        if (w == "v"):
            return 0
        else:
            return 1
    else:
        return 1

non_entity_ending_words = ["ean", "ian", "can", "man", "xan", "ban", "ish", "ese", "ans"]
def is_word_ending_with_non_entity_recognition(word):
    word = word.strip(",")
    if (word and len(word)>3 and any(entity == word[-3:] for entity in non_entity_ending_words)):
        return 0
    else:
        return 1

non_entity_recognition_in_prev_word_for_name_prefixes = ["Ms", "Mrs", "Mr", "Dr"]
def is_prev_word_for_non_entity_recognition_for_name_prefixes(prev):
    if (prev and any(entity in prev for entity in non_entity_recognition_in_next_word_specifics)):
        return 0
    else:
        return 1

non_entity_recognition_in_next_word = ["University", "Police", "government", "Times", "Post",
                                       "Institute", "Development", "Society", "Development",
                                       "Society", "River", "Lake", "Ocean", "Sea", "Canal", "Park",
                                       "studio", "Corporation", "Entertainment", "Legislature", "Pictures", "Authority", "Province", "Hills", "Hill", "Awards", "Airport", "Talks", "Daily", "religion", "Brands", "territory"]
def is_next_word_for_non_entity_recognition(next):
    if (next and any(entity == next for entity in non_entity_recognition_in_next_word)):
        return 0
    else:
        return 1

non_entity_recognition_in_prev_prev_word = ["University of", "College of", "Times of", "Gulf of", "Departments of", "Department of", "Secretary of", "friend of", "Union on", "State University", "Academy of", "Art of"]
def is_previous_two_words_for_non_entity_recognotion(prev, prev_prev):
    if (prev and prev_prev and any(entity == (" ".join([prev_prev, prev])) for entity in non_entity_recognition_in_prev_prev_word)):
        return 0
    else:
        return 1

non_entity_recognition_in_next_word_specifics = ["nation", "forces", "leaders", "officials", "strategy", "adviser", "woman", "man", "refugees"]
def is_next_word_for_non_entity_recognition_specifics(next):
    if (next and any(entity == next for entity in non_entity_recognition_in_next_word_specifics)):
        return 0
    else:
        return 1