"""
Emotion Detection using Watson NLP API

This module defines the emotion_detector function that interacts with the 
Watson NLP API to analyze the emotions present in a given text input. 
The function sends a POST request to the API endpoint with the text to be 
analyzed and processes the response to extract emotion scores and determine 
the dominant emotion.
"""

import json

import requests


def emotion_detector(text_to_analyze):
    """
    Analyze the emotion of the provided text using Watson 
    NLP API and return formatted response    

    :param text_to_analyze: The text input for which emotions need to be analyzed
    :return: A dictionary containing emotion scores and the dominant emotion
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, headers=headers,
                                 json=input_json, timeout=10)
    except (requests.exceptions.RequestException, requests.exceptions.Timeout):
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Check if the response status code is 400 (bad request - blank/invalid input)
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Convert response text to dictionary
    response_dict = json.loads(response.text)

    # Check if the response contains valid emotion predictions
    if 'emotionPredictions' not in response_dict or not response_dict['emotionPredictions']:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Extract emotion scores from the response
    emotions = response_dict['emotionPredictions'][0]['emotion']

    # Extract required emotions
    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    # Find the dominant emotion (emotion with highest score)
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }

    dominant_emotion = max(emotion_scores, key=lambda x: emotion_scores[x])

    # Return formatted output
    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
