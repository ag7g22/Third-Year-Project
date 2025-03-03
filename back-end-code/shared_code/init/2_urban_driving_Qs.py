import uuid
import json
from azure.cosmos import CosmosClient

# Configure the Proxy objects from the local.settings.json file.
with open('local.settings.json') as settings_file:
    settings = json.load(settings_file)
FUNCTION_KEY = settings['Values']['FunctionAppKey']
cosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])           # Cosmos Object
db_proxy = cosmos.get_database_client(settings['Values']['DatabaseName'])                                   # Proxy object for database
questions_proxy = db_proxy.get_container_client(settings['Values']['QuestionContainerName'])                # Proxy obj for "questions" container

topic = "Urban Driving"

questions = [
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "This is the explanation.",
        "questions": [

        ], 
        "correct_answers": [

        ],
        "incorrect_answers": [
            
        ]
    }
]

def count_unwritten_questions():
    count = 0
    for d in questions:
        if d.get("explanation") == "This is the explanation.":
            count += 1
    return count

def main():
    print("Compiling {} questions ...".format(len(questions)))

    unwritten_count = count_unwritten_questions()
    written_count = len(questions) - unwritten_count

    print("Written questions: {}, Unwritten questions: {}".format(written_count, unwritten_count))

    if unwritten_count == 0:
        for question in questions:
            questions_proxy.create_item(question)

        print("Questions upload completed.")
    else: 
        print("Questions upload failed.")

if __name__ == "__main__":
    main()