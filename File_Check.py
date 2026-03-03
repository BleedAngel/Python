import os

TARGET_DIR=input("target_dir:\n")
if not os.path.exists(TARGET_DIR):
    print("Error")
    exit()

def organize_files():
    FILE_COUNT=0
    ERROR_TIMES=0

    for filename in os.listdir(TARGET_DIR):
        FILE_COUNT+=1
        file_path=os.path.join(TARGET_DIR, filename)
        file_size=os.path.getsize(file_path)

        if(os.path.isfile(file_path)):
            try:
                with open(file_path,"rb") as f:
                    f.read(file_size)
            except Exception as e:
                ERROR_TIMES+=1
                print(f"{filename} Error: {e}")
                
    print(f"Error*{ERROR_TIMES} | Total*{FILE_COUNT}")

if __name__=="__main__":
    organize_files()
