import os
import hashlib
import input_validation as validate
from mode import EXECUTE_MODE as EXE_M,FILE_MODE_1 as FI_M1,FILE_MODE_2 as FI_M2

s=[]
with open(r"C:\Users\User\Desktop\2.txt","r",encoding="utf-8") as f:
    for line in f:
        s.append(line.strip("\n"))

#選擇模式
exe_m=s[0].lower()
validate.response(exe_m,EXE_M)

#選擇演算法模式
print("Supported algorithm: \n",hashlib.algorithms_available)
algorithm=s[1].lower()
validate.algorithm(algorithm)

#計算hash值
def calculate_hash(file_path,algorithm):
    hash_func=hashlib.new(algorithm)
    with open(file_path,"rb") as f:
        for chunk in iter(lambda: f.read(1024*8), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()

#存取hash值至txt檔
def save_hash(file_path,hash_value,hash_file):
    file_name=os.path.basename(file_path)
    print(f"✅ Saved hash for: '{file_name}'")
    with open(hash_file, "a") as f:
        f.write(f"{file_name},{hash_value}\n")

#對比hash值
def verify_hash(file_path,hash_file):
    validate.file(hash_file)
    
    current_hash=calculate_hash(file_path,algorithm)
    file_name=os.path.basename(file_path)
    with open(hash_file,"r") as f:
        for line in f:
            stored_file,stored_hash=line.strip().split(",")
            if(stored_file==file_name):
                if(stored_hash==current_hash):
                    print(f"✅ Integrity check passed: '{file_name}'")
                    return True
                else:
                    print(f"⚠️ Integrity check failed: '{file_name}'")
                    return False
                
    print(f"❌ No record found for: {file_path}")
    return False

#統計次數
save_summary=0
check_summary=0

#要求存取hash值
if "s" in exe_m:
    target_dir=s[2].strip("'").strip('"').strip(" ")
    validate.directory(target_dir)

    fi_m1=s[3].lower()
    validate.response(fi_m1,FI_M1)

    if(fi_m1=="w"):
        fi_m2=s[4].lower()
        validate.response(fi_m2,FI_M2)

        if(fi_m2==FI_M2[0]):
            hash_dir=s[5].strip("'").strip('"').strip(" ")
            validate.directory(hash_dir)
            target_dir_name=os.path.basename(target_dir)
            hash_file=os.path.join(hash_dir,f"hash_file({target_dir_name}).txt")

        if(fi_m2==FI_M2[1]):
            hash_file=input("Hash file: \n").strip("'").strip('"').strip(" ")
            validate.file(hash_file)
    
    if(fi_m1=="a"):
        hash_file=input("Hash file: \n").strip("'").strip('"').strip(" ")
        validate.file(hash_file)

    open(hash_file,fi_m1).close()

    #逐一生成並存取hash值
    for entry in os.scandir(target_dir):
        if(entry.is_file()):
            file_path=entry.path
            hash_value=calculate_hash(file_path,algorithm)
            save_hash(file_path,hash_value,hash_file)
            save_summary+=1

#要求對比hash值
if "v" in exe_m:
    check_dir=s[6].strip("'").strip('"').strip(" ")
    validate.directory(check_dir)

    #讀取已有的hash值存取txt檔
    if "s" not in exe_m:
        hash_file=s[7].strip("'").strip('"').strip(" ")
        validate.file(hash_file)

    #逐一對比hash值
    for entry in os.scandir(check_dir):
        if(entry.is_file()):
            file_path=entry.path
            verify_hash(file_path,hash_file)
            check_summary+=1
    
print(f"Hash file saved successfully!*{save_summary}")
print(f"File checked successfully!*{check_summary}")