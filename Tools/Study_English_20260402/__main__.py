import random
import word_bank

target_file=(r"C:\Users\acer\Downloads\1000單 - 工作表1.csv").strip().strip('"').strip("'")

# 題庫：英文單字+中文翻譯
dictionary=word_bank.abc(target_file)
words=list(dictionary.keys())
all_translations=[]
for v in dictionary.values():
    for t in v:
        all_translations.append(t)
correct_first_try=0

for i in range(10):
    word=random.choice(words)
    correct_ans=random.choice(dictionary[word])

    # 隨機選出其他選項
    options=random.sample(all_translations,4)
    while True:
        try:
            if correct_ans not in options:
                options[random.randrange(4)]=correct_ans
            else:
                break
        except:
            break
    random.shuffle(options)

    print(f"\n第 {i+1} 題：{word}")
    for idx,opt in enumerate(options,1):
        print(f"{idx}. {opt}")

    first_try=True
    time=0
    while True:
        choice=input("請輸入選項代碼 (1-4): ")
        if(choice.isdigit() and 1<=int(choice)<=4):
            if(options[int(choice)-1]==correct_ans):
                print("答對了！")
                if first_try:
                    correct_first_try+=1
                break
            else:
                print("答錯了，請再試一次。")
                first_try=False
        else:
            print("請輸入有效的選項代碼。")
            time+=1
        if(time>=4):
            print("False")
            break
        if(choice=="")

print(f"\n總題數: 10")
print(f"一次就答對的次數: {correct_first_try}")