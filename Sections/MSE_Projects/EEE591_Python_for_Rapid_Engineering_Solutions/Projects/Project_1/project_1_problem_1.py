#!/usr/bin/env python
# coding: utf-8

# In[1]:


##########################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - Project 1: project_1_problem_1.py
# Mark Khusid
##########################################################################################

##########################################################################################
# Problem 1 
##########################################################################################


# ## Problem 1

# ### Import Libraries

# In[2]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# ### Read Database

# In[3]:


heart = pd.read_csv("heart1.csv")


# ## Exploratory Data Analysis on Database

# ### Find Number of Rows with Missing Data

# In[4]:


print("Shape:", heart.shape)
print("\nMissing values:")
print(heart.isnull().sum())


# In[5]:


#heart.head()
print(heart.head())


# In[6]:


#print(heart.info())


# ### Descriptive Statistics Table of All Features

# In[7]:


print("\nDescriptive statistics:")
heart.describe()
#print(heart.describe())


# ### Create Boxplot of Every Variable

# In[8]:


fig, axes = plt.subplots(4, 4, figsize=(16, 8))
axes = axes.flatten()

for i, col in enumerate(heart.columns):
    heart.boxplot(column=col, ax=axes[i])
    axes[i].set_title(col)
    axes[i].grid(True)

# Hide unused subplots
for i in range(len(heart.columns), len(axes)):
    axes[i].set_visible(False)

plt.suptitle(
    "Box Plots of Heart Disease Dataset Variables",
    fontsize=18
)

plt.tight_layout()
plt.show()


# ## Create Correlation Matrices

# In[9]:


# Correlation matrix
corr = heart.corr()
print("\nCorrelation matrix:")
#corr
print(corr)


# ### Create Correlation Matrix Heatmap

# In[10]:


# Create heatmap
plt.figure(figsize=(24,8))
sns.heatmap(
    corr,
    annot=True,        # display correlation values
    cmap='coolwarm',   # red-blue color map
    center=0,          # white at zero correlation
    fmt='.3f',
    square=True
)

plt.title('Heart Disease Correlation Matrix')
plt.tight_layout()
plt.show()


# ### Show Highest Correlation Features to Target Label

# In[11]:


corr_target = corr[['a1p2']].sort_values(by='a1p2', ascending=False)
print(corr_target)


# ### Create Features to Target Correlation Heatmap

# In[12]:


plt.figure(figsize=(4,8))
sns.heatmap(
    corr_target,
    annot=True,
    cmap='coolwarm',
    center=0,
    vmin=-1,
    vmax=1
)

plt.title('Correlation with Heart Disease (a1p2)')
plt.tight_layout()
plt.show()


# In[13]:


print("\nCorrelation with heart disease variable a1p2:")
#print(corr["a1p2"].sort_values(key=lambda x: x.abs(), ascending=False))
#print(corr["a1p2"].sort_values(key=lambda x: x, ascending=False))
corr["a1p2"].sort_values(key=lambda x: x, ascending=False)


# ### Show Top Feature Pairwise Correlations

# #### Method 1

# In[14]:


# Top pairwise correlations, excluding duplicate/self correlations
abs_corr = corr.abs()
upper = abs_corr.where(np.triu(np.ones(abs_corr.shape), k=1).astype(bool))
top_corr = upper.stack().sort_values(ascending=False)


# In[15]:


print("\nMost highly correlated variable pairs:")
print(top_corr.head(10))


# #### Method 2

# In[16]:


print(corr.values.shape)


# In[17]:


print(*corr.values.shape)


# In[18]:


corr_2 = corr * np.tri(*corr.values.shape, k=-1).T
print(corr_2)


# In[19]:


corr_2_abs = corr_2.abs()
print(corr_2_abs)


# In[20]:


corr_2_unstack = corr_2_abs.unstack()
print(corr_2_unstack)


# In[21]:


type(corr_2_unstack)


# In[22]:


corr_2_unstack.sort_values(inplace=True, ascending=False)
top_corr_2 = corr_2_unstack.head(15)
print(top_corr_2)


# ### Create Top 10 Pairwise Correlations Heatmap

# In[23]:


