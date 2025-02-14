import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_friend_remove(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_friend_remove function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/friend/remove"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/friend/remove"
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
            { "id": 'user_id_2', 'username': 'AntWazHere'} 
        ], 'friend_requests': []})

        self.users_proxy.create_item({'id': 'user_id_2', 'username': 'AntWazHere', 'friends': [
            { "id": 'user_id_1', 'username': 'antoni_gn'},   
            { "id": 'user_id_3', 'username': 'river'}  
        ], 'friend_requests': []})
        
        self.users_proxy.create_item({'id': 'user_id_3', 'username': 'river', 'friends': [
            { "id": 'user_id_2', 'username': 'AntWazHere'}
        ], 'friend_requests': []})

    # tearDown method executed before each test
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])


    def test_remove_friend(self):
        # Send a request.
        request = {"id_1": "user_id_1", "id_2": "user_id_2"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Check if friend was removed:
        user_1 = self.users_proxy.read_item(item="user_id_1",partition_key="user_id_1")
        user_1_friends = user_1['friends']
        self.assertEqual([], user_1_friends)

        user_2 = self.users_proxy.read_item(item="user_id_2",partition_key="user_id_2")
        user_2_friends = user_2['friends']
        self.assertEqual([{ "id": 'user_id_3', 'username': 'river'}], user_2_friends)


    def test_remove_non_friend(self):
        # Send a request.
        request = {"id_1": "user_id_1", "id_2": "user_id_3"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Users are not friends.')