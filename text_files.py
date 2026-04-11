#Made by: Mathew Dusome
#File utilities for reading and writing lists to text files
#
#IMPORT:
#    import objects.text_files as text_files
#
#EXAMPLE 1: Write strings to file
#    names = ["Alice", "Bob", "Charlie"]
#    text_files.strings_write(names, "names.txt")
#
#EXAMPLE 2: Read strings from file
#    names = text_files.strings_read("names.txt")
#    print(names)  # Output: ['Alice', 'Bob', 'Charlie']
#
#EXAMPLE 3: Write integers to file
#    scores = [100, 85, 92, 78]
#    text_files.int_write(scores, "scores.txt")
#
#EXAMPLE 4: Read integers from file
#    scores = text_files.int_read("scores.txt")
#    print(scores)  # Output: [100, 85, 92, 78]
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
