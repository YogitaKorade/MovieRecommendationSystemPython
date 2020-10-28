import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pandastable import Table
import tkinter.messagebox as messagebox
import warnings
warnings.filterwarnings('ignore')

data=pd.read_csv('movie_metadata.csv')
#print(data.head())

#filling null vales for columns we want
data['actor_2_name']=data['actor_2_name'].replace(np.nan,'unlnown')
data['actor_3_name']=data['actor_3_name'].replace(np.nan,'unknown')
data['actor_1_name']=data['actor_1_name'].replace(np.nan,'unlnown')
data['director_name']=data['director_name'].replace(np.nan,'unknown')

window=tk.Tk()
window.title('Movie Recommendation')
window.geometry('600x600')

data.sort_values('movie_title',inplace=True)
val=[]
val=data['movie_title'].values.tolist()

#replace | with whitespace
data['genres']=data['genres'].str.replace('|',' ')
#print(data['genres'].head())

#removing special charector at the end
data['movie_title']=data['movie_title'].str[:-1]
#print(data['movie_title'].head)

#combining data into new col "comb_feature"
data['comb_feature']=data['actor_2_name']+' '+data['actor_1_name']+' '+data['actor_3_name']+' '+data['genres']+' '+data['director_name']
#print(data['comb_feature'].head())
 
def selectedFunction():
    l2.configure(text=ComboGrp1.get())
    v=l2.cget('text')
    v=v.strip()
    cv=CountVectorizer()
    count_matrix=cv.fit_transform(data['comb_feature'])
    #print(count_matrix)

    sim=cosine_similarity(count_matrix)    
    i=data.loc[data['movie_title']==v].index[0]
   
    lst=list(enumerate(sim[i]))
    lst=sorted(lst,key=lambda x:x[1],reverse=True)
    #print(lst[1:13])
    l=[]
    for i in range(0,11):
        a=lst[i][0]
        l.append(data['movie_title'][a])
        
    dff=pd.DataFrame(l)

    frame=tk.Frame(window)
    frame.grid()
    
    pt=Table(frame,dataframe=dff,showstatusbar=True)
    pt.show()

#=============================================================
l1=ttk.Label(window,text='select mavie name').grid(column=0,row=0) 

v=tk.StringVar()
ComboGrp1=ttk.Combobox(window,width=70,textvariable=v)
ComboGrp1.grid(column=0,row=1)
 ComboGrp1['values']=(val)

btn1=ttk.Button(window,text='submit',command=selectedFunction)
btn1.grid(column=0,row=2)
l2=ttk.Label(window)
l2.grid(column=0,row=3)

window.mainloop()
