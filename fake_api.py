import openai
import time

def fake_api(query,max,a):
    openai.api_key = "YOUR_FAKEOPEN_KEY"  # 使用假的 API 密钥
    openai.api_base = "https://ai.fakeopen.com/v1/"
    start_time = time.time()  # 记录开始时间

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': query}
        ],
        temperature=0.9,
        max_tokens=max,
        stream=True  # 开启流式输出
    )
    
    result = ""  # 创建一个空字符串来保存流式输出的结果

    for chunk in response:
        # 确保字段存在
        if 'choices' in chunk and 'delta' in chunk['choices'][0]:
            chunk_msg = chunk['choices'][0]['delta'].get('content', '')
            result += chunk_msg  # 将输出内容附加到结果字符串上

            if a:
                print(chunk_msg, end='', flush=True)
                time.sleep(0.05)
    
    return result  # 返回流式输出的完整结果

if __name__ == '__main__':
    while True:
        query = input("You: ")
        full_result = fake_api(query,1500)  # 将结果保存到 full_result 变量中