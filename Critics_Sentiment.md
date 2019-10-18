# Sentiment Analysis using Movie Reviews

### Did you like that movie? Wait I can't understand you. Let my write some code to understand what you're saying. Stop talking

#
## Hypothesis

- NULL- script to identify sentiment will be 90% accurate or greater

- ALT- script to identify sentiment will be less than 90% accurate.


#### The Stanford Movie Review dataset 

    Sample Review from 50k dataset

<img src="https://github.com/zuhbeer/NLP-CAP/blob/master/Screen%20Shot%202019-10-18%20at%2010.22.06%20AM.png" width="900">



#
### Reviews are cleaned via nltk, spacy, and sklearn libraries and put into a Pandas dataframe


<img src="https://github.com/zuhbeer/NLP-CAP/blob/master/Screen%20Shot%202019-10-18%20at%2010.27.27%20AM.png"  width="600">




#
### 12,500 positive and 12,500 negative reviews with corresponding iMDB score.


<img src="https://github.com/zuhbeer/NLP-CAP/blob/master/Screen%20Shot%202019-10-18%20at%2010.06.25%20AM.png" width="600">

#
### Vectorizing the Reviews, and creating a TF-IDF matrix. (Words to Numbers)

<img src="https://github.com/zuhbeer/NLP-CAP/blob/master/tfidf.png" width="700">

#
### Here come the models!


<img src="https://github.com/zuhbeer/NLP-CAP/blob/master/Log_reg.png" width="700">

    baseline score: 84%
#

<img src="https://github.com/zuhbeer/NLP-CAP/blob/master/RF.png" width="700">

    new high score: 92%

#
### What words are most important?

<img src="https://github.com/zuhbeer/NLP-CAP/blob/master/Screen%20Shot%202019-10-18%20at%2010.46.07%20AM.png"  width="400">

#
### Future work

- identify misclassified reviews 
- train model on different types of reviews
- create interface with a sentence input and sentiment output: negative, neutral, positive
