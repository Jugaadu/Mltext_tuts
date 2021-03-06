# # Homework with Yelp reviews data

# ## Introduction
#
# This assignment uses a small subset of the data from Kaggle's
#[Yelp Business Rating Prediction](https://www.kaggle.com/c/yelp-recsys-2013)
# competition.
#
# **Description of the data:**
#
# - **`yelp.csv`** contains the dataset. It is stored in the course repository
# (in the **`data`** directory), so there is no need to download anything from
# the Kaggle website.
# - Each observation (row) in this dataset is a review of a i
# particular business by a particular user.
# - The **stars** column is the number of stars (1 through 5
# ) assigned by the reviewer to the business. (Higher stars is better.) i
# In other words, it is the rating of the business by the person who i
# wrote the review.
# - The **text** column is the text of the review.
#
# **Goal:** Predict the star rating of a review using **only** the review text.
#
# **Tip:** After each task, I recommend that you check the shape and the
# contents of your objects, to confirm that they match your expectations.

# ## Task 1
#
# Read **`yelp.csv`** into a Pandas DataFrame and examine it.

from __future__ import print_function
import pandas as pd
import numpy as np

yelp = pd.read_csv('yelp.csv')
print("Shape of Yelp dataset = ", yelp.shape)
print ("Column Names of Yelp dataset: \n",yelp.columns)
#print yelp.head()
# ## Task 2
#
# Create a new DataFrame that only contains the **5-star** and **1-star** reviews.
yelp_5 = yelp[(yelp['stars'] == 5) | (yelp['stars'] == 1)]
print("Shape of New data containing 1 star and 5 star is", yelp_5.shape)
#
# - **Hint:** [How do I apply multiple filter criteria to a pandas DataFrame?]
#(https://www.youtube.com/watch?v=YPItfQ87qjM&list=
# PL5-da3qGB5ICCsgW1MxlZ0Hq8LL5U3u9y&index=9) explains how to do this.

# ## Task 3
#
# Define X and y from the new DataFrame, and then split X and y into
# training and testing sets, using the **review text** as the only feature and
# the **star rating** as the response.
#

y = yelp_5.stars

X = yelp_5.text


print("Shape of X: ", X.shape)
print("Shape of Y: ", y.shape)
# - **Hint:** Keep in mind that X should be a Pandas Series (not a DataFrame),
# since we will pass it to CountVectorizer in the task that follows.

# ## Task 4
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

vect = CountVectorizer()

X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 12)
print("Shape of training sample X:", X_train.shape)
print("Shape of test sample X:", X_test.shape)

#
# Use CountVectorizer to create **document-term matrices** from X_train and X_test.
#vect.fit(X_train)
X_train_dtm = vect.fit_transform(X_train)
print("Shape of X_train_dtm:", X_train_dtm.shape)
X_test_dtm = vect.transform(X_test)
print("Shape of X_test_dtm:", X_test_dtm.shape)


#print(X_train_dtm)

# ## Task 5
#
# Use Multinomial Naive Bayes to **predict the star rating** for the reviews
# in the testing set, and then **calculate the accuracy**
# and **print the confusion matrix**.
from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()

nb.fit(X_train_dtm, y_train)

y_pred_class = nb.predict(X_test_dtm)

from sklearn import metrics
print("Accuracy score :", metrics.accuracy_score(y_test,y_pred_class))
print("Confusion Matrix:\n",metrics.confusion_matrix(y_test, y_pred_class))

#
# - **Hint:** [Evaluating a classification model]
#(https://github.com/justmarkham/scikit-learn-videos/blob/master/09_classification_metrics.ipynb)
# explains how to interpret both classification accuracy and the confusion matrix.

# ## Task 6 (Challenge)
#
# Calculate the **null accuracy**, which is the classification accuracy that
# could be achieved by always predicting the most frequent class.
print("Data distribution in the Yelp data is :\n",yelp_5.stars.value_counts())

null_accuracy = len(yelp_5[yelp_5["stars"] == 5])/ len(yelp_5)

print("Null Accuracy is :", null_accuracy)

