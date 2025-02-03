import unittest
import requests
import json
from azure.cosmos import CosmosClient

class test_user_update_scores(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the user_update_scoresfunction.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/user/update/scores"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/user/update/scores"
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
        self.users_proxy.create_item({'id': 'user_id_1', 'username': 'antoni_gn', 'password': 'ILoveTricia',
                                'friends': [], 'friend_requests': [], 'streak': 0, 'daily_training_score': 0,
                                'recent_category_scores': 
                                    {
                                        'Driving Off': [0.29, 0.07, 0.94, 0.66, 0.11], 
                                        'Urban Driving': [0.03, 0.86, 0.28, 0.13, 0.73], 
                                        'Rural Driving': [0.81, 0.76, 0.57, 0.43, 0.1], 
                                        'Bigger Roads': [0.88, 0.82, 0.38, 0.4, 0.14], 
                                        'Motorways': [0.52, 0.98, 0.79, 0.45, 0.8],
                                        'Tricky Conditions': [0.8, 0.01, 0.22, 0.68, 0.54],
                                        'Breakdowns': [0.99, 0.09, 0.21, 0.77, 0.7]}
                               })
        
        self.users_proxy.create_item({'id': 'user_id_2', 'username': 'AntWazHere', 'password': 'ILoveTricia',
                                'friends': [], 'friend_requests': [], 'streak': 0, 'daily_training_score': 0,
                                'recent_category_scores': 
                                    {
                                        'Driving Off': [0.29, 0.07], 
                                        'Urban Driving': [0.03, 0.86], 
                                        'Rural Driving': [0.81, 0.76], 
                                        'Bigger Roads': [0.88, 0.82], 
                                        'Motorways': [0.52, 0.98],
                                        'Tricky Conditions': [0.8, 0.01],
                                        'Breakdowns': [0.99, 0.09]}
                               })
        
        self.users_proxy.create_item({'id': 'user_id_3', 'username': 'lesacafe', 'password': 'ILoveAnthony',
                                'friends': [], 'friend_requests': [], 'streak': 0, 'daily_training_score': 0,
                                'recent_category_scores': 
                                    {
                                        'Driving Off': [0.29], 
                                        'Urban Driving': [0.03], 
                                        'Rural Driving': [0.81], 
                                        'Bigger Roads': [0.88], 
                                        'Motorways': [0.52],
                                        'Tricky Conditions': [0.8],
                                        'Breakdowns': [0.99]}
                               })
        
        self.users_proxy.create_item({'id': 'user_id_4', 'username': 'rivscafe', 'password': 'ILoveAnthony',
                                'friends': [], 'friend_requests': [], 'streak': 0, 'daily_training_score': 0,
                                'recent_category_scores': 
                                    {
                                        'Driving Off': [0.75, 0.11, 0.42, 0.75, 0.15, 0.36, 0.14, 0.95, 0.32, 0.7], 
                                        'Urban Driving': [0.95, 0.57, 0.69, 0.92, 0.35, 0.44, 0.39, 0.57, 0.51, 0.87], 
                                        'Rural Driving': [0.49, 0.7, 0.69, 0.11, 0.85, 0.52, 0.68, 0.9, 0.08, 0.87], 
                                        'Bigger Roads': [0.86, 0.66, 0.6, 0.76, 0.5, 0.62, 0.35, 0.01, 0.86, 0.75], 
                                        'Motorways': [0.1, 0.64, 0.12, 0.91, 0.42, 0.66, 0.35, 0.82, 0.0, 0.42], 
                                        'Tricky Conditions': [0.4, 0.06, 0.1, 0.99, 0.99, 0.14, 0.97, 0.25, 0.75, 0.82], 
                                        'Breakdowns': [0.03, 0.02, 0.95, 0.72, 0.3, 0.96, 0.2, 0.07, 0.06, 0.22]}
                               })

    # tearDown method executed before each test
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])


    # @unittest.skip
    def test_update_scores_reset(self):
        # Try a login with correct credentials
        dict = {"id": "user_id_4", 
                "updates": {
                    'Driving Off': 0.14, 
                    'Urban Driving': 0.34, 
                    'Rural Driving': 0.45, 
                    'Bigger Roads': 0.03, 
                    'Motorways': 0.53,
                    'Tricky Conditions': 0.50,
                    'Breakdowns': 0.30}
                }
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for success.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Expected update:
        expected_update =   {
                                'Driving Off': [0.11, 0.42, 0.75, 0.15, 0.36, 0.14, 0.95, 0.32, 0.7, 0.14], 
                                'Urban Driving': [0.57, 0.69, 0.92, 0.35, 0.44, 0.39, 0.57, 0.51, 0.87, 0.34], 
                                'Rural Driving': [0.7, 0.69, 0.11, 0.85, 0.52, 0.68, 0.9, 0.08, 0.87, 0.45], 
                                'Bigger Roads': [0.66, 0.6, 0.76, 0.5, 0.62, 0.35, 0.01, 0.86, 0.75, 0.03], 
                                'Motorways': [0.64, 0.12, 0.91, 0.42, 0.66, 0.35, 0.82, 0.0, 0.42, 0.53], 
                                'Tricky Conditions': [0.06, 0.1, 0.99, 0.99, 0.14, 0.97, 0.25, 0.75, 0.82, 0.50], 
                                'Breakdowns': [0.02, 0.95, 0.72, 0.3, 0.96, 0.2, 0.07, 0.06, 0.22, 0.30]
                            }

        # Check if the items were updated:
        new_user = self.users_proxy.read_item(item='user_id_4',partition_key='user_id_4')
        recent_category_scores = new_user['recent_category_scores']
        self.assertEqual(recent_category_scores,expected_update)


    # @unittest.skip
    def test_update_scores(self):
        # Try a login with correct credentials
        dict = {"id": "user_id_1", 
                "updates": {
                    'Driving Off': 0.14, 
                    'Urban Driving': 0.34, 
                    'Rural Driving': 0.45, 
                    'Bigger Roads': 0.03, 
                    'Motorways': 0.53,
                    'Tricky Conditions': 0.50,
                    'Breakdowns': 0.30}
                }
        response = requests.put(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=dict)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()   

        # Check if you got the OK response for success.
        self.assertTrue(dict_response['result'])
        self.assertEqual(dict_response['msg'],'OK')

        # Expected update:
        expected_update =   {
                                'Driving Off': [0.29, 0.07, 0.94, 0.66, 0.11, 0.14], 
                                'Urban Driving': [0.03, 0.86, 0.28, 0.13, 0.73, 0.34], 
                                'Rural Driving': [0.81, 0.76, 0.57, 0.43, 0.1, 0.45], 
                                'Bigger Roads': [0.88, 0.82, 0.38, 0.4, 0.14, 0.03], 
                                'Motorways': [0.52, 0.98, 0.79, 0.45, 0.8, 0.53],
                                'Tricky Conditions': [0.8, 0.01, 0.22, 0.68, 0.54, 0.5],
                                'Breakdowns': [0.99, 0.09, 0.21, 0.77, 0.7, 0.30]
                            }

        # Check if the items were updated:
        new_user = self.users_proxy.read_item(item='user_id_1',partition_key='user_id_1')
        recent_category_scores = new_user['recent_category_scores']
        self.assertEqual(recent_category_scores,expected_update)