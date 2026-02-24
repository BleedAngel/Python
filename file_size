import os
import shutil

TARGET_DIR=input("target_dir:\n")
if not os.path.exists(TARGET_DIR):
    print("Error")
    exit()

def FILE_SIZE_CATEGORY(file_size):
    size=file_size
    if(size<=1*1024*1024):
        return "Small"
    elif(size<=10*1024*1024):
        return "Medium"
    else:
        return "Large"

def organize_files():
    for filename in os.listdir(TARGET_DIR):
        file_path=os.path.join(TARGET_DIR,filename)

        if(os.path.isfile(file_path)):
            moved=False

            file_size=os.path.getsize(file_path)
            category=FILE_SIZE_CATEGORY(size)
            dest_folder=os.path.join(TARGET_DIR,category)
            os.makedirs(dest_folder,exist_ok=True)
            print(f"{filename}({size//1024//1024} MB) → {category}")
            #shutil.move(file_path,os.path.join(dest_folder,filename))
            moved=True
            break

if __name__=="__main__":
    organize_files()

# example:
# target_dir="C:\Users\User\Downloads"
# filename="example.mp4"
# file_size=5*1024*1024 #bytes
# file_path="C:\Users\User\Downloads\example.mp4"
# dest_folder="C:\Users\User\Downloads\Text\example.txt"
