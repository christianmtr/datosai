import openai
import pandas as pd
from django.conf import settings


def get_data(csv):
    data_columns = {}

    df = pd.read_csv(csv)

    for column in df.columns:
        data_columns[column] = df[column].tolist()

    return data_columns


def compose_prompt(data):
    prompt = "Here is a description of the word list:\n\n"
    prompt += f"The list contains {len(data.keys())} columns.\n"
    prompt += "The columns and types of information identified are:\n"

    for column_header, column_data in data.items():
        prompt += f"- Header: {column_header}, column data:{', '.join(str(cd) for cd in column_data)}\n"

    prompt += "What is the type of information in each column?\n"
    prompt += "What are the patterns in the information in each column?\n"

    return prompt


def check_prompt_length(prompt, raise_exception=False):
    openai_max_token_len = settings.OPENAI_MAX_TOKEN_LEN
    prompt_length = len(prompt)
    message = f"Prompt too large, max token length is set to {openai_max_token_len}."

    if prompt_length > settings.OPENAI_MAX_TOKEN_LEN:
        if raise_exception:
            raise ValueError(message)
        print(message)


def send_request_to_openai(prompt, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=200  # Ajusta este valor según la longitud de tu prompt y la respuesta esperada
    )
    return response.choices[0].text.strip()
