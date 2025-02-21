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

topic = "Driving Off"

questions = [
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you need to wear glasses for driving, it's illegal to drive without them. you must be able to see claerly when you're driving.",
        "questions": [
            "You're about to drive your car. What should you do if you can't find the glasses you need to wear?",
            "How should you handle the situation if you can't find your glasses before driving?",
            "If you're about to drive and realize you don't have your glasses, how should you proceed?",
            "What actions should you take if you can't find your glasses while preparing to drive?",
            "What's the best course of action if you can't find your glasses for driving?"
        ], 
        "correct_answers": [
            "Find a way of getting home without driving.",
            "Look for a way to return home without driving.",
            "Find an alternative method to get home without using a car.",
            "Seek an alternative way to get home without driving.",
            "Figure out a way to get home without driving."
        ],
        "incorrect_answers": [
            "Borrow a friend's glasses and use those.",
            "Drive home at night, so that the lights will help you.",
            "Drive home slowly, keeping to quiet roads.",
            "Use a spare pair of old prescription glasses that don't fit properly.",
            "Don't worry about it, just rely on your memory of the road.",
            "Wait until it gets dark and then drive without your glasses.",
            "Ignore the issue and drive, hoping you'll be fine without your glasses.",
            "Drive in the opposite direction to look for your glasses.",
            "Use your phone to find your glasses while driving."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Any load will have an effect on the handling of your vehicle, and this becomes worse as you increase the load. You need to be aware of this when carrying passengers or heavy loads, fitting a roof rack or towing a trailer.",
        "questions": [
            "What would be affected if you carry a very heavy load on your vehicle?",
            "What would be impacted by carrying a heavy load  on your vehicle?",
            "What could be compromised if you carry a very heavy load in your vehicle?",
            "What issues might arise from carrying a load that's too heavy for your vehicle?",
            "What could be affected by overloading your vehicle?"
        ], 
        "correct_answers": [
            "The vehicle's handling.",
            "The vehicle's steering.",
            "The vehicle's manoeuvring.",
        ],
        "incorrect_answers": [
            "The vehicle's battery.",
            "The vehicle's gearbox.",
            "The vehicle's ventilation.",
            "The vehicle's battery.",
            "The vehicle brakes.",
            "The vehicle's wheels.",
            "The vehicle's heating.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Any load will have an effect on the handling of your vehicle, and this becomes worse as you increase the load. You need to be aware of this when carrying passengers or heavy loads, fitting a roof rack or towing a trailer.",
        "questions": [
            "What would be affected if you carry a very heavy load on your vehicle?",
            "What would be impacted by carrying a heavy load on your vehicle?",
            "What could be compromised if you carry a very heavy load in your vehicle?",
            "What issues might arise from carrying a load that's too heavy for your vehicle?",
            "What could be affected by overloading your vehicle?"
        ], 
        "correct_answers": [
            "The vehicle's handling.",
            "The vehicle's steering.",
            "The vehicle's manoeuvring.",
        ],
        "incorrect_answers": [
            "The vehicle's battery.",
            "The vehicle's gearbox.",
            "The vehicle's ventilation.",
            "The vehicle's battery.",
            "The vehicle brakes.",
            "The vehicle's wheels.",
            "The vehicle's heating.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Although a convex mirror gives a wide view of the scene behind, you should be aware that it won't show you everything behind or to the side of your vehicle. Before you move off, you'll need to look over your shoulder to check for everything not visible in the mirrors.",
        "questions": [
            "Why are vehicle mirrors often slightly curved (convex)?",
            "Why are car mirrors often designed with a convex shape?",
            "How does the convex shape of vehicle mirrors benefit drivers?",
            "What is the purpose of vehicle mirrors being slightly convex?",
            "What advantage does a convex mirror provide in vehicles?"
        ], 
        "correct_answers": [
            "They give a wider field of vision.",
            "They reduce blind spots by offering a wider angle.",
            "They improve rear and side visibility.",
            "They help cover a larger area in the reflection."
        ],
        "incorrect_answers": [
            "They totally cover blind spots.",
            "They make the traffic behind look bigger.",
            "They make it easier to judge the speed of the traffic behind.",
            "To make objects appear larger than they really are.",
            "Because curved mirrors are easier to clean than flat ones.",
            "So drivers can see around corners without turning.",
            "To reduce the amount of light reflected and prevent glare.",
            "To distort the view and make driving more challenging."
        ],
    }
]