from fake_api import fake_api

history = []

def main(query):
    if query == "clear":
        history.clear()
        return None
    else:
        history.append("user:" + query)
        while True:
            stream_str = stream(history)
            if stream_str[1]:
                break

def stream(query):
    query_gpt = ''
    result = fake_api(str(query))
    for value in result:
        if value:
            query_gpt = query_gpt + value
            return (value,True)
        else:
            history.append("chatgpt:" + query_gpt)
            return (None,False)

if __name__ == '__main__':
    while True:
        main(input('You:'))
        print("".join(history))
