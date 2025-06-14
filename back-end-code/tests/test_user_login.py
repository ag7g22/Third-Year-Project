import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_login(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_login function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/login"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/login"
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

    # tearDown method executed before each test
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])

    
    def test_successful_login(self):
        # Try a login with correct credentials
        dict_login = {"username": "antoni_gn", "password": "ILoveTricia"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict_login)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for successful login.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')


    def test_wrong_username(self):
        # Try a login with incorrect username
        dict_login = {"username": "lesacafe", "password": "ILoveTricia"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict_login)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Username or password incorrect')


    def test_wrong_password(self):
        # Try a login with incorrect password
        dict_login = {"username": "antoni_gn", "password": "ILoveTrisha"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict_login)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the error response for failed login.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Username or password incorrect')