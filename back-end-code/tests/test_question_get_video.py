import unittest
import requests
import json
from azure.storage.blob import BlobServiceClient

class test_question_get_feedback(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the question_get_video function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/question/get/video"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/question/get/video"
    TEST_URL = LOCAL_DEV_URL

    # Configure the Proxy objects from the local.settings.json file.
    with open('local.settings.json') as settings_file:
        settings = json.load(settings_file)
    FUNCTION_KEY = settings['Values']['FunctionAppKey']
    blob_service_client = BlobServiceClient.from_connection_string(settings['Values']['AZURE_STORAGE_CONNECTION_STRING'])
    video_proxy = blob_service_client.get_container_client(settings['Values']['VideoContainerName'])

    def test_questions_get_video(self):
        # Send a request to register same user. (Input is a dictionary)
        request = { "filename": 'Urban Driving 1.mp4' }
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got randomised questions.
        print(dict_response['msg'])
        self.assertTrue(dict_response['result'])

    def test_questions_get_invalid_video(self):
        # Send a request to register same user. (Input is a dictionary)
        request = { "filename": 'bombaclaat' }
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got randomised questions.
        print(dict_response['msg'])
        self.assertFalse(dict_response['result'])