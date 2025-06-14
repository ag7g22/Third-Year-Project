import random
from datetime import datetime, timezone
import pytz
from typing import Dict, List, Any
from azure.cosmos import ContainerProxy, CosmosDict
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
class AlreadyFriendsError(ValueError):
    pass
class NotFriendsError(ValueError):
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
    

    def add_friends(self, proxy: ContainerProxy, user_1: CosmosDict, user_2: CosmosDict):
        """
        - Adds user 2 to user 1's friend list.
        - Removes user 2 from user 1's friend request list if it hasn't already.
        """
        # Extract the appropriate info from the two users:
        user_1_request_list = user_1['friend_requests']
        user_1_friend_list = user_1['friends']
        user_2_entry = { 'id': user_2['id'], 'username': user_2['username'] }

        if user_2_entry in user_1_friend_list:
            raise AlreadyFriendsError('Already friends!')
        
        # Add to the friend_list
        user_1_friend_list.append(user_2_entry)

        # Only remove if user_2 is IN the friend_request list
        user_1['friend_requests'] = [
            {"id": friend['id'], "username": friend['username']} 
            for friend in user_1_request_list 
            if friend != user_2_entry
        ]

        # Save changes in database
        proxy.replace_item(item=user_1['id'], body=user_1)

    
    def remove_friends(self, proxy: ContainerProxy, user_1: CosmosDict, user_2: CosmosDict):
        """
        Remove user_2 from user_1's friend list and vice versa
        """
        # Extract the id and username to remove the entries
        user_1_entry = { "id": user_1['id'], "username": user_1['username'] }
        user_2_entry = { "id": user_2['id'], "username": user_2['username'] }

        user_1_friends = user_1['friends']
        user_2_friends = user_2['friends']

        if user_2_entry not in user_1_friends or user_1_entry not in user_2_friends:
            raise NotFriendsError('Not friends!')

        # Remove the users from their friend lists:
        user_1['friends'] = [
            {"id": friend['id'], "username": friend['username']} 
            for friend in user_1_friends 
            if friend != user_2_entry
        ]

        user_2['friends'] = [
            {"id": friend['id'], "username": friend['username']} 
            for friend in user_2_friends
            if friend != user_1_entry
        ]

        # Save changes in database
        proxy.replace_item(item=user_1['id'], body=user_1)
        proxy.replace_item(item=user_2['id'], body=user_2)
        
    
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
        # Get the questions by category OR get the sign questions:
        query = 'SELECT * FROM questions WHERE questions.topic = "{}"'.format(topic)
        
        if topic in ["sign_question", "no_sign_question"]:
            sign_value = topic == "sign_question"
            query = f'SELECT * FROM questions WHERE questions.sign_question = {str(sign_value).lower()}'

        query_result = self.query_items(proxy=proxy,query=query)
        return self.select_random(query_result, No_of_Qs)
    
    def sort_to_score_and_streak(self, user_stats: List[Dict[str,Any]]) -> List[Dict[str, Any]]:
        """
        Returns a list of user_stats in descending order by:
        - daily_training_score
        - streak
        Excludes users who completed today's training.
        """
        # Get current UTC time
        utc_now = datetime.now(pytz.utc)

        # Convert to UK time
        uk_time = utc_now.astimezone(pytz.timezone("Europe/London"))

        today_str = uk_time.strftime('%Y-%m-%d')

        # Filter out users who haven't completed today
        filtered_users = [
            user for user in user_stats
            if user.get('training_completion_date') == today_str
        ]

        # Sort the remaining users
        leaderboard = sorted(
            filtered_users,
            key=lambda x: (-x['daily_training_score'], -x['streak'], x['username'].lower())
        )

        return leaderboard[:10]  # Return top 10 only
    
    def convert_to_query_list(self, users: List[str]):
        """
        Returns a list of strings to this format for SQL:
        i.e. ["a","b","c"] -> ("a","b","c")
        """
        return '("' + '", "'.join(users) + '")'
    