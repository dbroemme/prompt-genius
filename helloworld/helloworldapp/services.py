import openai
from bardapi import Bard
import os
from dotenv import load_dotenv
load_dotenv()

from .models import Quiz, Question, Answer
import xml.etree.ElementTree as ET

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
        if line.startswith("```"):
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
Format your response using the following XML template.

<response>
<question>[QUESTION_TEXT]</question>
<a>A) [ANSWER_1]</a>
<b>B) [ANSWER_2]</b>
<c>C) [ANSWER_3]</c>
<d>D) [ANSWER_4]</d>
<correct_answer>[CORRECT_ANSWER_LETTER]</correct_answer>
</response>
'''

    #return call_chatgpt(prompt)
    return call_bard(prompt)



def create_question_with_answers(text, quiz):
    # Extract question text
    question_text = text.split("Question: ")[1].split("\n")[0].strip()

    # Extract answer options
    answer_options = text.split("?\n")[1:]
    print("answer_options")
    print(answer_options)
    answer_texts = []
    for option in answer_options:
        answer_texts.append(option.strip())

    # Extract correct answer
    correct_answer = text.split("Correct answer: ")[1].strip()

    # Create the question instance
    question = Question.objects.create(quiz=quiz, text=question_text)

    # Create the answer instances
    for answer_text in answer_texts:
        is_correct = (answer_text == correct_answer)
        Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)

    return question


def create_question_with_answers_from_xml(xml_text, quiz):
    # Parse the XML
    root = ET.fromstring(xml_text)

    # Extract question text
    question_text = root.find('question').text.strip()

    # Extract answer options
    answer_texts = []
    for child in root:
        if child.tag in ['a', 'b', 'c', 'd']:
            answer_texts.append(child.text.strip())

    # Extract correct answer
    correct_answer = root.find('correct_answer').text.strip()

    # Create the question instance
    question = Question.objects.create(quiz=quiz, text=question_text)

    # Create the answer instances
    for index, answer_text in enumerate(answer_texts):
        option = chr(ord('a') + index).upper()
        is_correct = (option == correct_answer.upper())
        Answer.objects.create(question=question, text=answer_text, option=option, is_correct=is_correct)

    return question