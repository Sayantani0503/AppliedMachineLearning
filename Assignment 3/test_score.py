import unittest
import joblib
import os
import time
import subprocess
import requests
from sklearn.base import BaseEstimator
from score import score
import warnings
warnings.filterwarnings("ignore")

class TestScoreFunction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model = joblib.load("/content/best_model.pkl")  # Load the saved model


    # Test if the function produce some output without crashing
    def test_smoke(self):
        text = "This is a test message"
        threshold = 0.5
        output = score(text, self.model, threshold)
        self.assertIsNotNone(output)


    # Test if  the input/output formats/types as expected
    def test_format(self):
        text = "Sample message"
        threshold = 0.5
        prediction, propensity = score(text, self.model, threshold)
        self.assertIsInstance(prediction, bool)
        self.assertIsInstance(propensity, float)


    # Test if prediction is always 0 or 1
    def test_prediction_values(self):
        text = "Hello, this is a test"
        threshold = 0.5
        prediction, _ = score(text, self.model, threshold)
        self.assertIn(prediction, [True, False])


    # Test if propensity score is between 0 and 1
    def test_propensity_range(self):
        text = "Some input text"
        threshold = 0.5
        _, propensity = score(text, self.model, threshold)
        self.assertGreaterEqual(propensity, 0)
        self.assertLessEqual(propensity, 1)


    # Test if threshold = 0 always returns prediction = 1
    def test_threshold_zero(self):
        text = "Random input text"
        threshold = 0.0
        prediction, _ = score(text, self.model, threshold)
        self.assertTrue(prediction)  # Should always be True (1)


    # Test if threshold = 1 always returns prediction = 0
    def test_threshold_one(self):
        text = "Another input text"
        threshold = 1.0
        prediction, _ = score(text, self.model, threshold)
        self.assertFalse(prediction)  # Should always be False (0)


    # Test if an obvious spam input returns prediction = 1
    def test_obvious_spam(self):
        spam_text = "Win money now!!! Click here for a free prize!!!"
        threshold = 0.5
        prediction, _ = score(spam_text, self.model, threshold)
        self.assertTrue(prediction)  # Should be classified as spam (1)


    # Test if an obvious non-spam input returns prediction = 0
    def test_obvious_non_spam(self):
        non_spam_text = "Hello, how are you doing today?"
        threshold = 0.5
        prediction, _ = score(non_spam_text, self.model, threshold)
        self.assertFalse(prediction)  # Should be classified as non-spam (0)



class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):        # Start the Flask server in the background
        cls.process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)  # Give the server time to start


    # Test the response from the Flask endpoint
    def test_flask(self):
        url = "http://127.0.0.1:5000/score"
        test_data = {"text": "This is a test message", "threshold": 0.5}
        response = requests.post(url, json=test_data)

        self.assertEqual(response.status_code, 200)  # Ensure the request was successful
        data = response.json()

        # Check if response contains expected keys
        self.assertIn("prediction", data)
        self.assertIn("propensity", data)

        # Check types of values
        self.assertIsInstance(data["prediction"], int)
        self.assertIsInstance(data["propensity"], float)

    @classmethod
    def tearDownClass(cls):      # Stop the Flask server
        cls.process.terminate()  # Kill the process
        cls.process.wait()



if __name__ == "__main__":
    unittest.main()
