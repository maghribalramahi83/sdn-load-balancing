"""
Copyright (c) 2026
Maghrib Abidalreda Maky Alrammahi
Email: maghrib.alramahi@uokufa.edu.iq

This code is part of the SVNMLQ-LC research project and was prepared solely by
Maghrib Abidalreda Maky Alrammahi.

Any use of this code, in whole or in part, in research, academic publication,
software development, reproduction, or derivative work should acknowledge the
author by citing the published ML-QTLB paper and referencing the official
project GitHub repository.

Official GitHub repository:
https://github.com/maghribalramahi83/sdn-load-balancing
""" 

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


# Load the dataset
dataset = pd.read_csv('E:\\Dataset MinMaxScaler with label.csv') # My dataset content to 9 columns and 4183 rows
#print((dataset))
# split the dataset into features (X) and class labels (y)
X = dataset.iloc[:, :-1].values  # all columns except the last one
y = dataset.iloc[:, -1].values   # last column only


# Split the dataset into training, validation, and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train an SVM classifier on the training set
clf = SVC(C=1,kernel = 'rbf',max_iter=100,gamma='auto')
clf.fit(X_train, y_train)
# Predict the class labels for the test data
y_pred = clf.predict(X_test)

val_size = 0.38  # fraction of training set size to use for validation set
val_samples = int(val_size * X_train.shape[0])
X_val, y_val = X_train[:val_samples], y_train[:val_samples]
val_acc = clf.score(X_val, y_val)



from sklearn.metrics import confusion_matrix
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
# Calculate the confusion matrix and other metrics for the binary classification
cm = confusion_matrix(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

print('Confusion matrix:\n', cm)
print('Precision:', precision * 100, "%")
print('Recall:', recall * 100, "%")
print('F1 score:', f1 * 100, "%") 
print("Accuracy: ", accuracy* 100, "%")

import seaborn as sns
import matplotlib.pyplot as plt
fig = plt.figure(dpi=300)
# Making the Confusion Matrix in polt
sns.heatmap(cm, annot=True, fmt='d', center=True)
plt.title('Confusion_Matrix of Support Vector Machines (SVM)', fontsize=12, fontweight='bold')
plt.show()

# Evaluate the model on the training set
train_acc = clf.score(X_train, y_train)
print("Training accuracy:", train_acc * 100, "%")

# Evaluate the model on the validation set
val_acc = clf.score(X_val, y_val)
print("Validation accuracy:", val_acc * 100, "%")

# Evaluate the model on the test set
test_acc = clf.score(X_test, y_test)
print("Test accuracy:", test_acc * 100, "%")


  # Check for underfitting, overfitting, or normal performance
if val_acc > train_acc and val_acc > test_acc:
    print("The model is underfitting")
elif val_acc > train_acc and val_acc <= test_acc:
    print("The model is performing normally")
elif train_acc > val_acc and test_acc > val_acc:
    print('The model is overfitting to the training data.')
elif train_acc > val_acc and train_acc > test_acc:
    print("The model is overfitting to the training data")
else:
    print('The model may have some other issue.')
    
    
#---------------------------------------رسم   
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
# Define the values to plot
values = [precision, recall, f1, accuracy]
labels = ['Precision', 'Recall', 'F1 score', 'Accuracy']

# Create a vertical bar plot
fig = plt.figure(dpi=300)
plt.bar(labels, values,width=0.3)
plt.ylim([0, 1.1])
plt.yticks(([0, 0.25 , 0.5, 0.75, 1]),fontsize=10, fontweight='bold')
# Set the y-axis tick format to display values as percentages %
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
plt.xticks((['Precision', 'Recall', 'F1 score', 'Accuracy']),fontsize=10, fontweight='bold')
# Set the title and axis labels
plt.title('Evaluation Metrics of SVM', fontsize=12, fontweight='bold')
plt.xlabel('Metric', fontsize=12, fontweight='bold')
plt.ylabel('Value', fontsize=12, fontweight='bold')

bars = plt.bar(labels, values, color='blue',width=0.3)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, '{:.0%}'.format(height), ha='center', va='bottom', fontsize=10, fontweight='bold')

# Display the plot
plt.show()
#-------------------------------------------------------------------
# طريقه اخرى للاستدعاء قيم X and y
# X = dataset.iloc[:,0:8] # 0:8 means select columns 0 to 7 (i.e., the first 8 columns).
# y = dataset.iloc[:, 8]# Means select  9th column
#------------------------------------------------------------------
# طريقه اخرى لحساب Training accuracy
# Evaluate the classifier's accuracy on the training set
#y_train_pred = classifier.predict(x_train)
#train_accuracy = np.mean(y_train_pred == y_train)
#print("Training Accuracy:", train_accuracy * 100, "%")
#-----------------------------------------------------------------
# طريقه اخرى لحساب Test accuracy  
#(y_pred = clf.predict(X_test))
#accuracy = np.mean(y_pred == y_test)
#print("Accuracy:", accuracy*100,'%')
#-------------------------------------------------------------------