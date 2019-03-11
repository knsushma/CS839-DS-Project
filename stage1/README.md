### Location Extraction From Natural Text


#### Setup & Requirements
```shell
pip3 install -r requirements.txt
```

#### Running the code
```shell
python3 main.py
```

#### Entity Type
```
Location
```

#### Tag Description
```
Locations are mentioned in the documents using **\<location\>....\</location\>** tags.
```

### Tag Examples

#### Positives
```
1. \<location\>United States\</location\>
2. \<location\>India\</location\>
3. \<location\>Europe\</location\>
```
#### Negatives
```
1. University of Southern California
2. California's economy
3. Hollywood star
```

#### Approach Followed

In this project stage we will perform information extraction (IE) from natural text documents, using a supervised learning approach. Here are the steps that we followed: 

* Collected 300 text documents from which we will extract mentions of LOCATION entity type. These documents contains well-formed sentences (such as those in news articles). 

* We went through documents and marked up the mentions of location entity type. After mark up of mentions, we had around 1100 mentions (over 300 documents).

* Let this set of documents be B. We split them into a set I of 200 documents and a set J of the remaining 100 documents. The set I will be used for development (dev set), and the set J will be used for reporting the accuracy of our extractor (the test set). The goal here is to develop an extractor that achieves at least precision of 90% or higher and as high recall as possible, but at least 60% in recall. 

* Performed cross validation (CV) on the set I to select the best classifier. We considered the following classifiers: decision tree, random forest, support vector machine, linear regression, and logistic regression. We used the scikit-learn package for this CV purpose. 

* After this step, Linear Regression model performed better when compared to other classifiers. We got accuracy of 88% using Linear Regression. Let's call this classifier as M.

* Then we debugged M using the same set I for which we did split on set I into two sets P and Q, train M on P, applied M to label examples in Q, then identified and debugged the false positive/negative examples; we improved recall by paying attention to the false negative examples). 

* Once after the debug on M, we repeated CV to see if another classifier may happen to provide more accurate this time.

* After above setps, Random Forest classifier performed better which provided 92% precision and 77% recall. As we were able to achieve required precision of 90% and recall of 60%, we did not perfom the Rules based postprocessing step. Let us call this as model X.

* Then we applied X to the set-aside test set J and found that model M reported 91% precision and 80% recall. 


