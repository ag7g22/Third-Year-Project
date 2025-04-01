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

topic = "Tricky Conditions"

questions = [
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you have to park your vehicle in foggy conditions, try to find a place to park off the road. If this isn't possible, park on the road facing in the same direction as the traffic. Leave your parking lights switched on and make sure they're clean.",
        "questions": [
            "What should you do if you park on the road when it's foggy?",
            "How should you park your vehicle in foggy conditions?",
            "If you're parking on the road in foggy weather, what should you do?",
            "When parking on a road in fog, what is the best practice?",
            "What action should you take when parking on the road during foggy conditions?"
        ],
        "correct_answers": [
            "Leave parking lights switched on.",
            "Turn on your parking lights.",
            "Leave your parking lights are on.",
            "Switch on your parking lights."
        ],
        "incorrect_answers": [
            "Leave main-beam headlights switched on.",
            "Leave dipped headlights switched on.",
            "Leave dipped headlights and fog lights switched on.",
            "Switch on your hazard warning lights.",
            "Turn on your fog lights and keep your main-beam headlights on."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you're planning to make a journey when it's foggy, listen to the weather reports. If visibility is very poor, avoid making unnecessary journeys. If you do travel, leave plenty of time - and if someone is waiting for you to arrive, let them know that your journey will take longer than normal. This will also take off any pressure you may feel to rush.",
        "questions": [
            "What should you do if you have to make a journey in foggy conditions?",
            "How should you prepare for a journey when it's foggy?",
            "What is the best approach for a journey in foggy weather?",
            "If you're planning a trip in foggy conditions, what should you do?",
            "When driving in fog, what preparation should you make for your journey?"
        ],
        "correct_answers": [
            "Leave plenty of time for your journey.",
            "Give yourself extra time to complete your journey.",
            "Allow more time for your journey.",
            "Plan your journey and allow for extra time.",
            "Take extra time for your trip."
        ],
        "incorrect_answers": [
            "Avoid using dipped headlights.",
            "Keep two seconds behind the vehicle ahead.",
            "Follow other vehicles' tail lights closely.",
            "Drive faster to minimize the time spent in fog.",
            "Only use your fog lights when you can't see the road ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Your headlights and tail lights help others on the road to see you. It may be headlights during the day if visibility is reduced; for example, due to heavy rain. In these conditions, the light might fade before the street lights are timed to switch on. Be seen to be safe.",
        "questions": [
            "Why should you switch your headlights on when it first starts to get dark?",
            "What is the reason for turning on your headlights when the daylight begins to fade?",
            "Why is it important to turn your headlights on when dusk sets in?",
            "When the light starts to dim, why should you use your headlights?",
            "Why is it a good idea to turn on your headlights as it begins to get dark?"
        ],
        "correct_answers": [
            "So others can see you more easily.",
            "To increase your visibility to other drivers.",
            "To help other road users see you more clearly.",
            "To ensure you're visible to other vehicles.",
            "To make yourself more noticeable to other drivers."
        ],
        "incorrect_answers": [
            "To make your dials easier to use.",
            "So that you can blend in with other drivers.",
            "Because the street lights are lit.",
            "To signal to other drivers you're slowing down.",
            "To improve your car's fuel efficiency."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You must make sure that other road users can see you, but you don't want to dazzle them. Use your dipped headlights during the day if visibility is poor. If visibility falls below 100 metres (328 feet), you may use your rear fog lights but don't forget to turn them off when visibility improves.",
        "questions": [
            "You're driving in heavy traffic on a wet road. Which lights should you use if there's a lot of surface spray?",
            "Which lights are best to use in heavy traffic when the road is wet and surface spray is present?",
            "What headlights should you turn on while driving in wet conditions with heavy traffic and surface spray?",
            "When driving on a wet road with surface spray and heavy traffic, which lights should you switch on?",
            "Which lights should be used when driving on a wet road with lots of spray in traffic?"
        ],
        "correct_answers": [
            "Dipped headlights.",
            "Dipped headlights."
        ],
        "incorrect_answers": [
            "Rear fog lights if visibility is more than 100 metres (328 feet).",
            "Sidelights only.",
            "Main-beam headlights.",
            "No lights at all.",
            "Daytime running lights only."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Cyclists, and motorcyclists, are very vulnerable in high winds. They can easily be blown well off course and veer into your path. Always allow plenty of room when overtaking them. Passing too close could cause a draught and unbalance the rider.",
        "questions": [
            "What should you do if you overtake a cyclist when it's windy?",
            "How should you overtake a cyclist during windy conditions?",
            "What precaution should you take when overtaking a cyclist in strong winds?",
            "When overtaking a cyclist in gusty weather, what should you do?",
            "What is the safest way to overtake a cyclist on a windy day?"
        ],
        "correct_answers": [
            "Allow extra room.",
            "Give the cyclist more space.",
            "Leave plenty of space when passing.",
            "Increase the gap between you and the cyclist.",
            "Maintain a safe distance from the cyclist."
        ],
        "incorrect_answers": [
            "Sound your horn repeatedly.",
            "Overtake very slowly.",
            "Keep close as you pass.",
            "Speed up to pass quickly.",
            "Move closer to the cyclist for better control."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Rear fog lights make it easier to spot a vehicle ahead in foggy conditions. Avoid the temptation to use another vehicles' lights as a guide, as may give you a false sense of security.",
        "questions": [
            "Why are vehicles fitted with rear fog lights?",
            "What is the purpose of rear fog lights on a vehicle?",
            "Why do some vehicles have rear fog lights?",
            "When should you use rear fog lights on your vehicle?",
            "What is the main function of rear fog lights?"
        ],
        "correct_answers": [
            "To make them more visible in thick fog.",
            "To improve visibility in dense fog.",
            "To ensure other drivers can see them in heavy fog.",
            "To enhance visibility during foggy conditions.",
            "To alert other road users of your presence in fog."
        ],
        "incorrect_answers": [
            "To make them more visible when driving at high speed.",
            "To warn drivers following closely to drop back.",
            "To show when they've broken down in a dangerous position.",
            "To indicate that the vehicle is reversing.",
            "To improve visibility at night regardless of fog."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Drive extremely carefully when the roads are icy. When travelling on ice, tyres make virtually no noise and steering feels light and unresponsive. In icy conditions, be very gentle when braking, accelerating and steering.",
        "questions": [
            "What would suggest you're driving on an icy road?",
            "What is a sign that the road might be icy while driving?",
            "How can you tell that the road surface is icy when driving?",
            "What is an indication that your vehicle is moving on ice?",
            "Which of the following suggests icy road conditions while driving?"
        ],
        "correct_answers": [
            "There's less tyre noise.",
            "There's less tyre noise."
        ],
        "incorrect_answers": [
            "There's less wind noise.",
            "There's less transmission noise.",
            "There's engine noise.",
            "There's increased engine vibration.",
            "There's a loud hum from the tyres."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Harsh use of the accelerator, brakes or steering is likely to lead to skidding, especially on slippery surfaces. Avoid steering and braking at the same time. In icy conditions, you must constantly assess what's ahead so that you can take appropriate action in time.",
        "questions": [
            "You're driving in freezing conditions. What should you do as you approach a sharp bend?",
            "What is the safest way to approach a sharp bend when driving in freezing conditions?",
            "How should you prepare to take a sharp bend on an icy road?",
            "What action should you take when approaching a bend in freezing weather?",
            "When driving in icy conditions, what should you do before a sharp turn?"
        ],
        "correct_answers": [
            "Slow down gently.",
            "Reduce your speed carefully.",
            "Ease off the accelerator smoothly.",
            "Decrease your speed gradually.",
            "Approach slowly to maintain control."
        ],
        "incorrect_answers": [
            "Coast into the bend.",
            "Firmly use your footbrake.",
            "Apply your parking brake.",
            "Accelerate through the bend.",
            "Maintain a high speed to avoid skidding."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You must use dipped headlights when daytime visibility is seriously reduced, generally to 100 metres (328 feet) or less. You may also use front or rear fog lights, but they must be switched off when visibility improves.",
        "questions": [
            "When must you use dipped headlights during the day?",
            "In which situation should you use dipped headlights during daylight hours?",
            "When are dipped headlights required while driving in the daytime?",
            "During the day, when is it necessary to turn on dipped headlights?",
            "Under what circumstances should you use dipped headlights in daylight?"
        ],
        "correct_answers": [
            "When you're driving in poor visibility.",
            "In conditions of reduced visibility.",
            "When visibility is significantly reduced.",
            "During periods of poor visibility.",
            "When it is difficult to see other vehicles or be seen."
        ],
        "incorrect_answers": [
            "When you're driving along narrow streets.",
            "When you're parking.",
            "All the time you're driving.",
            "Only when you're overtaking.",
            "When approaching traffic lights."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you're driving behind other traffic on the motorway at night, use dipped headlights. Main-beam headlights will dazzle the other drivers. Your headlights' dipped beam should fall short of the vehicle in front.",
        "questions": [
            "You're driving on a motorway at night. Which lights should you have on if there are other vehicles just ahead of you?",
            "What lights should you use on a motorway at night when following other vehicles?",
            "When driving behind other vehicles on a motorway at night, which headlights should be on?",
            "Which lights should you use when driving on a motorway at night with traffic ahead?",
            "When other vehicles are just ahead on a motorway at night, which lights are appropriate?"
        ],
        "correct_answers": [
            "Dipped headlights.",
            "Dipped headlights."
        ],
        "incorrect_answers": [
            "Main-beam headlights.",
            "Front fog lights.",
            "Sidelights only.",
            "Hazard warning lights.",
            "Full beam headlights."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you're driving on a motorway at night or in poor visibility, you must always use your headlights, even if the road is well-lit. Other road users must be able to see you, but you should avoid causing dazzle.",
        "questions": [
            "Which lights must you use if you're driving on a well-lit motorway at night?",
            "What lights should you use on a motorway at night when the road is well lit?",
            "When driving on a well-lit motorway at night, which lights are required?",
            "Which headlights are appropriate when traveling on a well-lit motorway at night?",
            "If the motorway is well-lit at night, what lights should you have on?"
        ],
        "correct_answers": [
            "Use your headlights.",
            "Use your headlights."
        ],
        "incorrect_answers": [
            "Use rear fog lights.",
            "Use only your sidelights.",
            "Use front fog lights.",
            "Drive without any lights on.",
            "Use hazard warning lights."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Skidding is usually caused by driver error. You should always adjust your driving to take account of the road and weather conditions.",
        "questions": [
            "What's the main cause of skidding?",
            "What factor is primarily responsible for causing skids?",
            "Who or what is usually at fault when a vehicle skids?",
            "What is the most common reason for a vehicle to skid?",
            "What is the primary cause of skidding while driving?"
        ],
        "correct_answers": [
            "The driver.",
            "The driver's error.",
        ],
        "incorrect_answers": [
            "The vehicle.",
            "The weather.",
            "The road.",
            "The tires.",
            "The vehicle's error."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If the headlights of an oncoming vehicle dazzle you, slow down or, if necessary, stop. Don't close your eyes or swerve, as you'll increase your chances of having a collision. Don't flash your headlights either, as this could dazzle other drivers and make the situation worse.",
        "questions": [
            "You're driving at night. What should you do if you're dazzled by headlights coming towards you?",
            "What action should you take if oncoming headlights dazzle you while driving at night?",
            "If you are blinded by headlights from an oncoming vehicle at night, what should you do?",
            "What should you do when your vision is impaired by bright headlights at night?",
            "How should you respond if headlights from an approaching vehicle are too bright?"
        ],
        "correct_answers": [
            "Slow down or stop.",
            "Reduce your speed or pull over safely.",
            "Lower your speed and, if necessary, come to a stop.",
            "Decrease your speed and be prepared to stop.",
            "Slow down to maintain control."
        ],
        "incorrect_answers": [
            "Flash your main-beam headlights.",
            "Pull down your sun-visor.",
            "Shade your eyes with your hand.",
            "Speed up to pass the oncoming vehicle.",
            "Keep looking directly at the headlights."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Driving in bad weather increases your risk of having a collision. If you have to travel, mirrors, number plates and windows of any snow or ice, so that you can see and be seen.",
        "questions": [
            "You're about to start a journey in freezing weather. What part of your vehicle should you clear of ice or snow?",
            "Before starting a journey in icy conditions, which parts of your vehicle should be cleared of snow and ice?",
            "What areas of your car must be free from ice or snow before setting off in freezing weather?",
            "In freezing weather, what parts of your vehicle must you clear of snow and ice before driving?",
            "Which vehicle parts should be de-iced before starting a journey in cold weather?"
        ],
        "correct_answers": [
            "The windows.",
            "The mirrors.",
            "The number plate.",
            "The windscreen.",
        ],
        "incorrect_answers": [
            "The bumper.",
            "The aerial.",
            "The boot.",
            "The exhaust pipe.",
            "The roof."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You won't be able to see as far ahead in fog as you can on a clear day. You'll need to reduce your speed so that, if a hazard looms out of the fog, you have the time and space to avoid action. Travelling in fog is hazardous. If you can, try to delay your journey until it has cleared.",
        "questions": [
            "Why should you reduce your speed when you're driving or riding in fog?",
            "What makes it necessary to slow down when driving in foggy conditions?",
            "Why is it important to reduce your speed in dense fog?",
            "Why should you drive more cautiously in foggy weather?",
            "What is the main reason for lowering your speed when driving in fog?"
        ],
        "correct_answers": [
            "It's more difficult to see what's ahead.",
            "Obstacles may appear suddenly.",
        ],
        "incorrect_answers": [
            "Fog increases tire grip.",
            "Your brakes work more effectively.",
            "There is more space on the road.",
            "Other vehicles travel faster."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Consider whether the increased risk is worth it. If the weather conditions are bad and your journey isn't essential, then don't drive. If you have to drive, make sure you're well prepared in case you get stuck.",
        "questions": [
            "There's been a heavy fall of snow. What should you consider before driving in these conditions?",
            "What should you think about before setting off during heavy snowfall?",
            "What is an important consideration before driving after a heavy snowstorm?",
            "What should you evaluate before traveling in severe snowy conditions?",
            "What should you assess before attempting to drive in heavy snow?"
        ],
        "correct_answers": [
            "Whether your journey is essential.",
            "Whether it's necessary to make the trip.",
            "Whether you can delay your journey.",
            "Whether you can use public transport instead.",
        ],
        "incorrect_answers": [
            "Whether you should drive without wearing your seat belt.",
            "Whether you should wear sunglasses to reduce the glare.",
            "Whether you should fit an amber flashing beacon to your car.",
            "Whether you should drive faster to minimize time spent on the road.",
            "Whether you should lower tire pressure for better grip."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "In snowy conditions, be careful with the steering, accelerator and brakes. Braking sharply while you're driving on snow is likely to make your car skid.",
        "questions": [
            "What should you do when you're driving in snowy conditions?",
            "How should you brake when driving on a snowy road?",
            "What is the safest way to slow down in snowy weather?",
            "What's the correct way to use your brakes on snow-covered roads?",
            "How should you prepare to stop while driving on snow?"
        ],
        "correct_answers": [
            "Brake gently in plenty of time.",
            "Reduce speed gradually and brake softly.",
            "Apply the brakes lightly and early.",
            "Use smooth, controlled braking.",
            "Start braking sooner than usual."
        ],
        "incorrect_answers": [
            "Use sidelights only.",
            "Brake firmly and quickly.",
            "Be ready to steer sharply.",
            "Accelerate to avoid skidding.",
            "Keep a short distance from the car ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "On the main beam, your lights could dazzle the driver in front. Dip your headlights as soon as the driver passes you and drop back so that the dipped beam falls short of the vehicle in front.",
        "questions": [
            "You're driving at night with your headlights on main beam. A vehicle is overtaking you. When should you dip your headlights?",
            "When should you dip your main beam headlights if another vehicle overtakes you at night?",
            "At night, when being overtaken, when should you switch to dipped headlights?",
            "When overtaken by another vehicle at night, when is it appropriate to dip your headlights?",
            "As a vehicle overtakes you at night, when should you lower your headlights from main beam?"
        ],
        "correct_answers": [
            "As soon as the vehicle passes you.",
            "Immediately after the overtaking vehicle is in front.",
            "When the overtaking vehicle moves ahead.",
            "As the vehicle completes the overtaking maneuver.",
            "Once the vehicle has safely passed you."
        ],
        "incorrect_answers": [
            "Before the vehicle starts to pass you.",
            "Only if the other driver dips their headlights.",
            "Some time after the vehicle has passed you.",
            "When the vehicle is far ahead.",
            "After you see the vehicle's rear lights."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You must use parking lights when parking at night on a road or in a lay-by on a road with a speed limit of 30 mph. You must also park in the direction of flow and not close to a junction.",
        "questions": [
            "What should you do when you park at night on a road that has a 40 mph speed limit?",
            "When parking at night on a road with a 40 mph speed limit, what should you do?",
            "If you're parking at night on a 40 mph road, what should you ensure regarding your lights?",
            "What action should you take when parking at night on a road with a 40 mph limit?",
            "On a 40 mph road, what should you do when parking at night?"
        ],
        "correct_answers": [
            "Leave parking lights switched on.",
            "Ensure your parking lights are on.",
            "Switch on your parking lights before leaving the vehicle.",
            "Activate your parking lights when you park at night.",
            "Make sure your parking lights are illuminated."
        ],
        "incorrect_answers": [
            "Leave dipped headlights switched on.",
            "Park near a street light.",
            "Park facing the traffic.",
            "Keep your fog lights on.",
            "Turn off all lights and leave your car in darkness."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Use the full-beam headlights only when you can be sure that you won't dazzle other road users.",
        "questions": [
            "You're driving on a clear night. Which lights should you use if the national speed limit applies and there's a steady stream of oncoming traffic?",
            "On a clear night, if the national speed limit applies and there's continuous oncoming traffic, what lights should you use?",
            "What lights should you use if you're driving on a clear night at the national speed limit and there's ongoing oncoming traffic?",
            "Driving at night on a clear road with the national speed limit and a steady flow of oncoming traffic, which lights should you use?",
            "If you're driving on a clear night with the national speed limit and there's a continuous flow of oncoming traffic, which lights should you have on?"
        ],
        "correct_answers": [
            "Dipped headlights.",
            "Dipped headlights."
        ],
        "incorrect_answers": [
            "Sidelights.",
            "Fog lights.",
            "Full-beam headlights.",
            "Main-beam headlights.",
            "Parking lights."
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
        print("Questions upload failed, not enough questions.")

if __name__ == "__main__":
    main()