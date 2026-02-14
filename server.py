"""
Flask server for Emotion Detection application
"""

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html')


@app.route('/emotionDetector')
def emotion_detector_route():
    """
    Analyze the emotion of the provided text and return formatted response
    
    :return: A formatted string containing emotion scores and the dominant emotion
    """
    # Get the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Check if text_to_analyze is None or empty
    if not text_to_analyze or text_to_analyze.strip() == '':
        return "Invalid text! Please try again!"

    # Call the emotion_detector function
    result = emotion_detector(text_to_analyze)

    # Check if dominant_emotion is None (error case)
    if result['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    # Extract the emotions and dominant emotion
    anger = result['anger']
    disgust = result['disgust']
    fear = result['fear']
    joy = result['joy']
    sadness = result['sadness']
    dominant_emotion = result['dominant_emotion']

    # Format the response as required
    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )

    return response_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
