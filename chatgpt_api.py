import openai
import config

openai.api_base = config.api_base
openai.api_key = config.api_key

def fake_api(query, model=config.model, temperature=0.8, max_tokens=2048):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role': 'user', 'content': query}
        ],
        temperature=temperature,
        max_tokens=max,
        stream=True
    )

    for chunk in response:
        if 'choices' in chunk and 'delta' in chunk['choices'][0]:
            chunk_msg = chunk['choices'][0]['delta'].get('content', '')
            yield chunk_msg
        else:
            yield False

if __name__ == '__main__':
    print(config.api_base)
    print(config.api_key)
    api = fake_api("你好")
    for value in api:
        if value:
            print(value, end='')

