import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_friend_all(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_friend_all function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/friend/all"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/friend/all"
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
            {'id': 'user_id_2', 'username': 'AntWazHere'},
            {'id': 'user_id_3', 'username': 'river'},
            {'id': 'user_id_4', 'username': 'lesacafe'}
        ], 'friend_requests': [
            {'id': 'user_id_5', 'username': 'Chaxluc09'},
            {'id': 'user_id_6', 'username': 'Silent4K'},
        ]})

    # tearDown method executed before each test
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])


    # @unittest.skip
    def test_successful_friend_all(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {'username': 'antoni_gn'}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        expected_result =   {
                                'friends': [
                                    {'id': 'user_id_2', 'username': 'AntWazHere'},
                                    {'id': 'user_id_3', 'username': 'river'},
                                    {'id': 'user_id_4', 'username': 'lesacafe'}
                                ], 'friend_requests': [
                                    {'id': 'user_id_5', 'username': 'Chaxluc09'},
                                    {'id': 'user_id_6', 'username': 'Silent4K'},
                                ]
                            }

        self.assertTrue(dict_response['result'])
        self.assertDictEqual(dict_response['msg'],expected_result)


    # @unittest.skip
    def test_unsuccessful_friend_all(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {'username': 'AntWazHere'}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for invalid user.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],"Unable to find user.")