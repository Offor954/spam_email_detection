# -*- coding: utf-8 -*-
"""Email_classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JIyMnEozhaE-UNYoV1z5hCEAliXqWi6N
"""

import pandas as pd # for data manipulations
import seaborn as sns # for data visualization
import matplotlib.pyplot as plt # for data visualization
import numpy as np # algebraic
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score # for model's performance evaluation
from sklearn.feature_extraction.text import TfidfVectorizer # used for text preprocessing
from sklearn.linear_model import LogisticRegression # machine learning algorithm  for binary classification tasks
from sklearn import svm # machine learning algorithm  for both regression and classification tasks
from sklearn.tree import DecisionTreeClassifier # algorithm for solving binary classification problem in data science
from sklearn.metrics import precision_score  # for model's performance evaluation
from sklearn.metrics import recall_score # for model's performance evaluation

"""**LOADING THE DATASET**"""

df =pd.read_csv('/content/drive/MyDrive/Datasets/mail_data.csv')

df

# let's find out how many rows and columns that we have in the dataset
df.shape

"""**DATA PREPROCESSING STAGE**"""

# let's check if there are missing values within the dataset
df.isnull().sum().sum()

# let's check for missing values in each of the columns specifically.
# First the category column
df['Category'].isnull().sum()

# The message column
df['Message'].isnull().sum()

"""**EDA = EXPLORATORY DATA ANALYSIS**"""

# let's check how many ham and spam mail exists in the dataset
df.groupby('Category')['Category'].count()

# Let's visualize the reslut using countplot()
plt.style.use('bmh')
sns.countplot(x='Category', data=df, width=0.7, palette='viridis', hue='Category')
plt.title('HAM vs SPAM Mails')
plt.show()

from wordcloud import WordCloud

# Combine all the messages into a single string
text = " ".join(message for message in df['Message'])

# Generate the word cloud
wordcloud = WordCloud(width=400, height=200, background_color='black').generate(text)
# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# dealing with the imbalance problem using the oversampling method

df['Category'].value_counts()

"""**DEALING WITH IMBALANCE DATA USING THE OVERSAMPLYING TECHNIQUE**"""

from imblearn.over_sampling import RandomOverSampler

# Separate features (X) and target variable (y)
x = df['Message']
y = df['Category']

# Initializing RandomOverSampler
oversampler = RandomOverSampler(random_state=42)

# Resample the data
x_resampled, y_resampled = oversampler.fit_resample(x.values.reshape(-1, 1), y)

# Creating a new DataFrame with the resampled data
df_resampled = pd.DataFrame({'Message': x_resampled.flatten(), 'Category': y_resampled})

# Display the value counts of the resampled target variable
print(df_resampled['Category'].value_counts())

"""**DATA ENCODE**"""

# Converting the category column to numerical values: ham==>>1 and spam==>0
mapping = {"ham": 0, "spam": 1}
# Convert categorical string values to numeric values using map() function
df["Category"] = df["Category"].map(mapping)

df_resampled

# prompt: i want to view one of the full spam text

# Assuming 'df' is your DataFrame as defined in the provided code.

# Print the first full spam message
spam_message = df[df['Category'] == 1]['Message'].iloc[0:5]
spam_message

"""**DATA SPLITING PHASE**"""

# Now let's separate the dataset into label and text
x= df_resampled['Message']
y= df_resampled['Category']

# let's print the values in x and y separately and see the content
print(x)

# let's print the values in x and y separately and see the content
print(y)

"""**SPLITING THE DATASET INTO TRAINING AND TESTING DATA**"""

# Now, let's split our x and y data into training and testing data using the train_test_split() function
x_train, x_test, y_train, y_test =train_test_split(x,y,test_size=0.2, random_state=42)

# After the splitting, let's print the shape of the x_train, x_test and y_train, y_test
x_train.shape
x_test.shape
y_train.shape
y_test.shape

"""Convert the message Variable into Numerical values using TFifVectorier"""

# Now, let us convert our text data stored in the variable x to numerical data using the TfidfVectorizer

#setting the parameters for the TFidvectorier
vectorizer= TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)

x_train_converted=vectorizer.fit_transform(x_train)
x_test_converted=vectorizer.transform(x_test)

print(x_train_converted)

print(x_test_converted)

"""**MODEL TRAINING**"""

classifier = LogisticRegression()

model = classifier.fit(x_train_converted, y_train)



"""**Evaluating the train model using the x_train**"""

y_predict = model.predict(x_train_converted)
print(y_predict)

"""**Accuracy**"""

train_accuarcy = accuracy_score(y_predict, y_train)
print(round(train_accuarcy,2))

"""**Evaluating the model using Test Data**"""

#Evaluating the model using Test Data
y_predict_test = model.predict(x_test_converted)
print(y_predict_test)

test_accuarcy = accuracy_score(y_predict_test , y_test)
print(round(test_accuarcy,2))

"""**BUILDING TH PREDICTIVE MODEL INTERFACE**"""

email=["Hi Jeremiah,Imagine if you could forecast 📈market trends, 🔄automate processes, 📶scale solutions faster, and drive smarter business decisions. AI makes it all possible todayJoin us for a Live Webinar featuring the most sought-after MBA-AI in Business and discover how to turn AI insights into winning strategies.AI is the future of leadership, and you can be the next AI Strategist.The wait is almost over: 📅 November 16; 10:00am to 12:00pm GMT"]

# Now let's transform the email to numeric data
email_input=vectorizer.transform(email)

# making Prediction
prediction =model.predict(email_input)
if(prediction==1):
    print(f"The result of the prediction is {prediction}")
else:
    print(f"The result of the prediction is {prediction}")

import pickle
# Save the model to a pickle file
with open('spamDetection_model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Save the vectorizer to a pickle file
with open('vectorizer.pkl', 'wb') as file:
  pickle.dump(vectorizer, file)

from sklearn.metrics import classification_report

# Assuming you have a trained model
y_pred = classifier.predict(x_test_converted)  # Predict on test set

# Print classification metrics
print(classification_report(y_test, y_pred))

# If using a classifier that supports probability prediction (e.g., LogisticRegression, RandomForest)
probabilities = classifier.predict_proba(x_test_converted)  # Probabilities for each class
print(probabilities[:10])  # Inspect first 10 predictions
