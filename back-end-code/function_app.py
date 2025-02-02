import datetime
import math
import json
import logging
import os

# shared_code folder imports
from shared_code.user import user, UniqueUserError, InvalidUserError, InvalidPasswordError
from shared_code.question import question
from shared_code.utility import utility, NoQueryError, ElementSizeError, InvalidStreakError, InvalidScoreError, BadPasswordError, BadUserError, ExistentUserError
from shared_code.open_ai import open_ai, ResponseError
from shared_code.evaluator import evaluator

# Azure imports
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from openai import AzureOpenAI

app = func.FunctionApp()

cosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
db_proxy = cosmos.get_database_client(os.environ['DatabaseName'])
users_proxy = db_proxy.get_container_client(os.environ['UserContainerName'])
questions_proxy = db_proxy.get_container_client(os.environ['QuestionContainerName'])
openai_proxy = AzureOpenAI(api_key=os.environ['OAIKey'], api_version="2024-02-01",
                        azure_endpoint=os.environ['OAIEndpoint'],
                        azure_deployment="gpt-35-turbo"
                        )

utility = utility()
oai = open_ai()
ml_model = evaluator()

# Cosmos decorator for registering a new player.
@app.cosmos_db_output(  arg_name="usercontainerbinding",
        	            database_name=os.environ['DatabaseName'],
                        container_name=os.environ['UserContainerName'],
                        create_if_not_exists=True,
                        connection='AzureCosmosDBConnectionString')
@app.route(route="user/register", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def user_register(req: func.HttpRequest, usercontainerbinding: func.Out[func.Document]) -> func.HttpResponse:
    """
    Recieves a player's username and password in a JSON string to register to player container.
    e.g. {"username":  "antoni_gn" , "password" : "ILoveTricia"}
    """
    input = req.get_json()
    logging.info('Python HTTP trigger function processed a USER_REGISTER request: {}'.format(input))

    # Converted to player object for validation.
    input_user = user(user_proxy=users_proxy,username=input['username'], password=input['password'])
    logging.info("Inputted new player: {}".format(input_user.to_dict()))

    try:
        if input_user.is_valid():
            # Insert in DB if player successfully validated.
            user_doc_for_cosmos = func.Document.from_dict(input_user.to_dict())
            usercontainerbinding.set(user_doc_for_cosmos)
            logging.info("SUCCESS: Input user added to database!")
            return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}),mimetype="application/json")

    # Send error messages based on is_valid()'s result.
    except UniqueUserError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Username already exists"})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except InvalidUserError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Username less than 5 characters or more than 15 characters"})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except InvalidPasswordError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Password less than 8 characters or more than 15 characters"})
        return func.HttpResponse(body=response_body,mimetype="application/json")



