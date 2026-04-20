import os
import hashlib
import input_validation as validate
from mode import EXECUTE_MODE as EXE_M,FILE_MODE_1 as FI_M1,FILE_MODE_2 as FI_M2

#選擇模式
exe_m=input(
    f"Supported execute_mode: \n"
    f"Save hash[{EXE_M[0]}] | "
    f"Verify hash[{EXE_M[1]}] | "
    f"Save & Verify[{EXE_M[2]}] \n"
    f"Choose execute_mode: \n"
).lower()
validate.response(exe_m,EXE_M)

#選擇演算法模式
print("Supported algorithm: \n",hashlib.algorithms_available)
algorithm=input("Choose algorithm: \n").lower()
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
    target_dir=input("Target_dir: \n").strip("'").strip('"').strip(" ")
    validate.directory(target_dir)

    fi_m1=input(
        f"Supported file_mode1: \n"
        f"Write file[{FI_M1[0]}] | "
        f"Append file[{FI_M1[1]}] \n"
        f"Choose file_mode1: \n"
    ).lower()
    validate.response(fi_m1,FI_M1)

    if(fi_m1=="w"):
        fi_m2=input(
            f"Supported file_mode2: \n"
            f"Make file[{FI_M2[0]}] | "
            f"Cover file[{FI_M2[1]}] \n"
            f"Choose file_mode2: \n"
        ).lower()
        validate.response(fi_m2,FI_M2)

        if(fi_m2==FI_M2[0]):
            hash_dir=input("Hash dir: \n").strip("'").strip('"').strip(" ")
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

    print(f"✅ Hash file saved successfully!*{save_summary}")

#要求對比hash值
if "v" in exe_m:
    check_dir=input("Check dir: \n").strip("'").strip('"').strip(" ")
    validate.directory(check_dir)

    #讀取已有的hash值存取txt檔
    if "s" not in exe_m:
        hash_file=input("Hash file: \n").strip("'").strip('"').strip(" ")
        validate.file(hash_file)

    #逐一對比hash值
    for entry in os.scandir(check_dir):
        if(entry.is_file()):
            file_path=entry.path
            verify_hash(file_path,hash_file)
            check_summary+=1

    print(f"✅ File checked successfully!*{check_summary}")