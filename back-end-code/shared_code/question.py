from shared_code.utility import utility

class question():
    """
    Class dealing with contructing questions for the quizzes in the application.
    """

    utility = utility()

    # Constructor for a single question:
    def __init__(self, questions, topic, image, correct_answers, incorrect_answers, sign_question):
        self.questions = questions
        self.topic = topic
        self.image = image
        self.correct_answers = correct_answers
        self.incorrect_answers = incorrect_answers
        self.sign_question = sign_question

    def to_dict(self):
        """
        Creates the question by randomising the question's contents to ensure variation, returns as a dictionary to send back.
        """
        selected_question = self.utility.select_random(self.questions, 1)
        selected_correct_answer = self.utility.select_random(self.correct_answers, 1)
        incorrect_answers = self.utility.select_random(self.incorrect_answers, 3)

        return {"question": selected_question[0], "topic": self.topic, "image": self.image, 
                "correct_answer": selected_correct_answer[0], "incorrect_answers": incorrect_answers,
                "sign_question": self.sign_question}
