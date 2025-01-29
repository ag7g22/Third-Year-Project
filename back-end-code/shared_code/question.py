import uuid
import random
from azure.cosmos import ContainerProxy

class question():
    """
    Class dealing with contructing questions for the quizzes in the application.
    """

    # Constructor for a single question:
    def __init__(self, questions, topic, correct_answers, incorrect_answers):
        self.questions = questions
        self.topic = topic
        self.correct_answers = correct_answers
        self.incorrect_answers = incorrect_answers

    def select_random(self, list, num_elements):
        """
        Selects a specified number of random element(s) from a list

        list: The list to select elements from.
        num_elements: Number of elements to select
        """
        if num_elements > len(list):
            raise ValueError("num_elements cannot be greater than the length of the list")
        
        return random.sample(list, num_elements)

    def to_dict(self):
        """
        Creates the question by randomising the question's contents to ensure variation, returns as a dictionary to send back.
        """
        selected_question = self.select_random(self.questions, 1)
        selected_correct_answer = self.select_random(self.correct_answers, 1)
        incorrect_answers = self.select_random(self.incorrect_answers, 3)

        return {"question": selected_question[0], "topic": self.topic, "correct_answer": selected_correct_answer[0], "incorrect_answers": incorrect_answers}
