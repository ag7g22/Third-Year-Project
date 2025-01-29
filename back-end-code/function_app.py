import datetime
import random
import json
import logging
import os

# shared_code folder imports
from shared_code.user import user, UniqueUserError, InvalidUserError, InvalidPasswordError
from shared_code.question import question

# Azure imports
import azure.functions as func
from azure.cosmos import CosmosClient

app = func.FunctionApp()

cosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
db_proxy = cosmos.get_database_client(os.environ['DatabaseName'])
users_proxy = db_proxy.get_container_client(os.environ['UserContainerName'])
questions_proxy = db_proxy.get_container_client(os.environ['QuestionContainerName'])

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

    # Search for the player's credentials in the database.
    query = 'SELECT * FROM users WHERE CONTAINS(users.username, "{0}") AND users.password = "{1}"'.format(username, password)
    players = list(users_proxy.query_items(query=query, enable_cross_partition_query=True))
    if players:
        logging.info("SUCCESS: login credentials validated.")
        response_body = json.dumps({"result": True, "msg": "OK"})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    else:
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
    query = 'SELECT * FROM users WHERE LOWER(users.username) LIKE LOWER("%{}%")'.format(search)
    query_result = list(users_proxy.query_items(query=query, enable_cross_partition_query=True))
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
    else:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to retrieve users"})
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

    # Get the recipient based on username
    query = 'SELECT * FROM users WHERE users.username = "{}"'.format(username)
    query_result = list(users_proxy.query_items(query=query, enable_cross_partition_query=True))

    if query_result:
        user = query_result[0]
        user_friend_stats = {"friends": user["friends"], "friend_requests": user["friend_requests"]}
        logging.info('username: {0}, -> {1}'.format(user['username'], user_friend_stats))

        # Send Response
        response_body = json.dumps({"result": True, "msg": user_friend_stats})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    else:
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

    # Get the recipient based on id
    query = 'SELECT * FROM users WHERE users.id = "{}"'.format(recipient_id)
    query_result = list(users_proxy.query_items(query=query, enable_cross_partition_query=True))

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
    else:
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

    # Get the recipient based on id
    query = 'SELECT * FROM users WHERE users.id = "{}"'.format(recipient_id)
    query_result = list(users_proxy.query_items(query=query, enable_cross_partition_query=True))

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
    else:
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

    # Get the recipient based on id
    query = 'SELECT * FROM users WHERE users.id = "{}"'.format(recipient_id)
    query_result = list(users_proxy.query_items(query=query, enable_cross_partition_query=True))

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
    else:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to remove friend request."})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    

@app.route(route="question/get/category", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def question_get_category(req: func.HttpRequest) -> func.HttpResponse:
    """
    Returns a randomised set of questions by category
    No_of_Qs: How many questions
    {"No_of_Qs": int, "topic": "topic"}
    """
    input = req.get_json()  
    logging.info('Python HTTP trigger function processed a QUESTION_GET_CATEGORY request.')

    No_of_Qs = input['No_of_Qs']
    topic = input['topic']

    # Get the questions by category
    query = 'SELECT * FROM questions WHERE questions.topic = "{}"'.format(topic)
    query_result = list(questions_proxy.query_items(query=query, enable_cross_partition_query=True))

    if query_result:
        # Create the question bank, with randomised questions.
        random_Qs = random.sample(query_result,No_of_Qs)
        quiz_Qs = []
        for q in random_Qs:
            quiz_Q = question(q['questions'], q['topic'], q['correct_answers'], q['incorrect_answers'])
            quiz_Qs.append(quiz_Q.to_dict())

        logging.info("Quiz Bank for the '{0}' topic created! First 3 Qs: {1}".format(topic, quiz_Qs[:3]))

        # Send Response
        response_body = json.dumps({"result": True, "msg": quiz_Qs})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    else:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to get questions."})
        return func.HttpResponse(body=response_body,mimetype="application/json")


@app.route(route="question/get/all", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def question_get_all(req: func.HttpRequest) -> func.HttpResponse:
    """
    Returns a randomised set of questions by all categories
    No_of_Qs: How many questions
    {"No_of_Qs": int}
    """
    input = req.get_json()  
    logging.info('Python HTTP trigger function processed a QUESTION_GET_ALL request.')

    No_of_Qs = input['No_of_Qs']

    # Get the questions by category
    query = 'SELECT * FROM questions'
    query_result = list(questions_proxy.query_items(query=query, enable_cross_partition_query=True))

    if query_result:
        # Create the question bank, with randomised questions.
        random_Qs = random.sample(query_result,No_of_Qs)
        quiz_Qs = []
        for q in random_Qs:
            quiz_Q = question(q['questions'], q['topic'], q['correct_answers'], q['incorrect_answers'])
            quiz_Qs.append(quiz_Q.to_dict())

        logging.info("Quiz Bank created! First 3 Qs: {}".format(quiz_Qs[:3]))

        # Send Response
        response_body = json.dumps({"result": True, "msg": quiz_Qs})
        return func.HttpResponse(body=response_body,mimetype="application/json")
    else:
        # If the query result gives nothing
        response_body = json.dumps({"result": False, "msg": "Unable to get questions."})
        return func.HttpResponse(body=response_body,mimetype="application/json")