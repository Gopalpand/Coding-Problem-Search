import os

vocab=[]
document=[]
dic={}
inverted_index = {}

with open("Qdata/index.txt","r",encoding="utf-8",errors="replace") as f:
    p=f.readlines()
    for i,lines in enumerate(p):
        terms=[word.lower() for word in lines.strip().split()[1:]]
        folder_path="Qdata/data"
        file_name=str(i+1)
        file_path=os.path.join(folder_path,file_name,file_name+".txt")
        with open(file_path,"r",encoding="utf-8",errors="replace") as fl:
            par=fl.read()
            par=par.split("Example")[0]
            terms+=[word.lower().strip() for word in par.strip().split()]
        document.append(terms)

for i in document:
    i=list(set(i))
    for j  in i:
        if j not in dic:
            dic[j]=1
        else:
            dic[j]+=1

with open("tfidfkey.txt","w",encoding="utf-8") as f:
    for i in dic:
        f.write("%s\n"%i)
    
with open("tfidfvalue.txt","w",encoding="utf-8") as f:
    for i in dic:
        f.write("%s\n"%dic[i])

with open("document.txt", "w",encoding="utf-8") as f:
    for sublist in document:
        f.write("%s\n" % ' '.join(sublist))

with open("tfidfkey.txt", "r",encoding="utf-8") as f:
    for i in f:
        x = []
        for j in range(len(document)):
            if i.strip() in document[j]:
                x.append(str(j))
        if len(x) > 0:
            inverted_index[i.strip()] = x

with open("tfidfinvertedindex.txt", "w",encoding="utf-8") as f:
    for key in inverted_index:
        f.write("%s\n"%key)
        f.write("%s\n"%' '.join(inverted_index[key]))
