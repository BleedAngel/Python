import os
folder=input()
for filename in os.listdir(folder):
    file_path=os.path.join(folder,filename)
    file_size=os.path.getsize(file_path)

    if(os.path.isfile(file_path)):
        with open(file_path,"rb") as f:
            data = f.read(file_size)
            print(data)