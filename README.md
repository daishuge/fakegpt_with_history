# **Fakegpt**

~~由 Pandora 项目的 api 地址的实现~~

Pandora项目暂时失败，Pandora项目的接口处于繁忙状态

api反代来自qchatgpt项目中的反代，感谢qchatgpt项目的反代

实现无需连接到 openai ，~~且 api 不会泄露~~ 现在怎么可能

## 依赖安装

```shell
pip install openai
```

## 如何获取Pandora项目的api?

Pandora 项目使用假的 api ，类似 fk-xxxxxxxxxxxxxx

请参考这个issue:

https://github.com/zhile-io/pandora/issues/183

## 项目结构

1.在fake_api.py中定义一个调用ai的函数

2.在main.py中让用户输入一个字符串，加入一个history列表

3.调用ai进行回答,并且输出后加入history列表

4.再次让用户输入,把用户新输入和history列表中所有内容交给chatgpt

请各位大佬指正,欢迎发起issue

### 这是来自我同学的一个项目

## Star

![star](https://api.star-history.com/svg?repos=hhhhhge/fakegpt&type=Date)