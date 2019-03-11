# CS839-DS-Project

### [Project on Data Extraction](https://sites.google.com/view/data-science-ask/home)


The goal of this project is to get our hands "dirty" as a budding data scientist (and to practice certain materials taught in the class). After finishing the project, we will gain a much better appreciation for working with "data in the wild", a better understanding of what it means to work as a data scientist, a deeper understanding of the class materials, a deeper understanding of how to use and debug machine learning models, a chance to work with popular data science tools in Python, and a glimpse into some research efforts in data science.

Specifically, in this project, we will collect data, "wrangle" the data, by extracting/cleaning/matching/integrating the data into a single unified data set, then analyze that data set to infer insights. 

```
Stage 1: Information extraction from natural text.
Stage 2: Crawling and extracting structured data from Web pages.
Stage 3: Entity matching.
Stage 4: Integrating and performing analysis.
```

## Stage 1
### Location Extraction From Natural Text

##### In this project stage your team will perform information extraction (IE) from natural text documents, using a supervised learning approach.

#### Setup & Requirements
```
Follow steps mentioned in python-setup-data-extraction.pdf
```

#### Running the code
```shell
main.py
```

#### Entity Type
```
Location
```

#### Tag Description
```
Locations are mentioned in the documents using <location>....</location> tags.
```

### Tag Examples

#### Positives
```
1. He recently moved to the <location>United States</location>.
2. The climate in <location>India</location> was pleasant that year.
3. The lady claimed to be from <location>Europe</location>.
```
#### Negatives
```
1. University of Southern California
2. California's economy
3. Hollywood star
```

#### Approach Followed

In this project stage we will perform information extraction (IE) from natural text documents, using a supervised learning approach. Here are the steps that we followed: 

*	Collected 300 text documents from which we will extract mentions of LOCATION entity type. These documents contain well-formed sentences (such as those in news articles). 

*	We went through documents and marked up the mentions of location entity type. After the mark up of these locations, we had around 1100 mentions (distributed among 300 documents).

*	We split these 300 documents into a set I of 200 documents and a set J of the remaining 100 documents. The set I will be used for development (dev set), and the set J will be used for reporting the accuracy of our extractor (the test set). The goal here is to develop an extractor that achieves a precision of at least 90% and as high recall as possible, but at least 60% in recall. 

*	Next we performed Cross Validation (CV) on the set I to select the best classifier. We considered the following classifiers: decision tree, random forest, support vector machine, linear regression, and logistic regression. We used the scikit-learn package for this CV purpose. 

*	After this step, Linear Regression model performed better when compared to other classifiers. We got an accuracy of 88% using Linear Regression. This is the classifier M.

*	Then we debugged M using the same set I.  For this, we further split up set I into two sets P and Q, trained M on P, applied M to label examples in Q, then identified and debugged the false positive/negative examples.

*	Once this debugging was done, we repeated CV to see if another classifier provided a better accuracy now.

*	Here we observed that the Random Forest classifier performed better which provided 92% precision and 77% recall. As we were able to achieve required precision of 90% and recall of 60%, we did not perform any Rule-based post-processing steps. This is the model X(and Y).

*	Then we applied Y to the set-aside test set J and found that model M reported 91% precision and 80% recall which represents the final accuracy measure of our model.


