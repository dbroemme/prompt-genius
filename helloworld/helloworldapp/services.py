import openai
from bardapi import Bard
import os
from dotenv import load_dotenv
load_dotenv()

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
