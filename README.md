### B.Tech (Computer Science & Engineering) Final Year Project - VNIT, Nagpur

#### Team Members -
1. Abdul Sattar Mapara
2. Saket Chopade
3. Rohan Salvi
4. Pritam Kumar Sahoo

#### Guided by -
1. Dr. U.A. Deshpande Sir (VNIT, Nagpur)
2. Dr. Sagar Sunkle Sir (TRDDC, Pune)

#### About the Project
The aim of the project is to gather time-stamped factual information about a given
topic/entity from a given set of documents (Brokerage Reports).

More precisely, given a set of documents (brokerage reports in PDF format), about a
company or a bank (or any organization) published over a period of 1-2 years, it is expected
that factual information about that company, or a bank (or any entity) to
be extracted (in the form of semi-structured statements) and classified as an increasing or decreasing trend.
The extracted facts are expected to be grouped by date/month.

#### Summary of Tasks Accomplished
1. Collecting and Processing the reports

    1. Brokerage Reports collected from - [trendlyne.com](https://trendlyne.com/)

    1. PDF -> Text conversion
    
    1. Text -> Sentence (Sentence Tokenization)
    
    1. Pass through spaCy pipeline for tokenization (into tokens), lemmatization, Part of Speech Tagging, Dependency Parse tree generation, Named Entity Recognition
    
1. Extraction of Date/Timestamp
    1. Using Named Entity Recognition
    1. Using Metadata associated with the reports
1. Extraction of Facts in the form of Semi Structured Statements
    1. Using Textacy library
    1. Using Dependency Parse tree generated by spaCy (Custom Approach)
    1. Explored relation extraction using Stanford Open IE
1. Sentiment Analysis (Sentence Classification)
    1. Dictionary based approach
    1. Machine learning based approach (using Support Vector Machines)
    1. Deep learning based approach (using Convolutional Neural Networks)
    
    <u>Note:</u> <i>Conversion of words to numbers done using custom word2vec model</i>
1. Application (using Flask framework) for demonstration of the project

#### About this Repository

This repository contains the source code written during the project for accomplishing the required tasks and experimentation.

This branch (master) contains the source code of the application developed for demonstration.

#### Demonstration

Video - Download [Final-Year-Project-Demo](https://github.com/pritamksahoo/B.Tech-Final-Year-Project/raw/master/Final-Year-Project-Demo.mp4)
