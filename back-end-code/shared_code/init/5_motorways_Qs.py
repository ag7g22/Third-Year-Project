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

topic = "Motorways"

questions = [
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "When approaching a contraflow system, reduce speed in good time and obey all speed limits. You may be travelling in a narrower lane than normal, with no permanent barrier between you and the oncoming traffic. Be aware that the hard shoulder may be used for traffic and the road ahead could be obstructed by slow-moving or broken-down vehicles.",
        "questions": [
            "What would you expect to find at a contraflow system on a motorway?",
            "What is a common feature of a motorway contraflow system?",
            "Which characteristic is typical of a contraflow system on a motorway?",
            "When approaching a contraflow system, what should you be prepared for?",
            "What should you expect when driving through a contraflow on a motorway?"
        ], 
        "correct_answers": [
            "Lower speed limits.",
            "Reduced speed limits.",
            "Slower traffic speeds.",
            "Decreased speed limits.",
            "Speed restrictions."
        ], 
        "incorrect_answers": [
            "Temporary traffic lights.",
            "Road humps.",
            "Wider lanes than normal.",
            "Higher speed limits.",
            "Permanent central barriers.",
            "Smooth and clear road conditions.",
            "Normal lane widths.",
            "Dedicated cycle lanes."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Never overtake on the left, unless the traffic is moving in queues and the queue on your right is moving more slowly than the one you're in.",
        "questions": [
            "You're travelling along a motorway. When are you allowed to overtake on the left?",
            "When is it permissible to overtake on the left while on a motorway?",
            "In what situation can you overtake on the left while driving on a motorway?",
            "Under what conditions are you allowed to overtake on the left on a motorway?",
            "What is the rule for overtaking on the left on a motorway?"
        ], 
        "correct_answers": [
            "When in queues and traffic to your right is moving more slowly than you are.",
            "If traffic on your right is moving slower than your lane.",
            "When traffic on your right-hand side is slower due to queuing.",
            "If the right lane traffic is moving slower in a queue.",
            "Only when the right-hand lane is moving slower in congested traffic."
        ], 
        "incorrect_answers": [
            "When you warn drivers behind by signalling left.",
            "When the traffic in the right-hand lane is signalling right.",
            "When you can see well ahead that the hard shoulder is clear.",
            "When driving in the fast lane.",
            "When there are no vehicles behind you.",
            "When the road ahead is completely clear.",
            "When your vehicle is faster than those on the right.",
            "When the speed limit on your lane is higher."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "To rejoin the carriageway from an emergency refuge area, you must use the emergency telephone and follow the operator's advice. A lane may have to be closed so that you can rejoin the carriageway safely.",
        "questions": [
            "You have stopped in an emergency refuge area. What must you do before you rejoin the carriageway?",
            "What should you do before leaving an emergency refuge area and rejoining the road?",
            "Before moving off from an emergency refuge area, what action must you take?",
            "What must you ensure before rejoining the carriageway from an emergency refuge area?",
            "What is the required action before exiting an emergency refuge area?"
        ], 
        "correct_answers": [
            "Use the emergency telephone.",
            "Call for assistance using the emergency phone.",
            "Contact the emergency services using the roadside phone.",
            "Report your situation using the emergency telephone.",
            "Notify authorities via the emergency telephone before moving off."
        ], 
        "incorrect_answers": [
            "Switch on your vehicle's headlights.",
            "Give an arm signal as you are moving off.",
            "Move away with your hazard lights on.",
            "Sound your horn before moving off.",
            "Flash your headlights to warn other drivers.",
            "Wait for a signal from passing vehicles.",
            "Start driving without checking for approaching traffic.",
            "Move off immediately if no vehicles are in sight."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "The studs between the carriageway and the hard shoulder are normally red. These change to green when there's a slip road, helping you to identify slip roads when visibility is poor or when it's dark.",
        "questions": [
            "What colour are the reflective studs between a motorway and a slip road?",
            "Which colour are the road studs that mark the boundary between a motorway and a slip road?",
            "What colour studs indicate a slip road on a motorway?",
            "Which coloured reflective studs are used between a motorway carriageway and a slip road?",
            "What is the colour of the reflective studs separating a motorway from a slip road?"
        ], 
        "correct_answers": [
            "Green",
            "Green"
        ], 
        "incorrect_answers": [
            "Red",
            "Amber",
            "White",
            "Blue",
            "Yellow",
            "Orange",
            "Purple",
            "Pink"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you feel yourself becoming tired, you should leave the motorway at the next exit or service and stop for a rest. If you must drive a long way, leave earlier and plan your journey to include rest stops. That way, you're less likely to become tired while driving and you'll still arrive in good time.",
        "questions": [
            "What should you do if you become tired while you're on the motorway?",
            "What is the best course of action if you start feeling drowsy on the motorway?",
            "If you feel sleepy while driving on the motorway, what should you do?",
            "What action should you take if you get tired during a motorway journey?",
            "How should you respond if fatigue sets in while you're driving on the motorway?"
        ],  
        "correct_answers": [
            "Leave the motorway at the next exit and rest.",
            "Take the next exit and find a safe place to rest.",
            "Pull off the motorway at the next service area and rest.",
            "Exit the motorway safely and take a break.",
            "Find the nearest service area and stop to rest."
        ],
        "incorrect_answers": [
            "Close all your windows and set the heating to warm.",
            "Increase your speed and turn up the radio volume.",
            "Pull up on the hard shoulder and change drivers.",
            "Open the windows and keep driving to stay alert.",
            "Take a quick nap in the fast lane.",
            "Drink a caffeinated beverage while driving.",
            "Pull into the central reservation to rest.",
            "Ignore the tiredness and continue driving."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "White studs are found between the lanes on motorways. They reflect the light from your headlights. This is especially useful in bad weather when visibility is restricted.",
        "questions": [
            "What colour are the reflective studs between the lanes on a motorway?",
            "Which colour studs separate lanes on a motorway?",
            "What colour reflective studs are used to mark lanes on a motorway?",
            "How are the reflective studs coloured between lanes on a motorway?",
            "What colour are the lane-dividing studs on a motorway?"
        ],
        "correct_answers": [
            "White",
            "White"
        ], 
        "incorrect_answers": [
            "Red",
            "Amber",
            "Green",
            "Blue",
            "Yellow",
            "Orange",
            "Purple",
            "Pink"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You'll see the first advance direction sign one mile from a motorway exit. If you're travelling at 60mph in the right-hand lane, you'll have about 50 seconds before you reach the countdown markers. There'll be another sign at the half-mile point. Don't cut across lanes of traffic at the last moment - move to the left-hand lane in good time.",
        "questions": [
            "You're driving on the motorway. Which lane should you get into well before you reach the exit?",
            "Which lane should you position yourself in when approaching a motorway exit?",
            "Before leaving the motorway, which lane should you move into?",
            "What is the safest lane to be in when preparing to exit a motorway?",
            "As you approach a motorway exit, which lane is recommended?"
        ],
        "correct_answers": [
            "The left-hand lane.",
            "The left-hand lane."
        ],
        "incorrect_answers": [
            "The middle lane.",
            "The right-hand lane.",
            "The outside lane.",
            "The overtaking lane.",
            "The fast lane."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Traffic on motorways usually travels faster than on other roads. You need to be looking further ahead to give yourself more time to react to any hazard that may develop.",
        "questions": [
            "What should you do while you're driving or riding along a motorway?",
            "When driving on a motorway, how far ahead should you look?",
            "What is important to do while driving on a motorway in comparison to other roads?",
            "How should your observation differ when driving on a motorway?",
            "What is a key safety measure to follow when driving on a motorway?"
        ], 
        "correct_answers": [
            "Look much further ahead than you would on other roads.",
            "Observe the road further ahead than you would on a other roads.",
            "Look further ahead than you would on a other roads.",
            "Keep your focus on the road well ahead than you would on a other roads."
        ],
        "incorrect_answers": [
            "Maintain a shorter separation distance than you would on other roads.",
            "Travel much faster than you would on other roads.",
            "Concentrate more than you would on other roads.",
            "Drive more aggressively than on other roads.",
            "Focus less on the traffic around you than you would on a other roads."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Reflective studs are used to help you in poor visibility. Different colours are used so that you'll know which lane you're in. Red on the left-hand edge of the carriageway for instance.",
        "questions": [
            "What colour are the reflective studs along the left-hand edge of the motorway?",
            "Which colour are the road studs on the left side of the motorway?",
            "What is the colour of the reflective studs marking the left-hand edge of the motorway?",
            "What colour are the reflective studs placed along the left-hand side of the motorway?",
            "Which colour are the reflective studs used on the left-hand edge of the motorway?"
        ],
        "correct_answers": [
            "Red",
            "Red"
        ], 
        "incorrect_answers": [
            "White",
            "Amber",
            "Green",
            "Blue",
            "Yellow",
            "Orange",
            "Purple",
            "Pink"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Plan well ahead when approaching a slip road. If you see traffic joining the motorway, be prepared to adjust your speed or move to another lane if it's safe to do so. This can help the flow of traffic joining the motorway, especially at peak times.",
        "questions": [
            "You're travelling in the left-hand lane of a three-lane motorway. How should you react to traffic joining from a slip road?",
            "What should you do when traffic is joining the motorway from a slip road while you're in the left-hand lane?",
            "How should you respond when vehicles are merging onto the motorway from a slip road while you're in the left lane?",
            "If you're in the left-hand lane of a three-lane motorway and vehicles are joining from a slip road, what should you do?",
            "When you're driving in the left-hand lane of a motorway and traffic is merging from a slip road, what is the best course of action?"
        ],
        "correct_answers": [
            "Adjust your speed or change lane if you can do so safely.",
            "Change your lane or adjust your speed to merge safely.",
            "If it's safe, change lanes or adjust your speed.",
            "Safely change lanes or adjust your speed.",
            "Slow down or move lanes to let merging traffic join safely."
        ],
        "incorrect_answers": [
            "Increase your speed to ensure they join behind you.",
            "Switch on your hazard warning lights.",
            "Maintain a steady speed.",
            "Speed up to prevent the merging traffic from joining.",
            "Ignore the merging traffic and continue at your current speed."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "When you've just joined a motorway, stay in the left-hand lane long enough to get used to the higher speeds of motorway traffic before considering overtaking.",
        "questions": [
            "What should you do immediately after joining a motorway?",
            "What is the first thing you should do after merging onto the motorway?",
            "As soon as you join the motorway, which lane should you use?",
            "When you join the motorway, which lane is it best to stay in first?",
            "What is the appropriate lane to be in right after entering the motorway?"
        ],
        "correct_answers": [
            "Stay in the left-hand lane.",
            "Remain in the left-hand lane.",
            "Position your vehicle in the left-hand lane.",
            "Keep to the left-hand lane.",
            "Stay in the left-hand lane."
        ],
        "incorrect_answers": [
            "Try to overtake.",
            "Re-adjust your mirrors.",
            "Position your vehicle in the centre lane.",
            "Accelerate quickly to the right lane.",
            "Change lanes to the middle lane right away."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "On some motorways, emergency areas are built at the side of the carriageway. If you break down, try to get your vehicle into the emergency area, where there's an emergency telephone. The phone connects directly to a control centre. Before rejoining the motorway, you must call the control centre—a lane may need to be closed to allow you to rejoin safely.",
        "questions": [
            "When would you use an emergency area on a motorway?",
            "Under what circumstances should you use an emergency area on the motorway?",
            "When is it appropriate to use an emergency area while on the motorway?",
            "In which situations would you need to stop in an emergency area on the motorway?",
            "What is the correct use of an emergency area on a motorway?"
        ],
        "correct_answers": [
            "In cases of emergency or breakdown.",
            "When your vehicle breaks down or in an emergency situation.",
            "If your vehicle is malfunctioning or you need urgent assistance.",
            "In the event of an emergency or vehicle issue on the motorway.",
            "When there is an emergency or breakdown requiring you to stop."
        ],
        "incorrect_answers": [
            "If you think you'll be involved in a road rage incident.",
            "To make a private phone call.",
            "To stop and check where you are.",
            "For taking a rest during a long journey.",
            "If you need to replan your route."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "It's illegal to reverse, cross the central reservation or drive against the traffic flow on a motorway. If you miss your exit, carry on until you reach the next one. Ask yourself why you missed your exit - if you think that your concentration is fading, take a break before continuing your journey.",
        "questions": [
            "What should you do if you're driving on a motorway and you miss the exit that you wanted to take?",
            "If you miss your exit while driving on the motorway, what should you do?",
            "What is the correct action if you miss an exit while driving on a motorway?",
            "You're driving on the motorway and miss the exit. What should you do next?",
            "If you miss your exit on the motorway, how should you react?"
        ],
        "correct_answers": [
            "Carry on to the next exit.",
            "Proceed to the next exit.",
            "Continue to the next exit.",
            "Go to the next exit.",
            "Proceed to the next exit."
        ],
        "incorrect_answers": [
            "Carefully reverse along the hard shoulder.",
            "Carefully reverse in the left-hand lane.",
            "Make a U-turn at the next gap in the central reservation.",
            "Turn around in the next available gap.",
            "Stop immediately and attempt a U-turn."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You must follow the mandatory signs on the gantries above motorway lanes, including the hard shoulder. Variable speed limits help keep the traffic moving and also help prevent bunching.",
        "questions": [
            "How do motorways reduce traffic bunching?",
            "What is one method motorways use to reduce traffic congestion?",
            "How are motorways designed to minimize traffic bunching?",
            "What helps to prevent traffic from bunching on a motorway?",
            "How can motorways help in managing traffic flow?"
        ],
        "correct_answers": [
            "By using variable speed limits.",
            "Using variable speed limits.",
            "By imposing variable speed limits.",
        ],
        "incorrect_answers": [
            "By using minimum speed limits.",
            "By using higher speed limits.",
            "By using advisory speed limits.",
            "By imposing strict speed limits across all lanes.",
            "By limiting the number of vehicles on the motorway."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "On motorways, reflective studs of various colours are fixed in the road between the lanes. These help you to identify which lane you're in when it's dark or in poor visibility. Amber-coloured studs are found on the right-hand edge of the main carriageway, next to the central reservation.",
        "questions": [
            "Where are the amber reflective studs found on a motorway?",
            "Which part of the motorway are the amber reflective studs located?",
            "Where would you find amber reflective studs on the motorway?",
            "What area of the motorway is marked by amber reflective studs?",
            "Where are the amber studs used to mark on a motorway?"
        ],
        "correct_answers": [
            "Between the central reservation and carriageway.",
            "Between the central reservation and the carriageway.",
            "Between the central reservation and the carriageway.",
            "Between the central reservation and carriageway.",
            "Between the central reservation and the main carriageway."
        ],
        "incorrect_answers": [
            "Between each pair of lanes.",
            "Between the acceleration lane and the carriageway.",
            "Between the hard shoulder and the carriageway.",
            "Between the slip road and the carriageway.",
            "Between the hard shoulder and the central reservation."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Using your hazard warning lights, as well as your brake lights, will give extra warning of the problem ahead. Only use them for long enough for your warning to be seen.",
        "questions": [
            "You're driving on a motorway and have to slow down suddenly due to a hazard ahead. How can you warn drivers behind the hazard?",
            "How should you signal to drivers behind you when you need to slow down suddenly on the motorway due to a hazard?",
            "What should you do to warn drivers behind you if you need to reduce speed suddenly because of a hazard on the motorway?",
            "What action can you take to alert drivers behind you to a hazard ahead when you're driving on the motorway?",
            "How can you give advance warning to drivers behind you if you need to slow down on the motorway due to a hazard?"
        ],
        "correct_answers": [
            "Switch on your hazard warning lights.",
            "Turn on your hazard lights.",
            "Activate your hazard warning lights.",
            "Use your hazard warning lights.",
        ],
        "incorrect_answers": [
            "Flash your headlights.",
            "Sound your horn.",
            "Switch on your headlights.",
            "Increase your speed to pass the hazard quickly.",
            "Use your fog lights to warn drivers."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "On busy roads, traffic may still travel at high speeds. Don't follow the vehicle in front too closely. If a driver behind seems to be 'pushing you', gradually increase your distance from the vehicle in front by slowing down gently. This will give you more space in front if you have to brake and will reduce the risk of a collision involving several vehicles.",
        "questions": [
            "You're travelling on the motorway. How can you lower the risk of collision when the vehicle behind is following too closely?",
            "What can you do to reduce the risk of a collision if the vehicle behind you is tailgating on the motorway?",
            "How should you react if a vehicle is following too closely on the motorway to avoid a potential collision?",
            "You're on the motorway and a vehicle is tailgating you. What should you do to reduce the risk of a collision?",
            "If a vehicle is following you too closely on the motorway, what can you do to help prevent an accident?"
        ],
        "correct_answers": [
            "Increase your distance from the vehicle in front.",
            "Leave more space between you and the vehicle ahead.",
            "Create more distance from the car in front.",
            "Increase your gap to the vehicle ahead.",
            "Maintain a greater distance from the vehicle ahead."
        ],
        "incorrect_answers": [
            "Move onto the hard shoulder and stop.",
            "Switch on your hazard warning lights.",
            "Brake sharply.",
            "Accelerate to create more space.",
            "Change lanes quickly to avoid the tailgating vehicle."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You should give away to traffic already on the motorway. Where possible, traffic may move over to let you in, but don't force your way into the traffic stream. Traffic could be travelling at high speed, so try to match your speed to filter in without affecting the traffic flow.",
        "questions": [
            "You're joining a motorway from a slip road. How should you deal with traffic already on the motorway?",
            "How should you approach joining a motorway from a slip road when there is traffic already on the motorway?",
            "What is the best way to merge onto a motorway from a slip road when there is traffic already on it?",
            "When joining a motorway from a slip road, what should you do to safely merge with the traffic?",
            "You're entering a motorway from a slip road. How should you behave when traffic is already on the motorway?"
        ],
        "correct_answers": [
            "Match your speed to traffic in the left-hand lane and filter into a safe gap.",
            "Adjust your speed to match that of traffic in the left-hand lane and merge into a gap.",
            "Synchronize your speed with traffic in the left-hand lane and merge when it's safe.",
            "Increase your speed to match traffic in the left-hand lane and move into a gap.",
            "Align your speed with the traffic in the left-hand lane and enter the motorway when a safe gap appears."
        ],
        "incorrect_answers": [
            "Use the slip road to accelerate until you're moving much faster than the motorway traffic.",
            "Stop at the end of the slip road and look for a safe gap.",
            "Carry on along the hard shoulder until you see a safe gap.",
            "Try to overtake traffic on the slip road before merging.",
            "Wait for the traffic to stop completely before merging."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Knowing the colours of the reflective studs on the road will help you judge your position, especially at night, in foggy conditions or when visibility is poor. Green studs are found at slip-roads entrances and exits.",
        "questions": [
            "Where would you find green reflective studs on a motorway?",
            "What do green reflective studs indicate on a motorway?",
            "Where are the green reflective studs located on a motorway?",
            "On a motorway, what do green reflective studs mark?",
            "Where are green reflective studs found on a motorway?"
        ],
        "correct_answers": [
            "At slip-road entrances and exits.",
            "On slip-road entrances and exits.",
            "At the entrances and exits of slip roads.",
            "Along slip-road exits and entrances.",
            "At locations where slip roads join or leave the motorway."
        ],
        "incorrect_answers": [
            "Separating driving lanes.",
            "Between the hard shoulder and the carriageway.",
            "Between the carriageway and the central reservation.",
            "Marking areas of the hard shoulder.",
            "Used to separate the carriageway from the central reservation."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "A long lorry with a heavy load will need more time to pass you than a car, especially on an uphill stretch of road. Slow down and allow the lorry to pass.",
        "questions": [
            "You're being overtaken by a long, heavily laden lorry. What should you do if it's taking a long time to overtake?",
            "What should you do if a long, heavily laden lorry is taking a long time to overtake you?",
            "How should you react if a lorry is struggling to overtake you on a motorway?",
            "What action should you take if a heavily laden lorry is taking longer than expected to overtake?",
            "What should you do when being overtaken by a large, slow-moving lorry?"
        ],
        "correct_answers": [
            "Slow down.",
            "Reduce your speed.",
            "Ease off the accelerator.",
            "Allow the lorry more space to overtake.",
            "Slow down to let the lorry pass."
        ],
        "incorrect_answers": [
            "Change direction.",
            "Speed up.",
            "Hold your speed.",
            "Flash your headlights to encourage it to pass.",
            "Move into the hard shoulder."
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