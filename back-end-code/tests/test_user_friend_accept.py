import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_friend_accept(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_friend_accept function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/friend/accept"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/friend/accept"
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
        self.users_proxy.create_item({'id': 'user_id_1', 'username': 'antoni_gn', 'friends': [
            {'id': 'user_id_2', 'username': 'AntWazHere'}
        ], 'friend_requests': [
            {'id': 'user_id_3', 'username': 'river'}
        ]})

        self.users_proxy.create_item({'id': 'user_id_2', 'username': 'AntWazHere', 'friends': [
            {'id': 'user_id_1', 'username': 'antoni_gn'}
        ], 'friend_requests': []})
        
        self.users_proxy.create_item({'id': 'user_id_3', 'username': 'river', 'friends': [], 'friend_requests': []})

    # tearDown method executed before each test
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])

    
    # @unittest.skip
    def test_successful_friend_accept(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"sender_id": "user_id_3", "sender_username": "river", "recipient_id": "user_id_1"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Check if friend was added:
        sender = self.users_proxy.read_item(item="user_id_1",partition_key="user_id_1")
        friends = sender['friends']
        recipient = friends[0]
        self.assertEqual({'id': 'user_id_3', 'username': 'river'}, recipient)


    # @unittest.skip
    def test_accept_already_friends(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"sender_id": "user_id_2", "sender_username": "AntWazHere", "recipient_id": "user_id_1"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Already friends!')


    # @unittest.skip
    def test_accept_no_friend_request(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"sender_id": "user_id_3", "sender_username": "lesacafe", "recipient_id": "user_id_2"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],"Haven't sent friend request!")