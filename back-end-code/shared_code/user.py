import uuid
from azure.cosmos import ContainerProxy

class UniqueUserError(ValueError):
    pass
class InvalidUserError(ValueError):
    pass
class InvalidPasswordError(ValueError):
    pass
class user():
    """
    Holds the information of a single user.
    """

    # Constructor to faciliate player creation:
    def __init__(self,user_proxy: ContainerProxy, username, password):
        # auto generated unique id
        self.id = str(uuid.uuid4())
        self.user_proxy = user_proxy
        self.username = username
        self.password = password

    def is_valid(self):
        """
        Validation method to check the user inputted is correct.
        """
        if not self.is_unique():
            raise UniqueUserError("Username already exists")
        
        elif not (5 <= len(self.username) <= 15):
            raise InvalidUserError("Username less than 5 characters or more than 15 characters")
        
        elif not (8 <= len(self.password) <= 15):
            raise InvalidPasswordError("Password less than 8 characters or more than 15 characters")
        
        return True


    def is_unique(self):
        """
        Iterates over list of players to check if it's unique
        """
        # Check if there is a player username already stored
        username = self.username
        query = 'SELECT * FROM users WHERE CONTAINS(users.username, "{}")'.format(username)
        existing_username = list(self.user_proxy.query_items(query=query, enable_cross_partition_query=True))
        if not existing_username:
            # If no existing username, then its unique.
            return True
        else:
            # If there is, username already taken.
            return False


    def to_dict(self):
        """
        Function return player info as a dictionary.
        """
        dict_representation = {'id': self.id, 'username': self.username, 'password': self.password,
                               'friends': [], 'friend_requests': [], 'streak': 0, 'daily_training_score': 0,
                               'recent_category_scores': {
                                    "Driving Off": [],
                                    "Urban Driving": [],
                                    "Rural Driving": [],
                                    "Bigger Roads": [],
                                    "Motorways": [],
                                    "Tricky Conditions": [],
                                    "Breakdowns": []
                               }}
        return dict_representation