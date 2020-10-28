import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from pandastable import Table
from tkinter import *
import tkinter.messagebox as messagebox
import warnings
warnings.filterwarnings("ignore")

data=pd.read_csv('ratings.csv')
#data.head(10)
Movie_genre=pd.read_csv('moviesData.csv')
#Movie_genre.head(10)
data=data.merge(Movie_genre,on='MovieID',how='left')
#data.head(10)
Average_ratings=pd.DataFrame(data.groupby('MovieTitle')['Rating'].mean())
#Average_ratings.head(10)
Average_ratings['Total_rating']=pd.DataFrame(data.groupby('MovieTitle')['Rating'].count())
#Average_ratings.head(10)
MovieUser=data.pivot_table(index='UserID',columns='MovieTitle',values='Rating')
#MovieUser.head(10)

window=tk.Tk()
window.title('Movie Recommendation')
window.geometry('600x600')


df=pd.read_csv('movies.csv')
df.sort_values('MovieTitle',inplace=True)
val=[]
val=df['MovieTitle'].values.tolist()


def selectedFunction():
    l2.configure(text=ComboGrp1.get())
    v=l2.cget('text')
    correlations=MovieUser.corrwith(MovieUser[v])#compute pairwise correlation between rows and columns.
    #print(correlations.head(20))
    recommendation=pd.DataFrame(correlations,columns=['CORRELATION'])
    recommendation.dropna(inplace=True)
    recommendation=recommendation.join(Average_ratings['Total_rating'])
    #print(recommendation.head(10))
    rec=recommendation[recommendation['Total_rating']>100].sort_values('CORRELATION',ascending=False).reset_index()
    rec=rec.merge(Movie_genre,on='MovieTitle',how='left')
    rc=rec.head()

    frame=tk.Frame(window)
    frame.grid()
    
    pt=Table(frame,dataframe=rc,showstatusbar=True)
    #pt.model.df=rec.head()
    pt.show()
    #print(rec.head(10))

l1=ttk.Label(window,text='select movie name').grid(column=0,row=0)

v=tk.StringVar()
ComboGrp1=ttk.Combobox(window,width=70,textvariable=v)
ComboGrp1.grid(column=0,row=1)
ComboGrp1['values']=(val)
#ComboGrp1.current(0)


btn1=ttk.Button(window,text='submit',command=selectedFunction)
btn1.grid(column=0,row=2)
l2=ttk.Label(window)
l2.grid(column=0,row=3)



#correlations=MovieUser.corrwith(MovieUser[l2])#compute pairwise correlation between rows and columns.
#correlations.head(10)

window.mainloop()