@app.route(route="user/login", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def user_login(req: func.HttpRequest) -> func.HttpResponse:
    """
    Recieves a login attempt in a JSON document and checks credentials in the DB.
    e.g. {"username":  "antoni_gn" , "password" : "ILoveTricia"}
    """
    input = req.get_json()
    logging.info('Python HTTP trigger function processed a PLAYER_LOGIN request: {}'.format(input))

    # Extract the details from the inputted JSON.
    username = input['username']
    password = input['password']

    try:
        # Search for the player's credentials in the database.
        query = 'SELECT * FROM users WHERE CONTAINS(users.username, "{0}") AND users.password = "{1}"'.format(username, password)
        users = utility.query_items(proxy=users_proxy,query=query)
        if users:
            logging.info("SUCCESS: login credentials validated.")
            response_body = json.dumps({"result": True, "msg": "OK"})
            return func.HttpResponse(body=response_body,mimetype="application/json") 

    # Handle error if theres no result returned (i.e. users = [])
    except NoQueryError:
        logging.info("FAILURE: Username or password incorrect")
        response_body = json.dumps({"result": False, "msg": "Username or password incorrect"})
        return func.HttpResponse(body=response_body,mimetype="application/json")       



@app.route(route="user/search", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def user_search(req: func.HttpRequest) -> func.HttpResponse:
    """
    Returns the search results from an inputted keyword.
    e.g. {"search": "search"} 
    (Note: to make it case in-sensitive, all search MUST be lowercase)
    """
    input = req.get_json()
    logging.info('Python HTTP trigger function processed a USER_SEARCH request.')

    # Collect all the users registered:
    search = input['search']

    try:
        query = 'SELECT * FROM users WHERE LOWER(users.username) LIKE LOWER("%{}%")'.format(search)
        query_result = utility.query_items(proxy=users_proxy,query=query)

        if query_result:
            # Retrieve the users
            logging.info('Successfully collected all usernames similar to "{}"!'.format(search))
            users = []

            for user in query_result:
                logging.info('id: {0}, username: {1}'.format(user['id'], user['username']))
                users.append({"id": user['id'], "username": user['username']})

            # Send Response
            response_body = json.dumps({"result": True, "msg": users})
            return func.HttpResponse(body=response_body,mimetype="application/json")
        
    # Handle error if theres no result returned (i.e. query_result = [])
    except NoQueryError:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to retrieve users"})
        return func.HttpResponse(body=response_body,mimetype="application/json")


@app.route(route="user/get/info", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def user_get_info(req: func.HttpRequest) -> func.HttpResponse:
    """
    Returns a user's profile info.
    { "id": "id" }
    """
    input = req.get_json()
    logging.info('Python HTTP trigger function processed a USER_GET_INFO request.')

    # Retrieve the user with the corrosponding id:
    id = input['id']

    try:
        query = 'SELECT * FROM users WHERE users.id = "{}"'.format(id)
        query_result = utility.query_items(proxy=users_proxy,query=query)

        if query_result:
            # Retrieve the user's info
            user = query_result[0]
            info = { "id": user['id'], "username": user['username'], "streak": user['streak'], "daily_training_score": user['daily_training_score'] }
            logging.info('User info extracted: {}'.format(info))

            # Send Response
            response_body = json.dumps({"result": True, "msg": info})
            return func.HttpResponse(body=response_body,mimetype="application/json")
        
    # Handle error if theres no result returned (i.e. query_result = [])
    except NoQueryError:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to retrieve user."})
        return func.HttpResponse(body=response_body,mimetype="application/json")

@app.route(route="user/update/info", methods=[func.HttpMethod.PUT], auth_level=func.AuthLevel.FUNCTION)
def user_update_info(req: func.HttpRequest) -> func.HttpResponse:
    """
    Updates a user's profile info with the given info, can be flexible as long as they're matching keys
    { 'id': 'id', 'updates': {
            'username': 'AntWazHere',
            'password': 'IFrigginLoveTricia',
            ...
        }
    }
    {'id': 'user_id_1', 'username': 'antoni_gn', 'password': 'ILoveTricia', 'streak': 1, 'daily_training_score': 100}
    """
    input = req.get_json()
    logging.info('Python HTTP trigger function processed a USER_UPDATE_INFO request.')

    # Retrieve the user with the corrosponding id:
    id = input['id']
    updates = input['updates']

    try:
        utility.update_user(proxy=users_proxy,id=id,info=updates)

        # Send Response
        response_body = json.dumps({"result": True, "msg": "OK"})
        return func.HttpResponse(body=response_body,mimetype="application/json")
        
    # Handle error if the update is invalid.
    except NoQueryError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Unable to retrieve user."})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except CosmosResourceNotFoundError:
        logging.info("FAILURE: Entity with the specified id does not exist in the system.")
        response_body = json.dumps({"result": False, "msg": "Unable to retrieve user."})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except ExistentUserError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Username already exists"})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except BadUserError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Username less than 5 characters or more than 15 characters"})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except BadPasswordError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Password less than 8 characters or more than 15 characters"})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except InvalidStreakError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Invalid streak value."})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except InvalidScoreError as e:
        logging.info("FAILURE: {}".format(e))
        response_body = json.dumps({"result": False, "msg": "Invalid daily_training_score value."})
        return func.HttpResponse(body=response_body,mimetype="application/json")


