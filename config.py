if_pandora = True                                                   #是否尝试使用pandora

long_text = True                                                    #是否启用概括

max_token = 1000                                                    #达到此token就概括,推荐1000~2000
smaller_text = 50                                                   #概括成此单词数

openai_api = "REAL_KEY"  #real_key
pandora_api = "FAKE_KEY"      #fake_key
# model="gpt-3.5-turbo"
model="gpt-4"

base_url = "https://ai.fakeopen.com/v1/"                            #pandora项目用的反代

print("配置文件导入成功")