# Top 10 correlations
top10 = top_corr.head(10)

# Convert to dataframe
top_df = pd.DataFrame(
    top10.values,
    index=[f"{a} vs {b}" for a,b in top10.index],
    columns=["Correlation"]
)

plt.figure(figsize=(8,6))

sns.heatmap(
    top_df,
    annot=True,
    cmap="Reds",
    fmt=".3f"
)

plt.title("Top 10 Pairwise Correlations")
plt.tight_layout()
plt.show()


# In[24]:


# Top 10 correlations
top10_2 = top_corr_2.head(10)

# Convert to dataframe
top_2_df = pd.DataFrame(
    top10_2.values,
    index=[f"{a} vs {b}" for a,b in top10_2.index],
    columns=["Correlation"]
)

plt.figure(figsize=(8,6))

sns.heatmap(
    top_2_df,
    annot=True,
    cmap="Reds",
    fmt=".3f"
)

plt.title("Top 10 Pairwise Correlations")
plt.tight_layout()
plt.show()


# ## Create Cross - Covariance Matrices

# In[25]:


# Cross-covariance matrix
cov = heart.cov()
print("\nCross-covariance matrix:")
print(cov)
#cov


# ### Create Cross - Covariance Heatmap

# In[26]:


# Plot heatmap
plt.figure(figsize=(12,10))

sns.heatmap(
    cov,
    annot=True,
    fmt=".1f",
    cmap="viridis"
)

plt.title("Cross-Covariance Matrix")
plt.tight_layout()
plt.show()


# ### Extract Top Pairwise Cross - Covariances Between Features

# #### Method 1

# In[27]:


cov = heart.cov().abs()
print(cov)


# In[28]:


upper = cov.where(
    np.triu(np.ones(cov.shape), k=1).astype(bool)
)

top_cov = (
    upper.stack()
         .sort_values(ascending=False)
)
print("Top Cross - Covariances")
print(top_cov.head(20))


# #### Method 2

# In[29]:


print(cov.values.shape)


# In[30]:


cov_2 = cov * np.tri(*cov.values.shape, k=-1).T
print(cov_2)
#cov_2


# In[31]:


cov_2_unstack = cov_2.unstack()
print(cov_2_unstack)


# In[32]:


cov_2_unstack_sorted = cov_2_unstack.sort_values(ascending=False)
print("Top Cross - Covariances")
print(cov_2_unstack_sorted.head(10))


# ### Create Heatmap of Features with High Covariances

# In[33]:


threshold = 50     # choose after inspecting values

mask = np.abs(cov) < threshold

plt.figure(figsize=(20,10))

sns.heatmap(
    cov,
    mask=mask,
    annot=True,
    cmap='coolwarm',
    fmt=".3f",
    center=0
)

plt.title(
    'Strong Cross-Covariances Among Heart Disease Variables'
)

plt.show()


# ### Extract Top Cross - Covariances of Features to Label

# In[34]:


print("\nCovariance with heart disease variable a1p2:")
print(cov["a1p2"].sort_values(key=lambda x: x.abs(), ascending=False))


# ### Create Heatmap of Cross - Covariance of Features with Label

# In[35]:


# extract covariance with heart disease
cov_a1p2 = cov[["a1p2"]]

# sort by magnitude
cov_a1p2 = cov_a1p2.reindex(
    cov_a1p2["a1p2"].abs().sort_values(ascending=False).index
)

plt.figure(figsize=(4,8))

sns.heatmap(
    cov_a1p2,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    linewidths=0.5
)

plt.title(
    "Cross-Covariance with Heart Disease (a1p2)",
    fontsize=14
)

plt.tight_layout()
plt.show()


# ## Create Pair Plot

# In[36]:


print("Generating Pair Plot (please be patient...)")


# In[37]:


# Pair plot
sns.set(style="whitegrid", context="notebook")
g = sns.pairplot(
    heart, 
    hue="a1p2", 
    height=1.5,
    palette=['navy', 'darkorange']
)

g.fig.suptitle(
    'Pairwise Relationships Among Heart Disease Risk Factors',
    fontsize=18,
    y=1.02
)
plt.show()

