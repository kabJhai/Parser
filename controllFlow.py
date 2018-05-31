import os.path
import sys
global functionName
global pathArray
global currentChecked
pathArray = []
checked = []
currentChecked = False
def constructName(line,k,l):
        functionName = ""
        while(k<l):
                functionName += line[k]
                k+=1
        return functionName
def returnFunctionName(line):
        k = line.find(" ")
        l = line.find("(")
        m = line.find(")")
        if((m >=0) and(line.find(";"))>=0):
            functionName = constructName(line,k,line.find(";"))
        else:
            functionName = constructName(line,k,l)
        if(functionName == ""):
                k = line.find("}")+1
                l = line.find("{")
                functionName = constructName(line,k,l)
        return functionName
    
def determinePath(paths):
        branchingStatements = ["while","for","if"]
        subPath = []
        openCurlyBraces = 0
        i = 0
        while(i<(len(paths))):
            if(paths[i].find("{")>=0):
                openCurlyBraces += 1
            elif(paths[i].find("}")>=0):
                openCurlyBraces -= 1
            if(paths[i].find("while")>=0):
                    k = 0
                    currentChecked = False
                    while(k<len(checked)):
                        if(paths[i] == checked[k]):
                            currentChecked = True
                        k+=1
                    if(currentChecked):
                        i = paths[i].index(len(subPath)-1)
                        continue
                    subPath.append(paths[i])
                    if(paths[i].find("{")>=0):
                        openCurlyBraces += 1
                        index = i + 1
                        while((paths[index].find("}")<0)):
                            subPath.append(paths[index])
                            index+=1
                    elif(paths[i+1].find("{")>=0):
                        openCurlyBraces += 1
                        index = i+2
                        while((paths[index].find("}")<0)):
                            subPath.append(paths[index])
                            index+=1
                    checked.append(paths[i])
            elif(paths[i].find(" if")>=0):
                    k = 0
                    currentChecked = False
                    while(k<len(checked)):
                        if(paths[i] == checked[k]):
                            currentChecked = True
                        k+=1
                    if(currentChecked):
                        i = paths[i].index(len(subPath)-1)
                        continue
                    subPath.append(paths[i])
                    if(paths[i].find("{")>=0):
                        openCurlyBraces += 1
                        index = i+1
                        while((paths[index].find("}")<0)):
                            subPath.append(paths[index])
                            index+=1
                    elif(paths[i+1].find("{")>=0):
                        openCurlyBraces += 1
                        index = i+2
                        while((paths[index].find("}")<0)):
                            subPath.append(paths[index])
                            index+=1
                    checked.append(paths[i])
            elif((paths[i].find("{")<0)and(paths[i].find("}")<0)and(paths[i].find("(")<0)):
                subPath.append(paths[i])
            i+=1
        print(subPath)
        print(checked)
        
def main():
        lines = []
        paths = list()
        branches = ["else","("]
        #file = input("Enter the source file: ").strip()
        file = "bigbang.c"
        if(os.path.isfile(file)):
            pass
        else:
            print(file+" doesnot exist")
            exit()
        fileData = open(file,"r")
        for line in fileData:
                #if(not(line.startswith("#"))):
                lines.append(line)
        i = 0
        while(i<len(lines)):
                #print("Here")
                branchIndex = 0 #To iterate the branch array
                while(branchIndex<len(branches)):
                        if((lines[i].find(branches[branchIndex]))>= 0):
                                #print(lines[i])
                                if(((lines[i].find("}"))>=0)and(lines[i][lines[i].find("else")-1] == "}")):
                                    paths.append(str(i+1)+"}")
                                paths.append(str(i+1)+" "+returnFunctionName(lines[i]).strip())
                        branchIndex+=1
                if((lines[i].find("{"))>=0):
                    paths.append(str(i+1)+"{")
                elif((lines[i].find("}"))>=0):
                    paths.append(str(i+1)+"}")
                i+=1
        determinePath(paths) 
main()
