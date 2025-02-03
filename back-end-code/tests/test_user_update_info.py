import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_update_info(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_update_info function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/update/info"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/update/info"
    TEST_URL = LOCAL_DEV_URL

    # Configure the Proxy objects from the local.settings.json file.
    with open('local.settings.json') as settings_file:
        settings = json.load(settings_file)
    FUNCTION_KEY = settings['Values']['FunctionAppKey']
    cosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])           # Cosmos Object
    db_proxy = cosmos.get_database_client(settings['Values']['DatabaseName'])                                   # Proxy object for database
    users_proxy = db_proxy.get_container_client(settings['Values']['UserContainerName'])                        # Proxy obj for "users" container

    # SetUp method executed before each test       
    def setUp(self):
        self.users_proxy.create_item({'id': 'user_id_1', 'username': 'antoni_gn', 'password': 'ILoveTricia', 'streak': 0, 'daily_training_score': 0})
        self.users_proxy.create_item({'id': 'user_id_2', 'username': 'lesacafe', 'password': 'ILoveTricia', 'streak': 2, 'daily_training_score': 0})

    # tearDown method executed before each test
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])


    # @unittest.skip
    def test_update_username(self):
        # Try a login with correct credentials
        dict = {"id": "user_id_1", 
                "updates": {
                    'username': 'AntWazHere'
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for success.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Check if the items were updated:
        new_user = self.users_proxy.read_item(item='user_id_1',partition_key='user_id_1')
        username = new_user['username']
        self.assertEqual(username,'AntWazHere')


    # @unittest.skip
    def test_update_password(self):
        # Try a login with correct credentials
        dict = {"id": "user_id_1", 
                "updates": {
                    'password': 'Moon_River'
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for success.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Check if the items were updated:
        new_user = self.users_proxy.read_item(item='user_id_1',partition_key='user_id_1')
        password = new_user['password']
        self.assertEqual(password,'Moon_River')


    # @unittest.skip
    def test_update_streak(self):
        # Try a login with correct credentials
        dict = {"id": "user_id_2", 
                "updates": {
                    'streak': 3
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for success.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Check if the items were updated:
        new_user = self.users_proxy.read_item(item='user_id_2',partition_key='user_id_2')
        streak = new_user['streak']
        self.assertEqual(streak, 3)


    # @unittest.skip
    def test_update_score(self):
        # Try a login with correct credentials
        dict = {"id": "user_id_2", 
                "updates": {
                    'daily_training_score': 400
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for success.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Check if the items were updated:
        new_user = self.users_proxy.read_item(item='user_id_2',partition_key='user_id_2')
        score = new_user['daily_training_score']
        self.assertEqual(score, 400)


    # @unittest.skip
    def test_update_multiple(self):
        # Try a login with correct credentials
        dict = {"id": "user_id_1", 
                "updates": {
                    'username': 'AntWazHere',
                    'password': 'Moon_River'
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for success.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Check if the items were updated:
        new_user = self.users_proxy.read_item(item='user_id_1',partition_key='user_id_1')
        username = new_user['username']
        password = new_user['password']
        self.assertEqual(username, 'AntWazHere')
        self.assertEqual(password, 'Moon_River')

    # @unittest.skip
    def test_nonexistent_user(self):
        # Try a login with incorrect username
        dict = {"id": "user_id_3",
                "updates": {
                    'username': 'Poopoo'
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Unable to retrieve user.')

    # @unittest.skip
    def test_unique_user_error(self):
        # Try a login with incorrect username
        dict = {"id": "user_id_1",
                "updates": {
                    'username': 'lesacafe'
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Username already exists')

    # @unittest.skip
    def test_invalid_username_error(self):
        # Try a login with incorrect username
        dict = {"id": "user_id_1",
                "updates": {
                    'username': 'anto'
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Username less than 5 characters or more than 15 characters')


    # @unittest.skip
    def test_invalid_password_error(self):
        # Try a login with incorrect username
        dict = {"id": "user_id_1",
                "updates": {
                    'password': 'ILov'
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Password less than 8 characters or more than 15 characters')


    # @unittest.skip
    def test_invalid_streak_error(self):
        # Try a login with incorrect username
        dict = {"id": "user_id_1",
                "updates": {
                    'streak': -1
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Invalid streak value.')


    # @unittest.skip
    def test_invalid_score_error(self):
        # Try a login with incorrect username
        dict = {"id": "user_id_1",
                "updates": {
                    'daily_training_score': -1
                }}
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Invalid daily_training_score value.')