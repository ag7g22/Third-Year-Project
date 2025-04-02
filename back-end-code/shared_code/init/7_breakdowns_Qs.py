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

topic = "Breakdowns"

questions = [
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Lorry drivers can be unaware of objects falling from their vehicles. If you see something fall onto the motorway, look to see if the driver pulls over. If they don't stop, don't attempt to retrieve the object yourself. Pull onto the hard shoulder near an emergency telephone and report the hazard.",
        "questions": [
            "What should you do if you see a large box fall from a lorry onto the motorway?",
            "If a large box falls from a lorry onto the motorway, what should you do?",
            "What is the correct action if you notice a large box fall off a lorry onto the motorway?",
            "How should you react if you see a large box fall from a lorry onto the motorway?",
            "You're driving and a large box falls off a lorry onto the motorway. What should you do?"
        ],
        "correct_answers": [
            "Go to the next emergency telephone and report the hazard.",
            "Report the hazard to the next emergency telephone.",
            "Use the nearest emergency telephone to report the hazard.",
            "Call the emergency services from the next available telephone.",
            "Report the box to the nearest motorway emergency phone."
        ],
        "incorrect_answers": [
            "Pull over to the hard shoulder, then remove the box.",
            "Catch up with the lorry and try to get the driver's attention.",
            "Stop close to the box until the police arrive.",
            "Attempt to move the box yourself.",
            "Wait for the box to be moved by other vehicles."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Follow the instructions given by the signs or by tunnel officials. In congested tunnels, a minor incident can soon turn into a major one, with serious or even fatal results.",
        "questions": [
            "You're going through a long tunnel. What will warn you of congestion or an incident ahead?",
            "What will indicate congestion or an incident ahead when you're driving through a long tunnel?",
            "When driving through a long tunnel, how will you be warned about congestion or incidents ahead?",
            "What should you look for in a tunnel to warn you of congestion or incidents ahead?",
            "While driving through a long tunnel, what will alert you to congestion or an incident?"
        ],
        "correct_answers": [
            "Variable message signs.",
            "Signs displaying variable messages.",
            "Message signs.",
            "Variable signs warning of incidents.",
            "Electronic message signs."
        ],
        "incorrect_answers": [
            "Hazard warning lines.",
            "Other drivers flashing their lights.",
            "Areas with hatch markings.",
            "Static warning signs.",
            "Pedestrian signs."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Park as far to the left as you can and leave the vehicle by the nearside door. Don't attempt even simple repairs. Instead, walk to an emergency telephone on your side of the road and phone for help. While waiting for help to arrive, stay by your car, keeping well away from the carriageway and hard shoulder.",
        "questions": [
            "Your car gets a puncture while you're driving on the motorway. What should you do when you've stopped on the hard shoulder?",
            "What should you do if your car gets a puncture on the motorway and you've stopped on the hard shoulder?",
            "You're on the hard shoulder after a puncture. What is the first thing you should do?",
            "What action should you take after stopping on the hard shoulder with a puncture?",
            "After your car gets a puncture on the motorway and you've stopped on the hard shoulder, what should you do?"
        ],
        "correct_answers": [
            "Use an emergency telephone and call for help.",
            "Call for help using an emergency telephone.",
            "Contact emergency services using the nearest phone.",
            "Use the emergency telephone to get assistance.",
            "Call for help using a motorway emergency phone."
        ],
        "incorrect_answers": [
            "Only change the wheel if you have a passenger to help you.",
            "Carefully change the wheel yourself.",
            "Try to wave down another vehicle for help.",
            "Attempt to drive to the nearest service station.",
            "Get out of the car and try to stop passing vehicles."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If someone has been injured, the sooner proper medical attention is given the better. Ask someone to phone to phone for help or do it yourself. An injured person should only be moved if their motorcyclist's helmet shouldn't be removed unless it's essential.",
        "questions": [
            "An injured motorcyclist is lying unconscious on the road. The traffic has stopped and there's no further danger. What could you do to help?",
            "What should you do if you find an injured motorcyclist lying unconscious on the road and there's no immediate danger?",
            "You're at the scene of an accident where a motorcyclist is unconscious on the road. What is the first thing you should do to help?",
            "How can you assist an injured motorcyclist who is lying unconscious on the road with no further danger?",
            "A motorcyclist is unconscious on the road. What is the most appropriate action to take?"
        ],
        "correct_answers": [
            "Seek medical assistance.",
            "Call for medical help.",
            "Contact emergency services for help.",
            "Dial the emergency number to report the incident.",
            "Request medical help immediately."
        ],
        "incorrect_answers": [
            "Remove their safety helmet.",
            "Remove their leather jacket.",
            "Move the person off the road.",
            "Try to revive the motorcyclist without help.",
            "Administer first aid without calling for help."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "At the scene of an incident, always be aware of the danger of further collisions or fire. The priority when dealing with an unconscious person is to ensure they can breathe. This may involve clearing their airway if you can see an obstruction or if they're having difficulty breathing.",
        "questions": [
            "You arrive at an incident. There's no danger from fire or further collisions and the emergency services have been called. What's your first priority when attending to an unconscious motorcyclist?",
            "What should you do first when you come across an unconscious motorcyclist, and there's no danger from fire or further collisions?",
            "You've arrived at the scene of an accident where a motorcyclist is unconscious. What is your first priority in this situation?",
            "At an accident scene with an unconscious motorcyclist, what should be your immediate priority if there's no immediate danger?",
            "When you find an unconscious motorcyclist at the scene of an accident, what should be your first action?"
        ],
        "correct_answers": [
            "Check whether they're breathing normally.",
            "Check for normal breathing.",
            "Ensure the motorcyclist is breathing properly.",
            "Assess whether the motorcyclist is breathing.",
            "Check their airway and breathing."
        ],
        "incorrect_answers": [
            "Check whether they have any bruising.",
            "Check whether they're bleeding.",
            "Check whether they have any broken bones.",
            "Assess if the motorcyclist is awake.",
            "Try to wake them up."
    ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "The DR ABC code has been devised by medical experts to give the best outcome until the emergency services arrive and take care of casualties.",
        "questions": [
            "At an incident, how could you help a casualty who has stopped breathing?",
            "What should you do to help a casualty who has stopped breathing at an incident?",
            "If you find someone who has stopped breathing at the scene of an incident, what should you do?",
            "What is the proper action to take if a casualty has stopped breathing at an accident scene?",
            "At the scene of an incident, how can you assist a casualty who is not breathing?"
        ],
        "correct_answers": [
            "Follow the DR ABC code.",
            "Perform the DR ABC procedure.",
            "Use the DR ABC method to assist the casualty.",
            "Follow the DR ABC sequence for first aid.",
            "Apply the DR ABC protocol for resuscitation."
        ],
        "incorrect_answers": [
            "Raise their legs to help them with circulation.",
            "Try to give them something to drink.",
            "Keep their head tilted forwards as far as possible.",
            "Perform chest compressions without following the DR ABC steps.",
            "Check their pulse without performing first aid."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you're in a collision that causes damage or injury to any other person, vehicle, animal or property, by law you must stop. Give your name, the vehicle's registration number to anyone who has reasonable grounds for requesting them.",
        "questions": [
            "What's the first thing you must do if you have a collision while you're driving your car?",
            "If you're involved in a collision while driving, what should you do first?",
            "What is the first step you must take if you're in a car collision?",
            "In the event of a collision while driving, what should be your first action?",
            "If you have an accident while driving, what's the first thing you must do?"
        ],
        "correct_answers": [
            "Stop at the scene of the incident.",
            "Stay at the scene of the collision.",
            "Stop your vehicle and remain at the scene.",
            "Do not leave the scene of the accident.",
            "Remain at the scene until it's safe to leave."
        ],
        "incorrect_answers": [
            "Stop only if someone waves at you.",
            "Call the emergency services.",
            "Call your insurance company.",
            "Drive away quickly to avoid traffic.",
            "Stop only to exchange insurance details."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "First, get yourself and anyone else well away from the crossing. If there's a railway telephone, use that to get instructions from the signal operator. Then, if there's time, move the vehicle clear of the crossing.",
        "questions": [
            "What should you do first if your vehicle has broken down on an automatic railway level crossing?",
            "If your vehicle breaks down on an automatic railway level crossing, what should you do first?",
            "What is the first thing you should do if your vehicle is stuck on a railway level crossing?",
            "If you break down on an automatic railway level crossing, what's the first thing you should do?",
            "What should be your first action if your vehicle breaks down on a level crossing?"
        ],
        "correct_answers": [
            "Get everyone out of the vehicle and clear of the crossing.",
            "Ensure all passengers are safely out of the vehicle and away from the tracks.",
            "Move all people from the vehicle and away from the railway tracks.",
            "Evacuate everyone from the vehicle and clear of the crossing.",
            "Leave the vehicle immediately and get away from the crossing."
        ],
        "incorrect_answers": [
            "Telephone your vehicle recovery service to move it.",
            "Try to push the vehicle clear of the crossing as soon as possible.",
            "Walk along the track to give warning to any approaching trains.",
            "Attempt to move the vehicle yourself to clear the crossing.",
            "Call the emergency services and wait inside the vehicle."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "A broken-down vehicle in a tunnel can cause serious congestion and danger to other road users. If your vehicle breaks down, get help without delay. Switch on your hazard warning lights, then go to an emergency telephone for help.",
        "questions": [
            "What should you do if your vehicle breaks down in a tunnel?",
            "If your vehicle breaks down inside a tunnel, what should you do?",
            "What is the first thing you should do if your vehicle breaks down in a tunnel?",
            "If you experience a breakdown while in a tunnel, what should be your first step?",
            "What should be your immediate action if your vehicle breaks down in a tunnel?"
        ],
        "correct_answers": [
            "Switch on hazard warning lights, then go and call for help.",
            "Activate hazard warning lights and find a way to call for assistance.",
            "Turn on your hazard lights and seek help as soon as possible.",
            "Switch on your hazard lights and immediately call for emergency assistance.",
            "Turn on your hazard warning lights and contact the emergency services."
        ],
        "incorrect_answers": [
            "Stand in the lane behind your vehicle to warn others.",
            "Stand in front of your vehicle to warn oncoming drivers.",
            "Stay in your vehicle and wait for the police.",
            "Try to push the vehicle out of the tunnel.",
            "Drive to the nearest exit as quickly as possible."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If the warning bells ring, leave the vehicle and get any passengers well clear of the crossing immediately.",
        "questions": [
            "What should you do if the warning bells start to ring while you're trying to restart the engine?",
            "What is the correct action if the warning bells ring while attempting to restart the engine?",
            "If the warning bells sound while you're trying to restart the engine, what should you do?",
            "What action should you take if the warning bells start ringing while you're trying to restart the car's engine?",
            "If the warning bells activate while attempting to restart your engine, what should be your first response?"
        ],
        "correct_answers": [
            "Get out of the car and clear of the crossing.",
            "Leave the vehicle immediately and move away from the crossing.",
            "Exit the car and move to a safe location away from the crossing.",
            "Get out of the car and move to safety, away from the railway tracks.",
            "Immediately exit the vehicle and clear the crossing area."
        ],
        "incorrect_answers": [
            "Run down the track to warn the signal operator.",
            "Carry on trying to restart the engine.",
            "Push the vehicle clear of the crossing.",
            "Attempt to fix the car while on the crossing.",
            "Call your insurance company for assistance."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Remember this procedure by saying DR ABC, This stands for Danger, Response, Airway, Breathing, Circulation. Give whatever first aid you can and stay with the injured person until a medical professional takes over.",
        "questions": [
            "At an incident, someone is unconscious and you want to help. What would be the first thing to check?",
            "What should you check first if someone is unconscious at an incident and you want to help?",
            "If you find someone unconscious at an incident, what's the first thing you should check?",
            "What is the first step in assisting an unconscious person at an incident?",
            "If a person is unconscious in an incident, what should you do first?"
        ],
        "correct_answers": [
            "Whether their airway is open.",
            "Check if their airway is clear.",
            "Ensure their airway is not blocked.",
            "First, check if their airway is clear.",
            "Check if their airway is open and unobstructed."
        ],
        "incorrect_answers": [
            "Whether their vehicle is insured.",
            "Whether they have allergies.",
            "Whether they're comfortable.",
            "Check if they have a mobile phone on them.",
            "Ask if they need water."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you can't get your vehicle onto the hard shoulder, use your hazard warning lights to warn others. Leave your vehicle only when you can safely get clear of the carriageway. Don't try to repair the vehicle or attempt to place any warning device on the carriageway.",
        "questions": [
            "Your vehicle has broken down on a motorway. What should you do if you aren't able to get onto the hard shoulder?",
            "What should you do if your car breaks down on a motorway and you can't reach the hard shoulder?",
            "If your vehicle breaks down on the motorway and you cannot move to the hard shoulder, what is the best course of action?",
            "What is the correct procedure if your car breaks down on a motorway and there's no access to the hard shoulder?",
            "If you are stuck on a motorway without being able to reach the hard shoulder, what should you do?"
        ],
        "correct_answers": [
            "Switch on your hazard warning lights.",
            "Turn on your hazard lights to warn other drivers.",
            "Activate your hazard warning lights immediately.",
            "Use hazard lights to alert other road users.",
            "Switch on your hazard warning lights."
        ],
        "incorrect_answers": [
            "Stand behind the vehicle to warn others.",
            "Stop the traffic behind and ask for help.",
            "Attempt to repair your vehicle quickly.",
            "Flag down passing cars for assistance.",
            "Walk to the nearest service area to get help."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If the property owner isn't available at the time, you must inform the police about the incident. This should be done as soon as possible, and in any case within 24 hours.",
        "questions": [
            "You lose control of your car and damage a garden wall. What must you do if the property owner isn't available?",
            "If you damage a garden wall with your car and the owner is not present, what should you do?",
            "After accidentally damaging a garden wall with your vehicle, what is your legal obligation if the owner is unavailable?",
            "What must you do if you hit and damage a garden wall but cannot find the property owner?",
            "If you accidentally crash into a garden wall and the owner isn't around, what action should you take?"
        ],
        "correct_answers": [
            "Report the incident to the police within 24 hours.",
            "Inform the police within 24 hours.",
            "Notify the police as soon as possible, within 24 hours.",
            "File a report with the police within 24 hours.",
            "Contact the police within 24 hours to report the incident."
        ],
        "incorrect_answers": [
            "Go back to tell the house owner the next day.",
            "Find someone in the area to tell them about it immediately.",
            "Report the incident to your insurance company when you get home.",
            "Leave a note on the garden wall.",
            "Take a photo and leave without reporting it."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If a casualty isn't breathing normally, cardiopulmonary resuscitation (CPR) may be needed to maintain circulation. Place two hands on the centre of the chest and press down hard and fast - around 5-6 centimetres about twice a second.",
        "questions": [
            "A casualty isn't breathing normally and needs CPR. At what rate should you press down and release on the centre of their chest?",
            "When performing CPR on a casualty who isn't breathing normally, what should be the rate of chest compressions?",
            "If someone needs CPR, how quickly should you press and release on the centre of their chest?",
            "What is the correct rate for chest compressions when performing CPR on a casualty who isn't breathing?",
            "During CPR, at what rate should chest compressions be performed?"
        ], 
        "correct_answers": [
            "120 times per minute.",
            "120 times per minute."
        ],
        "incorrect_answers": [
            "240 times per minute.",
            "10 times per minute.",
            "60 times per minute.",
            "30 times per minute.",
            "80 times per minute.",
            "160 times per minute."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If a casualty isn't breathing normally, cardiopulmonary resuscitation (CPR) may be needed to maintain circulation. Place two hands on the centre of the chest and press down hard and fast - around 5-6 centimetres about twice a second.",
        "questions": [
            "An adult casualty isn't breathing. To maintain circulation, CPR should be given. What's the correct depth to press down on their chest."
        ], 
        "correct_answers": [
            "5 to 6 centimetres.",
            "5 to 6 centimetres."
        ],
        "incorrect_answers": [
            "5 to 6 centimetres.",
            "10 to 15 centimetres.",
            "15 to 20 centimetres.",
            "1 to 2 centimetres.",
            "2 to 3 centimetres.",
            "20 to 25 centimetres."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you're involved in a collision, head restraints will reduce the risk of neck injury. They must be properly adjusted. Make sure they aren't positioned too low; in a crash, this could cause damage to the neck.",
        "questions": [
            "If you're involved in a collision, what will reduce the risk of neck injury?"
        ], 
        "correct_answers": [
            "A properly adjusted head restraint."
        ],
        "incorrect_answers": [
            "Anti-lock brakes.",
            "An air-sprung seat.",
            "A collapsible steering wheel."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If someone is suffering from shock, try to keep them warm and as comfortable as you can. Don't give them anything to eat or drink but are them confidently and try not to leave them alone.",
    "questions": [
        "You're at the scene of an incident. How could you help someone who's suffering from shock?",
        "What should you do to assist a person in shock at an incident?",
        "How can you best support someone in shock after an accident?",
        "What's the most appropriate way to help a shocked casualty at the scene?",
        "How can you comfort a person showing signs of shock at an accident?"
    ],
    "correct_answers": [
        "Reassure them.",
        "Speak calmly and offer reassurance.",
        "Keep them calm and provide reassurance.",
        "Stay with them and offer comforting words.",
        "Encourage them to stay calm and still."
    ],
    "incorrect_answers": [
        "Offer them some food.",
        "Offer them a cigarette.",
        "Give them a warm drink.",
        "Move them to a quieter place.",
        "Cover them with a heavy blanket."
    ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If possible, lay the casualty down. Protect yourself from exposure to blood and, when you're sure there's nothing in the wound, apply firm pressure using clean material.",
        "questions": [
            "You arrive at the scene of a crash where someone is bleeding heavily from a wound in their arm. Nothing is embedded in the wound. What could you do to help?",
            "What's the best first aid action if someone is bleeding heavily from their arm?",
            "How can you assist a casualty with heavy bleeding from the arm at an accident scene?",
            "What's the recommended first aid for a heavily bleeding arm wound?",
            "How should you treat a severe arm wound at the scene of an accident?"
        ],
        "correct_answers": [
            "Apply pressure over the wound.",
            "Use a clean cloth and press firmly on the wound.",
            "Elevate the arm and apply direct pressure.",
            "Cover the wound and apply pressure.",
            "Press down firmly on the wound."
        ],
        "incorrect_answers": [
            "Get them a drink.",
            "Dab the wound.",
            "Walk them around and keep talking.",
            "Leave the wound uncovered to air.",
            "Pour water over the wound to clean it."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you have ABS and need to stop in an emergency, keep your foot firmly on the brake pedal until the vehicle has stopped. When the ABS operates, you may hear a grating sound and feel vibration through the brake pedal. This is normal and should maintain pressure on the brake pedal until the vehicle stops.",
        "questions": [
            "How should you use anti-lock brakes when you need to stop in an emergency?",
            "What's the correct way to apply anti-lock brakes in an emergency stop?",
            "How do you safely use ABS during an emergency braking situation?",
            "What technique should you use with ABS in an emergency?",
            "How do anti-lock brakes work best during a sudden stop?"
        ],
        "correct_answers": [
            "Brake promptly and firmly until you've stopped.",
            "Press the brake pedal firmly without releasing.",
            "Maintain firm pressure on the brake pedal.",
            "Keep the brake pedal pressed down steadily.",
            "Apply continuous and strong pressure to the brake pedal."
        ],
        "incorrect_answers": [
            "Apply the parking brake to reduce the stopping distance.",
            "Keep pumping the footbrake to prevent skidding.",
            "Brake gently to avoid triggering the ABS.",
            "Release the brake pedal intermittently.",
            "Brake in short bursts to prevent lock-up."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You must stop if you've been involved in a collision that results in injury or damage. The police may ask to see your driving license and insurance details at the time or later at a police station.",
        "questions": [
            "Which document may the police ask you to produce after you've been involved in a collision?",
            "What document might the police request if you're involved in a road traffic accident?",
            "If you're in a collision, what document must you show to the police if requested?",
            "After a collision, what paperwork could the police require from you?",
            "What document should you have ready if the police investigate a collision you were involved in?"
        ],
        "correct_answers": [
            "Your driving license.",
            "Driving license.",
            "A valid driving license.",
            "Your current driving license.",
            "Your full driving license."
        ],
        "incorrect_answers": [
            "Your vehicle registration document.",
            "Your vehicle service record.",
            "Your theory test certificate.",
            "Your insurance policy.",
            "Your MOT certificate."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "A tyre bursting can lead to a loss of control, especially if you're travelling at high speed. Using the correct procedure should help you to stop the vehicle safely.",
        "questions": [
            "What should you do if a tyre bursts while you're driving?",
            "How should you respond to a tyre blowout on the road?",
            "What's the safest action to take if your tyre suddenly bursts?",
            "If a tyre bursts while driving, what is the correct procedure?"
        ],
        "correct_answers": [
            "Pull up slowly at the side of the road.",
            "Slow down gently and pull over safely.",
            "Carefully steer to the side and stop."
        ],
        "incorrect_answers": [
            "Brake as quickly as possible.",
            "Pull on the parking brake.",
            "Continue at a normal speed.",
            "Accelerate to maintain control."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "7_braking_fail.png", "sign_question": False,
        "explanation": "If this light comes on, you should have the brake system checked immediately. A faulty braking system could have dangerous consequences.",
        "questions": [
            "What does it mean if this light comes on while you're driving?",
            "What could this warning light indicate during your journey?",
            "What should you check if this light appears on the dashboard?"
        ],
        "correct_answers": [
            "A fault in the braking system.",
            "Brake system issue detected.",
            "Problem with the braking system.",
            "Brake system warning."
        ],
        "incorrect_answers": [
            "Your seat belt isn't fastened.",
            "A rear light has failed.",
            "The engine oil is low.",
            "A door is open."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you feel yourself becoming tense or upset, stop in a safe break. Tiredness can make things worse and may cause a different reaction to upsetting situations",
        "questions": [
            "A driver's behaviour has upset you. How can you get over this incident safely?",
            "If another driver's actions annoy you, what's the best way to calm down?",
            "How should you handle feeling upset by another driver's behaviour?",
            "What's the safest way to respond when another driver's actions frustrate you?"
        ],
        "correct_answers": [
            "Stop and take a break.",
            "Find a safe place to stop and relax.",
            "Take some time to calm down before continuing."
        ],
        "incorrect_answers": [
            "Gesture to them with your hand.",
            "Follow them, flashing your headlights.",
            "Shout abusive language.",
            "Speed up to overtake them aggressively."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "7_ESC.jpg", "sign_question": False,
        "explanation": "ECS is a computer-controlled technology that detects reduced traction and automatically makes corrective adjustments to prevent loss of control. The ESC light comes on briefly to alert the driver that the system has activated and the car is approaching its handling limits. It's a powerful driver aid but it cannot save a car once its traction limits have been exceeded.",
        "questions": [
            "What does it mean if the Electronic Stability Control (ESC) indicator light comes on briefly while you're driving?"
        ], 
        "correct_answers": [
            "The ESC system has activated."
        ],
        "incorrect_answers": [
            "The ESC system has a fault.",
            "The ESC system is switched off.",
            "The ESC system is running a routine test."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "The effects of shock may not be immediately obvious. Warning signs to look for include; A rapid pulse, sweating, pale grey skin and rapid shallow breathing.",
        "questions": [
            "Following a collision, a person has been injured. What would be a warning sign for shock?",
            "After a crash, how can you identify if someone is experiencing shock?",
            "What symptom might indicate that an injured person is in shock after an accident?",
            "What physical sign could suggest shock following a collision?"
        ],
        "correct_answers": [
            "Rapid shallow breathing.",
            "Sweating.",
            "Pale grey skin.",
            "A rapid pulse."
        ],
        "incorrect_answers": [
            "Warm dry skin.",
            "Flushed complexion.",
            "Slow pulse.",
            "Strong, steady breathing."
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