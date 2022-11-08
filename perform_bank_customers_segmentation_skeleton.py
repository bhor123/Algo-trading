# -*- coding: utf-8 -*-
"""Perform Bank Customers Segmentation - Skeleton.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TueMubb6Kp8PYmgQvN8Ioein8_HphyfX

# TASK #1: UNDERSTAND THE PROBLEM STATEMENT AND BUSINESS CASE

<table>
  <tr><td>
    <img src="https://drive.google.com/uc?id=1OjWCpwRHlCSNYaJoUUd2QGryT9CoQJ5e"
         alt="Fashion MNIST sprite"  width="1000">
  </td></tr>
  <tr><td align="center">
    <b>Figure 1. Customers Segmentation
  </td></tr>
</table>

![alt text](https://drive.google.com/uc?id=1Q43AkxxDy4g-zl5lIX4_PBJtTguh4Ise)

![alt text](https://drive.google.com/uc?id=1uS6vsccMt3koetsp3k9cAIfbpJw7Z1J8)

![alt text](https://drive.google.com/uc?id=1r1FjdO8duujUoI904Oy4vbza6KktxSXo)

![alt text](https://drive.google.com/uc?id=1vMr3ouoZ6Pc1mba1mBm2eovlJ3tfE6JA)

![alt text](https://drive.google.com/uc?id=1VvqzWWY8wFGeP4cl-rVtWVOg1P6saHfZ)

![alt text](https://drive.google.com/uc?id=1LpdL0-4E9lbc4s-x6eJ5zkyIVw_OpHuJ)

Data Source: https://www.kaggle.com/arjunbhasin2013/ccdata

# TASK #2: IMPORT LIBRARIES AND DATASETS
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# You will need to mount your drive using the following commands:
# For more information regarding mounting, please check this out: https://stackoverflow.com/questions/46986398/import-data-into-google-colaboratory

from google.colab import drive
drive.mount('/content/drive')

# You have to include the full link to the csv file containing your dataset


creditcard_df = pd.read_csv('/content/drive/MyDrive/udemy - Python+Finance/udemy-FinanceAutomation/Part 3. AI and ML in Finance/4. Marketing_data.csv')




# CUSTID: Identification of Credit Card holder 
# BALANCE: Balance amount left in customer's account to make purchases
# BALANCE_FREQUENCY: How frequently the Balance is updated, score between 0 and 1 (1 = frequently updated, 0 = not frequently updated)
# PURCHASES: Amount of purchases made from account
# ONEOFFPURCHASES: Maximum purchase amount done in one-go
# INSTALLMENTS_PURCHASES: Amount of purchase done in installment
# CASH_ADVANCE: Cash in advance given by the user
# PURCHASES_FREQUENCY: How frequently the Purchases are being made, score between 0 and 1 (1 = frequently purchased, 0 = not frequently purchased)
# ONEOFF_PURCHASES_FREQUENCY: How frequently Purchases are happening in one-go (1 = frequently purchased, 0 = not frequently purchased)
# PURCHASES_INSTALLMENTS_FREQUENCY: How frequently purchases in installments are being done (1 = frequently done, 0 = not frequently done)
# CASH_ADVANCE_FREQUENCY: How frequently the cash in advance being paid
# CASH_ADVANCE_TRX: Number of Transactions made with "Cash in Advance"
# PURCHASES_TRX: Number of purchase transactions made
# CREDIT_LIMIT: Limit of Credit Card for user
# PAYMENTS: Amount of Payment done by user
# MINIMUM_PAYMENTS: Minimum amount of payments made by user  
# PRC_FULL_PAYMENT: Percent of full payment paid by user
# TENURE: Tenure of credit card service for user

creditcard_df

creditcard_df.info()
creditcard_df.describe()

# Mean balance is $1564 
# Balance frequency is frequently updated on average ~0.9
# Purchases average is $1000
# one off purchase average is ~$600
# Average purchases frequency is around 0.5
# average ONEOFF_PURCHASES_FREQUENCY, PURCHASES_INSTALLMENTS_FREQUENCY, and CASH_ADVANCE_FREQUENCY are generally low
# Average credit limit ~ 4500
# Percent of full payment is 15%
# Average tenure is 11 years

# Let's see who made one off purchase of $40761!
creditcard_df[creditcard_df['ONEOFF_PURCHASES']==40761.25]



creditcard_df['CASH_ADVANCE'].max()

# Let's see who made cash advance of $47137!
# This customer made 123 cash advance transactions!!
# Never paid credit card in full
creditcard_df[creditcard_df['CASH_ADVANCE']==creditcard_df['CASH_ADVANCE'].max()]

"""# TASK #3: VISUALIZE AND EXPLORE DATASET"""

