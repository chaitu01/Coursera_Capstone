#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import lxml.html as lh
import pandas as pd
url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
col=[]
i=0
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    if len(T)!=3:
        break
    i=0
    for t in T.iterchildren():
        data=t.text_content() 
        if i>0:
            try:
                data=int(data)
            except:
                pass
        col[i][1].append(data)
        i+=1


# In[2]:


Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)


# In[4]:


df.columns = ['Borough', 'Neighbourhood','Postcode']

cols = df.columns.tolist()
cols

cols = cols[-1:] + cols[:-1]

df = df[cols]
df = df.replace('\n',' ', regex=True)
df.drop(df.index[df['Borough'] == 'Not assigned'], inplace = True)
df = df.reset_index(drop=True)
df = df.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(','.join).reset_index()
df.columns = ['Postcode','Borough','Neighbourhood']


# In[7]:


df['Neighbourhood'] = df['Neighbourhood'].str.strip()
df.loc[df['Neighbourhood'] == 'Not assigned', 'Neighbourhood'] = df['Borough']
df[df['Borough'] == 'Queen\'s Park']
df.shape
df.to_csv(r'df_can.csv')

