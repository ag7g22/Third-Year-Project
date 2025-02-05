import random
from typing import Dict, List, Any
from azure.cosmos import ContainerProxy
from shared_code.user import UniqueUserError, InvalidUserError, InvalidPasswordError

class NoQueryError(ValueError):
    pass
class ElementSizeError(ValueError):
    pass
class InvalidStreakError(ValueError):
    pass
class InvalidScoreError(ValueError):
    pass
class InvalidRCSError(ValueError):
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

        if self.update_user_is_valid(proxy=proxy, info=info):

            for key, value in info.items():
                user_to_update[key] = value

            proxy.replace_item(item=id, body=user_to_update)


    def update_user_is_valid(self, proxy: ContainerProxy, info: Dict):
        """
        Check if the update info is valid or not:
        """

        for key, value in info.items():
            
            if key == 'username':
                if not (5 <= len(value) <= 15):
                    raise InvalidUserError("Username less than 5 characters or more than 15 characters")    
                elif not self.is_unique(proxy=proxy, username=value):
                    raise UniqueUserError("Username already exists")  
            elif key == 'password':
                if not (8 <= len(value) <= 15):
                    raise InvalidPasswordError("Password less than 8 characters or more than 15 characters")
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
        

    def update_scores(self, proxy: ContainerProxy, id ,scores: Dict):
        """
        Updates a player's recent_category_scores attribute based on key, value changes.
        """
        user_to_update = proxy.read_item(item=id, partition_key=id)
        recent_category_scores = user_to_update['recent_category_scores']

        if self.update_scores_is_valid(scores):
            for key, value in scores.items():
                # Add the score to the user's appropriate recent_category_scores attribute
                self.add_score_to_category(recent_category_scores[key], value)

            proxy.replace_item(item=id, body=user_to_update)
                

    def add_score_to_category(self, scores: list, score_entry):
        """
        Add the score to the category, remove the least recent if the list exceeds 10.
        """
        scores.append(score_entry)
        if len(scores) > 10:
            scores.pop(0)

        return scores


    def update_scores_is_valid(self, scores: Dict):
        """
        Validates the scores in the updates attribute.
        """
        for key, value in scores.items():
            if not (0 <= value <= 1):
                raise InvalidRCSError("Score not between 0 and 1.")
            
        return True
    
    def check_score_lists(self, lists: Dict):
        for key, list in lists.items():
            if len(list) < 2:
                return False
        return True 

    
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
    
    def sort_to_score_and_streak(self, user_stats: List[Dict[str,Any]]) -> List[Dict[str, Any]]:
        """
        Returns a list of users_stats to ascending order:
        First daily_training_score, then higher streak
        """
        leaderboard = sorted(user_stats, key=lambda x: (-x['daily_training_score'], -x['streak'], x['username'].lower()))
        if len(leaderboard) > 10:
            leaderboard = leaderboard[:10]
        return leaderboard
    
    def convert_to_query_list(self, users: List[str]):
        """
        Returns a list of strings to this format for SQL:
        i.e. ["a","b","c"] -> ("a","b","c")
        """
        return '("' + '", "'.join(users) + '")'
    