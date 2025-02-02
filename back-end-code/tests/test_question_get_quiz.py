import unittest
import uuid
import requests
import json
from azure.cosmos import CosmosClient

class test_question_get_quiz(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the test_question_get_quiz function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/question/get/quiz"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/question/get/quiz"
    TEST_URL = LOCAL_DEV_URL

    # Configure the Proxy objects from the local.settings.json file.
    with open('local.settings.json') as settings_file:
        settings = json.load(settings_file)
    FUNCTION_KEY = settings['Values']['FunctionAppKey']
    cosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])           # Cosmos Object
    db_proxy = cosmos.get_database_client(settings['Values']['DatabaseName'])                                   # Proxy object for database
    users_proxy = db_proxy.get_container_client(settings['Values']['UserContainerName'])                        # Proxy obj for "users" container
    questions_proxy = db_proxy.get_container_client(settings['Values']['QuestionContainerName'])                # Proxy obj for "questions" container

    # SetUp method executed before each test
    # @unittest.skip       
    def setUp(self):
        # Dummy questions
        for i in range(1,8):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Driving Off",
                                                    "image": "n/a",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })
            
        for i in range(8,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Driving Off",
                                                    "image": "image.jpg",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                            "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                                })

        for i in range(1,8):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Urban Driving",
                                                    "image": "n/a",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })
            
        for i in range(8,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Urban Driving",
                                                    "image": "image.jpg",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                            "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                                })

        for i in range(1,8):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Rural Driving",
                                                    "image": "n/a",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })
            
        for i in range(8,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Rural Driving",
                                                    "image": "image.jpg",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                            "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                                })

        for i in range(1,8):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Bigger Roads",
                                                    "image": "n/a",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })
            
        for i in range(8,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Bigger Roads",
                                                    "image": "image.jpg",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                            "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                                })

        for i in range(1,8):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Motorways",
                                                    "image": "n/a",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })
            
        for i in range(8,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Motorways",
                                                    "image": "image.jpg",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                            "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                                })

        for i in range(1,8):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Tricky Conditions",
                                                    "image": "n/a",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })
            
        for i in range(8,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Tricky Conditions",
                                                    "image": "image.jpg",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                            "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                                })

        for i in range(1,8):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Breakdowns",
                                                    "image": "n/a",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })
            
        for i in range(8,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Breakdowns",
                                                    "image": "image.jpg",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                            "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                                })
            
        self.users_proxy.create_item({'id': 'user_id_1', 'username': 'antoni_gn', 'password': 'ILoveTricia',
                                'friends': [], 'friend_requests': [], 'streak': 0, 'daily_training_score': 0,
                                'recent_category_scores': {'Driving Off': [0.29, 0.07, 0.94, 0.66, 0.11], 'Urban Driving': [0.03, 0.86, 0.28, 0.13, 0.73], 'Rural Driving': [0.81, 0.76, 0.57, 0.43, 0.1], 'Bigger Roads': [0.88, 0.82, 0.38, 0.4, 0.14], 'Motorways': [0.52, 0.98, 0.79, 0.45, 0.8], 'Tricky Conditions': [0.8, 0.01, 0.22, 0.68, 0.54], 'Breakdowns': [0.99, 0.09, 0.21, 0.77, 0.7]}
                               })

    # tearDown method executed before each test
    # @unittest.skip
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.users_proxy.read_all_items():
            self.users_proxy.delete_item(item=doc,partition_key=doc['id'])
        for doc in self.questions_proxy.read_all_items():
            self.questions_proxy.delete_item(item=doc,partition_key=doc['id'])

    # @unittest.skip
    def test_questions_get_all_1(self):
        # Send a request to register same user. (Input is a dictionary)
        request =   { "No_of_Qs": 50, "username": "antoni_gn" }
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got randomised questions.
        print(dict_response['msg'])
        self.assertTrue(dict_response['result'])

    @unittest.skip
    def test_questions_get_random(self):
        # Send a request to register same user. (Input is a dictionary)
        request =   { "No_of_Qs": 40, "username": "n/a" }
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got randomised questions.
        # print(dict_response['msg'])
        self.assertTrue(dict_response['result'])