# Let's see if we have any missing data, luckily we don't!
sns.heatmap(creditcard_df.isna(), yticklabels=False,cmap="Blues", cbar_kws={'label': 'Missing Data'})

#sns.heatmap(creditcard_df.isna(), yticklabels=False, cbar=False, cmap="Blues") This is what the sir has used

creditcard_df.isna().sum()

# Fill up the missing elements with mean of the 'MINIMUM_PAYMENT' 
creditcard_df.loc[creditcard_df['MINIMUM_PAYMENTS'].isna()==True, 'MINIMUM_PAYMENTS']=creditcard_df['MINIMUM_PAYMENTS'].mean()

creditcard_df.isna().sum()

# Fill up the missing elements with mean of the 'CREDIT_LIMIT'
creditcard_df.loc[creditcard_df['CREDIT_LIMIT'].isna()==True, 'CREDIT_LIMIT']=creditcard_df['CREDIT_LIMIT'].mean()

creditcard_df.isna().sum()

sns.heatmap(creditcard_df.isna(), yticklabels=False,cmap="Blues", cbar_kws={'label': 'Missing Data'})

# Let's see if we have duplicated entries in the data
creditcard_df.duplicated().sum()

# Let's drop Customer ID since it has no meaning here 
creditcard_df.drop(columns=['CUST_ID'], axis=1, inplace=True)

creditcard_df.head()

len(creditcard_df.columns)

creditcard_df.columns

creditcard_df.columns[2]

plt.figure(figsize=(10,50))

for i in range(len(creditcard_df.columns)):
  plt.subplot(17, 1, i+1)
  sns.distplot(creditcard_df[creditcard_df.columns[i]], hist_kws={'color':'g'}, kde_kws={'color':'b', 'lw':3, 'label':'KDE'})
  plt.title(creditcard_df.columns[i])

plt.tight_layout()

# distplot combines the matplotlib.hist function with seaborn kdeplot()
# KDE Plot represents the Kernel Density Estimate
# KDE is used for visualizing the Probability Density of a continuous variable. 
# KDE demonstrates the probability density at different values in a continuous variable. 

# Mean of balance is $1500
# 'Balance_Frequency' for most customers is updated frequently ~1
# For 'PURCHASES_FREQUENCY', there are two distinct group of customers
# For 'ONEOFF_PURCHASES_FREQUENCY' and 'PURCHASES_INSTALLMENT_FREQUENCY' most users don't do one off puchases or installment purchases frequently 
# Very small number of customers pay their balance in full 'PRC_FULL_PAYMENT'~0
# Credit limit average is around $4500
# Most customers are ~11 years tenure

correlations = creditcard_df.corr()

plt.subplots(figsize=(20,20))
sns.heatmap(correlations, annot=True)



# sns.pairplot(creditcard_df)
# Correlation between 'PURCHASES' and ONEOFF_PURCHASES & INSTALMENT_PURCHASES 
# Trend between 'PURCHASES' and 'CREDIT_LIMIT' & 'PAYMENTS'



# 'PURCHASES' have high correlation between one-off purchases, 'installment purchases, purchase transactions, credit limit and payments. 
# Strong Positive Correlation between 'PURCHASES_FREQUENCY' and 'PURCHASES_INSTALLMENT_FREQUENCY'

"""# TASK #4: UNDERSTAND THE THEORY AND INTUITON BEHIND K-MEANS

![alt text](https://drive.google.com/uc?id=1EBCmP06GuRjVfPgTfH85Yhv9xIAZUj-K)

![alt text](https://drive.google.com/uc?id=1EYWyoec9Be9pYkOaJTjPooTPWgRlJ_Xz)

![alt text](https://drive.google.com/uc?id=1ppL-slQPatrmHbPBEaT3-8xNH01ckoNE)

![alt text](https://drive.google.com/uc?id=1Yfi-dpWW3keU5RLgwAT4YmQ2rfY1GxUh)

![alt text](https://drive.google.com/uc?id=1bLRDIZRda0NSTAdcbugasIjDjvgw4JIU)

![alt text](https://drive.google.com/uc?id=1rBQziDU0pS1Fz0m8VQRjQuBoGFSX1Spb)

![alt text](https://drive.google.com/uc?id=1BOX2q8R_8E4Icb4v1tpn1eymCTJY2b5o)

![alt text](https://drive.google.com/uc?id=1v7hJEPiigSeTTaYo0djbO-L4uEnTpcAU)

# TASK #5: FIND THE OPTIMAL NUMBER OF CLUSTERS USING ELBOW METHOD
"""

