import csv
import sys

def abc(target_file):
    result={}
    with open(target_file,newline='',encoding='utf-8') as f:
        reader=csv.reader(f)
        row_index=0
        for row in reader:
            if(len(row)>=2):
                key=row[0].strip()
                value=row[1].strip()
                # values=[]
                # for cell in row[1:]:
                #     # 先用「、」拆分，再清理空白
                #     parts=[]
                #     for v in cell.split("、"):
                #         v=v.strip()
                #         if v:
                #             parts.append(v)
                #     values.extend(parts)
                result.setdefault(key,[]).append(value)
            else:
                print(f"Error: row[{row_index}]")
                sys.exit()
            row_index+=1
    return result

if(__name__=="__main__"):
    target_file=(r"C:\Users\acer\Downloads\1000單 - 工作表1.csv").strip().strip('"').strip("'")
    abc(target_file)