import random
from typing import List, Dict, Any
from azure.cosmos import ContainerProxy, CosmosDict
from shared_code.user import user

class NoQueryError(ValueError):
    pass
class ElementSizeError(ValueError):
    pass
class InvalidStreakError(ValueError):
    pass
class InvalidScoreError(ValueError):
    pass
class ExistentUserError(ValueError):
    pass
class BadUserError(ValueError):
    pass
class BadPasswordError(ValueError):
    pass
class utility():
    """
    Utility class for CosmosDB services.
    """

    def query_items(self, proxy: ContainerProxy, query: str):
        """
        Returns items from a prxoy object's querying, returns error if there are no results.
        """
        result = list(proxy.query_items(query=query, enable_cross_partition_query=True))

        if result == []:
            raise NoQueryError("Unable to find result.")
        
        return result
    
    def update_user(self, proxy: ContainerProxy, id ,info: Dict):
        """
        Updates a player's info based on key, value changes.
        """
        
        user_to_update = proxy.read_item(item=id,partition_key=id)

        if self.update_is_valid(proxy=proxy,user_to_update=user_to_update, info=info):

            for key, value in info.items():
                user_to_update[key] = value

            proxy.replace_item(item=id, body=user_to_update)


    def update_is_valid(self, proxy: ContainerProxy, user_to_update: CosmosDict, info: Dict):
        """
        Check if the update info is valid or not:
        """

        for key, value in info.items():
            
            if key == 'username':
                if not (5 <= len(value) <= 15):
                    raise BadUserError("Username less than 5 characters or more than 15 characters")    
                elif not self.is_unique(proxy=proxy, username=value):
                    raise ExistentUserError("Username already exists")  
            elif key == 'password':
                if not (8 <= len(value) <= 15):
                    raise BadPasswordError("Password less than 8 characters or more than 15 characters")
            elif key == 'streak':
                if value < 0:
                    raise InvalidStreakError('Invalid streak value.')
            elif key == 'daily_training_score':
                if value < 0:
                    raise InvalidScoreError('Invalid daily_training_score value.')

        return True


    def is_unique(self, proxy: ContainerProxy, username):
        """
        Iterates over list of players to check if it's unique
        """
        # Check if there is a player username already stored
        query = 'SELECT * FROM users WHERE CONTAINS(users.username, "{}")'.format(username)
        existing_username = list(proxy.query_items(query=query, enable_cross_partition_query=True))
        if not existing_username:
            # If no existing username, then its unique.
            return True
        else:
            # If there is, username already taken.
            return False

    
    def select_random(self, list, num_elements):
        """
        Selects a specified number of random element(s) from a list

        list: The list to select elements from.
        num_elements: Number of elements to select
        """
        if num_elements == 0:
            return []

        if num_elements > len(list):
            raise ElementSizeError("num_elements cannot be greater than the length of the list")
        
        return random.sample(list, num_elements)
    
    def get_random_questions(self, proxy: ContainerProxy, No_of_Qs: int):
        # Get the questions by category
        query = 'SELECT * FROM questions'
        query_result = self.query_items(proxy=proxy,query=query)

        return self.select_random(query_result, No_of_Qs)
    
    def get_random_questions_topic(self, proxy: ContainerProxy, topic: str, No_of_Qs: int):
        # Get the questions by category
        query = 'SELECT * FROM questions WHERE questions.topic = "{}"'.format(topic)
        query_result = self.query_items(proxy=proxy,query=query)

        return self.select_random(query_result, No_of_Qs)