import sys

def find(target):
    with  open(target,'r',newline='') as f:
        prev=f.readline().split('/')[0]
        counter = 0
        line = "This is first line"
        while line:
            if prev == line.split('/')[0]:
                counter+=1
            else:
                if counter > 0:
                    with open('result.txt','a',newline='') as resultfile:
                        resultfile.write(str(counter+1)+" : "+prev+"\n")
                    counter = 0
                prev=line.split('/')[0];
            line=f.readline()

if __name__ == '__main__':
    find(sys.argv[1])
