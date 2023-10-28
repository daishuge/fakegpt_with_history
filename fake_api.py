import openai
import time

def fake_api(query,max,stream_true,tem,if_pandora):
    
    if if_pandora:
        openai.api_key = "YOUR_PANDORA_FAKE_KEY "    #fake_api
        openai.api_base = "https://ai.fakeopen.com/v1/"
    else:
        openai.api_key = "YOUR_OPNEIA_REAL_KEY"  #real_api
    start_time = time.time()  # 记录开始时间

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': query}
        ],
        temperature=tem,
        max_tokens=max,
        stream=True  # 开启流式输出
    )
    
    result = ""  # 创建一个空字符串来保存流式输出的结果

    for chunk in response:
        # 确保字段存在
        if 'choices' in chunk and 'delta' in chunk['choices'][0]:
            chunk_msg = chunk['choices'][0]['delta'].get('content', '')
            result += chunk_msg  # 将输出内容附加到结果字符串上

            if stream_true:
                print(chunk_msg, end='', flush=True)
                time.sleep(0.05)
    
    return result  # 返回流式输出的完整结果

if __name__ == '__main__':
    while True:
        print("\n")
        query = input("You: ")
        full_result = fake_api(query,1500,True,0.5)  # 将结果保存到 full_result 变量中