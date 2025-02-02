import unittest
import uuid
import requests
import json
from azure.cosmos import CosmosClient

class test_question_get_feedback(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the question_get_feedback function.
    """
    # URLS to test on
    LOCAL_DEV_URL = "http://localhost:7071/question/get/feedback"
    PUBLIC_URL = "https://driving-theory.azurewebsites.net/question/get/feedback"
    TEST_URL = LOCAL_DEV_URL

    # Configure the Proxy objects from the local.settings.json file.
    with open('local.settings.json') as settings_file:
        settings = json.load(settings_file)
    FUNCTION_KEY = settings['Values']['FunctionAppKey']
    cosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])           # Cosmos Object
    db_proxy = cosmos.get_database_client(settings['Values']['DatabaseName'])                                   # Proxy object for database
    questions_proxy = db_proxy.get_container_client(settings['Values']['QuestionContainerName'])                # Proxy obj for "questions" container

    input = { "incorrect_answers": 
                [
                    { 
                        "question": "What does a Yield sign indicate to a driver?",
                        "correct_ans": "You must slow down and give the right-of-way to other vehicles or pedestrians.",
                        "incorrect_ans": "You must come to a complete stop before proceeding."  
                    },
                    { 
                        "question": "What must a driver do at a STOP sign?",
                        "correct_ans": "Come to a complete stop and proceed when safe.",
                        "incorrect_ans": "Honk before proceeding."  
                    },
                    { 
                        "question": "What does a No U-Turn sign mean?",
                        "correct_ans": "Making a U-turn is prohibited in this area.",
                        "incorrect_ans": "The speed limit is only for trucks."  
                    },
                    { 
                        "question": "What does a Speed Limit 55 mph sign mean?",
                        "correct_ans": "You cannot exceed 55 mph, but you may drive slower if necessary.",
                        "incorrect_ans": "You must come to a complete stop before proceeding."  
                    },
                    { 
                        "question": "What should a driver do when approaching a Pedestrian Crossing sign?",
                        "correct_ans": "Slow down, be alert, and stop if pedestrians are crossing.",
                        "incorrect_ans": "Stop only if pedestrians wave at you."  
                    },
                    { 
                        "question": "What does a Slippery When Wet sign warn drivers about?",
                        "correct_ans": "The road may be slippery in wet conditions.",
                        "incorrect_ans": "You should stop driving when it's raining."  
                    },
                    { 
                        "question": "What does a One-Way sign indicate?",
                        "correct_ans": "You must only drive in the direction indicated by the sign.",
                        "incorrect_ans": "You can drive in either direction on this road."  
                    },
                    { 
                        "question": "What should a driver do when approaching a Railroad Crossing sign?",
                        "correct_ans": "Slow down, look, listen, and be prepared to stop if necessary.",
                        "incorrect_ans": "Ignore the sign if no other vehicles are stopping."  
                    },
                    { 
                        "question": "What should you do if you see a school bus with flashing red lights and an extended stop sign?",
                        "correct_ans": "Stop and remain stopped until the lights stop flashing and the sign retracts.",
                        "incorrect_ans": "Slow down and pass carefully."  
                    },
                    { 
                        "question": "What does a solid yellow line on your side of the road indicate?",
                        "correct_ans": "No passing is allowed.",
                        "incorrect_ans": "Passing is allowed only when there is no oncoming traffic."  
                    },
                    { 
                        "question": "When approaching an intersection with a flashing yellow light, you should:",
                        "correct_ans": "Slow down and proceed with caution.",
                        "incorrect_ans": "Stop immediately."  
                    },
                    { 
                        "question": "When driving in heavy rain, what should you do?",
                        "correct_ans": "Slow down and use windshield wipers.",
                        "incorrect_ans": "Use high-beam headlights."  
                    },
                    { 
                        "question": "When should you turn on your headlights?",
                        "correct_ans": "Whenever visibility is poor, such as rain, fog, or dusk.",
                        "incorrect_ans": "Only at night."  
                    },
                    { 
                        "question": "What is the best way to handle a skid on a slippery road?",
                        "correct_ans": "Steer in the direction you want to go and ease off the gas.",
                        "incorrect_ans": "Slam on the brakes."  
                    },
                    { 
                        "question": "When two vehicles arrive at a four-way stop at the same time, who has the right of way?",
                        "correct_ans": "The vehicle on the right.",
                        "incorrect_ans": "The vehicle on the left."  
                    },
                    { 
                        "question": "When making a left turn at an intersection, you must yield to:",
                        "correct_ans": "Vehicles going straight and pedestrians.",
                        "incorrect_ans": "No one, because you have the right of way."  
                    },
                    { 
                        "question": "When driving on a highway with a speed limit of 65 mph, but traffic is moving at 55 mph, you should:",
                        "correct_ans": "Drive at the same speed as traffic.",
                        "incorrect_ans": "Drive at 65 mph to follow the speed limit."  
                    },
                    { 
                        "question": "If a pedestrian is crossing the street at an unmarked crosswalk, you should:",
                        "correct_ans": "Stop and let them cross.",
                        "incorrect_ans": "Honk to warn them."  
                    },
                    { 
                        "question": "If another driver is tailgating you, what is the safest action to take?",
                        "correct_ans": "Move to another lane or let them pass.",
                        "incorrect_ans": "Ignore them and maintain your speed."  
                    },
                    { 
                        "question": "If an emergency vehicle with flashing lights is approaching from behind, you must:",
                        "correct_ans": "Speed up to avoid blocking it.",
                        "incorrect_ans": "Pull over to the right and stop."  
                    },
                    { 
                        "question": "When parking uphill with a curb, which way should you turn your wheels?",
                        "correct_ans": "Away from the curb.",
                        "incorrect_ans": "Straight ahead."  
                    },

                ] 
    }
    
    # SetUp method executed before each test
    # @unittest.skip       
    def setUp(self):
        pass

    # tearDown method executed before each test
    # @unittest.skip
    def tearDown(self) -> None:
        pass


    def test_questions_get_category_1(self):
        # Send a request to register same user. (Input is a dictionary)
        request = self.input
        response = requests.post(self.TEST_URL,params={"code": self.FUNCTION_KEY},json=request)

        # Get json response, check the response code for brevity
        self.assertEqual(200,response.status_code)
        dict_response = response.json()     

        # Check if you actually got randomised questions.
        print(dict_response['msg'])
        self.assertTrue(dict_response['result'])