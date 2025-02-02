from azure.cosmos import ContainerProxy

class ResponseError(ValueError):
    pass
class open_ai():
    """
    Class to handle the open AI operations.
    """

    schema = "{ 'question': '...', 'feedback', '...'}"
    
    def evaluate_wrong_answers(self, ai_proxy: ContainerProxy, incorrect_answers):
        """
        Uses the chat playground to get the ai repsonse.
        """

        chat_completion = ai_proxy.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Please return feedback from the following dictionary of incorrectly answered questions, and ONLY reply another list of dictionaries only including the question and it's informative feedback explaining WHY that is the answer. The dictionary schema form is {}, and the incorrect answers are the following: {}".format(self.schema, incorrect_answers)
                }
            ],
            model="gpt-3.5-turbo-0301"
        )

        reply = chat_completion.choices[0].message.content

        # Validate reply to compensate for non-deterministic results
        if not reply:
            raise ResponseError("Cannot generate suggestion")
        else:
            return reply