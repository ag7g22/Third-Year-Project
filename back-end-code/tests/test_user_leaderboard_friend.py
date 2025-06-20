import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_leaderboard(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_leaderboard function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/leaderboard/friend"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/leaderboard/friend"
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
        self.users_proxy.create_item({'id': 'user_id_1', 'username': 'user_1', 'streak': 15, 'daily_training_score': 600, 'friends': [
            {'id': 'user_id_2', 'username': 'user_2'},
            {'id': 'user_id_3', 'username': 'user_3'},
            {'id': 'user_id_4', 'username': 'user_4'},
            {'id': 'user_id_5', 'username': 'user_5'}
        ]})

        self.users_proxy.create_item({'id': 'user_id_2', 'username': 'user_2', 'streak': 12, 'daily_training_score': 500, 'friends': [
            {'id': 'user_id_1', 'username': 'user_1'},
        ]})
        self.users_proxy.create_item({'id': 'user_id_3', 'username': 'user_3', 'streak': 10, 'daily_training_score': 500, 'friends': [
            {'id': 'user_id_1', 'username': 'user_1'},
        ]})
        self.users_proxy.create_item({'id': 'user_id_4', 'username': 'user_4', 'streak': 60, 'daily_training_score': 200, 'friends': [
            {'id': 'user_id_1', 'username': 'user_1'},
        ]})
        self.users_proxy.create_item({'id': 'user_id_5', 'username': 'user_5', 'streak': 20, 'daily_training_score': 200, 'friends': [
            {'id': 'user_id_1', 'username': 'user_1'},
        ]})

        self.users_proxy.create_item({'id': 'user_id_6', 'username': 'user_6', 'streak': 4, 'daily_training_score': 400})

    # tearDown method executed before each test
    # @unittest.skip
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])

    # @unittest.skip
    def test_leaderboard(self):
        request = {"id": "user_id_1"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the leaderboard.
        print(dict_response['msg'])
        self.assertTrue(dict_response['result'])
        # self.assertEqual(dict_response['msg'],'OK')

    # @unittest.skip
    def test_no_users(self):
        request = {"id": "user_id_7"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for successful login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'No users registered to get leaderboard!')