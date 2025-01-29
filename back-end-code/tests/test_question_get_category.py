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
        for i in range(1,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SOq{}a".format(i), "SOq{}b".format(i), "SOq{}c".format(i), "SOq{}d".format(i)], "topic": "Setting Off",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })

        for i in range(1,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["CSq{}a".format(i), "CSq{}b".format(i), "CSq{}c".format(i), "CSq{}d".format(i)], "topic": "City Streets",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })

        for i in range(1,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["SRq{}a".format(i), "SRq{}b".format(i), "SRq{}c".format(i), "SRq{}d".format(i)], "topic": "Scenic Routes",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })

        for i in range(1,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["BRq{}a".format(i), "BRq{}b".format(i), "BRq{}c".format(i), "BRq{}d".format(i)], "topic": "Bigger Roads",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })

        for i in range(1,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["Mq{}a".format(i), "Mq{}b".format(i), "Mq{}c".format(i), "Mq{}d".format(i)], "topic": "Motorways",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })

        for i in range(1,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["TCq{}a".format(i), "TCq{}b".format(i), "TCq{}c".format(i), "TCq{}d".format(i)], "topic": "Tricky Conditions",
                                                    "correct_answers": ["CORRECT{}a".format(i), "CORRECT{}b".format(i), "CORRECT{}c".format(i), "CORRECT{}d".format(i)],
                                                    "incorrect_answers": ["WRONG{}a".format(i), "WRONG{}b".format(i), "WRONG{}c".format(i), "WRONG{}d".format(i),
                                                                          "WRONG{}e".format(i), "WRONG{}f".format(i), "WRONG{}g".format(i), "WRONG{}h".format(i)]
                                              })

        for i in range(1,11):
            self.questions_proxy.create_item({"id": str(uuid.uuid4()), "questions": ["Bq{}a".format(i), "Bq{}b".format(i), "Bq{}c".format(i), "Bq{}d".format(i)], "topic": "Breakdowns",
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


    def test_questions_get_category(self):
        # Send a request to register same user. (Input is a dictionary)
        request = {"No_of_Qs": 5, "topic": "Setting Off"}
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got randomised questions.
        print(dict_response['msg'])
        self.assertTrue(dict_response['result'])