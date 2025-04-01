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

topic = "Rural Driving"

questions = [
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Pull into the nearest passing place on the left if you meet another vehicle on a narrow road. If the nearest passing place is on the right, wait opposite it.",
        "questions": [
            "You're on a road that's only wide enough for one vehicle. What should you do if a car is coming towards you?",
            "What action should you take when you meet an oncoming vehicle on a narrow road?",
            "If you encounter another vehicle on a single-track road, what should you do?",
            "What should you do if a car approaches on a road only wide enough for one vehicle?",
            "How should you react if another vehicle is coming towards you on a narrow road?"
        ], 
        "correct_answers": [
            "Pull into a passing place on your left.",
            "Pull into a passing place on your left.",
            "Pull into a passing place on your left."
        ],
        "incorrect_answers": [
            "Pull into a passing place if your vehicle is wider.",
            "Pull into a passing place on your right.",
            "Force the other driver to reverse.",
            "Speed up to get through before the other vehicle.",
            "Move to the center of the road to claim priority."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Horses can be startled by the sound of a car engine or the rush of air caused by a vehicle passing too closely. Keep well back and only pass when it's safe. Leave them plenty of room; you may have to use the other side of the road to go past safely.",
        "questions": [
            "What should you do when you're overtaking a horse and rider?",
            "How should you pass a horse and rider on the road?",
            "What's the correct way to overtake a horse on the road?",
            "When overtaking a horse and rider, what precautions should you take?",
            "What should you consider when passing a horse on the road?"
        ], 
        "correct_answers": [
            "Go past slowly and carefully.",
            "Pass the horse at a slow speed and with caution.",
            "Overtake the horse slowly, giving plenty of space.",
            "Approach slowly and pass the horse calmly.",
            "Move past the horse with care and at low speed."
        ],
        "incorrect_answers": [
            "Flash your headlights as a warning.",
            "Go past as quickly as possible.",
            "Sound your horn as a warning.",
            "Rev your engine to alert the rider.",
            "Speed up to pass quickly before the horse reacts."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Be cautious, especially when your view is restricted by hedges, bushes, walls, large vehicles, etc. In the summer months, these junctions can become more difficult to deal with, because growing foilage may further obscure your view.",
        "questions": [
            "You're approaching an unmarked crossroads. How should you deal with the junction?"
            "What should you do when approaching an unmarked crossroads?",
            "How should you approach an unmarked crossroads safely?",
            "What's the safest way to handle an unmarked crossroads?",
            "What precautions should you take at an unmarked crossroads?"
        ], 
        "correct_answers": [
            "Slow down and look both ways.",
            "Slow down and look left and right."
        ],
        "incorrect_answers": [
            "Accelerate and look to the left.",
            "Slow down and keep to the right.",
            "Accelerate and keep to the middle.",
            "Slow down and look to the right.",
            "Accelerate and keep to the left.",
            "Slow down and look to the right.",
            "Accelerate and look to the right."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If someone in charge of animals asks you to stop, you should do so and switch off your engine. Animals are unpredictable and startle easily; they could turn and run into your path or the path of another moving vehicle.",
        "questions": [
            "What should you do when a person herding sheep asks you to stop?",
            "What action should you take if someone controlling animals signals you to stop?",
            "If a farmer waves at you to stop while herding cattle, what should you do?",
            "How should you respond if a person herding livestock signals you to halt?",
            "What is the correct response when someone managing animals requests you to stop?"
        ], 
        "correct_answers": [
            "Stop and switch off your engine.",
            "Come to a halt and turn off your engine.",
            "Stop your vehicle and turn off the engine.",
            "Pull over and switch off your engine.",
            "Stop completely and turn off the engine."
        ],
        "incorrect_answers": [
            "Continue on but drive slowly.",
            "Try to get past quickly.",
            "Ignore them as they have no authority.",
            "Sound your horn to get them to move.",
            "Rev your engine to scare the animals away.",
            "Drive around them at a reduced speed.",
            "Flash your headlights to warn them.",
            "Speed up to pass before the animals move.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "On a quiet country road, always be aware of a hazard just around the next bend, such as a slow-moving vehicle or pedestrians. Pedestrians are advised to walk on the right-hand side of the road if there's no pavement so that they may be walking towards you on your side of the road.",
        "questions": [
            "You're on a country road. What should you expect to see coming towards you on your side of the road?",
            "When driving on a quiet rural road, who might be walking towards you on your side?",
            "On a country lane, who is likely to approach you on your side of the road?",
            "What might you encounter on your side of a quiet country road?",
            "While driving on a rural road, who could be walking towards you on your side?"
        ], 
        "correct_answers": [
            "Pedestrians",
            "People walking",
            "Walkers",
            "People on foot"
        ],
        "incorrect_answers": [
            "Bicycles",
            "Motorcycles",
            "Horse riders",
            "Farm vehicles",
            "Joggers",
            "Cars",
            "Tractors",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "By driving all four wheels, the vehicle has a maximum grip on the road. This grip is especially helpful when travelling on slippy or uneven surfaces. However, having a four-wheel drive doesn't replace the skills you need to drive safely.",
        "questions": [
            "What's the main benefit of driving a four-wheel-drive vehicle?",
            "What advantage does a four-wheel-drive vehicle offer?",
            "Why might someone choose to drive a four-wheel-drive car?",
            "What is a key benefit of having a four-wheel-drive vehicle?",
            "What makes a four-wheel-drive vehicle useful on the road?"
        ], 
        "correct_answers": [
            "Improved grip on the road.",
            "Enhanced stability on slippery surfaces.",
            "Increased road grip in poor weather.",
            "More control on uneven terrain."
        ],
        "incorrect_answers": [
            "Lower fuel consumption.",
            "Improved passenger comfort.",
            "Shorter stopping distances.",
            "Easier parking.",
            "Reduced maintenance costs.",
            "Higher top speed.",
            "Quieter engine performance.",
            "Faster acceleration."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Horses and their riders move more slowly than other road users. They might not have time to cut across heavy traffic to take up a position in the right-hand lane. For this reason, a horse and rider may approach a roundabout in the left-hand lane even though they're turning right.",
        "questions": [
            "A horse rider is in the left-hand lane approaching a roundabout. Where should you expect the rider to go?",
            "Where might a horse rider positioned in the left-hand lane at a roundabout end up going?",
            "If a horse rider is in the left-hand lane approaching a roundabout, which direction could they take?",
            "At a roundabout, a horse rider in the left-hand lane might go where?",
            "What direction might a horse rider in the left-hand lane at a roundabout take?"
        ], 
        "correct_answers": [
            "In any direction.",
            "Possibly in any direction.",
            "Any exit from the roundabout.",
            "Any of the available routes."
        ],
        "incorrect_answers": [
            "In the right.",
            "In the left.",
            "In the middle.",
            "Only to the left.",
            "Only to the right.",
            "Straight ahead only.",
            "Only into the next exit.",
            "Only in the opposite direction."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "As you drive, look well ahead and all around so that you're ready for any hazards that might develop. If you have to stop in an emergency, react as soon as you can while keeping control of the vehicle. Keep both hands on the steering wheel so you can control the vehicle's direction of travel.",
        "questions": [
            "You're driving on a wet road. What should you do if you have to stop your vehicle in an emergency?",
            "On a wet road, how should you handle an emergency stop?",
            "What is the correct procedure for stopping in an emergency on a wet road?",
            "How should you stop your vehicle safely in an emergency on a wet surface?",
            "When stopping suddenly on a wet road, what should you do?"
        ], 
        "correct_answers": [
            "Keep both hands firmly on the steering wheel.",
            "Maintain a firm grip on the steering wheel.",
            "Hold the steering wheel securely with both hands.",
            "Ensure both hands are kept on the steering wheel.",
        ],
        "incorrect_answers": [
            "Apply the parking brake and footbrake together.",
            "Select reverse gear.",
            "Give an arm signal.",
            "Pump the brakes rapidly.",
            "Turn the steering wheel sharply.",
            "Switch to a lower gear immediately.",
            "Flash your headlights.",
            "Sound the horn to warn others."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Allow the horse rider to enter and exit the roundabout in their own time. They may feel safer keeping to the left around the roundabout. Don't get up close behind or alongside them, because that would probably upset the horse and create a dangerous situation.",
        "questions": [
            "You see a horse rider as you approach a roundabout. What should you do if they're signalling right but keeping well to the left?",
            "What action should you take if a horse rider at a roundabout signals right but stays to the left?",
            "At a roundabout, a horse rider signals right but positions on the left. How should you react?",
            "When approaching a roundabout, what should you do if a horse rider keeps left but indicates right?",
            "How should you handle the situation when a horse rider at a roundabout signals right but remains on the left side?"
        ], 
        "correct_answers": [
            "Stay well back.",
            "Give them plenty of space.",
            "Maintain a safe distance.",
            "Hold back and be patient.",
            "Allow them extra room."
        ],
        "incorrect_answers": [
            "Proceed as normal.",
            "Keep close to them.",
            "Cut in front of them.",
            "Sound your horn to alert them.",
            "Overtake them quickly.",
            "Try to squeeze past on the right.",
            "Move ahead before they complete their turn.",
            "Take the roundabout at speed to pass them."
    ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "It's important to keep a safe distance from the vehicle in front at all times. This still applies in congested tunnels, even if you're moving very slowly or have stopped. If the vehicle in front breaks down, you may need room to manoeuvre past it.",
        "questions": [
            "What should you do if you have to stop while you're going through a congested tunnel?",
            "How should you position your vehicle when stopped in a busy tunnel?",
            "When stopping in a congested tunnel, how much space should you leave?",
            "What precautions should you take when stationary in a crowded tunnel?",
            "While stopped in a tunnel with heavy traffic, what is the best practice?"
        ], 
        "correct_answers": [
            "Keep a safe distance from the vehicle in front.",
            "Leave enough space to manoeuvre around the vehicle ahead.",
            "Maintain a safe gap between your car and the one in front.",
            "Ensure there is sufficient distance from the vehicle ahead.",
            "Keep a reasonable distance to allow room for movement."
        ],
        "incorrect_answers": [
            "Ignore any message signs, as they're never up to date.",
            "Make a U-turn and find another route.",
            "Pull up very close to the vehicle in front to save space.",
            "Sound your horn to alert other drivers.",
            "Switch lanes frequently to find a faster route.",
            "Rev your engine to signal impatience.",
            "Flash your headlights to move traffic along.",
            "Follow the vehicle in front as closely as possible."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Windscreen pillars can obstruct your view, particularly at bends and junctions. Look out for other road users - especially cyclists, motorcyclists and pedestrians who can easily be overlooked.",
        "questions": [
            "When do windscreen pillars cause a serious obstruction to your view?",
            "At which situations do windscreen pillars block your view the most?",
            "When are windscreen pillars most likely to obstruct your view?",
            "What type of road situations can windscreen pillars make more difficult to see?",
            "When should you be extra cautious about windscreen pillars blocking your view?"
        ], 
        "correct_answers": [
            "When you're approaching bends and junctions.",
            "At bends and junctions.",
            "When turning at bends or junctions.",
            "When navigating around bends or junctions."
        ],
        "incorrect_answers": [
            "When you're approaching a one-way street.",
            "When you're driving on a motorway.",
            "When you're driving on a dual carriageway.",
            "When you're parked on the side of the road.",
            "When you're driving through a tunnel.",
            "When you're reversing into a parking space.",
            "When you're driving in a residential area.",
            "When you're in a traffic jam."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "When driving down a steep hill, gravity will cause your vehicle to speed up. This will make it more difficult for you to stop. To help keep your vehicle's speed under control, select a lower gear to give you more engine braking and make careful use of the brakes.",
        "questions": [
            "You're about to go down a steep hill. What should you do to control the speed of your vehicle?",
            "What is the best way to control your speed when driving downhill?",
            "How should you manage your vehicle's speed when descending a steep hill?",
            "What action should you take before going down a steep hill to control your vehicle's speed?",
            "What should you do to prevent your vehicle from speeding up too much while going downhill?"
        ], 
        "correct_answers": [
            "Select a low gear and use the brakes carefully.",
            "Select a low gear and use the brakes carefully."
            "Select a low gear and use the brakes carefully."
        ],
        "incorrect_answers": [
            "Select a high gear and use the brakes firmly.",
            "Select a high gear and use the brakes carefully.",
            "Select a low gear and avoid using the brakes.",
            "Select a low gear and use the brakes firmly."
            "Select a high gear and avoid using the brakes."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you're wearing sunglasses, you should remove them before driving into a tunnel. If you don't your vision will be restricted, even in tunnels that appear ti be well-lit.",
        "questions": [
            "What should you do before driving into a tunnel?",
            "What action should you take before entering a tunnel while wearing sunglasses?",
            "How can you ensure clear vision when driving into a tunnel?",
            "What is important to do before driving through a tunnel with sunglasses on?",
            "What should be removed before entering a tunnel if you're wearing them?"
        ], 
        "correct_answers": [
            "Take off your sunglasses.",
            "Remove your sunglasses.",
            "Take your sunglasses off.",
            "Remove sunglasses.",
            "Take off your sunglasses."
        ],
        "incorrect_answers": [
            "Switch off your radio.",
            "Close your sunroof.",
            "Switch on your windscreen wipers.",
            "Adjust your seat position.",
            "Open your windows for better visibility.",
            "Turn on your headlights.",
            "Check your tire pressure."
    ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "The engine will need more power to pull the vehicle up the hill. When approaching a steep hill you should select a lower gear to help maintain your speed. You should do this without hesitation so that you don't lose too much speed before engaging the lower gear.",
        "questions": [
            "What will happen to your car when you drive up a steep hill?",
            "What effect does driving up a steep hill have on your engine?",
            "When driving uphill, how does the engine perform?",
            "What should you expect when you drive up a steep incline?",
            "How does driving up a steep hill affect your vehicle's engine?"
        ], 
        "correct_answers": [
            "The engine will work harder.",
            "The engine will exert more effort.",
            "The engine will use more power."
        ],
        "incorrect_answers": [
            "Overtaking will be easier.",
            "The steering will feel heavier.",
            "The higher gears will pull better.",
            "The engine will produce less power.",
            "You will need to accelerate less.",
            "The car will be more fuel-efficient.",
            "The brakes will work more effectively.",
            "The vehicle will become lighter."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "No one has priority at unmarked crossroads, no matter what vehicle is passing by so there is no need to feel to have priority at the unmarked crossroads to ensure a safe passing.",
        "questions": [
            "Who has priority at an unmarked crossroads?",
            "At an unmarked crossroads, who has priority?",
            "Who has the right of way at an unmarked crossroads?",
            "When approaching an unmarked crossroads, who goes first?",
            "At an unmarked crossroads, who should give way?"
        ], 
        "correct_answers": [
            "No-one has priority.",
            "There is no priority at an unmarked crossroads.",
            "At an unmarked crossroads, you must all give way.",
            "No vehicle has priority at an unmarked junction.",
            "At an unmarked crossroad, each driver must assess the situation."
        ],
        "incorrect_answers": [
            "The larger vehicle.",
            "The faster vehicle.",
            "The smaller vehicle.",
            "The vehicle coming from the right.",
            "The vehicle on the main road.",
            "The vehicle travelling uphill.",
            "The vehicle with more passengers."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_mini_roundabout.png", "sign_question": True,
        "explanation": "When you see this sign, look out for any direction signs and judge whether you need to signal your intentions. Do this in good time so that other users approaching the roundabout know what you're planning to do.",
        "questions": [
            "What does this sign mean?",
            "What is indicated by this road sign?",
            "What does the sign you see mean?",
            "What is the meaning of this traffic sign?",
            "Which road feature does this sign indicate?"
        ],
        "correct_answers": [
            "Mini-roundabout",
            "A small roundabout",
        ],
        "incorrect_answers": [
            "Buses turning",
            "Keep right",
            "Ring road",
            "Pedestrian crossing",
            "No entry",
            "One-way street",
            "Cyclists ahead"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_train_lights.png", "sign_question": False,
        "explanation": "At a level crossing, flashing red lights mean you must stop. If the train passes but the lights keep flashing, wait. Another train may be coming.",
        "questions": [
            "You're waiting at a level crossing. What should you do if the red warning lights continue to flash after a train has passed by?",
            "What should you do if the red lights at a level crossing stay on after the train has passed?",
            "If the red warning lights are flashing at a level crossing after a train has passed, what should you do?",
            "You're at a level crossing and the red lights are still flashing after the train has passed. What action should you take?",
            "What should you do when the red lights at a level crossing stay on after the train has gone?"
        ],
        "correct_answers": [
            "Continue to wait.",
            "Wait until the red lights stop flashing.",
            "Remain stationary and wait for the lights to go off.",
            "Do not proceed until the flashing lights turn off."
        ],
        "incorrect_answers": [
            "Telephone the signal operator.",
            "Get out and investigate.",
            "Drive across carefully.",
            "Stop and reverse.",
            "Go around the barriers if safe to do so.",
            "Honk your horn to alert others."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_sharp_left.png", "sign_question": True,
        "explanation": "This sign indicates that the road will bend sharply to the left. Slow down in plenty of time and select the correct gear before you start to turn. Braking hard and late, while also sharply changing direction, is likely to cause a skid.",
        "questions": [
            "What should you expect if you see this sign ahead?",
            "What does this sign indicate about the road ahead?",
            "What does this road sign warn you about?",
            "Seeing this sign ahead, what should you anticipate on the road?",
            "What is the meaning of this sign as you approach?"
        ],
        "correct_answers": [
            "The road will bend sharply to the left.",
            "There is a sharp left bend ahead.",
            "The road will curve sharply to the left.",
            "A sharp left-hand bend is ahead."
        ],
        "incorrect_answers": [
            "The road will go steeply downhill.",
            "The road will bend sharply to the right.",
            "The road will go steeply uphill.",
            "The road will turn to a one-way street.",
            "There will be a roundabout ahead.",
            "The road will become narrower."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_danger.png", "sign_question": True,
        "explanation": "This sign is there to alert you to the likelihood of danger ahead. It may be accompanied by a plate indicating the type of hazard. Be ready to reduce your speed and take avoiding action.",
        "questions": [
            "What does this traffic sign mean?",
            "What is the meaning of this road sign?",
            "What does this sign indicate about the road ahead?",
            "What warning does this sign give to drivers?",
            "What is the purpose of this traffic sign?"
        ],
        "correct_answers": [
            "Danger ahead.",
            "There is a hazard ahead.",
            "A danger is present ahead.",
            "Caution: danger ahead.",
            "Warning: danger ahead."
        ],
        "incorrect_answers": [
            "Slippery road ahead.",
            "Tyres liable to punctures ahead.",
            "Service area ahead.",
            "Roadworks ahead.",
            "Steep hill ahead.",
            "Narrow bridge ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_tram_only.png", "sign_question": True,
        "explanation": "Take extra care when you encounter trams. Look out for the road markings and signs that alert you to them. Modern trams are very quiet and you may not hear them approaching.",
        "questions": [
            "What does this sign mean?",
            "What is indicated by this traffic sign?",
            "What does this road sign show?",
            "What does this sign represent?",
            "What does this symbol on the road mean?"
        ],
        "correct_answers": [
            "Route for trams.",
            "Tram route ahead.",
        ],
        "incorrect_answers": [
            "Give way to buses.",
            "Give way to trams.",
            "Route for buses.",
            "No entry for trams.",
            "Route for cyclists.",
            "Bus route ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_T_junction.png", "sign_question": True,
        "explanation": "This type of sign warns you of hazards ahead. Make sure you look at each sign and road marking that you pass so that you don't miss any vital information or instructions. This sign shows there's a T-junction with priority over vehicles from the right.",
        "questions": [
            "What does this sign mean?",
            "What is indicated by this road sign?",
            "What does this traffic sign warn of?",
            "What type of junction is indicated by this sign?",
            "What does this road sign suggest?"
        ],
        "correct_answers": [
            "T-junction.",
            "T-junction ahead.",
        ],
        "incorrect_answers": [
            "Turn left ahead.",
            "Give way.",
            "No through road.",
            "Road narrows ahead.",
            "Roundabout ahead.",
            "One-way street ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_truck_stop.jpg", "sign_question": False,
        "explanation": "Sometimes, large vehicles may need more spcae than other road users. If a vehicle needs more time and space to turn, be prepared to stop and wait.",
        "questions": [
            "What should you be prepared to do in this situation?",
            "How should you react in this situation?",
            "What is the best action to take in this scenario?",
            "How should you handle this situation?",
            "What should you do when facing this situation?"
        ],
        "correct_answers": [
            "Slow down and give way.",
            "Reduce speed and yield.",
            "Be prepared to slow down and give priority.",
            "Slow your vehicle and give way."
        ],
        "incorrect_answers": [
            "Sound your horn and continue.",
            "Squeeze through the gap.",
            "Report the driver to the police.",
            "Accelerate to pass through quickly.",
            "Ignore the situation and keep going."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_reversing_car.jpg", "sign_question": False,
        "explanation": "White lights at the rear of a car show that the driver has selected the reverse gear. The driver is hidden from view so can't see you approaching. Sound your horn to warn of your presence, and be ready to stop if the car reverses into your path.",
        "questions": [
            "What should you do if a vehicle begins reversing off a driveway?",
            "How should you react if a vehicle starts to reverse off a driveway?",
            "What is the proper action if a vehicle is backing out of a driveway?",
            "What should you do if you see a vehicle reversing out of a driveway?",
            "How should you handle a situation where a vehicle is reversing off a driveway?"
        ],
        "correct_answers": [
            "Sound your horn and be prepared to stop.",
            "Honk your horn and prepare to stop if necessary.",
            "Alert the driver with your horn and be ready to stop.",
            "Use your horn to alert the driver and be prepared to halt.",
            "Sound your horn and be ready to stop or avoid."
        ],
        "incorrect_answers": [
            "Drive through as you have priority.",
            "Speed up and drive through quickly.",
            "Move to the opposite side of the road.",
            "Ignore the vehicle and continue as normal.",
            "Flash your headlights to signal the vehicle."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_opp_priority.png", "sign_question": True,
        "explanation": "Priority signs are normally shown where the road is narrow and there isn't enough room for two vehicles to pass. Examples are narrow bridges, roadworks and where's a width restriction. Make sure you know who has priority; don't force your way through. Show courtesy and consideration to other road users.",
        "questions": [
            "What does this traffic sign indicate?",
            "What is the meaning of this traffic sign?",
            "What action does this traffic sign require you to take?",
            "What should you do if you see this traffic sign?",
            "How should you respond to this traffic sign?"
        ],
        "correct_answers": [
            "Give priority to oncoming traffic.",
            "Yield to vehicles coming from the opposite direction.",
            "Allow oncoming traffic to go first.",
            "Give way to vehicles approaching from the opposite direction.",
            "Let the oncoming traffic pass before proceeding."
        ],
        "incorrect_answers": [
            "Two-way traffic.",
            "One-way traffic only.",
            "No overtaking allowed.",
            "Traffic in both directions.",
            "You have priority over oncoming traffic."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_white_line.jpg", "sign_question": False,
        "explanation": "The continuous white line shows the edge of the carriageway. It can be especially useful when visibility is restricted, such as at night or in bad weather. It's discontinued in some places; for example, at junctions, lay-bys, entrances or other openings.",
        "questions": [
            "What does the solid white line along the side of the road mean?",
            "What is indicated by the solid white line at the side of the road?",
            "What should you understand if you see a solid white line on the side of the road?",
            "What does a solid white line at the edge of the road represent?",
            "What is the purpose of the solid white line at the side of the carriageway?"
        ],
        "correct_answers": [
            "Edge of the carriageway.",
            "Boundary of the road.",
            "Demarcation of the road's edge.",
            "The side limit of the road.",
            "Marking for the edge of the carriageway."
        ],
        "incorrect_answers": [
            "Cycle path.",
            "Traffic lights ahead.",
            "Footpath on the left.",
            "Bus lane.",
            "Pedestrian crossing."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_tourist.png", "sign_question": True,
        "explanation": "These signs indicate places of interest and are designed to guide you by the easiest route. They're particularly useful when you're unfamilar with the area.",
        "questions": [
            "What does this sign indicate?",
            "What does this road sign mean?",
            "What is represented by this traffic sign?",
            "What is the meaning of this sign?",
        ],
        "correct_answers": [
            "Tourist attraction.",
            "Tourist site."
        ],
        "incorrect_answers": [
            "Beware of trams.",
            "Beware of trains.",
            "Level crossing.",
            "Roadworks ahead.",
            "Pedestrian crossing."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_ford.png", "sign_question": True,
        "explanation": "If your brakes have been thoroughly soaked, you should check that they're working properly before you build up speed again. Before you do this, remember to check your mirrors and consider what's behind you.",
        "questions": [
            "You're driving on a country road and see this sign. What should you do after dealing with the hazard?",
            "What should you do after you've dealt with the hazard on a country road when you see this sign?",
            "When driving along a country road and seeing this sign, what should you do next?",
            "After addressing the hazard on a country road, what should you do when you see this sign?",
            "While driving on a country road, what's the next step after encountering this sign?"
        ],
        "correct_answers": [
            "Test your brakes.",
            "Check your brakes.",
            "Test your braking system.",
            "Make sure your brakes are working well."
        ],
        "incorrect_answers": [
            "Accelerate briskly.",
            "Switch on your hazard warning lights.",
            "Check your tyre pressures.",
            "Increase your speed cautiously.",
            "Turn on your fog lights."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_carriageway_end.png", "sign_question": True,
        "explanation": "Don't wait till the last moment before moving into the left-hand lane. Plan and don't rely on other traffic letting you in.",
        "questions": [
            "What does this sign indicate?",
            "What is the meaning of this sign?",
            "What does this road sign represent?",
            "When you see this sign, what does it mean?",
            "What is the interpretation of this sign?"
        ],
        "correct_answers": [
            "End of dual carriageway.",
            "Dual carriageway ends.",
        ],
        "incorrect_answers": [
            "End of narrow bridge.",
            "Road narrows.",
            "Tall bridge.",
            "No entry ahead.",
            "End of motorway."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_crossroads.png", "sign_question": True,
        "explanation": "The priority through the junction is shown by the broader line. You need to be aware of the hazard posed by traffic crossing or pulling out onto a major road.",
        "questions": [
            "What does this sign represent?",
            "What is the meaning of this sign?",
            "What does this road sign indicate?",
            "What should you understand from this sign?",
            "What is the interpretation of this sign?"
        ],
        "correct_answers": [
            "Crossroads.",
            "Intersection ahead.",
            "Crossroads ahead."
        ],
        "incorrect_answers": [
            "Level crossing without gate.",
            "Level crossing with gate.",
            "Ahead only.",
            "One-way road.",
            "No entry ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_cycle_route.png", "sign_question": True,
        "explanation": "When there's a cycle route ahead, a sign will show a bicycle in a red warning triangle. Watch out for children on bicycles and cyclists rejoining the main road.",
        "questions": [
            "What is the meaning of this sign?",
            "What does this road sign indicate?",
            "What does this sign represent?",
            "What is the interpretation of this sign?"
        ],
        "correct_answers": [
            "Cycle route ahead.",
            "Cycle path ahead.",
            "Cycling route ahead.",
        ],
        "incorrect_answers": [
            "Cycle in a single file.",
            "Cyclists must dismount.",
            "Cycles aren't allowed.",
            "Cycling prohibited.",
            "No cycling ahead."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_roundabout.png", "sign_question": True,
        "explanation": "As you approach a roundabout, look well ahead and check all signs. Decide which exit you wish to take and move into the correct position as you approach the roundabout, signalling as required.",
        "questions": [
            "What does this sign mean?",
            "What is indicated by this road sign?",
            "What does this traffic sign represent?",
            "What should you expect from this sign?"
        ],
        "correct_answers": [
            "Roundabout.",
            "Roundabout."
        ],
        "incorrect_answers": [
            "No vehicles.",
            "Mini-roundabout.",
            "Ring road.",
            "One-way street.",
            "Pedestrian zone.",
            "Dead end."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_left_white_marking.jpg", "sign_question": False,
        "explanation": "The road marking shows that overtaking drivers or riders need to return to the left. These markings show the direction drivers must pass hatch markings or solid double white lines. They're also used to show the route that high vehicles should take under a low-arched bridge.",
        "questions": [
            "What does this curved arrow road marking mean?",
            "What is the meaning of this curved arrow on the road?",
            "What should you interpret from this curved arrow road marking?",
            "What does this road marking with a curved arrow indicate?"
        ],
        "correct_answers": [
            "Overtaking traffic should move back to the left.",
            "Vehicles overtaking should return to the left lane.",
            "Traffic moving to the left should return to the original lane.",
            "After overtaking, drivers should move back to the left."
        ],
        "incorrect_answers": [
            "The road ahead bends to the left.",
            "Heavy vehicles should take the next road on the left to avoid a weight limit.",
            "The road ahead has a chamber to the left.",
            "There is a left turn ahead.",
            "The road narrows to the left.",
            "A pedestrian crossing is ahead on the left."
    ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_bush_road.jpg", "sign_question": False,
        "explanation": "Pedestrians walking on a road with no pavement should walk against the direction of the traffic. You can't see around this bend and if pedestrians are on the road you need to be able to deal with the situation safely. Always keep this in mind and give yourself time to react if a hazard does appear.",
        "questions": [
            "You're driving towards this left-hand bend. What danger should you be anticipating?",
            "What potential hazard should you expect when approaching this left-hand bend?",
            "As you drive towards this left-hand bend, what danger might you encounter?",
            "What risk should you look out for when approaching this left-hand curve?"
        ],
        "correct_answers": [
            "Pedestrians walking towards you.",
            "Pedestrians coming towards you.",
            "People walking in the opposite direction.",
            "Walkers approaching from the other side of the bend."
        ],
        "incorrect_answers": [
            "A vehicle overtaking you.",
            "The road getting narrower.",
            "Mud on the road.",
            "A pothole in the road.",
            "Loose gravel on the road.",
            "Animals crossing the road."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_hidden_dip.png", "sign_question": True,
        "explanation": "You won't be able to see any hazards that might be hidden in the dip. As well as oncoming traffic, the dip may conceal cyclists, horse riders, parked vehicles or pedestrians on the road.",
        "questions": [
            "You're about to overtake. What should you do when you see this sign?",
            "What action should you take when you see this sign while preparing to overtake?",
            "What is the correct response when you encounter this sign while overtaking?",
            "When you see this sign before overtaking, what should you do?"
        ],
        "correct_answers": [
            "Hold back until you can see clearly ahead.",
            "Wait until your view ahead is clear before overtaking.",
            "Do not overtake until the road ahead is visible.",
            "Wait until visibility improves before attempting to overtake."
        ],
        "incorrect_answers": [
            "Move to the right to get a better view.",
            "Switch your headlights on before overtaking.",
            "Overtake the other driver as quickly as possible.",
            "Accelerate to pass the vehicle quickly.",
            "Look for another place to overtake immediately.",
            "Overtake as soon as you feel it's safe."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "3_bridge_big.jpg", "sign_question": False,
        "explanation": "The higehst point of the bridge is in the centre, so a large vehicle might have to move to the centre of the road to have enough room to pass safely under the bridge.",
        "questions": [
            "What type of vehicle could you expect to meet in the middle of the road?",
            "Which vehicle might you encounter in the middle of the road?",
            "What kind of vehicle could be found in the center of the road?",
            "Which vehicle could be driving in the middle of the road?"
        ],
        "correct_answers": [
            "Lorry",
            "Truck",
            "Heavy goods vehicle",
            "Large vehicle"
        ],
        "incorrect_answers": [
            "Car",
            "Bicycle",
            "Motorcycle",
            "Trailer",
            "Limousine"
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