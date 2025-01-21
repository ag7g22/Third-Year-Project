import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_search(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_search function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/search"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/search"
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
        # Dummy users as only id and username is needed.
        self.users_proxy.create_item({'id': 'user_id_1', 'username': 'antoni_gn'})
        self.users_proxy.create_item({'id': 'user_id_2', 'username': 'AntWazHere'})
        self.users_proxy.create_item({'id': 'user_id_3', 'username': 'river'})


    # tearDown method executed before each test
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])


    # @unittest.skip
    def test_search_1(self):
        request = { "search": "Ant" }
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the True response for successful search.
        self.assertTrue(dict_response['result'])
        actual_result = dict_response['msg']
        self.assertEqual(actual_result[0]['id'],'user_id_1')
        self.assertEqual(actual_result[1]['id'],'user_id_2')


    # @unittest.skip
    def test_search_2(self):
        request = { "search": "er" }
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the True response for successful search.
        self.assertTrue(dict_response['result'])
        actual_result = dict_response['msg']
        self.assertEqual(actual_result[0]['id'],'user_id_2')
        self.assertEqual(actual_result[1]['id'],'user_id_3')


    def test_search_3(self):
        request = { "search": "" }
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the True response for failed search.
        self.assertTrue(dict_response['result'])