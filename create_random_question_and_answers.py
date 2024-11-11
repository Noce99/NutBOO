import json
import pathlib
import os
import random

NUM_OF_QUESTIONS = 50

if __name__ == "__main__":
    current_path = pathlib.Path(__file__).parent.resolve()
    questions_and_answers_path = os.path.join(current_path, "src_web", "questions_and_answers.json")

    random_questions_and_answers = []
    for i in range(NUM_OF_QUESTIONS):
        a = random.randint(1, 2)
        if a == 1:
            input_type = "text"
            answer = "82"
        else:
            input_type = "photo"
            answer = ""
        random_questions_and_answers.append(
            {
                "question": "How many 4000 in Italy?",
                "answers": [answer],
                "type_of_answer": input_type, # text / photo
                "question_id": i
            }
        )

    with open(questions_and_answers_path, mode='w') as f:
        f.write(json.dumps(random_questions_and_answers, indent=4))
