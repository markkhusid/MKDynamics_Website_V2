#!/usr/bin/env python
# coding: utf-8

# In[1]:


##########################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - Project 1: project_1_problem_2.py
# Mark Khusid
##########################################################################################

##########################################################################################
# Problem 2 
##########################################################################################


# ## Problem 2

# ### Import Machine Learning Libraries

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import Perceptron
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score


# ### Read Database

# In[3]:


# Read data
heart = pd.read_csv("heart1.csv")


# ### Create Accuracy Results Dictionary

# In[4]:


accuracy_results_dict = {}


# ### Separate Features and Labels in Arrays

# In[5]:


X = heart.iloc[:, :-1]
y = heart.iloc[:, -1]


# In[6]:


#print(heart.shape)


# In[7]:


#print(X.shape)


# In[8]:


#print(y.shape)


# In[9]:


#print(X[:5])


# In[10]:


#print(y[:5])


# ### Train / Test Split

# In[11]:


# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.30,
    random_state=0,
    stratify=y
)


# In[12]:


#print(X_train[:5])


# In[13]:


#print(y_train[:5])


# In[14]:


#print(X_test[:5])


# In[15]:


#print(y_test[:5])


# ### Scale the Training Data

# In[16]:


# Standardize for algorithms that need it
sc = StandardScaler()

X_train_std = sc.fit_transform(X_train)
X_test_std = sc.transform(X_test)


# In[17]:


#print(X_train_std[:2])


# In[18]:


#print(X_test_std[:2])


# ## Perceptron

# In[19]:


# Perceptron
ppn = Perceptron(
    max_iter=100,
    eta0=0.0001,
    tol=1e-6,
    #fit_intercept=True,
    random_state=0,
    verbose=False
)


# In[20]:


ppn.fit(X_train_std, y_train);


# In[21]:


y_pred = ppn.predict(X_test_std)


# In[22]:


#print(y_pred[0:10])


# In[23]:


#print(y_test.iloc[0:10].values)


# ### Get Accuracy

# In[24]:


print("Perceptron Results:")


# In[25]:


preceptron_train_acc = accuracy_score(y_train, ppn.predict(X_train_std))
#print(f"Perceptron training accuracy = {preceptron_train_acc:.3f}")


# In[26]:


perceptron_acc = accuracy_score(y_test, y_pred)
#print(f"Perceptron testing accuracy = {perceptron_acc:.3f}")


# In[27]:


# Note that this only counts the samples where the predicted value was wrong
#print(f'Misclassified: {(y_test != y_pred).sum():.0f} out of {len(y_test):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {perceptron_acc:.3f}')


# In[28]:


print(f"    Accuracy: {perceptron_acc:.3f}")


# In[29]:


accuracy_results_dict.update(
    {
        "Perceptron": perceptron_acc
    })


# In[30]:


#print(accuracy_results_dict)


# ### Get Combined Accuracy

# In[31]:


X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined = np.hstack((y_train, y_test))
#print('Number in combined ',len(y_combined))


# In[32]:


y_combined_pred = ppn.predict(X_combined_std)


# In[33]:


#print(y_combined_pred[0:10])


# In[34]:


#print(y_combined[0:10])


# In[35]:


perceptron_combined_acc = accuracy_score(y_combined, y_combined_pred)
#print(f"Perceptron combined data training accuracy = {perceptron_combined_acc:.3f}")


# In[36]:


# Note that this only counts the samples where the predicted value was wrong
#print(f'Misclassified: {(y_combined != y_combined_pred).sum():.0f} out of {len(y_combined):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {perceptron_combined_acc:.3f}')


# In[37]:


print(f"    Combined: {perceptron_combined_acc:.3f}")
print()


# In[38]:


accuracy_results_dict.update(
    {
        "Perceptron_combined": perceptron_combined_acc
    })


# In[39]:


#print(accuracy_results_dict)


# ## Logistic Regression

# In[40]:


#from inspect import signature

#print(signature(LogisticRegression))


# In[41]:


# Logistic Regression
LR_accuracy_list = []
c_vals = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
#for c_val in c_vals:
#    lr = LogisticRegression(
#        C            = c_val,
#        solver       = "liblinear",
#        max_iter     = 1000,
#        random_state = 0
#    )

#    lr.fit(X_train_std, y_train)

#    acc = accuracy_score(y_test, lr.predict(X_test_std))

#    LR_accuracy_list.append(acc)


# In[42]:


#print(LR_accuracy_list)


# In[43]:


#LR_accuracy_max = max(LR_accuracy_list)
#print(LR_accuracy_max)


