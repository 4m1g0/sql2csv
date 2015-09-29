#! /usr/bin/python3

import sys
import re

MAX_BYTES = 524288 # max bytes stored in memory befor writting to disk (512KB)
MAX_MEMORY = 1073741824 # max memory stored before crash (1GB)

def main(argv):
    if len(argv) < 1:
        print("Error. Usage: sql2csv <filename>")
        sys.exit(2)
    try:
        f = open(argv[0], 'r', encoding='utf-8')
    except:
        print ("Error. file '" + argv[0] + "' doesn't exist")
        sys.exit(3)
    
    currentRow = ''
    currentFile = None
    comillas = False
    inRow = False
    while True:
        char = f.read(1)
        #print(char)
        #input()
        if char == '':
            break
        
        if comillas:
            if char == "'":
                comillas = False
            currentRow += char
            continue
        
        if char == "'":
            comillas = True
            currentRow += char
            continue
        
        if char == "(":
            table = getTableName(currentRow)
            if table:
                currentFile = open(table + '.csv', 'a')
            inRow = True
            currentRow = ""
            continue
            
        if char == ")":
            currentFile.write(currentRow + '\n')
            currentRow = ""
            inRow = False
            
        
        currentRow += char
        if len(currentRow) > MAX_BYTES:
            if inRow:
                currentFile.write(currentRow)
                currentRow = ''
            elif len(currentRow) > MAX_MEMORY:
                raise Exception('Max memory reached parsing text between rows')
                
    #fin while
#fin main
            
def getTableName(text):
    text = text.lower()
    m = re.search('insert into ([^\s]*)', text)
    if m:
        return m.group(1)
    return None
    

if __name__ == "__main__":
   main(sys.argv[1:])
