import numpy as np
import enchant
import nltk
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
            if(is_previous_word_preposition_for_entity_recognition(words[index-1])):
                feature_set.append(1)
            else:
                feature_set.append(0)

            if(is_previous_word_for_entity_recognition(words[index-1])):
                feature_set.append(1)
            else:
                feature_set.append(0)


            if (is_previous_word_ending_with_comma( words[index - 1])):
                feature_set.append(1)
            else:
                feature_set.append(0)


            if (is_next_word_for_entity_recognition(words[index + 1])):
                feature_set.append(1)
            else:
                feature_set.append(0)
        else:
            feature_set.extend([0,0,0,0])

        #Negative Cases
        if (is_index_not_out_of_bound(index, entity[1], corpus_length)):
            # if (is_next_word_verb(words[index + 1])):
            #     feature_set.append(0)
            # else:
            #     feature_set.append(1)

            if (is_word_ending_with_non_entity_recognition( words[index ])):
                feature_set.append(0)
            else:
                feature_set.append(1)

            if (is_next_word_for_non_entity_recognition(words[index + 1])):
                feature_set.append(0)
            else:
                feature_set.append(1)


            if (is_index_not_out_of_bound(index, entity[1], corpus_length) and
                    is_previous_two_words_for_non_entity_recognotion(words[index - 1], words[index - 2])):
                feature_set.append(0)
            else:
                feature_set.append(1)


            if (is_index_not_out_of_bound(index, entity[1], corpus_length) and
                    is_previous_two_words_preposition_and_THE(words[index - 1], words[index - 2])):
                feature_set.append(0)
            else:
                feature_set.append(1)
        else:
            feature_set.extend([1,1,1, 1])


        feature_frame.append(feature_set)

    return feature_frame



def is_index_not_out_of_bound(current_index, word_length, length_of_corpus):
    if(current_index > 0 and current_index+word_length < length_of_corpus):
        return True
    else:
        return False

#Features for Positivity
def is_english_word(word):
    en_lang = enchant.Dict("en_US")
    if (en_lang.check(str(word))):
        return True
    else:
        return False

entity_recognition_prepositions = ["in", "of", "at", "near", "to", "from", "across", "with", "and", "as", "outside" ]
#entity_recognition_prepositions = ["in", "at", ]
def is_previous_word_preposition_for_entity_recognition(prev):
    if (prev and any(prev == prep for prep in entity_recognition_prepositions)):
        return True
    else:
        return False

entity_recognition_specifics = ["eastern" ,"western", "southern", "northern"]
def is_previous_word_for_entity_recognition(prev):
    if (prev and any(prev == word for word in entity_recognition_specifics)):
        return True
    else:
        return False

def is_previous_word_ending_with_comma(prev):
    if (prev and prev[-1] == ","):
        return True
    else:
        return False

entity_recognition_in_next_word= ["City", "County", "State"]
def is_next_word_for_entity_recognition(word):
    if(word and any(entity == word for entity in entity_recognition_in_next_word)):
        return True
    else:
        return False


#Features for negativity
def is_next_word_verb(word):
    #print(word, wordnet.synsets(word))
    if(wordnet.synsets(word)):
        w = wordnet.synsets(word)[0].pos()
        if (w == "v"):
            return True
        else:
            return False
    else:
        return False

#Indian, American
def is_word_ending_with_non_entity_recognition(word):
    if (word and len(word)>2 and word[-2:-1]=="an"):
        return True
    else:
        return False

non_entity_recognition_in_next_word = ["University", "Police", "government", "Times", "Post"]
def is_next_word_for_non_entity_recognition(next):
    if (next and any(entity == next for entity in non_entity_recognition_in_next_word)):
        return True
    else:
        return False

non_entity_recognition_in_prev_prev_word = ["University of", "College of", "Times of"]
def is_previous_two_words_for_non_entity_recognotion(prev, prev_prev):
    if (prev and prev_prev and any(entity == (" ".join([prev_prev, prev])) for entity in non_entity_recognition_in_prev_prev_word)):
        return True
    else:
        return False

#entity_recognition_prepositions_in_prev_prev_word = ["in", "at", "of", "from", "near", "across"]
def is_previous_two_words_preposition_and_THE(prev, prev_prev):
    if (prev and prev.lower() == "the" and prev_prev and any(prev_prev.lower() == prep for prep in entity_recognition_prepositions) ):
        return True
    else:
        return False


# def starts_with_uppercase_letter(word):
#     if(word[0].isupper()):
#         return True
#     else:
#         return False
#
#
# def is_all_lowercase(word):
#     if word.islower():
#         return True
#     else:
#         return False

# def is_previous_word_THE(word):
#     if(word.tolower() == "the"):
#         return True
#     else:
#         return False

# def is_all_capital(word):
#     if word and word.isupper():
#         return True
#     else:
#         return False