# In[44]:


#LR_accuracy_max_index = np.argmax(np.array(LR_accuracy_list))
#print(LR_accuracy_max_index)


# In[45]:


# Best accuracy with index 1
LR_accuracy_max_index = 1


# In[46]:


lr_used = \
    LogisticRegression(
        C            = c_vals[LR_accuracy_max_index],
        solver       = "liblinear",
        max_iter     = 1000,
        random_state = 0
    )

lr_used.fit(X_train_std, y_train);


# In[47]:


y_pred = lr_used.predict(X_test_std)


# In[48]:


#print(y_pred[0:10])


# In[49]:


#print(y_test.iloc[0:10].values)


# ### Get Accuracy

# In[50]:


print("Logistic Regression Results:")


# In[51]:


lr_train_acc = accuracy_score(y_train, lr_used.predict(X_train_std))
#print(f"Logistic Regression training accuracy = {lr_train_acc:.3f}")


# In[52]:


lr_acc = accuracy_score(y_test, y_pred)
#print(f"Logistic Regression testing accuracy = {lr_acc:.3f}")


# In[53]:


#print(f'Misclassified: {(y_test != y_pred).sum():.0f} out of {len(y_test):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {lr_acc:.3f}')


# In[54]:


print(f"    Accuracy: {lr_acc:.3f}")


# In[55]:


accuracy_results_dict.update(
    {
        "LR": lr_acc
    })


# In[56]:


#print(accuracy_results_dict)


# ### Get Combined Accuracy

# In[57]:


lr_combined_used = \
    LogisticRegression(
        C            = c_vals[LR_accuracy_max_index],
        solver       = "liblinear",
        max_iter     = 1000,
        random_state = 0
    )

lr_combined_used.fit(X_combined_std, y_combined);


# In[58]:


y_combined_pred = lr_combined_used.predict(X_combined_std)


# In[59]:


#print(y_combined_pred[0:10])


# In[60]:


#print(y_combined[0:10])


# In[61]:


lr_combined_acc = accuracy_score(y_combined, y_combined_pred)
#print(f"Logistic Regression combined data testing accuracy = {lr_combined_acc:.3f}")


# In[62]:


#print(f'Misclassified: {(y_combined != y_combined_pred).sum():.0f} out of {len(y_combined):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {lr_combined_acc:.3f}')


# In[63]:


print(f"    Combined Accuracy: {lr_combined_acc:.3f}")
print()


# In[64]:


accuracy_results_dict.update(
    {
        "LR_combined": lr_combined_acc
    })


# In[65]:


#print(accuracy_results_dict)


# ## Support Vector Machine

# In[66]:


#from inspect import signature

#print(signature(SVC))


# In[67]:


#SVM_accuracy_list = []
#degree_vals = list(range(0,7))

#for degree in degree_vals:
#    svm = SVC(
#        C            = 0.01,
#        degree       = degree,
#        kernel       = "linear",
#        max_iter     = -1,
#        random_state = 0
#    )

#    svm.fit(X_train_std, y_train)

#    acc = accuracy_score(y_test, svm.predict(X_test_std))

#    SVM_accuracy_list.append(acc)


# In[68]:


#print(SVM_accuracy_list)


# In[69]:


SVM_accuracy_list = []
c_vals = [0.001, 0.01, 0.1, 1, 10, 100, 1000]

#for c_val in c_vals:
#    svm = SVC(
#        C            = c_val,
#        kernel       = "linear",
#        max_iter     = -1,
#        random_state = 0
#    )

#    svm.fit(X_train_std, y_train)

#    acc = accuracy_score(y_test, svm.predict(X_test_std))

#    SVM_accuracy_list.append(acc)


# In[70]:


#print(SVM_accuracy_list)


# In[71]:


#SVM_accuracy_max = max(SVM_accuracy_list)
#print(SVM_accuracy_max)


# In[72]:


#SVM_accuracy_max_index = np.argmax(np.array(SVM_accuracy_list))
#print(SVM_accuracy_max_index)


# In[73]:


# Best accuracy index = 1
SVM_accuracy_max_index = 1


# In[74]:


SVM_used = \
    SVC(
        C            = c_vals[SVM_accuracy_max_index],
        kernel       = "linear",
        max_iter     = -1,
        random_state = 0,
        verbose      = False
    )

SVM_used.fit(X_train_std, y_train);


# In[75]:


y_pred = SVM_used.predict(X_test_std)


# In[76]:


#print(y_pred[0:10])


# In[77]:


#print(y_test.iloc[0:10].values)


# ### Get Accuracy

