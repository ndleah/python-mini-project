import pandas as pd
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from surprise import SVD
from surprise import Dataset
from surprise import Reader
import streamlit as st
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
st.set_page_config(page_title='Retail Recommendation System',layout='wide')
st.header("Recommendation System")
st.text("")
st.subheader("Data")
df = pd.read_excel('/Users/aameerkhan/Downloads/OnlineRetail.xlsx')
st.write(df)
st.text("")
df.dropna(inplace=True)
df = df.loc[df['Quantity'] > 0]
st.subheader("Countries and items available")
st.table(df.value_counts('Country'))
df1 = df['Description']
duplicates = df1.duplicated()
st.write("Number of duplicates:", duplicates.sum())
duplicated_rows = df1[duplicates]
most_common_duplicates = duplicated_rows.value_counts().head(10)
st.text("")
st.subheader("Most popular items Globally:")
for item, count in most_common_duplicates.iteritems():
    st.write(f"{item}: {count}\n")
most_popular_items = df.groupby(['Country'])['Description'].sum().sort_values(ascending=False).reset_index()
st.text("")
st.subheader("Most popular items - Country wise")
st.write(most_popular_items.head(25))
sns.set_style('whitegrid')
plt.figure(figsize=(6, 4))
ax=sns.histplot(x=duplicated_rows, alpha=0.8, color='b')
ax.set(xlabel='Item Description', ylabel='Count', title='Most Popular Items Globally')

st.pyplot(plt) 
st.text("")
  
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])


df['date_new'] = df.InvoiceDate.dt.strftime('%Y-%m')
top_items_monthly = []
for month in df.date_new.unique():
    trans_month = df.loc[df.date_new == month]
    trans_month = (trans_month.groupby(['InvoiceNo', 'Description'])['Quantity']
                  .sum().unstack().reset_index().fillna(0)
                  .set_index('InvoiceNo'))

trans_month[trans_month >= 1] = True
trans_month[trans_month.isna()] = False 
import warnings
warnings.filterwarnings('ignore')
frequent_itemsets = apriori(trans_month, min_support=0.03,use_colnames=True)
associationRules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

top_k = associationRules.sort_values(by=['support'],ascending=False).iloc[:10][['antecedents','support']].reset_index(drop=True)

top_items_monthly.append((month, top_k))
pivot_dfs = []
for i, montly_pairs in enumerate(top_items_monthly):
    month, data = montly_pairs
    inv_map = {k: v for k, v in enumerate(data.antecedents)}
    rows = []
    for index, row in df.loc[(df.date_new == month)].iterrows():
        keys = [inv_map[k] for tup in str(row['Description']).split(',') for k,v in inv_map.items() if str(row['Description']) in list(v)]
        for key in keys:
            rows.append([month, key])
    pivot_df = pd.DataFrame(rows, columns=['month','Item'])
    pivot_df.head()
    pivot_dfs.append(pivot_df.pivot_table(values=["Item"],index=["month"],aggfunc="count",fill_value=0))
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df.set_index('InvoiceDate', inplace=True)

monthly_df = df.groupby(pd.Grouper(freq='M'))['Description'].value_counts()

repeated_products = monthly_df[monthly_df > 1]

for month, counts in repeated_products.groupby(level=0):
    st.write(f"Month: {month.strftime('%B %Y')}")
    st.write(counts)

df1 = df[['CustomerID', 'Description','StockCode', 'Quantity']]
ratings_matrix = df1.pivot_table(index=['CustomerID'], columns=['StockCode'], values='Quantity', fill_value=0)
algo = SVD()
reader = Reader(rating_scale=(1, 5))
surprise_data = Dataset.load_from_df(df1[['CustomerID', 'StockCode', 'Quantity']], reader)

trainset = surprise_data.build_full_trainset()
testset = trainset.build_anti_testset()
algo.fit(trainset)
predictions = algo.test(testset)

top_n = {}
for uid, iid, true_r, est, _ in predictions:
    if uid not in top_n.keys():
        top_n[uid] = [(iid, est)]
    else:
        top_n[uid].append((iid, est))

df1.dropna(subset=["StockCode", "Description"], inplace=True)

descriptions = df1.groupby("StockCode").first()["Description"]


desc_dict = descriptions.to_dict()
global_top_n = {}

for uid, user_ratings in top_n.items():
    user_ratings.sort(key=lambda x: x[1], reverse=True)
    global_top_n[uid] = []
    for iid, est_rating in user_ratings[:5]:
        if iid in desc_dict:
            global_top_n[uid].append((iid, desc_dict[iid]))

all_items = [iid for uid in global_top_n for iid, desc in global_top_n[uid]]
item_counts = {iid: all_items.count(iid) for iid in set(all_items)}

st.subheader("Most Recommended Items (in number of recommendations):")
for item, count in sorted(item_counts.items(), key=lambda x: x[1], reverse=True):
    if item in desc_dict:
        desc = desc_dict[item]
        st.write("\t", "Item ID:", item, "(\"" + str(desc) + "\")", f"recommended {count} times") 
