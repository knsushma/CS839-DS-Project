import re
from feature_extraction import *
from model_training import *
from model_evaluation import *
from itertools import islice



def form_dataset_matrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity):
    data_frame = []
    for index in range(0,len(named_entity)):
        data_frame.append(([named_entity[index][1]] + positive_entity_feature_set[index] + [1]))
    for index in range(0,len(unnamed_entity)):
        data_frame.append(([unnamed_entity[index][1]] + negative_entity_feature_set[index] + [0]))
    #data_frame = np.array(data_frame)

    return data_frame
disposable_words = ["I", "He", "She", "They", "Those", "The", "Mr", "Ms", "Mrs", "January", "February", "March", "April", "May", "June", "July", "August",
                    "September", "October", "November", "December", "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Sept", "Oct", "Nov", "Dec", "Sunday", "Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Good", "Christmas", "New Year", "Eastern", "President", "Twitter", "Facebook", "Google", "Bloomberg", "Volkswagen", "Trump", "Ivanka", "Donald", "Takata", "Prime", "Vice", "Minister" ]
# disposable_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
#                     'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
#                     'under',"about","upon","these","those","this","that","i","they","them", "Mr", ""]



def form_feature_dataframe(start_index, end_index):
    dataframe = []
    for file_prefix in range(start_index,end_index):

        filePath = "Data/TrainRecords/" + str(file_prefix) + ".txt"
        document = open(filePath, 'r', encoding="utf8")

        named_entity = []
        unnamed_entity = []

        complete_data = document.read()
        words = complete_data.split()
        words = [word.strip(" .;:()") for word in words]
        iter_words = iter(enumerate(words))
        for index, word in iter_words:
            word = re.sub("\'s", "", word)
            word = re.sub("\’s", "", word)
            word = word.strip(",")
            if "location" in word:
                if word.count("location") == 2:
                    location = re.sub('<[^>]*>', '', word)
                    named_entity.append([index,location, 1])
                else:
                    labeled_data = " ".join(words[index:])
                    matched_data = re.match('<[^>]*>[a-z A-Z\s*]*</[^>]*>', labeled_data)
                    if matched_data:
                        len_of_word_matched = len(matched_data[0].split(" "))
                        named_entity.append([index, re.sub('<[^>]*>', '', matched_data[0]), len_of_word_matched])
                        next(islice(iter_words, len_of_word_matched-1, len_of_word_matched-1), None)
            else:
                # Reduce the unneccesary words, skip them from saving it in unnamed_entity
                if word and word[0].isupper() and word.lower() not in [X.lower() for X in disposable_words] and not (any(ch.isdigit() for ch in word)):
                    unnamed_entity.append([index, word, 1])

        positive_entity_feature_set = extract_feature_set(words, {en[0]:en[1:] for en in named_entity})
        negative_entity_feature_set = extract_feature_set(words, {en[0]:en[1:] for en in unnamed_entity})

        dataset = form_dataset_matrix(positive_entity_feature_set, negative_entity_feature_set, named_entity, unnamed_entity)
        dataframe.extend(dataset)
    return np.array(dataframe)
#print(np.array(dataset))
# check = np.array(training_dataframe)
# print(check[np.where(check[:,-1] == '1')].tolist())
# df = np.array(training_dataframe)
print("on train now")
training_dataframe = form_feature_dataframe(60, 210)
print("on test now")
test_dataframe = form_feature_dataframe(211, 267)

predict_accuracy_on_diff_classifiers(training_dataframe)
#print(df[0:160], df[-66:])
model_evaluation(training_dataframe, test_dataframe)