# In[78]:


print("Support Vector Machine Results:")


# In[79]:


SVM_train_acc = accuracy_score(y_train, SVM_used.predict(X_train_std))
#print(f"SVM training accuracy = {SVM_train_acc:.3f}")


# In[80]:


SVM_acc = accuracy_score(y_test, y_pred)
#print(f"SVM testing accuracy = {SVM_acc:.3f}")


# In[81]:


#print(f'Misclassified: {(y_test != y_pred).sum():.0f} out of {len(y_test):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {SVM_acc:.3f}')


# In[82]:


print(f"    Accuracy: {SVM_acc:.3f}")


# In[83]:


accuracy_results_dict.update(
    {
        "SVM": SVM_acc
    })


# In[84]:


#print(accuracy_results_dict)


# ### Get Combined Accuracy

# In[85]:


SVM_combined_used = \
    SVC(
        C            = c_vals[SVM_accuracy_max_index],
        kernel       = "linear",
        max_iter     = -1,
        random_state = 0,
        verbose      = False
    )

SVM_combined_used.fit(X_combined_std, y_combined);


# In[86]:


y_combined_pred = SVM_combined_used.predict(X_combined_std)


# In[87]:


#print(y_combined_pred[0:10])


# In[88]:


#print(y_combined[0:10])


# In[89]:


SVM_combined_acc = accuracy_score(y_combined, y_combined_pred)
#print(f"SVM combined data testing accuracy = {SVM_combined_acc:.3f}")


# In[90]:


#print(f'Misclassified: {(y_combined != y_combined_pred).sum():.0f} out of {len(y_combined):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {SVM_combined_acc:.3f}')


# In[91]:


print(f"    Combined Accuracy: {SVM_combined_acc:.3f}")
print()


# In[92]:


accuracy_results_dict.update(
    {
        "SVM_combined": SVM_combined_acc
    })


# In[93]:


#print(accuracy_results_dict)


# ## Decision Tree

# In[94]:


#from inspect import signature

#print(signature(DecisionTreeClassifier))


# In[95]:


#print(list(range(1,11)))


# In[96]:


#DTree_accuracy_list = []
#depth_vals = list(range(1,11))

#for depth in depth_vals:
#    tree = DecisionTreeClassifier(
#        criterion       = 'entropy',
#        max_depth       = depth,
#        random_state    = 0
#    )

#    tree.fit(X_train_std, y_train)

#    acc = accuracy_score(y_test, tree.predict(X_test_std))

#    DTree_accuracy_list.append(acc)


# In[97]:


#print(DTree_accuracy_list)


# In[98]:


DTree_accuracy_list = []
depth_vals = list(range(1,11))

#for depth in depth_vals:
#    tree = DecisionTreeClassifier(
#        criterion       = 'gini',
#        max_depth       = depth,
#        random_state    = 0
#    )

#    tree.fit(X_train_std, y_train)

#    acc = accuracy_score(y_test, tree.predict(X_test_std))

#    DTree_accuracy_list.append(acc)


# In[99]:


#print(DTree_accuracy_list)


# In[100]:


#DTree_accuracy_max = max(DTree_accuracy_list)
#print(DTree_accuracy_max)


# In[101]:


#DTree_accuracy_max_index = np.argmax(np.array(DTree_accuracy_list))
#print(DTree_accuracy_max_index)


# In[102]:


# Best accuracy index = 2
DTree_accuracy_max_index = 2


# In[103]:


DTree_used = \
    DecisionTreeClassifier(
        criterion       = 'gini',
        max_depth       = depth_vals[DTree_accuracy_max_index],
        random_state    = 0
    )

DTree_used.fit(X_train_std, y_train);


# In[104]:


y_pred = DTree_used.predict(X_test_std)


# In[105]:


#print(y_pred[0:10])


# In[106]:


#print(y_test.iloc[0:10].values)


# ### Get Accuracy

# In[107]:


print("Decision Tree Results:")


# In[108]:


DTree_train_acc = accuracy_score(y_train, DTree_used.predict(X_train_std))
#print(f"Decision Tree training accuracy = {DTree_train_acc:.3f}")


# In[109]:


DTree_acc = accuracy_score(y_test, y_pred)
#print(f"Decision Tree testing accuracy = {DTree_acc:.3f}")


# In[110]:


#print(f'Misclassified: {(y_test != y_pred).sum():.0f} out of {len(y_test):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {DTree_acc:.3f}')


# In[111]:


print(f"    Accuracy: {DTree_acc:.3f}")


# In[112]:


accuracy_results_dict.update(
    {
        "DTree": DTree_acc
    })


