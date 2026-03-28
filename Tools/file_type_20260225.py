import os
import shutil

FILE_TYPE={
    "Image":[".jpg",".png",".jpeg"],
    "Video":[".mp4",".mov",".mkv"],
    "Music":[".mp3",".aac",".wav"],
    "Text":[".txt"],
}

TARGET_DIR=input("target_dir:\n").strip("'").strip('"')
if not os.path.exists(TARGET_DIR):
    print("Error")
    exit()

def organize_files():

    count={key:0 for key in FILE_TYPE.keys()}
    count["Other"]=0

    for filename in os.listdir(TARGET_DIR):
        file_path=os.path.join(TARGET_DIR,filename)

        if(os.path.isfile(file_path)):
            moved=False

            for folder,extensions in FILE_TYPE.items():
                if(filename.lower().endswith(tuple(extensions))):
                    dest_folder=os.path.join(TARGET_DIR,folder)
                    #os.makedirs(dest_folder,exist_ok=True)
                    print(f"{filename} → {folder}")
                    #shutil.move(file_path,os.path.join(dest_folder,filename))
                    moved=True
                    count[folder]+=1
                    break

            if(moved==False):
                dest_folder=os.path.join(TARGET_DIR,"Other")
                #os.makedirs(dest_folder,exist_ok=True)
                print(f"{filename} → Other")
                #shutil.move(file_path,os.path.join(dest_folder,filename))
                moved=True
                count["Other"]+=1
                continue

    summary=" | ".join([f"{key}*{value}"for key,value in count.items() if(value>0)])
    print(summary)

if __name__=="__main__":
    organize_files()

# example:
# target_dir="C:\Users\User\Downloads"
# filename="example.txt"
# file_path="C:\Users\User\Downloads\example.txt"
# dest_folder="C:\Users\User\Downloads\Text\example.txt"
