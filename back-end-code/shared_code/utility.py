import math
import random
from azure.cosmos import ContainerProxy

class NoQueryError(ValueError):
    pass
class ElementSizeError(ValueError):
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
    
    def select_random(self, list, num_elements):
        """
        Selects a specified number of random element(s) from a list

        list: The list to select elements from.
        num_elements: Number of elements to select
        """
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
    
    def get_topic_training_questions(self, proxy: ContainerProxy, topic: str, percentage: float, No_of_Qs: int):
        """
        Returns the training topic questions according to the given percentage and number of total questions.
        """

        # Get the questions by category
        query = 'SELECT * FROM questions WHERE questions.topic = "{}"'.format(topic)
        query_result = self.query_items(proxy=proxy,query=query)

        # Only sample the given percentage of No_of_Qs
        Q_size = math.floor(No_of_Qs * percentage)
        
        return self.select_random(query_result, Q_size)