# In[113]:


#print(accuracy_results_dict)


# ### Get Combined Accuracy

# In[114]:


DTree_combined_used = \
    DecisionTreeClassifier(
        criterion       = 'gini',
        max_depth       = depth_vals[DTree_accuracy_max_index],
        random_state    = 0
    )

DTree_combined_used.fit(X_combined_std, y_combined);


# In[115]:


y_combined_pred = DTree_combined_used.predict(X_combined_std)


# In[116]:


#print(y_combined_pred[0:10])


# In[117]:


#print(y_combined[0:10])


# In[118]:


DTree_combined_acc = accuracy_score(y_combined, y_combined_pred)
#print(f"Decision Tree combined data testing accuracy = {DTree_combined_acc:.3f}")


# In[119]:


#print(f'Misclassified: {(y_combined != y_combined_pred).sum():.0f} out of {len(y_combined):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {DTree_combined_acc:.3f}')


# In[120]:


print(f"    Combined Accuracy: {DTree_combined_acc:.3f}")
print()


# In[121]:


accuracy_results_dict.update(
    {
        "DTree_combined": DTree_combined_acc
    })


# In[122]:


#print(accuracy_results_dict)


# ## Random Forest

# In[123]:


#from inspect import signature

#print(signature(RandomForestClassifier))


# In[124]:


RForest_accuracy_list = []
num_tree_vals = [1, 5, 11, 51, 101, 501, 1001]

#for num_trees in num_tree_vals:
#    forest = RandomForestClassifier(
#        criterion       = 'entropy',
#        n_estimators    = num_trees,
#        random_state    = 0,
#        n_jobs          = 8
#    )

#    forest.fit(X_train_std, y_train)

#    acc = accuracy_score(y_test, forest.predict(X_test_std))

#    RForest_accuracy_list.append(acc)


# In[125]:


#print(RForest_accuracy_list)


# In[126]:


#RForest_accuracy_max = max(RForest_accuracy_list)
#print(RForest_accuracy_max)


# In[127]:


#RForest_accuracy_max_index = np.argmax(np.array(RForest_accuracy_list))
#print(RForest_accuracy_max_index)


# In[128]:


# Best Accuracy Index = 3
RForest_accuracy_max_index = 3


# In[129]:


RForest_used = \
    RandomForestClassifier(
        criterion       = 'entropy',
        n_estimators    = num_tree_vals[RForest_accuracy_max_index],
        random_state    = 0,
        n_jobs          = 8
    )

RForest_used.fit(X_train_std, y_train);


# In[130]:


y_pred = RForest_used.predict(X_test_std)


# In[131]:


#print(y_pred[0:10])


# In[132]:


#print(y_test.iloc[0:10].values)


# ### Get Accuracy

# In[133]:


print("Random Forest Results:")


# In[134]:


RForest_train_acc = accuracy_score(y_train, RForest_used.predict(X_train_std))
#print(f"Random Forest training accuracy = {RForest_train_acc:.3f}")


# In[135]:


RForest_acc = accuracy_score(y_test, y_pred)
#print(f"Random Forest testing accuracy = {RForest_acc:.3f}")


# In[136]:


#print(f'Misclassified: {(y_test != y_pred).sum():.0f} out of {len(y_test):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {RForest_acc:.3f}')


# In[137]:


print(f"    Accuracy: {RForest_acc:.3f}")


# In[138]:


accuracy_results_dict.update(
    {
        "RForest": RForest_acc
    })


# In[139]:


#print(accuracy_results_dict)


# ### Get Combined Accuracy

# In[140]:


RForest_combined_used = \
    RandomForestClassifier(
        criterion       = 'entropy',
        n_estimators    = num_tree_vals[RForest_accuracy_max_index],
        random_state    = 0,
        n_jobs          = 8
    )

RForest_combined_used.fit(X_combined_std, y_combined);


# In[141]:


y_combined_pred = RForest_combined_used.predict(X_combined_std)


# In[142]:


#print(y_combined_pred[0:10])


# In[143]:


#print(y_combined[0:10])


# In[144]:


RForest_combined_acc = accuracy_score(y_combined, y_combined_pred)
#print(f"Random Forest combined data testing accuracy = {RForest_combined_acc:.3f}")


# In[145]:


#print(f'Misclassified: {(y_combined != y_combined_pred).sum():.0f} out of {len(y_combined):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {RForest_combined_acc:.3f}')


# In[146]:


print(f"    Combined Accuracy: {RForest_combined_acc:.3f}")
print()


# In[147]:


