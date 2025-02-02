import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class evaluator():
    """
    Machine learning model code for evaluating a user's recent scores and returns 
    a predicted ratio of which topics to go over in the next training session.
    """

    def get_predicted_scores(self, recent_category_scores):
        # Predict the next score for each category
        predicted_scores = {}
        for category, scores in recent_category_scores['recent_category_scores'].items():
            predicted_scores[category] = 1 - self.predict_next_score(scores)

        # Normalise the scores by dividing all predicted scores with sum of all scores to 2 sf
        total_score = sum(predicted_scores.values())
        for category, score in predicted_scores.items():
            predicted_scores[category] = round(score / total_score, 2)

        # Return the predicted scores
        return predicted_scores

    # Function to predict the next score for each category
    def predict_next_score(self, category_scores):
        # Prepare the data: previous scores (X) and the next score (y)
        X = np.array([category_scores[:-1]]).reshape(-1, 1)  # Features: previous scores (excluding last one)
        y = category_scores[1:]  # Target: next scores

        # Train the Random Forest model
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)

        # Predict the next score
        next_score = model.predict([category_scores[-1:]])  # Predict next based on the last score
        return round(next_score[0], 2)