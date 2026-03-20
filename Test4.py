s=[True,False,0,1,0.0,[],{},""]
x=0
for i in s:
    if not i:
        print(f"index={x};{i}=>1")
    if (i==False):
        print(f"index={x};{i}=>2")
    x+=1