# Let's scale the data first
scaler = StandardScaler()
creditcard_scaled_df = scaler.fit_transform(creditcard_df)

creditcard_scaled_df.shape

#inertia_ of the kmeans holds the WCSS values for a particular model

scores_1 = []

for i in range(1,20):
  kmeans = KMeans(n_clusters=i)
  kmeans.fit(creditcard_scaled_df)
  scores_1.append(kmeans.inertia_)

plt.plot(scores_1, 'bx-')
plt.title('Applying elbow method to find number of clusters')
plt.xlabel('Clusters')
plt.ylabel('WCSS')
plt.show()







# From this we can observe that, 4th cluster seems to be forming the elbow of the curve. 
# However, the values does not reduce linearly until 8th cluster. 
# Let's choose the number of clusters to be 7.

"""# TASK #6: APPLY K-MEANS METHOD"""

#We have selected 8 clusters as the optimal number of clusters for our model
kmeans = KMeans(8)
kmeans.fit(creditcard_scaled_df)
labels = kmeans.labels_

labels

kmeans.cluster_centers_.shape

cluster_centers = pd.DataFrame(data=kmeans.cluster_centers_, columns=[creditcard_df.columns])

cluster_centers

# In order to understand what these numbers mean, let's perform inverse transformation
cluster_centers = scaler.inverse_transform(cluster_centers)
cluster_centers = pd.DataFrame(data=cluster_centers, columns=[creditcard_df.columns])
cluster_centers

# First Customers cluster (Transactors): Those are customers who pay least amount of intrerest charges and careful with their money, Cluster with lowest balance ($104) and cash advance ($303), Percentage of full payment = 23%
# Second customers cluster (revolvers) who use credit card as a loan (most lucrative sector): highest balance ($5000) and cash advance (~$5000), low purchase frequency, high cash advance frequency (0.5), high cash advance transactions (16) and low percentage of full payment (3%)
# Third customer cluster (VIP/Prime): high credit limit $16K and highest percentage of full payment, target for increase credit limit and increase spending habits
# Fourth customer cluster (low tenure): these are customers with low tenure (7 years), low balance

#I think the labels is used to segrated the different entries into different clusters
labels.min()

pd.DataFrame(data=labels)

creditcard_cluster_df = pd.concat([creditcard_df, pd.DataFrame(data={'cluster': labels})], axis=1)

creditcard_cluster_df

for i in creditcard_df.columns[:]:
  plt.figure(figsize=(35,5))  
  for j in range(8):
    plt.subplot(1,8,j+1)
    clusters_df = creditcard_cluster_df[creditcard_cluster_df['cluster']==j]
    clusters_df[i].hist(bins=20)
    plt.title('{} \nCluster {}'.format(i,j))
  plt.show()





# concatenate the clusters labels to our original dataframe

# Plot the histogram of various clusters

"""# TASK 7: APPLY PRINCIPAL COMPONENT ANALYSIS AND VISUALIZE THE RESULTS

![alt text](https://drive.google.com/uc?id=1xDuvEnbuNqIjX5Zng39TCfGCf-BBDGf0)
"""

# For dimensionality reduction and data visualisation
# PCA better if we have some correlation
#I personally think the autoencoders are better than PCA

# Obtain the principal components 
pca = PCA(n_components=2)
PCA_df = pca.fit_transform(creditcard_scaled_df)
PCA_df

# Create a dataframe with the two components
PCA_df = pd.DataFrame(data=PCA_df, columns=['PCA1', 'PCA2'])

# Concatenate the clusters labels to the dataframe
PCA_cluster_df = pd.concat([PCA_df, pd.DataFrame(data=labels, columns=['Cluster'])], axis=1)

plt.figure(figsize=(10,10))
sns.scatterplot(x='PCA1', y='PCA2', data=PCA_cluster_df, hue='Cluster', palette=['red', 'green', 'blue', 'pink', 'violet', 'yellow', 'orange', 'black'])

"""# TASK #8: UNDERSTAND THE THEORY AND INTUITION BEHIND AUTOENCODERS

![alt text](https://drive.google.com/uc?id=1g0tWKogvKaCrtsfzjApi6m8yGD3boy4x)

![alt text](https://drive.google.com/uc?id=1AcyUL_F9zAD2--Hmyq9yTkcA9mC6-bwg)

![alt text](https://drive.google.com/uc?id=1xk1D5uldId0DWywRJ3-OAVBcIr5NGCq_)

# TASK #9: TRAIN AUTOENCODERS (PERFORM DIMENSIONALITY REDUCTION USING AUTOENCODERS)
"""

#Autoenconders works best if the input data has some correlations 
#It performs poorly if the input data has no correlation at all 
#Tied weights => WEights from the input layer to the hidden layer will be equal to the weights from hidden layer to output => W = W(T)

