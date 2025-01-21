import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_player_register(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_register function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/register"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/register"
    TEST_URL = LOCAL_DEV_URL

    # Configure the Proxy objects from the local.settings.json file.
    with open('local.settings.json') as settings_file:
        settings = json.load(settings_file)
    FUNCTION_KEY = settings['Values']['FunctionAppKey']
    cosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])           # Cosmos Object
    db_proxy = cosmos.get_database_client(settings['Values']['DatabaseName'])                                   # Proxy object for database
    users_proxy = db_proxy.get_container_client(settings['Values']['UserContainerName'])                        # Proxy obj for "users" container

    # tearDown method executed before each test
    # @unittest.skip
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])

    # @unittest.skip
    def test_register_good_player(self):
        # Send a request to register user. (Input is a dictionary)
        request = {"username": "antoni_gn", "password": "ILoveTricia"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got OK response for valid user.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Test the DB was correctly updated
        query = 'SELECT * FROM player WHERE CONTAINS(player.username, "antoni_gn") AND player.password = "ILoveTricia"'
        query_result = list(self.users_proxy.query_items(query=query, enable_cross_partition_query=True))
        query_result_stripped = [{"username": item['username'], "password": item['password'], 
                                 "streak": item['streak'], "friends": item['friends'], "friend_requests": item['friend_requests'], 
                                 "daily_training_score": item['daily_training_score'], "recent_category_scores": item['recent_category_scores']}
                                 for item in query_result]

        actual_result = query_result_stripped[0]
        expected_result = {'username': 'antoni_gn', 'password': 'ILoveTricia', 'streak': 0, 'friends': [], 'friend_requests': [], 
                           'daily_training_score': 0,
                            'recent_category_scores': {
                                'category_1': [],
                                'category_2': []
                            }}        

        self.assertEqual(actual_result,expected_result)


    # @unittest.skip
    def test_unique_player_error(self):
        # Add user to database.
        self.users_proxy.create_item(
            {  
                'id': 'user_id_1',
                'username': 'antoni_gn', 'password': 'ILoveTricia', 'streak': 0, 'friends': [], 'friend_requests': [], 
                'daily_training_score': 0,
                'recent_category_scores': {
                    'category_1': [],
                    'category_2': []
                }
            } 
        )

        # Send a request to register same user. (Input is a dictionary)
        request = {"username": "antoni_gn", "password": "ILoveTricia"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got error response for already existing user.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Username already exists')


    # @unittest.skip
    def test_short_username_error(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"username": "anto", "password": "ILoveTricia"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got error response for username less than 5 characters.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Username less than 5 characters or more than 15 characters')


    # @unittest.skip
    def test_long_username_error(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"username": "antoni_gnnnnnnnn", "password": "ILoveTricia"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got error response for username more than 15 characters.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Username less than 5 characters or more than 15 characters')


    # @unittest.skip
    def test_short_password_error(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"username": "antoni_gn", "password": "ILoveTr"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got error response for password less than 8 characters.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Password less than 8 characters or more than 15 characters')


    # @unittest.skip
    def test_long_password_error(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"username": "antoni_gn", "password": "ILoveTriciaaaaaa"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got error response for password less than 8 characters.
        self.assertFalse(dict_response['result'])
        self.assertEqual(dict_response['msg'],'Password less than 8 characters or more than 15 characters')