print("Null Accuracy other method :",yelp_5.stars.value_counts().head(1) / len(yelp_5))
#
# - **Hint:** [Evaluating a classification model]
# (https://github.com/justmarkham/scikit-learn-videos/blob/master/09_classification_metrics.ipynb)
# explains null accuracy and demonstrates two ways to calculate it,
# though only one of those ways will work in this case. Alternatively,
# you can come up with your own method to calculate null accuracy!

# ## Task 7 (Challenge)
#
# Browse through the review text of some of the **false positives** and
# **false negatives**. Based on your knowledge of how Naive Bayes works,
# do you have any ideas about why the model is incorrectly classifying these reviews?

print("False Positive Examples\n")

print(X_test[y_test < y_pred_class][:20],"\n")
print ("False Negative Examples ")
print(X_test[y_test> y_pred_class][:20])

#
confusion = metrics.confusion_matrix(y_test,y_pred_class)
print("Confusion matrix :\n",confusion)
# - **Hint:** [Evaluating a classification model]
# (https://github.com/justmarkham/scikit-learn-videos/blob/master/09_classification_metrics.ipynb)
# explains the definitions of "false positives" and "false negatives".
# - **Hint:** Think about what a false positive means in this context, and
# what a false negative means in this context. What has scikit-learn
# defined as the "positive class"?

# ## Task 8 (Challenge)
#Calcualate the spaminess of each token

X_train_token = vect.get_feature_names()

print("Length of training tokens:", len(X_train_token))

star_1 = nb.feature_count_[0,:]
star_5 = nb.feature_count_[1,:]
# create a dataframe of tokens with separate star_1 and star_5 count)

tokens = pd.DataFrame({'token': X_train_token, 'star_1': star_1, 'star_5': star_5}).set_index('token')

print(tokens.head())
#
# Calculate which 10 tokens are the most predictive of **5-star reviews**,
# and which 10 tokens are the most predictive of **1-star reviews**.


tokens['star_1'] = tokens.star_1 + 1
tokens['star_5'] = tokens.star_5 + 1


print('tokens sample:', tokens.sample(5,random_state = 6))

print('Class count :',nb.class_count_)

tokens['star_1'] = tokens.star_1/nb.class_count_[0]
tokens['star_5'] = tokens.star_5/nb.class_count_[1]
#
print('tokens sample:', tokens.sample(5,random_state = 6))

tokens['star_ratio'] = tokens.star_5/tokens.star_1
tokens = tokens.sort_values('star_ratio',ascending = False)

print(tokens)

#####
# - **Hint:** Naive Bayes automatically counts the number of times each token
# appears in each class, as well as the number of observations in each class.
# You can access these counts via the `feature_count_` and `class_count_`
# attributes of the Naive Bayes model object.

# ## Task 9 (Challenge)
#
# Up to this point, we have framed this as a **binary classification problem**
# by only considering the 5-star and 1-star reviews. Now, lets repeat the
# model building process using all reviews, which makes this a
# **5-class classification problem**.
#
# Here are the steps:
#

# - Define X and y using the original DataFrame. (y should contain 5 different classes.)
y = yelp.stars

X = yelp.text


# - Split X and y into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 12)

# - Create document-term matrices using CountVectorizer.
X_train_dtm = vect.fit_transform(X_train)
X_test_dtm = vect.transform(X_test)
# - Calculate the testing accuracy of a Multinomial Naive Bayes model.
nb.fit(X_train_dtm, y_train)

y_pred_class = nb.predict(X_test_dtm)

print("Accuracy score :", metrics.accuracy_score(y_test,y_pred_class))
print("Confusion Matrix:\n",metrics.confusion_matrix(y_test, y_pred_class))


# - Compare the testing accuracy with the null accuracy, and comment on the results.

# - Print the confusion matrix, and comment on the results.

# (This [Stack Overflow answer](http://stackoverflow.com/a/30748053/1636598)

# explains how to read a multi-class confusion matrix.)

# - Print the [classification report](http://scikit-learn.org/stable/modules/model_evaluation.html

#classification-report), and comment on the results. If you are unfamiliar
# with the terminology it uses, research the terms, and then try to figure out
# how to calculate these metrics manually from the confusion matrix!
