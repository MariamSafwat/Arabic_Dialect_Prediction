# Arabic_Dialect_Prediction

## Overview
Many countries speak Arabic; however, each country has its own dialect, the aim of this project is to build a model that predicts the dialect given the text.

## Data Pre-processing
Remove anything in the text that doesn’t affect arabic dialect identification, like:
1. Mentions 
2. Emojis
3. Digits
4. URLs
5. English words
6. The MSA relative pronounsالذي , التي , الذين )  ) and the dialectal relative pronoun اللى ) )
7. Punctuations
8. ( # ) and ( _ ) in hashtags
9. The laughing words (هههه..إلخ)

## ML Model
1. Count Vectorizer with Logistic Regression -> F1-score: 0.53
2. TfidfVectorizer, (3,7) character n-gram with Linear SVM Classifier -> F1-score: 0.59
3. TfidfVectorizer, (2,6) word n-gram with Linear SVM Classifier -> F1-score: 0.39

## DL Architecture
LSTM with 0.2 Dropout, loss: categorical_crossentropy, optimizer: adam -> Acc: 0.518

## Deployment
Deployment is done using FastAPI

## Instructions to test the project
The api code is found in code/server.py
The following command will run the server
```
uvicorn main:app
```
Then navigate to http://127.0.0.1:8000/docs in your browser and you will see the documentation page created automatically by FastAPI.
To make a prediction, first click the “predict” route and then click on the button “Try it out”. Write any arabic text then click the execute button to make a prediction and get the result.
