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
        "explanation": "Make sure you carry out the manoeuvres without causing a hazard to other vehicles. Choose a place to turn that's safe and considers other road users.",
        "questions": [
            "You're parked in a busy high street. What's the safest way to turn your vehicle around so you can drive in the opposite direction?",
            "How should you safely turn your car around in a busy high street?",
            "What is the safest method for turning your vehicle around in a busy high street?",
            "If you're parked on a busy street, how can you safely turn your car around?",
            "What's the best way to safely change direction when you're parked on a busy road?"
        ], 
        "correct_answers": [
            "Turn around in a quiet side road.",
            "Use a quiet side road to turn your car around safely.",
            "Find a less busy side street to turn around.",
            "The safest way is to turn around in a quieter, less congested road.",
            "Turning around in a side road with minimal traffic is the safest option."
        ],
        "incorrect_answers": [
            "Carry out a U-turn.",
            "Ask someone to stop the traffic.",
            "Drive into a side road and reverse out into the main road.",
            "Perform a three-point turn in the middle of the street.",
            "Reverse into a busy road from a side street.",
            "Use a junction to make a turn even if it's not safe.",
            "Perform a turn in the middle of the busy high street."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "In queueing traffic, motorcyclists could be passing you on either side. Use your mirrors and check your blind area before changing lanes or changing direction.",
        "questions": [
            "You're driving in a slow-moving queue of traffic. What should you do before changing lane?",
            "Before changing lanes in slow-moving traffic, what should you check for?",
            "What should you do before changing lane in a queue of traffic?",
            "Before switching lanes in heavy traffic, what is essential to check?"
        ], 
        "correct_answers": [
            "Look for motorcyclists filtering through the traffic.",
            "Check for motorcyclists weaving through the traffic before changing lanes.",
            "Ensure there are no motorcyclists passing on either side before moving.",
            "Look for any motorcyclists filtering through the traffic around you.",
            "Check your mirrors and blind spots for motorcyclists before changing lanes."
        ],
        "incorrect_answers": [
            "Sound the horn and flash your lights.",
            "Change down to first gear.",
            "Give a 'slowing down' arm signal.",
            "Check your rearview mirror only.",
            "Accelerate to get ahead of the traffic.",
            "Wait for the traffic light to change.",
            "Look out for pedestrians only."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Large vehicles can hide other vehicles that are overtaking—especially motorcycles. You need to be aware of the possibility of hidden vehicles and not assume that it's safe to turn.",
        "questions": [
            "You're waiting to turn right out of a minor road. It's clear to the left but a lorry is coming from the right. Why should you wait, even if you have enough time to turn?",
            "Why should you wait before turning right when a lorry is coming from the right, even if it's clear to the left?",
            "You're about to turn right out of a minor road, but there's a lorry coming from the right. Why is it important to wait before turning?",
            "What is the reason to wait before turning right when a large vehicle is approaching from the right?"
        ], 
        "correct_answers": [
            "Anything overtaking the lorry will be hidden from view.",
            "Other vehicles, like motorcycles, may be hidden behind the lorry.",
            "A vehicle overtaking the lorry may not be visible to you.",
            "Vehicles overtaking the lorry could be blocked from your view, making it unsafe to turn.",
            "Hidden vehicles behind the lorry could pose a hazard if you turn too soon."
        ],
        "incorrect_answers": [
            "The lorry could suddenly speed up.",
            "The lorry might be slowing down.",
            "The load on the lorry might be unstable.",
            "The lorry could stop suddenly.",
            "There could be a sudden change in weather conditions.",
            "The road surface could be slippery."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "In England, Scotland and Northern Ireland, there's a 30 mph speed limit where there are street lights unless signs show another limit.",
        "questions": [
            "There are no speed-limit signs on the road. In England, Scotland and Northern Ireland, how is a 30 mph limit generally indicated?",
            "How can you tell a 30 mph speed limit is in place when there are no signs on the road in England, Scotland, and Northern Ireland?",
            "In the absence of speed-limit signs, what indicates a 30 mph limit in England, Scotland, and Northern Ireland?",
            "When there are no speed-limit signs, what shows that the speed limit is 30 mph in England, Scotland, and Northern Ireland?",
            "What indicates a 30 mph speed limit on a road in England, Scotland, and Northern Ireland when there are no signs?"
        ], 
        "correct_answers": [
            "By street lighting.",
            "By the presence of street lights.",
            "By the street lights that are present.",
        ],
        "incorrect_answers": [
            "By hazard warning lines.",
            "By pedestrian islands.",
            "By double or single yellow lines.",
            "By the width of the road.",
            "By the color of the road signs.",
            "By the type of vehicles on the road."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "When approaching a junction where the traffic lights have failed, you should proceed with caution. Treat the situation as an unmarked junction and be prepared to stop.",
        "questions": [
            "You're approaching a crossroads. What should you do if the traffic lights have failed?",
            "What should you do when you approach a crossroads and the traffic lights are not working?",
            "How should you respond if the traffic lights at a crossroads have failed?",
            "What action should you take when you come across a junction with non-functional traffic lights?",
            "If the traffic lights have failed at a crossroads, what is the correct procedure?"
        ], 
        "correct_answers": [
            "Be prepared to stop for any traffic.",
            "Be ready to stop and give way to any vehicles.",
            "Treat the junction as if it has no traffic lights and be prepared to stop.",
            "Treat it as an unmarked junction and stop if necessary."
        ],
        "incorrect_answers": [
            "Be prepared to brake sharply to a stop.",
            "Brake sharply to a stop before looking.",
            "Brake and stop only for large vehicles.",
            "Drive through the junction without stopping.",
            "Assume other drivers will stop for you.",
            "Proceed through the junction without hesitation.",
            "Only stop if the junction is congested."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "At a pelican crossing, the green light means you may proceed as long as the crossing is clear. If someone hasn't finished crossing, be patient and wait for them, whether they're disabled or not.",
        "questions": [
            "You've stopped at a pelican crossing. What should you do if a disabled person is crossing slowly in front of you and the lights change to green?",
            "What should you do if the lights change to green at a pelican crossing and a disabled person is still crossing slowly?",
            "When the lights change to green and a disabled person is still crossing in front of you, what should you do?",
            "At a pelican crossing, the lights change to green while a disabled person is crossing slowly in front of you. What is the correct action?",
            "If a disabled person is crossing slowly and the lights change to green at a pelican crossing, what should you do?"
        ], 
        "correct_answers": [
            "Wait for them to finish crossing.",
            "Allow them to finish crossing before moving.",
            "Wait for the pedestrian to cross.",
            "Do not move until the pedestrian has cleared the crossing.",
            "Wait until the crossing is clear before proceeding."
        ],
        "incorrect_answers": [
            "Sound your horn.",
            "Edge forward slowly.",
            "Drive in front of them.",
            "Rev your engine to signal them to hurry up.",
            "Drive around them if there is space.",
            "Start moving to encourage them to hurry.",
            "Flash your lights to signal them to move faster."
        ]
    },
    {
        "id": str(uuid.uuid4()), 
        "topic": topic, 
        "image": "n/a", 
        "sign_question": False,
        "explanation": "If you see a bus ahead, watch out for pedestrians. They might not be able to see you if they're behind the bus.",
        "questions": [
            "You're driving in town. Why should you be careful if there's a bus at a bus stop on the other side of the road?",
            "What should you be aware of when driving near a bus that is stopped on the other side of the road?",
            "When there's a bus at a bus stop on the opposite side of the road, why should you be cautious?",
            "Why do you need to watch out when there's a bus at a bus stop on the other side of the road?"
        ], 
        "correct_answers": [
            "Pedestrians might come from behind the bus.",
            "People may cross the road unexpectedly from behind the bus.",
            "A pedestrian could step out from behind the bus without warning.",
            "You may not see pedestrians coming from behind the bus."
        ],
        "incorrect_answers": [
            "The bus might have broken down.",
            "The bus might move off suddenly.",
            "The bus could be waiting for passengers to board.",
            "The bus might block your lane.",
            "The bus might be in the wrong lane.",
            "The bus might be a double-decker and block your view."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You should slow down and be prepared to stop, as you would for an able-bodied person. Don't wave them across, as other traffic may not stop.",
        "questions": [
            "You're driving towards a zebra crossing. What should you do if a person in a wheelchair is waiting to cross?",
            "What action should you take when a person in a wheelchair is waiting at a zebra crossing?",
            "What is the correct response if a person in a wheelchair is waiting to cross at a zebra crossing?",
            "When you approach a zebra crossing and a person in a wheelchair is waiting, what should you do?",
            "How should you react if a person in a wheelchair is waiting to cross at a zebra crossing?"
        ], 
        "correct_answers": [
            "Be prepared to stop.",
            "Slow down and be ready to stop.",
            "Give way and stop for the person in the wheelchair.",
            "Ensure you are ready to stop for the person in a wheelchair."
        ],
        "incorrect_answers": [
            "Wave to the person to cross.",
            "Wave to the person to wait.",
            "Drive past quickly to avoid delay.",
            "Honk your horn to signal the person to cross.",
            "Ignore the person and keep driving.",
            "Speed up to pass the crossing before they cross."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Your brake lights will indicate to traffic behind that you're slowing down. Good anticipation will allow you time to check your mirrors before slowing.",
        "questions": [
            "Other than direction indicators, how can you give signals to other road users?",
            "What other methods can you use to signal to other road users besides direction indicators?",
            "Apart from using direction indicators, how else can you signal your intentions to other drivers?",
            "What alternative signals can be used by drivers, aside from direction indicators?",
            "How else can you communicate your driving intentions to others, other than using direction indicators?"
        ], 
        "correct_answers": [
            "By using brake lights.",
            "By using your brake lights.",
            "By using brake lights."
        ],
        "incorrect_answers": [
            "By using fog lights.",
            "By using interior lights.",
            "By using side lights.",
            "By using your headlights.",
            "By using the horn.",
            "By flashing the headlights.",
            "By using hazard warning lights."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "In England, Scotland and Northern Ireland, there's a 30 mph speed limit where there are street lights unless signs show another limit.",
        "questions": [
            "In England, Scotland and Northern Ireland what will the speed limit usually be where you can see street lights but no speed-limit signs?"
        ], 
        "correct_answers": [
            "30 mph",
            "30 mph"
        ],
        "incorrect_answers": [
            "20 mph",
            "40 mph",
            "50 mph",
            "60 mph"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "At mini-roundabouts, there isn't much room for a long vehicle to manoeuvre. It will have to swing out wide so that it can complete the turn safely. Keep well back and don't try to move up alongside it.",
        "questions": [
            "You're approaching a mini-roundabout. What should you do if a long vehicle in front signals left but positions over to the right?",
            "How should you react if a large vehicle signals left at a mini-roundabout but moves towards the right?",
            "What action should you take if you're behind a long vehicle at a mini-roundabout and it signals left but veers to the right?",
            "When you see a long vehicle signaling left at a mini-roundabout but positioning to the right, what should you do?",
            "If a large vehicle at a mini-roundabout signals left but moves to the right, how should you respond?"
        ], 
        "correct_answers": [
            "Keep well back.",
            "Stay well behind.",
            "Maintain a safe distance.",
            "Keep a good distance."
        ],
        "incorrect_answers": [
            "Sound your horn.",
            "Overtake on the left.",
            "Follow the same course as the lorry.",
            "Pull up beside the long vehicle.",
            "Try to pass on the right."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Using a vehicle for short journeys means the engine doesn't have time to reach its normal operating temperature. When an engine is running below its normal operating temperature, it produces increased amounts of pollution. Walking and cycling don't create pollution and have health benefits as well.",
        "questions": [
            "What can people who live or work in towns and cities do to help reduce urban pollution levels?",
            "What are some ways to cut down on pollution in cities and towns?",
            "How can people reduce the environmental impact of short trips in urban areas?",
            "What can you do to reduce pollution levels in cities and towns instead of using a car?"
        ], 
        "correct_answers": [
            "Walk or cycle.",
            "Choose to walk or ride a bike",
            "Walk or cycle.",
            "Opt for walking or cycling.",
        ],
        "incorrect_answers": [
            "Over-rev in low gear.",
            "Drive short journeys.",
            "Drive more quickly.",
            "Use a vehicle for all your trips.",
            "Keep the engine running when stopped."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Take care if you have to pass an obstruction, such as a parked vehicle, on your side of the road. Give way to oncoming traffic if there isn't enough room for you both to continue safely.",
        "questions": [
            "What should you do when there's an obstruction on your side of the road?",
            "How should you proceed when an obstruction is blocking your side of the road?",
            "What should you do when you can't pass an obstruction safely?",
            "How should you handle an obstruction on your side of the road when there's oncoming traffic?",
            "What is the safest action when encountering an obstruction on your side of the road?"
        ], 
        "correct_answers": [
            "Give way to oncoming traffic.",
            "Allow oncoming vehicles to pass.",
            "Let the oncoming traffic go first.",
            "Give priority to oncoming traffic."
        ],
        "incorrect_answers": [
            "Accelerate to get past first.",
            "Wave oncoming vehicles through.",
            "Carry on, as you have priority.",
            "Speed up to avoid the obstruction.",
            "Honk the horn to alert oncoming vehicles.",
            "Stop and wait for oncoming vehicles to stop."
        ]
    },
    {
        "id": str(uuid.uuid4()), 
        "topic": topic, 
        "image": "n/a", 
        "sign_question": False,
        "explanation": "You mustn't use your vehicle's horn between 11:30 pm and 7 am in a built-up area or when you're stationary unless a moving vehicle poses a danger. Its function is to alert other road users to your presence.",
        "questions": [
            "When should you use your vehicle's horn?",
            "What is the purpose of using your vehicle's horn?",
            "Under what circumstances should you sound your horn?",
            "When is it appropriate to use your horn in a vehicle?",
            "Why should you use your vehicle's horn?"
        ], 
        "correct_answers": [
            "To alert others to your presence.",
            "To warn other road users of your presence.",
            "To make other drivers aware of your vehicle.",
            "To signal danger or your presence on the road."
        ],
        "incorrect_answers": [
            "To greet other road users.",
            "To signal your annoyance.",
            "To allow you right of way.",
            "To inform others that you're waiting.",
            "To indicate you're turning.",
            "To give a warning to pedestrians."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You can overtake other traffic on either side when travelling on a one-way street. Make full use of your mirrors and ensure it's clear all around before you attempt to overtake. Look for signs and road markings, and use the most suitable lane for your destination.",
        "questions": [
            "Where may you overtake on a one-way street?",
            "On a one-way street, where is overtaking permitted?",
            "Can you overtake on both sides of a one-way street?",
            "In a one-way street, is it okay to overtake on the left and right?",
            "Where can you overtake other traffic on a one-way street?"
        ], 
        "correct_answers": [
            "On either the right or the left.",
            "You can overtake on both sides.",
            "Overtaking is allowed on either side.",
            "You can pass vehicles on the right or left side.",
            "On a one-way street, overtaking can be done on both sides."
        ],
        "incorrect_answers": [
            "Overtaking isn't allowed.",
            "Only on the left-hand side.",
            "Only on the right-hand side.",
            "You cannot pass any vehicles.",
            "Overtaking is only allowed if the road is clear ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_right_hand_lane_closed.png", "sign_question": True,
        "explanation": "Yellow-and-black temporary signs may be used to inform you about roadworks or lane restrictions. Look well ahead. If you have time to change lanes, do so in a timely manner.",
        "questions": [
            "What does this sign mean?",
            "What is the meaning of this road sign?",
            "What information does this sign convey?",
            "What should you understand from this sign?"
        ],
        "correct_answers": [
            "The right-hand lane is closed.",
            "Right-hand lane closure.",
            "Lane closure on the right.",
            "Right-hand lane is under maintenance.",
            "Right-hand lane out of service."
        ],
        "incorrect_answers": [
            "The right-hand lane ahead is narrow.",
            "Right-hand lane for turning right.",
            "Right-hand lane for buses only.",
            "Right-hand lane for cyclists only.",
            "Right-hand lane for high occupancy vehicles."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_mini_roundabout.png", "sign_question": True,
        "explanation": "These markings show the direction in which the traffic should go at the mini-roundabout.",
        "questions": [
            "Where would you find these road markings?",
            "What type of junction features these markings?",
            "In which location would you typically see these markings?",
            "What do these road markings indicate?",
            "Which road feature is marked like this?"
        ],
        "correct_answers": [
            "At a mini-roundabout.",
            "At a Mini-roundabout junction.",
            "On a mini-roundabout.",
        ],
        "incorrect_answers": [
            "On a pedestrian crossing.",
            "On a motorway.",
            "At a railway crossing.",
            "At a bus lane entrance.",
            "At a controlled junction."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_cycle_route_ahead.png", "sign_question": True,
        "explanation": "More people are cycling today and cycle routes are being extended in our towns and cities to provide safe cycling routes. Respect the presence of cyclists on the road and give them plenty of room if you need to pass.",
        "questions": [
            "What does this sign mean?",
            "What is indicated by this road sign?",
            "Which type of route is indicated by this sign?"
        ],
        "correct_answers": [
            "Cycle route ahead.",
            "A cycle route.",
            "Cycle path ahead.",
            "Cycle route starts here."
        ],
        "incorrect_answers": [
            "Cycle parking only.",
            "No cycling.",
            "End of cycle route.",
            "Pedestrian zone only.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_school_bus.png", "sign_question": True,
        "explanation": "Vehicles used to carry children to and from school will be travelling at busy times of the day. If you're following a vehicle with this sign, be prepared for it to make frequent stops. It might pick up or set down passengers in places other than normal bus stops.",
        "questions": [
            "Where would you see this sign?",
            "Where is this warning sign typically found?",
            "Where would you expect to see this sign?",
            "This sign is usually displayed where?"
        ],
        "correct_answers": [
            "On the rear of a school bus or coach.",
            "At the back of a vehicle used for children.",
            "On the rear of a vehicle carrying schoolchildren.",
            "On a dedicated school bus.",
            "On the back of a coach transporting pupils."
        ],
        "incorrect_answers": [
            "At playground areas.",
            "In the window of a car taking children to school.",
            "At the side of the road.",
            "On a vehicle used for carpooling.",
            "On a public transit bus."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_cyclist_signal_right.png", "sign_question": False,
        "explanation": "Keep well back and give the cyclist time and room to turn safely. Don't intimidate them by getting too close or trying to squeeze.",
        "questions": [
            "What should you do as you approach this cyclist?",
            "How should you behave when approaching this cyclist?",
            "What's the safest way to approach this cyclist?",
            "What precautions should you take when nearing this cyclist?"
        ],
        "correct_answers": [
            "Stay well back and give them plenty of room.",
            "Hold back and wait until they have completed the turn.",
            "Give the cyclist space and don't try to overtake.",
            "Allow the cyclist enough time to make the turn safely."
        ],
        "incorrect_answers": [
            "Speed up to pass them before they turn.",
            "Sound your horn to warn them.",
            "Move closer to encourage them to hurry.",
            "Try to squeeze past before they complete the turn."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_road_humps.png", "sign_question": False,
        "explanation": "Because the road has a dark colour, changes in level aren't easily seen. White triangles painted on the road surface give you an indication of where there are road humps.",
        "questions": [  
            "Where would you see this road marking?",
            "where would you commonly find this road marking?",
            "What does this marking usually accompany on the road?"
        ], 
        "correct_answers": [
            "On road humps.",
            "At speed-reducing road humps.",
            "On traffic-calming road humps.",
            "Near speed control humps."
        ],
        "incorrect_answers": [
            "At a box junction.",
            "At traffic lights.",
            "Near a level crossing.",
            "In a pedestrian zone."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_box_junction.jpg", "sign_question": False,
        "explanation": "The purpose of yellow box markings is to keep junctions clear of queuing traffic. You may only wait in the marked area when you're turning right and your exit lane is clear but you can't complete the turn because of oncoming traffic or other traffic waiting to turn right.",
        "questions": [
            "When may you stop and wait in a box junction?",
            "In which situation is it permissible to wait in a box junction?",
            "What is the exception to stopping in a box junction?",
            "When is it allowed to remain stationary in a box junction?"
        ],
        "correct_answers": [
            "When oncoming traffic prevents you from turning right.",
            "If your exit road is clear but you're waiting to turn right.",
            "When you're waiting to turn right and oncoming traffic is blocking you.",
            "If you are turning right and cannot complete the turn due to oncoming traffic."
        ],
        "incorrect_answers": [
            "When you're on a roundabout.",
            "When you're in a queue of traffic going ahead.",
            "When you're in a queue of traffic turning left.",
            "When stopping to pick up passengers."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_hump_bridge.png", "sign_question": True,
        "explanation": "You'll need to slow down. At hump bridges, your view ahead will be restricted and the road will often be narrow. If the bridge is very steep, sound your horn to warn others of your approach. Going over the bridge too fast is highly dangerous to other road users and could even cause your wheels to leave the road, resulting in loss of control.",
        "questions": [
            "What does this sign mean?",
            "What is the purpose of this road sign?",
            "What hazard does this road sign indicate?",
            "What feature of the road does this sign warn you about?"
        ],
        "correct_answers": [
            "Hump bridge.",
            "Hump bridge."
        ],
        "incorrect_answers": [
            "Low bridge.",
            "Traffic-calming bump.",
            "Uneven road.",
            "Narrow bridge."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_no_stopping.png", "sign_question": True,
        "explanation": "This is the sign for a clearway. Clearways are stretches of road where you aren't allowed to stop unless it's an emergency. Stopping where these restrictions apply may be dangerous and is likely to cause an obstruction. Restrictions might apply for several miles and this may be indicated on the sign.",
        "questions": [
            "What does this sign mean?",
            "What restriction does this road sign indicate?",
            "What must you not do when you see this sign?",
            "What rule applies where this sign is displayed?"
        ],
        "correct_answers": [
            "No stopping.",
            "Stopping is prohibited.",
            "You must not stop at any time.",
            "Stopping is not allowed in this area."
        ],
        "incorrect_answers": [
            "National speed limit applies.",
            "No entry.",
            "Waiting restrictions apply.",
            "Parking is prohibited."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_marked_area_red.jpg", "sign_question": False,
        "explanation": "These are known as advanced stop lines. When lights are red (or about to become red), you should stop at the first white line. However, if you've crossed that line as the lights change, you must stop at the second line even if it means you're in the area reserved for cyclists.",
        "questions": [
            "This junction, controlled by traffic lights, has a marked area between two stop lines. What's this for?",
            "At a traffic light-controlled junction, why is there a marked area between the stop lines?",
            "Why is there a marked area between the two stop lines at a junction controlled by traffic lights?"
        ],
        "correct_answers": [
            "To allow cyclists to position in front of other traffic.",
            "So cyclists can wait ahead of other vehicles.",
            "It provides a space for cyclists to be in front of vehicles at the lights.",
            "Cyclists are given a safe space to move ahead of traffic."
        ],
        "incorrect_answers": [
            "To allow cyclists and pedestrians to cross the road together.",
            "To allow people with disabilities to cross the road.",
            "To allow taxis to position in front of other traffic.",
            "To prevent traffic from blocking the junction.",
            "To give buses priority over other vehicles.",
            "To make room for larger vehicles to turn."
    ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_ped_cyc.png", "sign_question": True,
        "explanation": "This sign shows a shared route for pedestrians and cyclists: when it ends, the cyclists will be rejoining the main road.",
        "questions": [
            "What does this sign mean?",
            "What's the meaning of this sign?",
            "What does this sign convey?"
        ], 
        "correct_answers": [
            "A route for pedestrians and cyclists.",
            "A route for pedestrians and cyclists."
        ],
        "incorrect_answers": [
            "No route for pedestrians and cyclists.",
            "A route for cyclists only.",
            "A route for pedestrians only.",
            "No route for pedestrians.",
            "No route for cyclists."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_one_way.png", "sign_question": True,
        "explanation": "In a one-way system, traffic may pass you on either side. Always be aware of all traffic signs and understand their meaning. Look well ahead and react tp them in good time.",
        "questions": [
            "What should you be aware of if you've just passed this sign?",
            "What does this sign indicate you need to be aware of?",
            "After passing this sign, what should you expect about the traffic?"
        ],
        "correct_answers": [
            "All traffic is going one way.",
            "Traffic is now moving in a single direction.",
            "The road is one-way.",
            "All vehicles must travel in the same direction."
        ],
        "incorrect_answers": [
            "Only one lane is in use.",
            "You can't stop on this road.",
            "This is a single-track road.",
            "There are restrictions on turning left or right.",
            "This road has a speed limit reduction.",
            "You must yield to pedestrians."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_30_starts_20_ends.png", "sign_question": True,
        "explanation": "Where you see this sign, the 20 mph restriction ends and a 30 mph restriction starts. Check all around for possible hazards and only increase your speed if it's safe to do so.",
        "questions": [
            "What does this sign mean?",
            "What is indicated by this sign?",
            "What does this road sign show?"
        ],
        "correct_answers": [
            "End of 20 mph zone.",
            "The 20 mph speed limit has ended.",
            "This marks the end of the 20 mph zone.",
            "You are leaving the 20 mph zone."
        ],
        "incorrect_answers": [
            "Minimum speed limit 30 mph.",
            "No vehicles over 30 tonnes.",
            "New speed limit 20 mph.",
            "Start of a 30 mph zone.",
            "End of a 30 mph zone.",
            "No entry for vehicles over 30 mph."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_level_crossing.jpg", "sign_question": False,
        "explanation": "These signals are found at level crossings, swing or lifting bridges, some airfields and emergency access sites. The flashing red lights mean stop whether or not the way seems to be clear.",
        "questions": [
            "Where would you find these flashing light signals?",
            "Where are these flashing lights commonly used?",
            "What area is marked by these flashing light signals?"
        ],
        "correct_answers": [
            "Level crossings.",
            "Railway level crossings.",
        ],
        "incorrect_answers": [
            "Pelican crossings.",
            "Motorway exits.",
            "Zebra crossings.",
            "Bus stops.",
            "Pedestrian crossings.",
            "Traffic signals at junctions."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_zebra_crossing.png", "sign_question": True,
        "explanation": "Look well ahead and be ready to stop for any pedestrians crossing, or about to cross, the road. Also, check the pavements for anyone who looks like they might step into the road.",
        "questions": [
            "What does this sign mean?",
            "What is indicated by this sign?",
            "What warning does this sign give?"
        ],
        "correct_answers": [
            "Zebra crossing ahead.",
            "Zebra crossing is coming up.",
            "Ahead, there is a zebra crossing.",
            "Warning: zebra crossing ahead."
        ],
        "incorrect_answers": [
            "Pedestrian zone - no vehicles.",
            "No pedestrians allowed.",
            "School crossing patrol.",
            "Pedestrian crossing without priority.",
            "No vehicles allowed here.",
            "School zone crossing only."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_stop.png", "sign_question": True,
        "explanation": "Stop' signs are situated at junctions where visibility is restricted or where there's heavy traffic. they MUST be obeyed: you must stop. Look carefully before moving off.",
        "questions": [
            "What must you do when you see this sign?",
            "What action should you take upon seeing this sign?",
            "What does this sign require you to do?"
        ],
        "correct_answers": [
            "Stop even if the road is clear.",
            "You must stop, even if there are no vehicles coming.",
            "Stop regardless of whether the road is clear.",
            "You are required to stop, even if no cars are approaching."
        ],
        "incorrect_answers": [
            "Stop only if children are waiting to cross.",
            "Stop only if a red light is showing.",
            "Stop only if traffic is approaching.",
            "Stop only when there is heavy traffic.",
            "Stop only if a vehicle is in the way.",
            "Stop if the pedestrian lights are red."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": True,
        "explanation": "Bus-lane signs show the vehicles allowed to use the lane and its times of operation. Where no times are shown, the bus lane is in operation 24 hours a day.",
        "questions": [
            "What does it mean if the signs at a bus lane show no times of operation?",
            "What is the implication of no times of operation being shown on a bus lane sign?",
            "What should you understand if there are no times listed for a bus lane?"
        ],
        "correct_answers": [
            "The lane is in operation 24 hours a day.",
            "The bus lane operates all day, every day.",
            "The lane is active at all times, day and night.",
            "The bus lane is always in operation, 24/7."
        ],
        "incorrect_answers": [
            "The lane is only in operation in daylight hours.",
            "The lane isn't in operation.",
            "The lane is only in operation at peak times.",
            "The lane is not active on weekends.",
            "The lane operates only during rush hour.",
            "The lane operates only when there is heavy traffic."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_urban_clearway.png", "sign_question": True,
        "explanation": "Urban clearways are provided to keep the traffic flowing at busy times. You may stop only briefly to set down or pick up passengers. Times of operation will vary from place to place, so always check the signs.",
        "questions": [
            "What does this sign mean?"
        ], 
        "correct_answers": [
            "No parking on the days and times shown."
        ],
        "incorrect_answers": [
            "End of urban clearway restrictions.",
            "You can park on the days and times shown.",
            "No parking at all from Monday to Friday."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_wait_restrict.png", "sign_question": True,
        "explanation": "There'll be a plate or additional sign to tell you when the restrictions apply.",
        "questions": [
            "What does this sign mean?",
            "What does this sign indicate?",
            "What is the meaning of this road sign?"
        ],
        "correct_answers": [
            "Waiting restrictions apply.",
            "Waiting is not allowed in this area.",
            "You cannot wait or park in this area.",
            "Parking or waiting is prohibited here."
        ],
        "incorrect_answers": [
            "Waiting permitted.",
            "National speed limit applies.",
            "Clearway (no stopping)",
            "You can park during certain hours.",
            "Loading and unloading allowed.",
            "Parking is allowed with a permit."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "2_park_verge.png", "sign_question": True,
        "explanation": "In order to keep roads free from parked cars, there are some areas where you're allowed to park on the verge. Only do this where you see the sign. Parking on verges or footways anywhere else could lead to a fine..",
        "questions": [
            "What does this sign mean?"
        ], 
        "correct_answers": [
            "Vehicles may park fully on the verge or footway."
        ],
        "incorrect_answers": [
            "Vehicles may not park on the verge or footway.",
            "Vehicles may park on the right-hand side of the road only.",
            "Vehicles may park on the light-hand side of the road only."
        ]
    },
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