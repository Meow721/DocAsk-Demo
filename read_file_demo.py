# 练习：用 Python 读取本地文本文件

with open("notes.txt","r",encoding="utf-8") as f:
    text=f.read()

print("文件的内容是：")
print(text)
print("一共有",len(text),"个字符")