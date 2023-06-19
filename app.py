import math
from flask import Flask,render_template
app = Flask(__name__)
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

urlist=[]
with open("Qdata\Qindex.txt","r",encoding="utf-8") as f:
    urlist=[x.strip() for x in f.readlines()]
titlist=[]
with open("Qdata\index.txt","r",encoding="utf-8") as f:
    titlist=[x.strip() for x in f.readlines()]

def load_dic():
    dic={}
    with open("tfidfkey.txt","r",encoding="utf-8") as f:
        dic_term=f.readlines()
    with open("tfidfvalue.txt","r",encoding="utf-8") as f:
        dic_value=f.readlines()
    
    for (key,value) in zip(dic_term,dic_value):
        dic[key.strip()]=int(value.strip())
    return dic

dic=load_dic()


def load_doc():
    doc=[]
    with open("document.txt","r",encoding="utf-8") as f:
        doc=f.readlines()
    doc = [docs.strip().split(' ') for docs in doc]
    return doc

doc=load_doc()


def load_inverted():
    inverted_index={}
    with open("tfidfinvertedindex.txt","r",encoding="utf-8") as f:
        inverted_index_term=f.readlines()
    for i in range(0,len(inverted_index_term),2):
        key=inverted_index_term[i].strip()
        value=inverted_index_term[i+1].strip().split()
        inverted_index[key]=value
    return inverted_index


inverted_index=load_inverted()


def get_tf_value(term):
    term_value={}
    if term in inverted_index:
        for i in inverted_index[term]:
            if i not in term_value:
                term_value[i]=1
            else:
                term_value[i]+=1
    for i in term_value:
        term_value[i]/=(len(doc[int(i)]))
    return term_value


def get_idf_value(term):
    return math.log(len(dic)/dic[term])

def calculate_sorted_order_of_documents(query_term):
    potential_document={}
    for term in query_term:
        if term not in dic:
            continue
        tf_value=get_tf_value(term)
        idf_value=get_idf_value(term)
        for i in tf_value:
            if i not in potential_document:
                potential_document[i]=tf_value[i]*idf_value
            else:
                potential_document[i]+=tf_value[i]*idf_value
    if len(potential_document)==0:
        return potential_document
    for document in potential_document:
        potential_document[document]/=len(query_term)
    potential_document=dict(sorted(potential_document.items(),key=lambda item:item[1],reverse=True))
    keylist=[]
    poturl={}

    for i in potential_document:
        keylist.append(i)
        # print("Documents :",i,potential_document[i])

    for i in range(0,min(len(keylist),50)):
        # print("Documents :",keylist[i],urlist[int(keylist[i])])
        poturl[titlist[int(keylist[i])]]=(urlist[int(keylist[i])])
    return poturl


# query=input("Enter your query: ")
# query_term=[word.lower() for word in query.strip().split()]
# potentail_url=calculate_sorted_order_of_documents(query_term)

app.config['SECRET_KEY']='your_secret_key'
class SearchForm(FlaskForm):
    search=StringField('Enter Your Search term')
    submit=SubmitField('Search')

@app.route('/',methods=['GET','POST'])
def home():
    form=SearchForm()
    results=[]
    if form.validate_on_submit():
        query=form.search.data
        query_term=[word.lower() for word in query.strip().split()]
        results=calculate_sorted_order_of_documents(query_term)
        if (len(results)==0):
            print("No result found! Try using other reference term.")
        # elif (len(results)>20):
        #     results=results[:15:]
    return render_template('index.html',form=form,results=results)
