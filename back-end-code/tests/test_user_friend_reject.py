import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_friend_reject(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_friend_reject function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/friend/reject"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/friend/reject"
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
        # Dummy users as only id, username, friends and friend_requests are needed.
        self.users_proxy.create_item({'id': 'user_id_1', 'username': 'antoni_gn', 'friends': [], 'friend_requests': []})

        self.users_proxy.create_item({'id': 'user_id_2', 'username': 'AntWazHere', 'friends': [], 'friend_requests': [
            {'id': 'user_id_1', 'username': 'antoni_gn'}
        ]})
        
        self.users_proxy.create_item({'id': 'user_id_3', 'username': 'river', 'friends': [
            {'id': 'user_id_1', 'username': 'antoni_gn'},
            {'id': 'user_id_5', 'username': 'Chaxluc09'}
        ], 'friend_requests': []})

        self.users_proxy.create_item({'id': 'user_id_4', 'username': 'lesacafe', 'friends': [], 'friend_requests': [
            {'id': 'user_id_2', 'username': 'AntWazHere'}
        ]})
        
        self.users_proxy.create_item({'id': 'user_id_5', 'username': 'Chaxluc09', 'friends': [
            {'id': 'user_id_3', 'username': 'river'}
        ], 'friend_requests': [
            {'id': 'user_id_1', 'username': 'antoni_gn'}
        ]})

    # tearDown method executed before each test
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])

    
    # @unittest.skip
    def test_successful_friend_reject(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"sender_id": "user_id_1", "sender_username": "antoni_gn", "recipient_id": "user_id_2"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Check if friend request was removed:
        sender = self.users_proxy.read_item(item="user_id_2",partition_key="user_id_2")
        friend_requests = sender['friend_requests']
        self.assertEqual([], friend_requests)


    # @unittest.skip
    def test_accept_already_removed(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"sender_id": "user_id_1", "sender_username": "antoni_gn", "recipient_id": "user_id_4"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],"Haven't sent friend request!")


    # @unittest.skip
    def test_accept_already_friends(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"sender_id": "user_id_1", "sender_username": "antoni_gn", "recipient_id": "user_id_3"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()

        # Check if you actually got OK response for valid user.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],"Already friends!")