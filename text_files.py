#Made by: Mathew Dusome
#Add file work with lists
def strings_write(string_list,file_name):
    with open(file_name, 'w') as f:
        f.writelines("\n".join(string_list))
    
def int_write(int_list,file_name): 
    with open(file_name, 'w') as f:
        for i in int_list:
            f.write(f"{i}\n")
            
def strings_read(file_name):
    with open(file_name, 'r') as f:
        return f.read().splitlines() 
    
def int_read(file_name):
    temp2=[]
    with open(file_name, 'r') as f:
        temp = f.read().splitlines()
        for i in temp:
            temp2.append(int(i))
    return temp2