@app.route(route="user/friend/all", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def user_friend_all(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retrieve all the inputted user's friends and friend requests.
    e.g. {"username": "antoni_gn"}
    """
    input = req.get_json()
    logging.info('Python HTTP trigger function processed a USER_FRIEND_ALL request.')

    # Extract json input
    username = input['username']

    try:
        # Get the recipient based on username
        query = 'SELECT * FROM users WHERE users.username = "{}"'.format(username)
        query_result = utility.query_items(proxy=users_proxy,query=query)

        if query_result:
            user = query_result[0]
            user_friend_stats = {"friends": user["friends"], "friend_requests": user["friend_requests"]}
            logging.info('username: {0}, -> {1}'.format(user['username'], user_friend_stats))

        # Send Response
        response_body = json.dumps({"result": True, "msg": user_friend_stats})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except NoQueryError:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to find user."})
        return func.HttpResponse(body=response_body,mimetype="application/json")


@app.route(route="user/friend/request", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def user_friend_request(req: func.HttpRequest) -> func.HttpResponse:
    """
    Requesting user gets added the to requested user's "friend_requests" list.
    e.g. {"sender_id": "sender_id", "sender_username": "antoni_gn", "recipient_id": "recipient_id"}
    """
    input = req.get_json()
    logging.info('Python HTTP trigger function processed a USER_FRIEND_REQUEST request.')

    # Extract json input
    sender_id = input['sender_id']
    sender_username = input['sender_username']
    recipient_id = input['recipient_id']

    try:
        # Get the recipient based on id
        query = 'SELECT * FROM users WHERE users.id = "{}"'.format(recipient_id)
        query_result = utility.query_items(proxy=users_proxy,query=query)

        if query_result:
            logging.info("User found: {}".format(query_result))
            user_to_update = query_result[0]
            friend_request_list = user_to_update['friend_requests']
            friend_list = user_to_update['friends']
            new_friend = {"id": sender_id, "username": sender_username}

            # Check if that user already requested:
            if new_friend in friend_request_list:
                response_body = json.dumps({"result": False, "msg": "Already sent a friend request!"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
            elif new_friend in friend_list:
                response_body = json.dumps({"result": False, "msg": "Already friends!"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
            else:
                # Add to the friend_request_list
                new_friend_request_list = []
                new_friend_request_list.append(new_friend)

                # If the friend_request_list already has contents inside
                if friend_request_list != []:

                    for friend in friend_request_list:
                        new_friend_request_list.append({"id": friend['id'], "username": friend['username']})

                # Modify the user via field names as keys:
                user_to_update['friend_requests'] = new_friend_request_list

                # Save changes in database
                users_proxy.replace_item(item=user_to_update['id'], body=user_to_update)

                logging.info("New state of user after REQUESTING friend: {}".format(user_to_update))

                # Send Response
                response_body = json.dumps({"result": True, "msg": "OK"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
    
    except NoQueryError:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to send friend request."})
        return func.HttpResponse(body=response_body,mimetype="application/json")


@app.route(route="user/friend/accept", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def user_friend_accept(req: func.HttpRequest) -> func.HttpResponse:
    """
    Requesting user gets added the to requested user's "friends" list.
    e.g. {"sender_id": "sender_id", "sender_username": "antoni_gn", "recipient_id": "recipient_id"}
    """
    input = req.get_json()
    logging.info('Python HTTP trigger function processed a USER_FRIEND_ACCEPT request.')

    # Extract json input
    sender_id = input['sender_id']
    sender_username = input['sender_username']
    recipient_id = input['recipient_id']

    try:
        # Get the recipient based on id
        query = 'SELECT * FROM users WHERE users.id = "{}"'.format(recipient_id)
        query_result = utility.query_items(proxy=users_proxy,query=query)

        if query_result:
            logging.info("User found: {}".format(query_result))
            user_to_update = query_result[0]
            friend_request_list = user_to_update['friend_requests']
            friend_list = user_to_update['friends']
            new_friend = {"id": sender_id, "username": sender_username}

            # Check if that user already befriended:
            if new_friend in friend_list:
                response_body = json.dumps({"result": False, "msg": "Already friends!"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
            elif new_friend not in friend_request_list:
                response_body = json.dumps({"result": False, "msg": "Haven't sent friend request!"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
            else:
                # Add to the friend_list
                new_friend_list = []
                new_friend_list.append(new_friend)

                # If the friend_list already has contents inside
                if friend_list != []:

                    for friend in friend_list:
                        new_friend_list.append({"id": friend['id'], "username": friend['username']})

                # Remove from friend_requests_list
                new_friend_request_list = []

                if friend_request_list != []:
                    for friend in friend_request_list:
                        if friend != new_friend:
                            new_friend_request_list.append({"id": friend['id'], "username": friend['username']})

                # Modify the user via field names as keys:
                user_to_update['friends'] = new_friend_list
                user_to_update['friend_requests'] = new_friend_request_list

                # Save changes in database
                users_proxy.replace_item(item=user_to_update['id'], body=user_to_update)

                logging.info("New state of user after ADDING friend: {}".format(user_to_update))

                # Send Response
                response_body = json.dumps({"result": True, "msg": "OK"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
            
    except NoQueryError:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to add friend."})
        return func.HttpResponse(body=response_body,mimetype="application/json")


@app.route(route="user/friend/reject", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def user_friend_reject(req: func.HttpRequest) -> func.HttpResponse:
    """
    Requesting user gets removed from the to requested user's "friend_requests" list.
    e.g. {"sender_id": "sender_id", "sender_username": "antoni_gn", "recipient_id": "recipient_id"}
    """
    input = req.get_json()  
    logging.info('Python HTTP trigger function processed a USER_FRIEND_REJECT request.')

    # Extract json input
    sender_id = input['sender_id']
    sender_username = input['sender_username']
    recipient_id = input['recipient_id']

    try:
        # Get the recipient based on id
        query = 'SELECT * FROM users WHERE users.id = "{}"'.format(recipient_id)
        query_result = utility.query_items(proxy=users_proxy,query=query)

        if query_result:
            logging.info("User found: {}".format(query_result))
            user_to_update = query_result[0]
            friend_request_list = user_to_update['friend_requests']
            friend_list = user_to_update['friends']
            new_friend = {"id": sender_id, "username": sender_username}

            # Check if that user already requested:
            if new_friend in friend_list:
                response_body = json.dumps({"result": False, "msg": "Already friends!"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
            elif new_friend not in friend_request_list:
                response_body = json.dumps({"result": False, "msg": "Haven't sent friend request!"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
            else:
                # Remove from friend_requests_list
                new_friend_request_list = []

                if friend_request_list != []:
                    for friend in friend_request_list:
                        if friend != new_friend:
                            new_friend_request_list.append({"id": friend['id'], "username": friend['username']})

                # Modify the user via field names as keys:
                user_to_update['friend_requests'] = new_friend_request_list

                # Save changes in database
                users_proxy.replace_item(item=user_to_update['id'], body=user_to_update)

                logging.info("New state of user after REJECTING friend request: {}".format(user_to_update))

                # Send Response
                response_body = json.dumps({"result": True, "msg": "OK"})
                return func.HttpResponse(body=response_body,mimetype="application/json")
    except NoQueryError:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to remove friend request."})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    

@app.route(route="question/get/category", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def question_get_category(req: func.HttpRequest) -> func.HttpResponse:
    """
    Returns a randomised set of questions by category.
    No_of_Qs: How many questions in total.
    {"No_of_Qs": int, "topic": "topic"}
    """
    input = req.get_json()  
    logging.info('Python HTTP trigger function processed a QUESTION_GET_CATEGORY request.')

    No_of_Qs = input['No_of_Qs']
    topic = input['topic']

    try:
        # Create the TOPIC question bank, with randomised questions.
        random_Qs = utility.get_random_questions_topic(proxy=questions_proxy, topic=topic,No_of_Qs=No_of_Qs)
        quiz_Qs = []
        
        for q in random_Qs:
            quiz_Q = question(q['questions'], q['topic'], q['image'], q['correct_answers'], q['incorrect_answers'])
            quiz_Qs.append(quiz_Q.to_dict())

        logging.info("'{0}' topic quiz Bank of {1} questions created! First Question: {2}".format(topic, len(quiz_Qs), quiz_Qs[0]))
        # Send Response
        response_body = json.dumps({"result": True, "msg": quiz_Qs})
        return func.HttpResponse(body=response_body,mimetype="application/json")
        
    except NoQueryError:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to get questions."})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    except ElementSizeError as e:
        # If the random.sample method fails
        response_body = json.dumps({"result": False, "msg": e})
        return func.HttpResponse(body=response_body,mimetype="application/json")


@app.route(route="question/get/quiz", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def question_get_quiz(req: func.HttpRequest) -> func.HttpResponse:
    """
    Returns a randomised set of questions by all categories, you can define the amount by percentage of each category you want.
    The percentage is to what to reccommend to the user depending on their recent quiz performances, handled by the ML model.
    (i.e. Higher percentages means the user performed more poorly on that specific topic)
    No_of_Qs: How many questions in total.
    ML model returns result
    {"No_of_Qs": int, "username": "username"}
    OR No ML model result was used
    {"No_of_Qs": int, "username": "n/a"}
    """
    input = req.get_json()  
    logging.info('Python HTTP trigger function processed a QUESTION_GET_ALL request.')

    No_of_Qs = input['No_of_Qs']
    username = input['username']

    try:
        if username == "n/a":
            # Create the question bank, with randomised questions.
            random_Qs = utility.get_random_questions(proxy=questions_proxy,No_of_Qs=No_of_Qs)

            quiz_Qs = []
            for q in random_Qs:
                quiz_Q = question(q['questions'], q['topic'], q['image'], q['correct_answers'], q['incorrect_answers'])
                quiz_Qs.append(quiz_Q.to_dict())

            logging.info("Quiz Bank of {} questions created! First Question: {}".format(len(quiz_Qs), quiz_Qs[0]))
            # Send Response
            response_body = json.dumps({"result": True, "msg": quiz_Qs})
            return func.HttpResponse(body=response_body,mimetype="application/json")
        else:

            # Get the user based on the username
            query = 'SELECT * FROM users WHERE users.username = "{}"'.format(username)
            query_result = utility.query_items(proxy=users_proxy,query=query)

            user = query_result[0]
            recent_category_scores = {'recent_category_scores': user['recent_category_scores'] }
            logging.info(recent_category_scores)

            # Run the ml model to get the suggested distribution of topics in this quiz.
            topics = ml_model.get_predicted_scores(recent_category_scores=recent_category_scores)
            logging.info('Ratios of topics: {}'.format(topics))

            Qs = []
            Qs.extend(utility.get_random_questions_topic(proxy=questions_proxy,topic="Driving Off",No_of_Qs=math.floor(No_of_Qs * topics['Driving Off'])))
            Qs.extend(utility.get_random_questions_topic(proxy=questions_proxy,topic="Urban Driving",No_of_Qs=math.floor(No_of_Qs * topics['Urban Driving'])))
            Qs.extend(utility.get_random_questions_topic(proxy=questions_proxy,topic="Rural Driving",No_of_Qs=math.floor(No_of_Qs * topics['Rural Driving'])))
            Qs.extend(utility.get_random_questions_topic(proxy=questions_proxy,topic="Bigger Roads",No_of_Qs=math.floor(No_of_Qs * topics['Bigger Roads'])))
            Qs.extend(utility.get_random_questions_topic(proxy=questions_proxy,topic="Motorways",No_of_Qs=math.floor(No_of_Qs * topics['Motorways'])))
            Qs.extend(utility.get_random_questions_topic(proxy=questions_proxy,topic="Tricky Conditions",No_of_Qs=math.floor(No_of_Qs * topics['Tricky Conditions'])))
            Qs.extend(utility.get_random_questions_topic(proxy=questions_proxy,topic="Breakdowns",No_of_Qs=math.floor(No_of_Qs * topics['Breakdowns'])))

            random_Qs = utility.select_random(Qs, len(Qs))
            quiz_Qs = []
            for q in random_Qs:
                quiz_Q = question(q['questions'], q['topic'], q['image'], q['correct_answers'], q['incorrect_answers'])
                quiz_Qs.append(quiz_Q.to_dict())

            logging.info("Quiz Bank of {} questions created! First Question: {}".format(len(quiz_Qs), quiz_Qs[0]))

            # Send Response
            response_body = json.dumps({"result": True, "msg": quiz_Qs})
            return func.HttpResponse(body=response_body,mimetype="application/json")
        
    except NoQueryError:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to get questions."})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    except ElementSizeError:
        # If the random.sample method fails
        response_body = json.dumps({"result": False, "msg": "num_elements cannot be greater than the length of the list"})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    

@app.route(route="question/get/feedback", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def question_get_feedback(req: func.HttpRequest) -> func.HttpResponse:
    """
    Returns AI generated responses to give specific feedback about incorrect answers from a quiz.
    { "incorrect_answers": [
                                { 
                                    "question": "What does a Yield sign indicate to a driver?",
                                    "correct_ans": "You must slow down and give the right-of-way to other vehicles or pedestrians."
                                    "incorrect_ans": "You must come to a complete stop before proceeding."  
                                }, ...
                            ] 
    }
    """
    input = req.get_json()  
    logging.info('Python HTTP trigger function processed a QUESTION_GET_FEEDBACK request.')

    incorrect_answers = input['incorrect_answers']

    try:
        feedback = oai.evaluate_wrong_answers(ai_proxy=openai_proxy,incorrect_answers=incorrect_answers)
        logging.info("SUCCESS: generated feedback!")
        response_body = json.dumps({"result": True, "msg": feedback})
        return func.HttpResponse(body=response_body,mimetype="application/json")

    except ResponseError:
        logging.info("FAILURE: Cannot generate feedback.")
        response_body = json.dumps({"result": False, "msg": "Cannot generate feedback." })
        return func.HttpResponse(body=response_body,mimetype="application/json")