#"__main__"=>直接執行 / "myscript"=>被匯入
if(__name__=="__main__"):
    print(123)
def hi():
    print("hi,bro~")
    print(__name__)