from tensorflow.keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.optimizers import SGD

input_df = Input(shape=(17,))

x = Dense(7, activation='relu')(input_df)
x = Dense(500, activation='relu')(x)
x = Dense(500, activation='relu')(x)
x = Dense(2000, activation='relu')(x)

encoded = Dense(10, activation='relu')(x)   #This is the bottleneck that we have created within the network, this is the output from the encoded network 


x = Dense(2000, activation='relu')(encoded)
x = Dense(500, activation='relu')(x)


decoded = Dense(17)(x)

#Developing the Autoencoder over here 
autoencoder = Model(input_df, decoded)

#Developing the encoder here (THIS IS THE FIRST HALP OF THE SLIDE ABOVE, viz ONLY ENCODING WILL BE DONE OVER HERE)
encoder = Model(input_df, encoded)

autoencoder.compile(optimizer='adam', loss='mse')

creditcard_scaled_df.shape

autoencoder.fit(creditcard_scaled_df, creditcard_scaled_df, batch_size=128, epochs=25, verbose=1)

autoencoder.summary()









"""# TASK #10: APPLY AUTOENCODERS (PERFORM DIMENSIONALITY REDUCTION USING AUTOENCODERS)"""

pred = encoder.predict(creditcard_scaled_df)
pred.shape

pred

#WE had applied the dimensionality reduction, we went fro m 17 features down to 10 features

"""Now we have the pred, this will be treated as creditcard_scaled_df and 
1. we will be applying the inverse_transform to get the original dataframe but with reduced number of components. (I don't think this is possible with the scaler variable as it was working on 17 columns, where as now we have only 10 columns
2. Then finding the optimal number of clusters required 
3. Then applying the kmeans
4. Finally applying the PCA

"""



creditcard_encoded_df = pd.DataFrame(data=pred, columns=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'])
creditcard_encoded_df

"""PART1 => Finding optimal number of clusters required"""

scores_2 = []

for i in range(1,20):
  kmeans = KMeans(n_clusters=i)
  kmeans.fit(pred)
  scores_2.append(kmeans.inertia_)

plt.plot(scores_2, 'bx-')
plt.title('Applying elbow method to find number of clusters')
plt.xlabel('Clusters')
plt.ylabel('WCSS')
plt.show()

plt.plot(scores_1, 'rx-')
plt.plot(scores_2, 'bx-')

"""It seems as if 4 is the optimal number of clusters (Sir used it) for the pred input 
*I dont know why, the error term for the scores_2 is significantly less than scores_1. Sir had it huge, i have it low*

It is my personal preference to have 8 customer segments 
"""







"""Applying Kmeans on the pred """

kmeans = KMeans(4)
kmeans.fit_transform(pred)
labels = kmeans.labels_
cluster_centers_df = kmeans.cluster_centers_

cluster_centers_df #Ignore this

pd.DataFrame(data=cluster_centers_df, columns=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']) #Ignore this

creditcard_encoded_cluster_df = pd.concat([creditcard_df, pd.DataFrame(data=labels, columns=['cluster'])], axis=1)

creditcard_encoded_cluster_df.head()

#Ignore this entirely 
for i in creditcard_encoded_df.columns[:]:
  plt.figure(figsize=(35,5))  
  for j in range(8):
    plt.subplot(1,8,j+1)
    clusters_df = creditcard_encoded_cluster_df[creditcard_encoded_cluster_df['cluster']==j]
    clusters_df[i].hist(bins=20)
    plt.title('{} \nCluster {}'.format(i,j))
  plt.show()









"""Now we will be applying the PCA on the final creditcard_encoded_df"""

pca_encoded = PCA(n_components=2)
PCA_encoded_df = pca_encoded.fit_transform(pred)
PCA_encoded_df

PCA_encoded_df = pd.DataFrame(data=PCA_encoded_df, columns=['PCA1', 'PCA2'])

PCA_encoded_df

PCA_encoded_cluster_df = pd.concat([PCA_encoded_df, pd.DataFrame(data=labels, columns=['Cluster'])], axis=1)

PCA_encoded_cluster_df

plt.figure(figsize=(10,10))
sns.scatterplot(x='PCA1', y='PCA2', data=PCA_encoded_cluster_df, hue='Cluster', palette=['red', 'green', 'blue', 'pink'])

"""#And with that we are done, notice how the data is much more classified on applying encoder-decoder along with PCA insted of only applying *PCA*"""









"""# EXCELLENT JOB! YOU SHOULD BE PROUD OF YOUR NEWLY ACQUIRED SKILLS"""