import unittest
import requests
import json
import uuid
import random
from azure.cosmos import CosmosClient

class test_user_get_info(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_get_info function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/get/info"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/get/info"
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
        """
        user = {'id': 'user_id_1', 'username': 'antoni_gn', 'rank': { 'level': 1, 'exp': 0, 'exp_threshold': 10000 },
                               'streak': 0, 'daily_training_score': 0, 'training_completion_date': 'n/a', 'achievements': [] }
        
        self.users_proxy.create_item(user)
        """

        test_user_1 = {'id': str(uuid.uuid4()), 'username': 'antoni_gn', 'password': 'ILoveTricia',
                               'friends': [], 'friend_requests': [], 'rank': { 'level': 15, 'exp': 7500, 'exp_threshold': 16000 },
                               'streak': 5, 'daily_training_score': 7500, 'training_completion_date': '16/02/2025', 
                               'achievements': [
                                   'Hello World!', 'Start of a Journey', 'Levelin up', 'Gear 2nd'
                                   ],
                                'recent_category_scores': {
                                    "Driving Off": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Urban Driving": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Rural Driving": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Bigger Roads": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Motorways": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Tricky Conditions": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Breakdowns": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                }}
        
        test_user_2 = {'id': str(uuid.uuid4()), 'username': 'lesacafe', 'password': 'ILoveAnthony',
                               'friends': [], 'friend_requests': [], 'rank': { 'level': 16, 'exp': 12500, 'exp_threshold': 17000 },
                               'streak': 75, 'daily_training_score': 6000, 'training_completion_date': '16/02/2025', 
                               'achievements': [
                                   'Hello World!', 'Start of a Journey', 'Levelin up', 'Gear 2nd', 'Gear 3rd'
                                   ],
                                'recent_category_scores': {
                                    "Driving Off": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Urban Driving": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Rural Driving": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Bigger Roads": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Motorways": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Tricky Conditions": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Breakdowns": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                }}
        
        test_user_3 = {'id': str(uuid.uuid4()), 'username': 'Chaxluc09', 'password': 'Cuphead09',
                               'friends': [], 'friend_requests': [], 'rank': { 'level': 6, 'exp': 12500, 'exp_threshold': 7000 },
                               'streak': 10, 'daily_training_score': 2500, 'training_completion_date': '16/02/2025', 
                               'achievements': [
                                   'Hello World!', 'Start of a Journey', 'Gear 2nd'
                                   ],
                                'recent_category_scores': {
                                    "Driving Off": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Urban Driving": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Rural Driving": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Bigger Roads": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Motorways": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Tricky Conditions": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Breakdowns": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                }}
        
        test_user_4 = {'id': str(uuid.uuid4()), 'username': 'Potato', 'password': 'MarvieHinj',
                               'friends': [], 'friend_requests': [], 'rank': { 'level': 11, 'exp': 12500, 'exp_threshold': 7000 },
                               'streak': 16, 'daily_training_score': 4500, 'training_completion_date': '16/02/2025', 
                               'achievements': [
                                   'Hello World!', 'Start of a Journey', 'Levelin up', 'Gear 2nd'
                                   ],
                                'recent_category_scores': {
                                    "Driving Off": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Urban Driving": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Rural Driving": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Bigger Roads": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Motorways": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Tricky Conditions": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                    "Breakdowns": [round(random.uniform(0.5,1.01), 2) for _ in range(10)],
                                }}

        self.users_proxy.create_item(test_user_1)
        self.users_proxy.create_item(test_user_2)
        self.users_proxy.create_item(test_user_3)
        self.users_proxy.create_item(test_user_4)

    # tearDown method executed before each test
    @unittest.skip
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])

    @unittest.skip
    def test_successful_info(self):
        # Try a login with correct credentials
        dict_login = {"username": "antoni_gn"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict_login)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        expected_info = {'id': 'user_id_1', 'username': 'antoni_gn', 'rank': { 'level': 1, 'exp': 0, 'exp_threshold': 10000 },
                               'streak': 0, 'daily_training_score': 0, 'training_completion_date': 'n/a', 'achievements': [] }

        # Check if you got the OK response for successful login.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],expected_info)

    @unittest.skip
    def test_nonexistent_user(self):
        # Try a login with incorrect username
        dict_login = {"username": "dddddddd"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict_login)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Unable to retrieve user.')

    def test(self):
        pass