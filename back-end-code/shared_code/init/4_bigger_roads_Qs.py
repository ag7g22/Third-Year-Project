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

topic = "Bigger Roads"

questions = [
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Leaving your indicators on could confuse other road users and may even lead to a crash. Be aware that if you haven't turned sharply, your indicators may not self-cancel and you'll need to turn them off manually.",
        "questions": [
            "Why should you make sure that your indicators are cancelled after turning at a junction?",
            "What's the reason for cancelling your indicators after a turn?",
            "Why is it important to turn off your indicators after turning at a junction?",
            "What could happen if you forget to cancel your indicators after a turn?",
            "What is the risk of leaving your indicators on after turning at a junction?"
        ], 
        "correct_answers": [
            "To avoid misleading other road users.",
            "To prevent confusing other drivers.",
            "To ensure other drivers aren't misled by your signals.",
            "To keep other road users informed about your intentions.",
            "To avoid causing confusion or accidents."
        ],
        "incorrect_answers": [
            "To avoid damage to the indicator relay.",
            "To avoid dazzling other road users.",
            "To avoid flattening the battery.",
            "To prevent the indicator from flashing when not needed.",
            "To ensure the vehicle runs more smoothly.",
            "To save fuel.",
            "To avoid unnecessary noise from the indicator."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Emergency vehicles use blue flashing lights. If you see or hear one, move out of it's way as soon as it's safe and legal to do so.",
        "questions": [
            "Which vehicle will use a blue flashing beacon?",
            "What kind of vehicle uses a blue flashing light?",
            "Which vehicle is likely to have a blue flashing beacon?",
            "When might you see a blue flashing beacon on a vehicle?",
            "What type of vehicle uses a blue flashing light?"
        ], 
        "correct_answers": [
            "Bomb disposal",
            "A bomb disposal vehicle",
            "A vehicle involved in bomb disposal",
            "Vehicles dealing with bomb disposal"
        ],
        "incorrect_answers": [
            "Breakdown recovery",
            "Motorway maintenance",
            "Snow plough",
            "Police car",
            "Ambulance",
            "Fire engine",
            "Road maintenance vehicle",
            "Hazardous material vehicles"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "'Tailgating' is the term used when a driver or rider follows the vehicle in front too closely. It's dangerous because it restricts your view of the road ahead and leaves no safety margin if the vehicle in front needs to slow down or stop suddenly.",
        "questions": [
            "Why is it dangerous to travel too close to the vehicle ahead?",
            "What is the risk of following the vehicle in front too closely?",
            "Why should you avoid tailgating?",
            "What danger does tailgating pose to your driving?",
            "What happens if you follow the vehicle ahead too closely?"
        ], 
        "correct_answers": [
            "Your view of the road ahead will be restricted.",
            "It limits your ability to see the road ahead.",
            "You can't see what's ahead of you properly.",
            "You won't have enough time to react if the vehicle in front stops suddenly."
        ],
        "incorrect_answers": [
            "Your satnav will be confused.",
            "Your engine will overheat.",
            "Your mirrors will need adjusting.",
            "Your brakes will wear out faster.",
            "You may run out of fuel.",
            "Your tires will wear unevenly.",
            "The car's headlights will stop working."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "When a long vehicle is going to turn right, it may need to keep close to the left-hand curb. This is to prevent the rear end of the trailer from cutting the corner. You need to be aware of how long vehicles behave in such situations. Don't overtake the lorry, because it could turn as you're alongside. Stay behind and wait for it to turn.",
        "questions": [
            "You're following a long vehicle approaching a crossroads. What should you do if the driver signals right but moves close to the left-hand kerb?",
            "What should you do if you're behind a long vehicle turning right but staying near the left curb?",
            "How should you react if a long vehicle signals right but moves towards the left-hand kerb?",
            "If you're behind a long vehicle approaching a junction and moving left despite signaling right, what should you do?",
            "What is the safest thing to do when following a long vehicle that signals right but moves left?"
        ], 
        "correct_answers": [
            "Wait behind the long vehicle.",
            "Stay behind and wait for the vehicle.",
            "Don't overtake the vehicle.",
            "Remain behind the vehicle."
        ],
        "incorrect_answers": [
            "Warn the driver about the wrong signal.",
            "Overtake on the right-hand side.",
            "Report the driver to the police.",
            "Attempt to overtake the vehicle on the left.",
            "Try to cut in front of the vehicle.",
            "Drive faster to pass the vehicle.",
            "Overtake the vehicle on the left and speed up."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "An amber flashing beacon on a vehicle indicates that it's moving slowly or stopped and a possible hazard. Look well ahead on a dual carriageway and you should be able to see and respond to these vehicles in good time.",
        "questions": [
            "What type of vehicle uses an amber flashing beacon on a dual carriageway?",
            "Which vehicle would have an amber flashing beacon on a dual carriageway?",
            "On a dual carriageway, what kind of vehicle is likely to have an amber flashing light?",
            "What vehicle typically uses an amber flashing beacon when moving slowly or stopped on a dual carriageway?",
            "Which vehicle commonly uses an amber flashing beacon to indicate it’s moving slowly on a dual carriageway?"
        ], 
        "correct_answers": [
            "A tractor",
            "A slow-moving vehicle",
        ],
        "incorrect_answers": [
            "A doctor on call",
            "An ambulance",
            "A fire engine",
            "A police car",
            "A snow plough",
            "A breakdown recovery vehicle",
            "A tow truck"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you're driving in high winds, be aware that the conditions might make a motorcyclist (or cyclist) swerve or wobble. Take this into consideration if you're following or wish to overtake a two-wheeled vehicle.",
        "questions": [
            "Why should you allow extra room while overtaking a motorcyclist on a windy day?",
            "What's the reason you need to give extra space when passing a motorcyclist in windy conditions?",
            "Why do you need to be cautious when overtaking a cyclist or motorcyclist on a windy day?",
            "What could happen if you don't allow enough room when overtaking a motorcyclist in strong winds?",
            "Why should you take extra care when overtaking a motorcyclist on a windy road?"
        ], 
        "correct_answers": [
            "The rider may be blown in front of you.",
            "The wind might cause the rider to swerve into your path.",
            "High winds could push the rider into your lane.",
            "The wind can affect the motorcyclist's balance and cause them to wobble.",
            "The rider may move unexpectedly due to the wind."
        ],
        "incorrect_answers": [
            "The rider may turn off suddenly to get out of the wind.",
            "The rider may stop suddenly.",
            "The rider may be travelling faster than normal.",
            "The motorcyclist may need to brake sharply.",
            "The cyclist might be trying to avoid the wind gusts.",
            "The wind could make the motorcyclist's bike go off-road.",
            "The rider may speed up to get away from the wind."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "It's illegal to use a hand-held mobile or similar device when driving or riding, except in a genuine emergency. The safest option is to switch off your mobile phone before you set off and use a message service. If you've forgotten to switch your phone off and it rings, you should leave it. When you've stopped in a safe place, you can see who called and return the call if necessary.",
        "questions": [
            "What should you do if your mobile phone rings while driving or riding?",
            "How should you handle a phone call while you're driving or riding?",
            "If your mobile rings when driving, what's the best course of action?",
            "What is the safest option if your phone rings while you're behind the wheel?",
            "What should you do if your phone goes off when you're driving?"
        ], 
        "correct_answers": [
            "Leave it until you've stopped in a safe place.",
            "Wait until you've pulled over safely before answering.",
            "Do not answer the phone until you are stationary and in a safe location.",
            "Ignore the call until you have safely stopped your vehicle.",
            "Let the call go unanswered and pull over safely before checking it."
        ],
        "incorrect_answers": [
            "Stop immediately.",
            "Answer it immediately.",
            "Pull up to the nearest kerb.",
            "Pull over in the middle of the road to take the call.",
            "Check your phone as soon as it rings.",
            "Answer the call while driving and talk hands-free.",
            "Turn off the engine and answer the call immediately."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Sometimes your separation distance is shortened by a driver moving into the gap you've allowed. When this happens, react positively stay calm and drop further back to re-establish a safe following distance.",
        "questions": [
            "You're leaving a safe gap as you follow a large vehicle. What should you do if a car moves into this gap?",
            "What should you do if another vehicle moves into the gap you've left while following a large vehicle?",
            "How should you react if another car fills the gap you left behind when following a large vehicle?",
            "If another car moves into your safe following distance, what is the best action to take?",
            "You're driving behind a large vehicle and a car cuts into the gap. How should you respond?"
        ],
        "correct_answers": [
            "Drop back further.",
            "Increase the distance between your vehicle and the one in front.",
            "Re-establish a safe following distance by dropping back.",
            "Calmly drop back to create a safe space again.",
            "Keep a safe distance by falling back further."
        ],
        "incorrect_answers": [
            "Flash your headlights.",
            "Start to overtake.",
            "Sound your horn.",
            "Speed up to get past the car.",
            "Drive closer to the car in front.",
            "Change lanes aggressively to regain the gap.",
            "Try to intimidate the car by getting closer."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "When the central reservation is narrow, it may not be able to contain your vehicle. In this case, you should treat a dual carriageway as one road. Wait until the road is clear in both directions before turning right. If you try to treat it as two separate roads and wait in the middle, your vehicle will stick out and cause an obstruction that may lead to a collision.",
        "questions": [
            "You're turning right onto a dual carriageway. What should you do if the central reservation is too narrow to contain your vehicle?",
            "If the central reservation is too narrow for your vehicle, how should you proceed when turning right onto a dual carriageway?",
            "What should you do if you can't wait in the central reservation because it's too narrow when turning right onto a dual carriageway?",
            "When the central reservation doesn't fit your vehicle, how should you handle turning right onto a dual carriageway?",
            "What is the safest way to turn right onto a dual carriageway if the central reservation is too narrow for your vehicle?"
        ], 
        "correct_answers": [
            "Wait until the road is clear in both directions.",
            "Wait for both directions to be clear before proceeding.",
            "Ensure the road is clear in both directions before making the turn.",
            "Only proceed once both directions of traffic are clear.",
            "Wait until it's safe to turn right without blocking the road."
        ], 
        "incorrect_answers": [
            "Emerge slowly to show your intentions.",
            "Stop in the first lane so that other vehicles give way.",
            "Proceed to the central reservation and wait.",
            "Make the turn as soon as there's a gap in one direction.",
            "Turn quickly to avoid blocking the road.",
            "Wait in the middle of the road until it's clear.",
            "Ignore the traffic in the other direction and proceed."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "When turning right at a crossroads where the oncoming traffic is also turning right it's generally safer to turn behind the approaching vehicle. This allows you a clearer view of approaching traffic and is called turning offside to offside. However, some junctions, usually controlled by traffic light filters, are marked for vehicles to turn nearside to nearside.",
        "questions": [
            "You're turning right at a crossroads. An oncoming driver is also turning right. What's the advantage of turning behind the oncoming vehicle?",
            "Why is it safer to turn behind an oncoming vehicle at a crossroads when both vehicles are turning right?",
            "What is the benefit of turning right behind an oncoming vehicle at a crossroads?",
            "When both you and an oncoming vehicle are turning right, why should you consider turning behind the other vehicle?",
            "If you're turning right and an oncoming driver is turning right, why should you turn behind them?"
        ], 
        "correct_answers": [
            "You'll have a clearer view of any approaching traffic.",
            "Turning behind the oncoming vehicle allows you to see traffic more clearly.",
            "By turning behind, you can better observe oncoming traffic.",
            "Turning behind gives you a better view of any potential hazards.",
            "This method provides a clearer view of the road ahead."
        ], 
        "incorrect_answers": [
            "You'll use less fuel because you can stay in a high gear.",
            "You'll be able to turn without stopping.",
            "You'll have more time to turn.",
            "You'll make a smoother turn with less effort.",
            "You'll avoid waiting at a traffic light.",
            "It will help you to get into the right lane more quickly.",
            "You will be able to overtake the oncoming vehicle more easily."
        ]
    },
    {
        "id": str(uuid.uuid4()), 
        "topic": topic, 
        "image": "n/a", 
        "sign_question": False,
        "explanation": "Pedestrians and riders on two wheels can be harder to see than other road users. Make sure you look for them, especially at junctions. Effective observation, coupled with appropriate action, can save lives.",
        "questions": [
            "Which is the most vulnerable road user?",
            "Who is most at risk on the road?",
            "Which type of road user is more likely to be injured in a collision?",
            "Who is more vulnerable to accidents on the road?",
            "Which road user is most at risk in traffic?"
        ], 
        "correct_answers": [
            "Motorcyclist",
            "Motorcyclist",
        ], 
        "incorrect_answers": [
            "Car driver",
            "Tractor driver",
            "Lorry driver",
            "Bus driver",
            "Van driver",
            "Cyclist",
            "Pedestrian",
            "Taxi driver"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Keep a steady course to give the driver behind an opportunity to overtake safely. If necessary, slow down. Reacting incorrectly to another driver's impatience can lead to danger.",
        "questions": [
            "You're driving in traffic at the speed limit for the road. What should you do if the driver behind is trying to overtake?",
            "What should you do if a driver behind you is trying to overtake while you're driving at the speed limit?",
            "A driver is trying to overtake you while you're driving at the speed limit. How should you react?",
            "What should you do if the driver behind you wants to overtake when you're already driving at the speed limit?",
            "If you're at the speed limit and another driver tries to overtake, how should you respond?"
        ], 
        "correct_answers": [
            "Keep a steady course and allow the driver behind to overtake.",
            "Maintain your lane and give the driver behind space to pass.",
            "Don't change your speed or direction; let the driver behind overtake safely.",
            "Drive steadily and let the driver behind overtake when it's safe.",
            "Allow the overtaking driver to pass by keeping your speed steady."
        ], 
        "incorrect_answers": [
            "Accelerate to get away from the driver behind.",
            "Move closer to the car ahead, so the driver has no room to overtake.",
            "Wave the driver behind to overtake when it's safe.",
            "Pull over to the side of the road to let them pass.",
            "Slow down suddenly to block the driver from overtaking.",
            "Move into the next lane to prevent them from overtaking.",
            "Speed up to avoid being overtaken.",
            "Change lanes quickly to prevent the overtaking maneuver."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Make sure that you know the speed limit for the road that you're on. The speed limit on a dual carriageway or motorway is 70 mph for cars and motorcycles unless signs indicate otherwise. The speed limits for different types of vehicles are listed in The Highway Code.",
        "questions": [
            "What's the national speed limit for cars and motorcycles on a dual carriageway?",
            "What's the national speed limit for cars and motorcycles on a dual carriageway?"
        ], 
        "correct_answers": [
            "70 mph",
            "70 mph"
        ],
        "incorrect_answers": [
            "50 mph",
            "40 mph",
            "30 mph",
            "60 mph",
            "80 mph"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "A long vehicle may have to straddle lanes either on or approaching a roundabout so that the rear wheels don't mount the kerb. If you're following a long vehicle, stay well back and give it plenty of room.",
        "questions": [
            "Which vehicle might have to take a different course from normal at a roundabout?",
            "Which type of vehicle may need to straddle lanes when approaching a roundabout?",
            "What kind of vehicle may behave differently at a roundabout because of its size?",
            "When approaching a roundabout, which vehicle is more likely to take a wider course?",
            "Which type of vehicle might need more room to manoeuvre at a roundabout?"
        ], 
        "correct_answers": [
            "Long vehicle",
            "Large vehicle",
            "HGV (Heavy Goods Vehicle)",
            "Articulated lorry",
            "Truck"
        ], 
        "incorrect_answers": [
            "Van",
            "Sports car",
            "Estate car",
            "Small hatchback",
            "SUV",
            "Compact car",
            "Motorcycle",
            "Crossover vehicle"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Don't pass cyclists too closely. Always leave as much room as you would for a car, and don't cut in front of them",
        "questions": [
            "Which vehicle should you allow extra room as you overtake them?",
            "What type of vehicle requires extra space when overtaking?",
            "When overtaking, which road user requires a larger safety margin?",
            "Which type of vehicle should you pass with caution, leaving extra room?",
            "Which road user needs more space when you're overtaking?"
        ], 
        "correct_answers": [
            "Bicycle",
            "Cyclist",
            "Bike",
        ], 
        "incorrect_answers": [
            "Tractor",
            "Road-sweeper",
            "Lorry",
            "Bus",
            "Caravan",
            "Motorcycle",
            "Heavy goods vehicle",
            "Truck"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_cyclist_left.jpg", "sign_question": False,
        "explanation": "Make allowances for cyclists, and give them plenty of room. Don't overtake and then immediately turn left. Be patient and turn behind them when they've passed the junction.",
        "questions": [
            "You're following a cyclist. What should you do when you wish to turn left a short distance ahead?",
            "What is the safest action when turning left while following a cyclist?",
            "How should you proceed when preparing to turn left while following a cyclist?",
            "When you plan to turn left shortly, how should you react if there's a cyclist ahead?"
        ],
        "correct_answers": [
            "Hold back until the cyclist has passed the junction.",
            "Wait until the cyclist clears the junction before turning.",
            "Allow the cyclist to pass the junction before making your turn.",
            "Do not overtake; wait for the cyclist to cross the junction."
        ],
        "incorrect_answers": [
            "Overtake the cyclist before you reach the junction.",
            "Pull alongside the cyclist and stay level until after the junction.",
            "Go around the cyclist on the junction.",
            "Honk to alert the cyclist before overtaking.",
            "Turn left ahead of the cyclist.",
            "Squeeze past the cyclist before the junction."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "The speed limit for cars towing caravans or trailers on dual carriageways or motorways is 60 mph. Due to the increased weight and size of the combination, you should plan further ahead. Take care in windy weather, as a strong side wind can make a caravan or large trailer unstable.",
        "questions": [
            "What's the speed limit for a car towing a caravan on a dual carriageway?",
            "What is the maximum speed allowed for a car towing a caravan on a dual carriageway?",
            "At what speed can a car with a caravan travel on a dual carriageway?",
            "What speed limit applies to a car towing a caravan on a dual carriageway?"
        ],
        "correct_answers": [
            "60 mph",
            "60 mph"
        ],
        "incorrect_answers": [
            "70 mph",
            "50 mph",
            "40 mph",
            "30 mph",
            "80 mph"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "A motorcycle can be lost from sight behind another vehicle. The use of headlights helps to make it more conspicuous and therefore more easily seen.",
        "questions": [
            "Why do motorcyclists use dipped headlights in daylight?",
            "What is the purpose of motorcyclists using dipped headlights during the day?",
            "Why might a motorcyclist keep their headlights dipped in daylight?",
            "For what reason do motorcyclists turn on dipped headlights during the daytime?"
        ],
        "correct_answers": [
            "So that the rider can be seen more easily.",
            "To increase the visibility of the motorcycle.",
            "To make the rider more noticeable to other road users.",
            "To enhance the motorcyclist's visibility during daylight."
        ],
        "incorrect_answers": [
            "To stop the battery overcharging.",
            "To improve the rider's vision.",
            "The rider is inviting you to proceed.",
            "To signal that the motorcycle is slowing down.",
            "To reduce glare from oncoming traffic.",
            "To warn pedestrians of their approach."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Whatever light is showing, you should know which light is going to appear next and be able to take appropriate action. For example, when amber is showing on its own, you'll know that red will appear next. This should give you ample time to anticipate and respond safely.",
        "questions": [
            "What does a red traffic light mean?",
            "What action should you take when you see a red traffic light?",
            "How should you respond to a red traffic signal?",
            "What must you do when the traffic light turns red?"
        ],
        "correct_answers": [
            "You must stop and wait behind the stop line.",
            "Stop immediately and wait at the stop line.",
            "Do not proceed; remain stationary behind the stop line.",
            "Come to a complete stop and stay behind the line."
        ],
        "incorrect_answers": [
            "You should stop unless turning left.",
            "Stop, if you're able to brake safely.",
            "Proceed with care.",
            "Continue if no other vehicles are approaching.",
            "Move slowly through the junction.",
            "Yield to oncoming traffic before proceeding."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_emerge_dual.jpg", "sign_question": False,
        "explanation": "Before emerging right onto a dual carriageway, make sure that the central reservation is deep enough to protect your vehicle. If it isn't, you should treat the dual carriageway as one road and check that it's clear in both directions before pulling out. Neglecting to do this could place part or all of your vehicle in the path of approaching traffic and cause a collision..",
        "questions": [
            "You're turning right onto a dual carriageway. What should you do before emerging?",
            "What safety check should you perform before turning right onto a dual carriageway?",
            "When preparing to turn right onto a dual carriageway, what must you consider?",
            "What should you check before emerging right onto a dual carriageway?"
        ],
        "correct_answers": [
            "Check that the central reservation is wide enough for your vehicle.",
            "Ensure that the central reservation can accommodate your vehicle safely.",
            "Confirm that the central reservation is deep enough to protect your vehicle.",
            "Make sure the reservation is spacious enough for your vehicle to wait safely."
        ],
        "incorrect_answers": [
            "Stop, apply the parking brake, and then select a low gear.",
            "Make sure that you leave enough room for the vehicle behind.",
            "Position your vehicle well to the left of the side road.",
            "Move quickly into the dual carriageway to avoid blocking traffic.",
            "Turn as soon as the nearest lane is clear.",
            "Signal and pull out immediately when a gap appears."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_no_motorcycles.png", "sign_question": True,
        "explanation": "You must comply with all traffic signs and be especially aware of those signs that apply specifically to the type of vehicle you're using.",
        "questions": [
            "What does this sign mean?",
            "What restriction does this sign indicate?",
        ],
        "correct_answers": [
            "No motorcycles.",
            "Motorcycles prohibited.",
            "Motorcycles not allowed.",
        ],
        "incorrect_answers": [
            "No cars.",
            "Cars only.",
            "Motorcycles only.",
            "No vehicles allowed.",
            "Bicycles only.",
            "No entry for any vehicle.",
            "Cars are prohibited.",
            "Cars not allowed."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_max_com.png", "sign_question": True,
        "explanation": "This sign gives you an early warning of a speed restriction. If you're travelling at a higher speed, slow down in good time. You could come across queuing traffic due to roadworks or a temporary obstruction.",
        "questions": [
            "What does this traffic sign mean?",
            "What does this road sign indicate?",
            "What is the purpose of this traffic sign?",
            "What regulation does this sign enforce?"
        ],
        "correct_answers": [
            "Compulsory maximum speed limit.",
            "Compulsory maximum speed limit.",
        ],
        "incorrect_answers": [
            "Advisory maximum speed limit.",
            "Advised separation distance.",
            "Compulsory minimum speed limit.",
            "Recommended speed limit.",
            "Minimum safe speed.",
            "Speed limit suggestion."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_hazard_warn.jpg", "sign_question": False,
        "explanation": "The centre of the road is usually marked by a broken white line, with lines that are shorter than the gaps. When the lines become longer than the gaps, this is a hazard warning line. Look well ahead for these, especially when you're planning to overtake or turn off.",
        "questions": [
            "What do the long white lines along the centre of the road mean?",
            "What is indicated by long white lines in the middle of the road?",
            "What do the lengthy white markings on the road's centre signify?",
            "What message do long white center lines on the road convey?"
        ],
        "correct_answers": [
            "Hazard warning",
            "Warning of a hazard ahead",
        ],
        "incorrect_answers": [
            "Bus lane",
            "Lane marking",
            "Give way",
            "Parking restriction",
            "Cycle lane",
            "No overtaking"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_national.png", "sign_question": True,
        "explanation": "This sign doesn't tell you the speed limit in figures. You should know the speed limit in the figures. You should know the speed limit for the type of road that you're on and the type of road that you're on and the type of vehicle that you're driving. Study your copy of The Highway Code.",
        "questions": [
            "What's the meaning of this sign?",
            "What does this sign indicate?",
            "What rule does this traffic sign enforce?",
            "What does this road sign mean?"
        ],
        "correct_answers": [
            "National speed limit applies.",
            "National speed limit."
        ],
        "incorrect_answers": [
            "No entry for vehicles.",
            "No waiting on the carriageway.",
            "Local speed limit applies.",
            "Speed limit restriction lifted.",
            "No speed limit applies.",
            "End of speed restriction."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Motorcycles and scooters are generally smaller than other vehicles and can be difficult to see. Wearing bright clothing makes it easier for other good road users to see a motorcyclist approaching, especially at junctions.",
        "questions": [
            "Why do motorcyclists wear bright clothing?",
            "What is the purpose of motorcyclists wearing high-visibility gear?",
            "Why might a motorcyclist choose to wear bright-colored attire?",
            "What is the reason for motorcyclists wearing fluorescent clothing?"
        ],
        "correct_answers": [
            "To make them more visible.",
            "To increase their visibility to other road users.",
            "To be easily seen by other drivers.",
            "To enhance their visibility on the road."
        ],
        "incorrect_answers": [
            "It helps them keep cool in summer.",
            "They must do so by law.",
            "The colours are popular.",
            "It makes them look more stylish.",
            "To follow a fashion trend.",
            "It improves their riding speed."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_yellow_lines.jpg", "sign_question": False,
        "explanation": "These lines may be painted on the road on the approach to a roundabout, a village or a particular hazard. The lines are raised and painted yellow, and their purpose is to make you aware of your speed. Reduce your speed in good time so that you avoid having to brake harshly over the last few metres before reaching the junction.",
        "questions": [
            "What's the purpose of the yellow lines painted across the road?",
            "What do the yellow lines painted on the road indicate?",
            "Why are yellow lines marked across the roadway?",
        ],
        "correct_answers": [
            "To make you aware of your speed.",
            "To alert you to your current speed.",
            "To prompt speed awareness."
        ],
        "incorrect_answers": [
            "To show a safe distance between vehicles.",
            "To keep the area clear of traffic.",
            "To warn you to change direction.",
            "To mark a pedestrian crossing.",
            "To indicate a bus lane.",
            "To signal an upcoming speed bump."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Don't reverse into a main road from a side road because your view will be restricted. The main road is likely to be busy and the traffic on it moving quickly.",
        "questions": [
            "Why could it be dangerous to reverse from a side road into a main road?",
            "What makes reversing from a side road onto a main road dangerous?",
            "What hazard exists when reversing from a side road onto a main road?",
            "Why is it risky to reverse into a main road from a side road?"
        ],
        "correct_answers": [
            "Your view will be restricted.",
            "You won't have a clear view of oncoming traffic.",
            "Your visibility may be limited when reversing.",
            "It's hard to see traffic approaching from behind."
        ],
        "incorrect_answers": [
            "Your mirrors will need adjusting.",
            "Your reversing lights will be hidden.",
            "Your reverse sensors will beep.",
            "The road surface may be uneven.",
            "Your car might not be in the correct gear.",
            "The side road might be too narrow."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If other drivers flash their headlights, this isn't a signal to show priority. The flashing of headlights has the same meaning as sounding the horn; it's a warning of their presence.",
        "questions": [
            "Other drivers may sometimes flash their headlights at you. What's the official meaning of this signal?",
            "What does it mean when another driver flashes their headlights at you?",
            "If another driver flashes their headlights, what are they signaling?",
            "What is the purpose of a driver flashing their headlights at you?"
        ],
        "correct_answers": [
            "They're warning you of their presence.",
            "They are alerting you to their presence.",
            "They want to make you aware of their approach.",
            "They're notifying you that they are nearby."
        ],
        "incorrect_answers": [
            "There's a radar speed trap ahead.",
            "There's a fault with your vehicle.",
            "They're giving way to you.",
            "You need to pull over.",
            "You should stop immediately.",
            "The road is closed ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "A green flashing beacon on a vehicle means the driver or passenger is a doctor on an emergency call. Give way to them if it's safe to do so. Be aware that the vehicle may be travelling quickly or may stop in a hurry.",
        "questions": [
            "What type of emergency vehicle is fitted with a green flashing beacon?",
            "Which emergency vehicle uses a green flashing beacon?",
            "What type of vehicle has a green flashing light to indicate an emergency?",
            "What emergency service vehicle is marked with a green flashing beacon?"
        ],
        "correct_answers": [
            "Doctor's car",
            "Doctor's vehicle",
        ],
        "incorrect_answers": [
            "Ambulance",
            "Fire engine",
            "Road gritter",
            "Police car",
            "Rescue vehicle"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_two_whites.jpg", "sign_question": False,
        "explanation": "You may cross the solid white line to pass a stationary vehicle or to pass a pedal cycle, horse or road maintenance vehicle if it's travelling at 10 mph or less. You may also cross the solid white line to enter a side road or access a property.",
        "questions": [
            "When may you cross a double solid white line in the middle of the road?",
            "Under what circumstances can you cross a double solid white line?",
            "When is it allowed to cross a double solid white line on the road?",
            "In which situation may you cross a double solid white line?"
        ],
        "correct_answers": [
            "To pass a road maintenance vehicle travelling at 10 mph or less.",
            "To overtake a road maintenance vehicle moving at 10 mph or less.",
            "When passing a road maintenance vehicle traveling at or below 10 mph.",
            "To pass a vehicle working on the road at 10 mph or slower."
        ],
        "incorrect_answers": [
            "To pass traffic that's queuing back at a junction.",
            "To pass a vehicle that's towing a trailer.",
            "To pass a car signalling to turn left ahead.",
            "When overtaking a slow-moving vehicle in your lane.",
            "To avoid a hazard in the road.",
            "When there's a lane closure ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "There are times when other drivers make incorrect or ill-judged decisions. Be tolerant and try not to retaliate or react aggressively. Always consider the safety of other road users, your passengers and yourself.",
        "questions": [
            "You're driving along this road. What should you do if the red car cuts in front of you?",
            "If the red car cuts in front of you while you're driving, what should you do?",
            "What action should you take if the red car moves in front of your vehicle?",
            "What should you do when the red car cuts into your lane ahead?"
        ],
        "correct_answers": [
            "Drop back to leave the correct separation distance.",
            "Increase the gap between you and the red car.",
            "Maintain a safe distance from the red car.",
            "Back off to ensure there's enough space between you and the red car."
        ],
        "incorrect_answers": [
            "Give a long blast on the horn.",
            "Accelerate to get closer to the red car.",
            "Flash your headlights several times.",
            "Tailgate the red car to force them to move.",
            "Move into the adjacent lane immediately.",
            "Speed up to prevent the red car from cutting in."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "While it's in operation, other vehicles must not use this part of the carriageway except to pick up or set down passengers. At other times, when the lane isn't in operation, you should still be aware that there may be cyclists using the lane. Give them plenty of room as you pas and allow for their movement from side to side, especially in windy weather or on a bumpy road.",
        "questions": [
            "A cycle lane, marked by a solid white line, is in operation. What does this mean for car drivers?",
            "What should car drivers do when a cycle lane with a solid white line is in operation?",
            "What is the rule for car drivers when a cycle lane is marked by a solid white line?",
            "What are car drivers prohibited from doing when a cycle lane with a solid white line is active?"
        ],
        "correct_answers": [
            "They mustn't drive along the lane.",
            "Car drivers are not allowed to drive in the lane.",
            "Car drivers must avoid using the cycle lane.",
            "Car drivers should not enter the cycle lane."
        ],
        "incorrect_answers": [
            "They may use the lane when necessary.",
            "They may drive in the lane at any time.",
            "They may park in the lane.",
            "They can cross the lane when overtaking.",
            "They can enter the lane to overtake a cyclist.",
            "They may briefly use the lane if there is no cyclist."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Satnavs can be useful when driving on unfamiliar routes. However, they can also distract you and cause you to lose control if you look at or adjust them while you're driving. Set the satnav before starting your journey, or pull up in a safe place before making any changes to it.",
        "questions": [
            "How can you make sure that a satellite navigation (satnav) system doesn't distract you when you're driving?",
            "What can you do to avoid distraction from a satnav while driving?",
            "How can you prevent your satnav from being a distraction when you're on the road?",
            "What should you do to keep your satnav from distracting you during your drive?"
        ],
        "correct_answers": [
            "Set it before your journey.",
            "Program the satnav before you start driving.",
            "Set your destination before starting your trip.",
            "Pre-set the satnav to avoid distractions while driving."
        ],
        "incorrect_answers": [
            "Turn it off while you're driving in built-up areas.",
            "Only set the destination when you're lost.",
            "Choose a voice that you find calming.",
            "Adjust the satnav while you're driving to find the best route.",
            "Turn off the satnav when you don't need directions.",
            "Keep changing the settings as you drive."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_diversion.png", "sign_question": True,
        "explanation": "When a diversion route has been put in place, drivers are advised to follow a symbol, which may be a black triangle, square, circle or diamond shape on a yellow background.",
        "questions": [
            "What does this sign indicate?",
            "What is the meaning of this sign?",
            "What does this sign represent?"
        ],
        "correct_answers": [
            "A diversion route.",
            "A marked diversion for vehicles.",
        ],
        "incorrect_answers": [
            "A cycle route.",
            "A pedestrian route.",
            "A picnic area.",
            "A road closure.",
            "A bus lane.",
            "A footpath."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "4_heavy_goods.png", "sign_question": False,
        "explanation": "These markers must be fitted to vehicles over 13 metres long, heavy goods vehicles, and rubbish skips placed on the road. They;re refelctive to make them easier to see in the dark.",
        "questions": [
            "Where would you expect to see these markers?"
        ], 
        "correct_answers": [
            "On a heavy goods vehicle."
        ],
        "incorrect_answers": [
            "On a diversion sign.",
            "On a motorway sign.",
            "On a railway bridge."
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