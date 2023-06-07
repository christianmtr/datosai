import openai
import pandas as pd
from django.conf import settings
from openai.error import AuthenticationError


def get_data(csv):
    data_columns = {}

    df = pd.read_csv(csv)

    for column in df.columns:
        data_columns[column] = df[column].tolist()

    return data_columns


def compose_prompt(data):
    prompt = "What can you tell me about the data in this lists?\n"
    prompt += "Type of information or a pattern on each list?\n"

    for column_header, column_data in data.items():
        prompt += f"- Header: {column_header}; column data:{', '.join(str(cd) for cd in column_data)}\n"

    prompt += "What is the type of information in each column?\n"
    prompt += "What are the patterns in the information in each column?\n"

    return prompt


def check_prompt_length(prompt, raise_exception=False):
    openai_max_token_len = settings.OPENAI_MAX_TOKEN_LEN
    prompt_length = len(prompt)
    message = f"Prompt too large, max token length is set to {openai_max_token_len}, "
    message += f"current prompt length is {prompt_length}."

    if prompt_length > settings.OPENAI_MAX_TOKEN_LEN:
        if raise_exception:
            raise ValueError(message)
        print(message)


def send_request_to_openai(prompt, api_key):
    if not api_key:
        raise AuthenticationError('The current user has not set an API key.')

    openai.api_key = api_key
    response = openai.Completion.create(
        engine='text-ada-001',
        prompt=prompt,
        max_tokens=200,
        temperature=0.5,
    )
    return response.choices[0].text.strip()
