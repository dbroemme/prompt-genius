import openai
from bardapi import Bard
import os
from dotenv import load_dotenv
load_dotenv()

from .models import Question, Answer

def call_bard(query):
    bard = Bard()
    answer = bard.get_answer(query)
    print(answer)

    # Only return response text within the delimeter,
    # typically triple backticks
    response_text = ""
    lines = answer['content'].split('\n')
    inside_delimeter = False
    for line in lines:
        if line == "```":
            inside_delimeter = not inside_delimeter
        elif inside_delimeter:
            if len(line) > 0:
                response_text = response_text + line + '\n'

    return (response_text)

def call_chatgpt(prompt, temperature = 0.7, max_tokens = 1024):
    # Set up OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].text


def generate_question(topic):

    # Define the prompt to generate trivia questions on the given topic
    prompt = f'''Generate one trivia question on the topic of {topic}.
Provide four possible answers and then indicate the letter of the correct answer.
Format your response using the following template format.

Question: [QUESTION_TEXT]
A) [ANSWER_1]
B) [ANSWER_2]
C) [ANSWER_3]
D) [ANSWER_4]

Correct answer: [CORRECT_ANSWER_LETTER]
'''

    #return call_chatgpt(prompt)
    return call_bard(prompt)

def create_question_with_answers(text, quiz):
    # Split the text into the question and answer options
    question_text, answer_options = text.split('?\n')

    # Get the question text
    question_text = question_text.replace("Question: ", "").strip() + "?"

    # Split the answer options into individual lines
    answer_lines = answer_options.strip().split('\n')

    # Extract the correct answer letter
    correct_answer_line = answer_lines.pop().replace("Correct answer: ", "").strip()[0]

    # Create the question instance
    question = Question.objects.create(text=question_text, quiz=quiz)

    # Iterate through the answer lines to create answer instances
    for line in answer_lines:
        answer_text = line.strip()
        is_correct = answer_text.startswith(correct_answer_line)
        answer = Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
        print(str(answer))

    return question