accuracy_results_dict.update(
    {
        "RForest_combined": RForest_combined_acc
    })


# In[148]:


#print(accuracy_results_dict)


# ## K - Nearest Neighbor (KNN)

# In[149]:


#from inspect import signature

#print(signature(KNeighborsClassifier))


# In[150]:


#print(list(range(1,51)))


# In[151]:


KNN_accuracy_list = []
k_vals = list(range(1,51))

#for k_val in k_vals:
#    knn = KNeighborsClassifier(
#        n_neighbors = k_val,
#        n_jobs = 8
#    )

#    knn.fit(X_train_std, y_train)

#    acc = accuracy_score(y_test, knn.predict(X_test_std))

#    KNN_accuracy_list.append(acc)


# In[152]:


#print(KNN_accuracy_list)


# In[153]:


#KNN_accuracy_max = max(KNN_accuracy_list)
#print(KNN_accuracy_max)


# In[154]:


#KNN_accuracy_max_index = np.argmax(np.array(KNN_accuracy_list))
#print(KNN_accuracy_max_index)


# In[155]:


#print(f"Maximum KNN accuracy achieved with K = {k_vals[KNN_accuracy_max_index]}")


# In[156]:


# Best Accuracy Index = 32
KNN_accuracy_max_index = 32


# In[157]:


KNN_used = \
    KNeighborsClassifier(
        n_neighbors = k_vals[KNN_accuracy_max_index],
        n_jobs = 8
    )

KNN_used.fit(X_train_std, y_train);


# In[158]:


y_pred = KNN_used.predict(X_test_std)


# In[159]:


#print(y_pred[0:10])


# In[160]:


#print(y_test.iloc[0:10].values)


# ### Get Accuracy

# In[161]:


print("K - Nearest Neighbor (KNN) Results:")


# In[162]:


KNN_train_acc = accuracy_score(y_train, KNN_used.predict(X_train_std))
#print(f"KNN training accuracy = {KNN_train_acc:.3f}")


# In[163]:


KNN_acc = accuracy_score(y_test, y_pred)
#print(f"KNN testing accuracy = {KNN_acc:.3f}")


# In[164]:


#print(f'Misclassified: {(y_test != y_pred).sum():.0f} out of {len(y_test):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {KNN_acc:.3f}')


# In[165]:


print(f"    Accuracy: {KNN_acc:.3f}")


# In[166]:


accuracy_results_dict.update(
    {
        "KNN": KNN_acc
    })


# In[167]:


#print(accuracy_results_dict)


# ### Get Combined Accuracy

# In[168]:


KNN_combined_used = \
    KNeighborsClassifier(
        n_neighbors = k_vals[KNN_accuracy_max_index],
        n_jobs = 8
    )

KNN_combined_used.fit(X_combined_std, y_combined);


# In[169]:


y_combined_pred = KNN_combined_used.predict(X_combined_std)


# In[170]:


#print(y_combined_pred[0:10])


# In[171]:


#print(y_combined[0:10])


# In[172]:


KNN_combined_acc = accuracy_score(y_combined, y_combined_pred)
#print(f"KNN combined data testing accuracy = {KNN_combined_acc:.3f}")


# In[173]:


#print(f'Misclassified: {(y_combined != y_combined_pred).sum():.0f} out of {len(y_combined):.0f} samples.')  # how'd we do?
#print(f'Accuracy: {KNN_combined_acc:.3f}')


# In[174]:


print(f"    Combined Accuracy: {KNN_combined_acc:.3f}")
print()


# In[175]:


accuracy_results_dict.update(
    {
        "KNN_combined": KNN_combined_acc
    })


# In[176]:


#print(accuracy_results_dict)


# ## Create Accuracy Results Dataframe

# In[177]:


df_accuracy_results = \
    pd.DataFrame(
        accuracy_results_dict.items(),
        columns = ['Algorithm', 'Accuracy']
    )
#print(df_accuracy_results)


# In[178]:


df_accuracy_results = df_accuracy_results.sort_values(
    by="Accuracy",
    ascending=False
)


# In[179]:


#print(df_accuracy_results)


# In[180]:


df_accuracy_results = df_accuracy_results.sort_values(
    by="Accuracy",
    ascending=False
)

ax = df_accuracy_results.plot.bar(
    x="Algorithm",
    y="Accuracy",
    figsize=(12,8),
    title="Algorithms Tried and Their Accuracies"
)

for container in ax.containers:
    ax.bar_label(
        container,
        fmt='%.3f',      # 3 digits after decimal
        padding=3
    )

plt.tight_layout()
plt.show()

