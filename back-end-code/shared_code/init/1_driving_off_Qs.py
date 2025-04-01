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
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Accelerating and braking gently and smoothly will help to save fuel and reduce wear on your vehicle. This makes it better for the environment too.",
        "questions": [
            "What's most likely to increase fuel consumption?",
            "What factors are most likely to lead to higher fuel consumption?",
            "What can significantly increase fuel consumption?",
            "What factors tend to raise fuel consumption levels?",
            "What conditions are likely to boost fuel consumption?"
        ], 
        "correct_answers": [
            "Harsh braking and accelerating.",
            "Sudden braking and rapid acceleration.",
            "Aggressive braking and fast acceleration.",
            "Hard braking and rapid throttle use.",
            "Abrupt stopping and quick speeding up."
        ],
        "incorrect_answers": [
            "Staying in high gears.",
            "Accelerating around bends.",
            "Poor steering control."
            "Driving at a constant speed on the highway.",
            "Using cruise control on long trips.",
            "Using premium fuel in a car that doesn't require it.",
            "Keeping windows closed while driving.",
            "Regularly servicing the engine and replacing air filters."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Ecosafe driving is all about looking and planning further ahead. This helps raise hazard awareness and reduce the need for late and heavy braking. It will also make your journey more comfortable, considerably reducing your fuel bills and emissions that can damage the environment.",
        "questions": [
            "How can driving in an ecosafe manner help protect the environment?",
            "In what ways does ecosafe driving reduce environmental harm?",
            "What benefits does driving in an ecosafe way offer for the environment?",
            "How does ecosafe driving contribute to environmental protection?",
            "Why is ecosafe driving important for the planet?"
        ], 
        "correct_answers": [
            "By reducing exhaust emissions.",
            "By lowering fuel consumption and emissions.",
            "Through reducing fuel usage and harmful emissions.",
            "By cutting down on the pollution caused by vehicle emissions.",
            "By decreasing harmful exhaust emissions from the vehicle."
        ],
        "incorrect_answers": [
            "By increasing the number of cars on the road.",
            "Through increased fuel bills.",
            "Through the legal enforcement of speed regulations.",
            "By encouraging aggressive acceleration and braking.",
            "By reducing the need for vehicle maintenance.",
            "Through frequent idling at traffic lights.",
            "By frequently using the car for short trips.",
            "By keeping the vehicle in poor mechanical condition."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Holding the clutch down or staying in neutral for too long will cause your vehicle to freewheel. This is known as 'coasting' and it's dangerous because it reduces your control of the car.",
        "questions": [
            "What will happen if you hold the clutch pedal down or roll in neutral for too long?",
            "What is the consequence of coasting in neutral or keeping the clutch pedal pressed?",
            "How does holding the clutch down or using neutral for extended periods affect your driving?",
            "Why is coasting in neutral or with the clutch down considered dangerous?",
            "What is the risk of driving with the clutch pressed or in neutral for too long?"
        ], 
        "correct_answers": [
            "It will reduce your control.",
            "It will reduce control over the vehicle.",
            "It will make the car harder to control.",
            "It will compromise your control of the car.",
            "It will lower your ability to control the car."
        ],
        "incorrect_answers": [
            "It will improve tyre wear.",
            "It will use more fuel.",
            "It will cause the engine to overheat.",
            "It will increase braking efficiency.",
            "It will make the car go faster.",
            "It will save fuel in the long term.",
            "It will improve engine performance.",
            "It will improve fuel efficiency."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "An engine can use more oil during long journeys than on shorter trips. Insufficient engine oil is potentially dangerous: it can lead to excessive wear, mechanical breakdown and expensive repairs. Most cars have a dipstick to allow the oil level to be checked. If not, you should refer to the vehicle handbook.",
        "questions": [
            "When should you check the engine oil level?",
            "What is the best time to check the engine oil before a trip?",
            "When is it most important to check the oil level in your car?",
            "How often should you check your engine oil?",
            "When is it important to check the engine oil?"
        ], 
        "correct_answers": [
            "Before a long journey.",
            "Before going on a long trip.",
            "Before starting a long drive.",
            "Prior to long-distance travel.",
            "Before embarking on a long journey."
        ],
        "incorrect_answers": [
            "Every time you drive the car.",
            "Early in the morning.",
            "When the engine is hot.",
            "Immediately after filling up with fuel.",
            "Only during scheduled maintenance.",
            "Once every few months.",
            "When the car starts making noise.",
            "Only when the oil light comes on.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Harsh braking, frequent gear changes and harsh acceleration increase fuel consumption. A car uses less fuel when travelling at a constant low speed in an appropriate high gear. You need to look well ahead so you're able to anticipate hazards early. Easing off the accelerator and timing your approach at junctions, for example, can reduce the fuel consumption of your vehicle.",
        "questions": [
            "What will reduce fuel consumption?",
            "How can you improve fuel efficiency while driving?",
            "What driving behavior helps save fuel?",
            "What can help lower your car's fuel usage?",
            "How can you drive more economically to save fuel?"
        ], 
        "correct_answers": [
            "Driving more slowly.",
            "Driving at a constant low speed.",
            "Maintaining a steady, moderate speed.",
            "Staying in higher gears and driving slowly.",
            "Reducing speed and avoiding rapid acceleration."
        ],
        "incorrect_answers": [
            "Late and heavy braking.",
            "Accelerating rapidly.",
            "Staying in lower gears.",
            "Driving at high speeds on highways.",
            "Frequent hard accelerations.",
            "Idling for long periods.",
            "Driving with the air conditioning on at full blast.",
            "Driving aggressively in heavy traffic.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If your trailer starts to swerve or snake, reduce speed gently to regain control. Do not accelerate or brake harshly.",
        "questions": [
            "What should you do if your trailer starts to swerve or snake?",
            "How should you react if your trailer begins to sway?",
            "What is the correct action when your trailer starts to fishtail?",
            "How do you regain control if your trailer starts swerving?",
            "What should you do when your trailer begins to snake on the road?"
        ], 
        "correct_answers": [
            "Reduce speed gently.",
            "Slow down gradually.",
            "Ease off the accelerator and slow down.",
            "Gently reduce speed to regain control.",
            "Gradually reduce speed without abrupt movements."
        ],
        "incorrect_answers": [
            "Steer sharply.",
            "Brake firmly.",
            "Increase speed.",
            "Pull over immediately without reducing speed.",
            "Turn the wheel quickly to correct the swerve.",
            "Accelerate to stabilize the trailer.",
            "Suddenly brake to stop the movement.",
            "Make sudden steering corrections to stop the swerving.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Wasting fuel costs you money and also causes unnecessary pollution. Ensuring your tyres are correctly inflated, avoiding carrying unnecessary weight and removing a roof rack that's not in use will all help to reduce your fuel consumption.",
        "questions": [
            "What's most likely to waste fuel?",
            "What common factor leads to higher fuel consumption?",
            "What can cause your car to use more fuel than necessary?",
            "Which factor contributes to wasting fuel?",
            "What is most likely to increase your fuel consumption?"
        ], 
        "correct_answers": [
            "Under-inflated tyres.",
            "Tyres that are not properly inflated.",
            "Having tyres with low pressure.",
            "Tyres with insufficient air pressure.",
            "Low tyre pressure increases fuel consumption."
        ],
        "incorrect_answers": [
            "Driving on motorways.",
            "Using different brands of fuel.",
            "Reducing your speed.",
            "Driving in colder weather.",
            "Using air conditioning moderately.",
            "Driving at night.",
            "Changing your driving route regularly.",
            "Driving with the windows closed."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you find that your vehicle bounces as you drive around a corner or bend in the road, the shock absorbers might be worn. To test your shock absorbers, sharply press and release above each wheel. If the vehicle continues to bounce, take it to be checked by a qualified mechanic.",
        "questions": [
            "What does it mean if your vehicle keeps bouncing after you sharply press down and release on the bodywork over a wheel?",
            "What is indicated if your car continues bouncing after pressing down on the bodywork near the wheel?",
            "What could be the cause if your car bounces when you press down sharply on the bodywork over the wheel?",
            "If your car bounces after pressing down over the wheel, what is most likely the issue?",
            "What does persistent bouncing in your car after pressing down on the bodywork suggest?"
        ], 
        "correct_answers": [
            "The shock absorbers are worn.",
            "The shock absorbers need replacing.",
            "Worn shock absorbers are causing the bounce.",
            "The vehicle's shock absorbers are damaged.",
            "There's a problem with the shock absorbers."
        ],
        "incorrect_answers": [
            "The tyres are worn.",
            "The vehicle is on soft ground.",
            "The tyres are under-inflated.",
            "The suspension springs are broken.",
            "The brake pads are worn.",
            "There's too much weight in the car.",
            "The car has a low fuel level.",
            "The alignment of the wheels is off.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "By looking well ahead and recognising hazards in good time, you can avoid late and heavy braking. Watch the traffic flow and look well ahead for potential hazards so you can control your speed in good time. Avoid over-revving the engine and accelerating harshly, as this increases wear to the engine and uses more fuel.",
        "questions": [
            "How can you reduce the damage your vehicle causes to the environment?",
            "What can help minimize the environmental impact of your driving?",
            "How can you lessen the harm your car does to the environment?",
            "What is an effective way to reduce your vehicle's environmental footprint?",
            "How can you drive in a way that's less harmful to the environment?"
        ], 
        "correct_answers": [
            "Anticipate well ahead.",
            "By planning ahead and anticipating hazards.",
            "Look ahead to avoid sudden braking.",
            "Anticipating traffic flow and hazards early.",
            "By recognizing hazards in time and controlling speed."
        ],
        "incorrect_answers": [
            "Brake heavily.",
            "Use narrow side streets.",
            "Use busy routes.",
            "Drive at high speeds to reach destinations faster.",
            "Keep accelerating rapidly.",
            "Drive aggressively to save time.",
            "Use the engine to maintain high RPMs for long periods.",
            "Ignore traffic flow and potential hazards."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Try to plan your journey so that you can take rest stops. It's recommended that you take a break of at least 15 minutes after every two hours of driving or riding. This should help to maintain your concentration.",
        "questions": [
            "Do you need to plan rest stops when you're planning a long journey?",
            "Is it important to plan regular breaks on a long drive?",
            "Should you take planned breaks on long journeys?",
            "What's the importance of planning rest stops during a long journey?",
            "Should you plan rest stops on a long trip? Why?"
        ], 
        "correct_answers": [
            "Yes, regular stops help concentration.",
            "Yes, stopping regularly helps you stay alert.",
            "Yes, it's important to take breaks to maintain focus.",
            "Yes, taking breaks improves concentration and reduces fatigue.",
            "Yes, planned stops reduce tiredness and improve safety."
        ],
        "incorrect_answers": [
            "Yes, you should plan to stop every half an hour.",
            "No, you'll be less tired if you get there as soon as possible.",
            "No, only fuel stops will be needed.",
            "No, you can drive straight through without breaks.",
            "Yes, but only if you feel tired.",
            "No, your concentration won't be affected.",
            "Yes, but only if you're traveling with passengers.",
            "No, you can rely on GPS for directions and skip breaks."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Some modern batteries are maintenance-free. Check your vehicle handbook and, if necessary, make sure that the plates in each battery cell are covered with fluid.",
        "questions": [
            "The fluid level in your battery is low. What fluid should you use to top it up?",
            "If the fluid level in your car battery is low, what should you use to refill it?",
            "What fluid is required to top up a car battery with low fluid levels?",
            "When topping up the fluid in your car battery, which fluid should you use?",
            "What is the correct fluid to use when the battery fluid is low?"
        ], 
        "correct_answers": [
            "Distilled Water.",
            "Distilled Water.",
        ],
        "incorrect_answers": [
            "Engine oil.",
            "Engine coolant.",
            "Battery acid.",
            "Regular tap water.",
            "Brake fluid.",
            "Transmission fluid.",
            "Antifreeze.",
            "Hydraulic fluid."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Any load must be securely fastened to the vehicle. The safest way to carry items on the roof is in a specially designed roof box. This will help to keep your luggage secure and dry. and it also has less wind resistance than loads carried exposed on the roof rack.",
        "questions": [
            "How should a load be carried on your roof rack?",
            "What is the correct way to secure a load on a roof rack?",
            "How can you safely transport items on a roof rack?",
            "What should you do to ensure a roof rack load is safe?",
            "When using a roof rack, how should you secure the load?"
        ], 
        "correct_answers": [
            "Securely fastened with suitable restraints.",
            "The load should be properly secured with restraints.",
            "Use appropriate fastenings to keep the load secure.",
            "Make sure the load is firmly tied down to prevent movement.",
            "Fasten the load securely to prevent it from shifting or falling off."
        ],
        "incorrect_answers": [
            "Visible in your exterior mirror.",
            "Covered with plastic sheeting.",
            "Loaded towards the rear of the vehicle.",
            "Left loose to make unloading easier.",
            "Tied down with lightweight string.",
            "Balanced on one side for easy access.",
            "Held in place by the wind resistance.",
            "Kept in place by its weight alone.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Top up the battery with distilled water and make sure each cell plate is covered.",
        "questions": [
            "You need to top up your battery with distilled water. What level should you fill it to?",
            "When topping up a battery with distilled water, how much should you add?",
            "At what level should distilled water be filled in a car battery?",
            "How high should the distilled water level be when refilling a car battery?",
            "What is the correct level for distilled water in a vehicle battery?"
        ], 
        "correct_answers": [
            "Just above the cell plates.",
            "The water should be slightly above the cell plates.",
        ],
        "incorrect_answers": [
            "Just below the cell plates.",
            "Halfway up the battery.",
            "The top of the battery.",
            "Completely full to the top.",
            "Fill until water spills over.",
            "Leave the battery dry for better performance.",
            "Fill it only after the battery stops working.",
            "Only add water when the battery is completely empty."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You will feel the effect of engine braking when you take your foot off the accelerator. Changing to a lower gear will increase the effect.",
        "questions": [
            "When will you feel the effects of engine braking?",
            "When will you feel the engine braking effects?"
        ], 
        "correct_answers": [
            "When you change to a lower gear.",
            "When selecting a lower gear and releasing the accelerator.",
            "When you ease off the accelerator and let the engine slow the vehicle."
        ],
        "incorrect_answers": [
            "When you only use the parking brake.",
            "When you change to a higher gear.",
            "When you're in neutral.",
            "When you press the accelerator pedal harder.",
            "When you apply the handbrake while moving.",
            "When using cruise control at high speeds.",
            "When coasting downhill in neutral.",
            "When pressing both the brake and accelerator at the same time."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Check the tyre pressures when the tyres are cold. This will give a more accurate reading. The heat generated on a long journey will raise the pressure inside the tyre.",
        "questions": [
            "When should tyre pressures be checked?",
            "At what time should you check your tyre pressures for accuracy?",
            "When is the time to check your tyre pressures?",
            "For an accurate reading, when should you check your tyre pressure?",
            "When should you ideally check your tyres' air pressure?"
        ], 
        "correct_answers": [
            "When tyres are cold.",
            "When the tyres are cold."
        ],
        "incorrect_answers": [
            "When tyres are hot.",
            "After any lengthy journey.",
            "After travelling at high speed.",
            "Immediately after braking heavily.",
            "Only when the tyre warning light comes on.",
            "While the car is parked in direct sunlight.",
            "During or after refueling the vehicle.",
            "Only when the tyres appear visibly deflated.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Seat belts save lives and reduce the risk of injury. If you're carrying passengers under 14 years old, it's your responsibility as the driver to ensure that their seat belts are fastened or they're seated in an approved child restraint.",
        "questions": [
            "You're carrying two 13-year-old children and their parents in your car. Who's responsible for seeing that the children wear seat belts?",
            "Who is responsible for ensuring 13-year-old children wear seat belts in a vehicle?",
            "If a driver has 13-year-old children as passengers, who must ensure they wear seat belts?",
            "In a car, who has the legal responsibility for ensuring that 13-year-old passengers are wearing seat belts?",
            "When carrying 13-year-old passengers, who must make sure they are securely fastened with seat belts?"
        ], 
        "correct_answers": [
            "You, the driver.",
            "You as the driver.",
            "The driver."
        ],
        "incorrect_answers": [
            "The children.",
            "The front-seat passenger.",
            "The children's parents.",
            "The police.",
            "The car manufacturer.",
            "The person sitting next to them.",
            "The government.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "It's your responsibility to ensure that all children in your car are secure. Suitable restraints include a child seat, baby seat, booster seat, or booster cushion. Any restraint used must be suitable for the child's size and weight and fitted according to the manufacturer's instructions.",
        "questions": [
            "You're carrying a child under three years old in your car. Which restraint is suitable for a child of this age?",
            "What type of restraint should be used for a child under three years old in a vehicle?",
            "Which safety restraint is appropriate for securing a child under the age of three in a car?",
            "What is the safest way to secure a child under three while traveling in a car?",
            "How should a child under three years old be seated in a vehicle?"
        ],
        "correct_answers": [
            "A child seat.",
            "A rear-facing baby seat.",
            "A properly fitted baby or child seat.",
            "A child seat."
        ],
        "incorrect_answers": [
            "An adult seat belt.",
            "An adult holding a child.",
            "An adult lap belt.",
            "A cushion to elevate the child.",
            "A folded blanket to act as a seat.",
            "No restraint is necessary in slow-moving traffic.",
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "It can be frustrating and worrying to find that your planned route is blocked by roadworks or diversions. If you've planned an alternative, you'll feel less stressed and more able to concentrate fully on your driving. If your original route is mostly on motorways, it's a good idea to plan an alternative using non-motorway roads. Always carry a map with you in case you're lost.",
        "questions": [
            "You plan your route before starting a journey. Why should you also plan an alternative route?",
            "Why is it important to plan an alternative route when mapping out your journey?",
            "What are the benefits of having a backup route before starting your trip?",
            "Why shouldn't you rely solely on one route when traveling?",
            "What might happen if you don't have an alternative route prepared?"
        ], 
        "correct_answers": [
            "Your original route may be blocked.",
            "Your original route may have road blocks.",
            "There may be road blocks on your original route.",
            "Your original route may have blocked roads.",
            "Your original route may have roads under construction."
        ],
        "incorrect_answers": [
            "You may get held up by a tractor.",
            "Your maps may have different scales.",
            "You may find you have to pay a congestion charge."
            "You may need to pay at toll gates in your route.",
            "There may be heavy traffic in your original route.",
            "Your original route may be slower than your alternative route.",
            "Your may get held up by ticket inspectors."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Batteries contain hazardous acid, and they must be disposed of safely. This means taking them to an appropriate disposal site.",
        "questions": [
            "How should you dispose of a used vehicle battery?",
            "How do you properly dispose of a used vehicle battery?",
            "What is the correct way to get rid of an old vehicle battery?",
            "Where should you take a used car battery for safe disposal?",
            "What should you do with an old vehicle battery to ensure environmental safety?"
        ], 
        "correct_answers": [
            "Take it to a local-authority disposal site.",
            "Dispose of it at an authorized recycling or disposal facility.",
            "Take it to a designated hazardous waste collection center.",
            "Return it to a car battery retailer that accepts old batteries for disposal."
        ],
        "incorrect_answers": [
            "Leave it on waste land.",
            "Put it in the dustbin.",
            "Bury it in your garden.",
            "Throw it in a river or lake.",
            "Dump it in a regular landfill.",
            "Leave it by the roadside.",
            "Burn it to get rid of it."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": True,
        "explanation": "Traffic signs that are circular with a red border are the type of signs that NEED to be followed by drivers on the road. This is a key feature that drivers must remember especially in heavy traffic.",
        "questions": [
            "How can you identify traffic signs that give orders?",
            "What shape traffic signs tell that they give orders?",
            "How can you tell a traffic sign is meant to give orders?",
            "How can you identify that a traffic sign gives orders?"
        ], 
        "correct_answers": [
            "They're circular with a red border.",
            "They're circle with a red border.",
            "They're circular with a red border."
        ],
        "incorrect_answers": [
            "They're triangular with a blue border.",
            "They're rectangular with a yellow border.",
            "They're square with a brown border.",
            "They're circular with a blue border.",
            "They're circle with a blue border.",
            "They're triangular with a red border."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If your vehicle bounces as you drive around a corner or bend in the road, the shock absorbers might be worn. To test your shock absorbers, sharply press down and release above each wheel. If the vehicle continues to bounce, take it to be checked by a qualified mechanic.",
        "questions": [
            "What does it mean if your vehicle keeps bouncing after you sharply press down and release on the bodywork over a wheel?",
            "Why might your vehicle continue bouncing after being pressed down and released above a wheel?",
            "What could be the cause if your car bounces excessively when driving over bumps?",
            "If your car bounces repeatedly after being pushed down, what might be the issue?",
            "What problem could worn shock absorbers cause when driving around corners or over bumps?"
        ], 
        "correct_answers": [
            "The shock absorbers are worn.",
            "The shock absorbers may be faulty.",
            "The suspension system may be compromised due to worn shock absorbers.",
            "The shock absorbers are not functioning properly.",
            "The shock absorbers are worn."
        ],
        "incorrect_answers": [
            "The tyres are under-inflated.",
            "The tyres are worn.",
            "The vehicle is on soft ground.",
            "The brakes are faulty.",
            "The steering system is malfunctioning.",
            "The vehicle's weight distribution is uneven.",
            "The wheels are misaligned.",
            "The power steering fluid is low."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "When you pass your standard car driving test, you are permitted to tow a trailer, but there is a limit to how heavy that trailer can be. The maximum authorised mass (MAM) of a trailer that you can legally tow is 3,500kg. This is the combined weight of the trailer and its contents. If the trailer exceeds this weight, you would need to pass a further driving test or meet additional requirements to tow a heavier trailer. It's important to know and adhere to this limit for safety and legal reasons.",
        "questions": [
            "You've just passed your driving test. What's the maximum authorised mass (MAM) of any trailer that you can tow?",
            "After passing your driving test, what is the maximum authorised mass (MAM) of a trailer you are allowed to tow?",
            "Now that you've passed your driving test, what is the heaviest trailer you can legally tow?",
            "Following your successful driving test, what is the highest authorised mass (MAM) for a trailer you can tow?",
            "Once you've passed your driving test, what is the legal MAM limit for a trailer you can tow?"
        ], 
        "correct_answers": [
            "3,500kg",
            "3,500kg",
            "3,500kg",
        ],
        "incorrect_answers": [
            "4,500kg",
            "5,500kg",
            "6,500kg",
            "4,000kg",
            "3,000kg",
            "5,000kg",
            "7,000kg"
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "All vehicles need to be serviced to keep working efficiently. An efficient engine uses less fuel and produces fewer harmful emissions than an engine that's running inefficiently. Keeping the vehicle serviced to the manufacturer's schedule should also keep it reliable and reduce the chance of it breaking down.",
        "questions": [
            "How will you benefit from following the manufacturer's service schedule for your vehicle?",
            "Why is it important to follow the service schedule set by the manufacturer?",
            "What are the advantages of keeping your vehicle maintained according to the manufacturer's recommendations?",
            "How does servicing your vehicle regularly help in the long run?",
            "What could be the result of keeping up with your vehicle's scheduled maintenance?"
        ], 
        "correct_answers": [
            "Your vehicle will remain reliable.",
            "Your car will stay dependable.",
            "Your car will be less likely to breakdown.",
            "Your vehicle will be more reliable and efficient.",
            "Your car will continue to run efficiently."
        ],
        "incorrect_answers": [
            "Your vehicle tax will be lower.",
            "Your vehicle will be cheaper to insure.",
            "Your journey times will be reduced.",
            "Your car will become faster.",
            "Your car will never need repairs.",
            "Your fuel costs will automatically drop to zero.",
            "Your vehicle will require no further maintenance in the future."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Modern vehicles provide the driver with a good view of both the road ahead and behind using well-positioned mirrors. However, the mirrors can't see every angle of the scene behind and to the sides of the vehicle. It's essential that you know when and how to check the vehicle's blind spots so that you're aware of any hidden hazards.",
        "questions": [
            "What does the term 'blind spot' mean?",
            "What is a blind spot when driving?",
            "What area around your vehicle are considered blind spots?",
            "What is a 'blind spot'?",
            "What does 'blind spot' mean?"
        ], 
        "correct_answers": [
            "An area not visible to the driver.",
            "An area of the road that cannot be seen using mirrors alone.",
            "An area around a vehicle that the driver cannot see directly.",
            "An area of the road that is outside the driver's field of vision.",
            "An area that requires a shoulder check because mirrors do not cover it."
        ],
        "incorrect_answers": [
            "An area covered by your right-hand mirror.",
            "An area not covered by your headlights.",
            "An area covered by your left-hand mirror.",
            "A place where only pedestrians can walk.",
            "A spot on the road that is always safe from other traffic.",
            "A section of the road that does not require checking before turning or changing lanes.",
            "A part of the car that always remains clean and visible."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If you see that parts of the tread on your tyres are wearing before others, it may indicate a brake, suspension or wheel-alignment fault. Regular servicing will help to detect faults at an early stage and this will avoid the risk of minor faults becoming serious or even dangerous.",
        "questions": [
            "What can cause excessive or uneven tyre wear?"
        ], 
        "correct_answers": [
            "A faulty braking system.",
            "A faulty suspension system.",
            "A faulty wheel-alignment."
        ],
        "incorrect_answers": [
            "A faulty gearbox.",
            "A faulty exhaust system.",
            "A faulty electrical system.",
            "A faulty set of shock absorbers.",
            "A faulty set of window wipers.",
            "A faulty steering wheel.",
            "A faulty gear stick."   
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "In the event that the trailer becomes detached from the towing vehicle, the breakaway cable activates the trailer brakes before snapping. This allows the towing vehicle to get free of the trailer and out of danger.",
        "questions": [
            "What safety device must be fitted to a trailer braking system?",
            "Which device is used to engage a trailer's brakes if it becomes detached?",
            "What safety mechanism is required for trailers with braking systems?"
        ], 
        "correct_answers": [
            "Breakaway cable.",
            "Breakaway cable.",
            "Breakaway cable."
        ],
        "incorrect_answers": [
            "Corner steadies.",
            "Jockey wheel.",
            "Stabiliser.",
            "Towbar extension.",
            "Brake fluid reservoir.",
            "Handbrake lever.",
            "Wheel chocks."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Your tyres may be of different treads and makes. They can even be second-hand, as long as they're in good condition. They must, however, be intact, without cuts or tears. When checking the side walls for cuts and bulges, don't forget to check the side of the tyre that's hidden from view, under the car.",
        "questions": [
            "What makes your tyres illegal?",
            "When are tyres considered illegal?",
            "Under what circumstances would your tyres be illegal?",
            "How can a tyre be deemed illegal for road use?"
        ], 
        "correct_answers": [
            "If they have large, deep cuts in the side wall.",
            "If they have deep cuts or damage to the sidewall.",
            "If they have visible bulges or tears in the sidewall.",
            "If the sidewall is damaged or has deep cuts."
        ],
        "incorrect_answers": [
            "If they're different makes.",
            "If they were bought second-hand.",
            "If they have different tread patterns.",
            "If they have a little bit of dirt on them.",
            "If the brand is not the same as the other tyres.",
            "If they are slightly worn but still have tread left.",
            "If they have minor cosmetic scratches."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "If possible, avoid the early morning, late afternoon, and early evening 'rush hour'. Doing this should allow you to have a better journey, with fewer delays. This should help you to arrive at your destination feeling less stressed.",
        "questions": [
            "How will your journey be affected by travelling outside the busy times of day?",
            "What are the benefits of avoiding peak traffic hours when travelling?",
            "Why might it be better to drive outside of rush hour?",
            "How can travelling at off-peak times improve your journey?",
            "What advantage does travelling during quieter times provide?"
        ], 
        "correct_answers": [
            "Your journey will have fewer delays.",
            "Your journey will have less congestion and delays.",
            "Your journey will be smoother and quicker.",
            "Your journey more efficient and quicker.",
            "Your journey will have less traffic and fewer hold-ups."
        ],
        "incorrect_answers": [
            "Your journey will take longer.",
            "Your journey will use more fuel.",
            "Your journey will be more hazardous.",
            "Your journey will encounter more roadblocks and diversions.",
            "Your journey will have greater traffic.",
            "Your journey will be more stressful than usual."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "You may remove your seat belt while you're carrying out a manoeuvre that includes reversing. However, you must remember to put it back on again before you resume driving.",
        "questions": [
            "When may you drive without wearing your seat belt?",
            "Under what circumstances is it allowed to drive without a seat belt?",
            "When can you remove your seat belt while driving?",
            "Is it ever acceptable to drive without a seat belt?",
            "When is it okay to unbuckle your seat belt while driving?"
        ], 
        "correct_answers": [
            "When you're carrying out a manoeuvre that includes reversing.",
            "When you're performing a reversing manoeuvre.",
            "When you're reversing as part of a manoeuvre.",
            "When you're reversing, as long as it's on again before moving forward.",
        ],
        "incorrect_answers": [
            "When you're driving slowly in queueing traffic.",
            "When you're testing your brakes.",
            "When you're moving off on a hill.",
            "When you're parking in a space.",
            "When you're driving at low speed in a car park.",
            "When you're on a private road.",
            "When you're driving on an empty road late at night."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "'Kick down' selects a lower gear, enabling the vehicle to accelerate faster.",
        "questions": [
            "You're driving a car fitted with automatic transmission. When would you use 'kick down'?",
            "What is the purpose of using the 'kick down' feature in an automatic transmission car?",
            "When should you activate the 'kick down' in an automatic vehicle?",
            "In what situation would you use the 'kick down' function in an automatic car?",
            "What happens when you use 'kick down' in a car with automatic transmission?"
        ], 
        "correct_answers": [
            "To accelerate quickly.",
            "To achieve faster acceleration.",
            "To increase your speed quickly.",
            "To shift to a lower gear for more power."
        ],
        "incorrect_answers": [
            "To engage cruise control.",
            "To brake progressively.",
            "To improve fuel economy.",
            "To activate the car's air conditioning.",
            "To slow down the vehicle gradually.",
            "To shift the car into neutral."
        ]
    },
    {
        "id": str(uuid.uuid4()), "topic": topic, "image": "n/a", "sign_question": False,
        "explanation": "Having tyres correctly inflated and in good condition will ensure they have maximum grip on the road; how well your tyres grip the road has a significant effect on your car's stopping distance.",
        "questions": [
            "What will affect your vehicle's stopping distance?",
            "Which factor influences how quickly your vehicle can stop?",
            "What condition of your vehicle impacts its stopping distance?",
            "How do tyres affect the stopping distance of your car?",
            "What plays a key role in determining your car's stopping distance?"
        ], 
        "correct_answers": [
            "The condition of the tyres.",
            "The tyres grip on the road.",
            "The condition and inflation of your tyres.",
        ],
        "incorrect_answers": [
            "The speed limit.",
            "The time of day.",
            "The street lighting.",
            "The type of road surface.",
            "The weather conditions.",
            "The weight of the driver."
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