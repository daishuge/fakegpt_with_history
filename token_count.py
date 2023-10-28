import jieba

def token_count(str_list):
    total_tokens = 0
    for s in str_list:
        tokens = jieba.lcut(s)  # 使用jieba库进行分词
        total_tokens += len(tokens)
    if total_tokens>=5:
        print("目前token:"+str(total_tokens)+"\n")
    
    return total_tokens


if __name__=="__main__":
    my_chinese_list = ["你好世界", "我爱Python", "你怎么样？"]
    tokens = token_count(my_chinese_list)
    print(f"总共有 {tokens} 个tokens.")