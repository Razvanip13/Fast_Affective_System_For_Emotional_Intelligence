# FASEL 

This was my final project for the Bachelor's Thesis. It is a system that can monitor the emotions of the people who are taking online exams, through voice and video. For full information about the whole system, please check out the <b> Documentation </b> which contains my Bachelor's Thesis. 

---

## Architecture

There are two APIs and one client. The AI API can be accessed only through requests to the CRUD API. That offers more scalability as if by instance somebody wants to implement their own AI in this project, they can connect the CRUD API requests to their own API

<img src="/images/deployment_diagram.PNG" display="center">

## Emotional Charts

The system monitors people's emotions while taking online tests. While solving the test, a thread is open and periodically it takes capture of the web camera, sending them to the CRUD API through base64 format, ending up to the AI API and predicting the emotion for that capture. The same flow is applied for the speech channel, with the only difference that the user will need to press a button in order to register their answer. 

<img src="/images/emotional_charts_horizonally.png" display="center">

## Datasets

<img src="/images/fer2013.PNG" display="center">

## Technologies



## Requirements
