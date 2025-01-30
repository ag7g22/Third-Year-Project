import unittest
import uuid
import requests
import json
from azure.cosmos import CosmosClient

class test_question_get_category(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the question_get_category function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/question/get/category"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/question/get/category"
    TEST_URL = LOCAL_DEV_URL

    # Configure the Proxy objects from the local.settings.json file.
    with open('local.settings.json') as settings_file:
        settings = json.load(settings_file)
    FUNCTION_KEY = settings['Values']['FunctionAppKey']
    cosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])           # Cosmos Object
    db_proxy = cosmos.get_database_client(settings['Values']['DatabaseName'])                                   # Proxy object for database
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

    # tearDown method executed before each test
    # @unittest.skip
    def tearDown(self) -> None:
        # Get rid of all the items inbetween tests.
        for doc in self.questions_proxy.read_all_items():
            self.questions_proxy.delete_item(item=doc,partition_key=doc['id'])


    def test_questions_get_category_1(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"No_of_Qs": 5, "topic": "Driving Off"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got randomised questions.
        print(dict_response['msg'])
        self.assertTrue(dict_response['result'])


    def test_questions_get_category_2(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"No_of_Qs": 7, "topic": "Breakdowns"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got randomised questions.
        print(dict_response['msg'])
        self.assertTrue(dict_response['result'])