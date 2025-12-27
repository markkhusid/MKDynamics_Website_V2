# Master's in Computer Science (Cybersecurity) - Portfolio Project

:::{note}
Minor modifications have been made to the original submitted report to correct typographical errors and for optimal presentation in Myst Markdown format.
:::

## Download the PDF
[Download](Mark_Khusid_Portfolio_Project.pdf)

## Portfolio Project Report: Summary

### CSE548: Advanced Computer Network Security

This summary presents the outcomes of four projects conducted within the scope of the CSE548 Advanced Network Security course, which emphasize the integration of network security principles with practical implementations and machine learning techniques. There were four individual projects in this course.

#### Project 1: Packet Filter Firewall: Implementation of an Iptables-Based Packet Filter Firewall

Project 1 is titled: Packet Filter Firewall: Implementation of an Iptables-Based Packet Filter Firewall.  The project involved setting up a firewall with rules ensuring controlled access and restricted communication between nodes in a simulated network.  To meet the requirements of this project, we set up an iptables firewall and a web server on a Gateway / Server virtual machine.  The iptables firewall was used to restrict network and internet access of the client as well as the  Gateway / Server as per the project requirements.  Verification of the Gateway / Server was performed and found to be in compliance.

#### Project 2: SDN-Based Stateless Firewall: Implementation of an SDN-Based Stateless Firewall

Project 2 is titled: SDN – Based Stateless Firewall.  The firewall resided on an Open Virtual Switch that implements the OpenFlow protocol.  A POX instance acts as the controller for the Open Virtual Switch.  Containers are instantiated using Mininet to create four containers.  Layer 2 and Layer 3 firewall rules are applied to the controller using a firewall application running the on application plane.  Various tests are performed in order to test the functionality of the firewall application.

#### Project 3: SDN-Based DoS Attacks and Mitigation Project

Project 3  is titled: SDN – Based DoS Attacks and Mitigation Project.  The purpose of this project is to learn about Software Defined Networking and implementing Denial of Service (DoS) attack mitigation.  In this project an Open Virtual Switch is created that operates on the OpenFlow protocol.  A POX instance acts as the controller for the Open Virtual Switch.  Containers are instantiated using Mininet to create four containers.  The L3 firewall application was modified to detect DoS attacks and permanently block the offending MAC address.  Various tests are performed in order to test the functionality of the firewall application.

#### Project 4: Machine Learning-Based Anomaly Detection

Project 4 is titled: Machine Learning – Based Anomaly Detection.  The purpose of this Project is to use machine learning to spot abnormal patterns in network traffic and identify potential attacks from hackers.  Training data for the machine learning models is provided by the Course Team.  Two distinct models are trained and tested against three different test sets.  Testing / validation accuracy and loss are determined, as well as construction of a confusion matrix for the three separate testing conditions.  An assessment is made to determine the model with the most testing accuracy, and then to figure out why that model fares better than others.  This determination involves examining the training data and testing data to notice any particular patterns in the categories and subcategories of attacks. 

### CSE572: Data Mining

This summary presents the outcomes of three projects conducted within the scope of the CSE572 Data Mining course.  The first project consisted of extracting glucose level time series data and its properties for a person using an artificial pancreas.  The second project consisted of training a machine model to assess whether the person has eaten a meal or not.  The third project consisted of clustering the glucose data to determine the amount of carbohydrates the person has consumed in each meal.

#### Project 1: Extracting Time Series Properties of Glucose Levels in Artificial Pancreas Project

Project 1 is titled:  Extracting Time Series Properties of Glucose Levels in Artificial Pancreas Project.  Data for this project was provided as two separated Comma Separated Value (CSV) files.  The first CSV file contained CGM sensor data, while the second contained insuling pump data.  Both the CGM sensor data and insulin pump data were in reversed chronological order, meaning the latest data were the first rows of the files.  Additionally, the data from the CGM sensor and insulin pump were taken asynchronously from each other; therefore, synchronization would have to be performed.  The CGM sensor and insulin pump data also had many columns that added unecessary dimensionality that needed to be reduced.  Finally, there were many missing data points and over fifty – five thousand rows of data.  An effective strategy was required for dealing with the missing data points and the sheer number of rows.

#### Project 2: Machine Model Training Project

Project 2 is titled:  Machine Model Training Project.  The goal of this project is to train a machine to differentiate between the person eating a meal versus not eating a meal given the person’s CGM sensor’s time series data.  As in Project 1, insulin pump and CGM sensor data were provided; however, for this project two sets of data were available.  The datasets had similar problems that occurred in Project 1; however, Project 2’s insulin pump datasets had the additional issue of non – uniform date and time recording.  This necessitated an additional step of pre – processing of the date and time columns within the datasets.  

#### Project 3: Cluster Validation Project

Project 3 is titled: Cluster Validation Project.  In this Project, the person’s carborhydrate input provided Insulin Pump dataset is separated into bins and an unsupervised clustering algorithm is used to cluster the data and compare it to the binned ground truth.  Using techniques similar to Projects 1 and 2, the Insulin Pump data and the CGM sensor data were extracted to find the carbohydrates ingested and blood glucose levels.  As in Project 2, the CGM sensor data was cleaned, missing data imputed, features extracted and normalized.  The data were then fed into a K-Means clustering machine and a DBSCAN machine.  The results from both machines were compared and contrasted.

## CSE548 Advanced Network Security: Portfolio Project Report

Abstract — This report presents the outcomes of four projects conducted within the scope of the CSE548 Advanced Network Security course, which emphasize the integration of network security principles with practical implementations and machine learning techniques. The projects include:

1. Packet Filter Firewall: Implementation of an iptables-based packet filter firewall with rules ensuring controlled access and restricted communication between nodes in a simulated network.
2. SDN-Based Stateless Firewall: Design and testing of a stateless firewall using Software Defined Networking (SDN) principles with OpenFlow and POX controller to implement Layer 2 and Layer 3 filtering.
3. SDN-Based DoS Mitigation: Identification and mitigation of Denial of Service (DoS) attacks in an SDN environment through dynamic blocking of malicious traffic using customized firewall logic.
4. Machine Learning for Anomaly Detection: Development of machine learning models to detect anomalies in network traffic using the NSL-KDD dataset, achieving significant precision and recall across multiple testing scenarios.

The report highlights technical implementations, analytical insights, and contributions in each project.  Observations and improvements in system designs are further discussed.

### Introduction
In this portfolio project report, we will be reviewing the results obtained from the four projects in this course.  The projects were:

1. Packet Filter Firewall (iptables) Project.  
2. SDN (Software Defined Network) – Based Stateless Firewall Project.
3. SDN (Software Defined Network) – Based DoS (Denial of Service) Attacks and Mitigation Project.
4. Machine Learning – Based Anomaly Detection Project.

In Project 1 (Packet Filter Firewall (iptables), the aim was to set up and configure a packet filter firewall, test network connectivity and ensuring the proper functioning of the firewall.  In Project 2 (SDN – Based Stateless Firewall), the aim was to delve into Software Defined Networking principles by implementing a firewall using OpenFlow [^myref_1] rules.  In Project 3 (SDN – Based DoS Attacks and Mitigation Project,  the aim was to understand, detect and mitigate DoS attacks in a SDN network environment.  Finally, in Project 4 (Machine Learning – Based Anomaly Detection), the aim was to use machine learning in identifying abnormal patterns in network traffic.  This included indications of potential threats such as intrusions or malware.

### Project Overviews, Setup and Descriptions

#### Project 1: Packet Filter Firewall (iptables) Project

In Project 1, we set up an iptables firewall on a Gateway / Server that follows conditions determined by the following requirements:
- A client can send pings to 8.8.8.8 though a Gateway / Server
    - A client can access a webpage residing on the Gateway / Server
    - A client can not access any IP addresses besides 8.8.8.8
    - The client can not ping the Gateway / Server
    - The server can not perform pings to localhost
    - The server can not perform pings to the client
    - The server can not perform pings to 8.8.8.8

The server provides Network Address Translation for the client so that packets from the client appear to come from the Gateway / Server.
	A diagram of the Lab Network Topology is shown in [](#CSE548_Fig_1):

```{figure} images/CSE548_Fig_1.png
:label: CSE548_Fig_1
Lab Network Topology
```

In [](#CSE548_Fig_1) Lab Network Topology, we have a client that is connected to the 10.0.2.0 network, and a Gateway/Server that is connected to both the 10.0.2.0 and 10.0.1.0 network.  The aim is to setup a firewall and routing provisions on the Gateway/Server to satisfy the requirements mentioned above.

To setup the Project, two virtual machines were created: one for the Client, the other for the Gateway/Server.  The Client’s virtual machine network setup is shown in [](#CSE548_Fig_2): Client Network Setup below:

```{figure} images/CSE548_Fig_2.png
:label: CSE548_Fig_2
Client Network Setup
```

The Gateway/Server’s network setup is shown in [](#CSE548_Fig_3): Gateway/Server Network Setup. We can see that the Gateway/Server’s network setup is multi – homed so that it can have a network port to both the 10.0.1.0 and 10.0.2.0 networks.  After the Virtual Machines were started, the Client’s network setup is verified by using the ifconfig Linux command.

```{figure} images/CSE548_Fig_3.png
:label: CSE548_Fig_3
Gateway/Server Network Setup
```

The output of the ifconfig Linux command is shown in [](#CSE548_Fig_4): Client's ifconfig Output below:

```{figure} images/CSE548_Fig_4.png
:label: CSE548_Fig_4
Client's *ifconfig* Output
```

As required, the Client’s *ifconfig* output has an IP address of 10.0.2.4.  However, for the Gateway/Server, its network port that is connected to the 10.0.2.0 network has an IP address of 10.0.2.6.  Pings from the client to the Gateway server over the 10.0.2.0 network operate as normal.  In order for the Client to be able to have access to the 10.0.1.0 network visible at the Gateway/Server’s other network port, a default gateway routing entry had to be added to the Client’s routing table.  This informs the the Client’s operating system of how to handle packets whose IP addresses are not on the local network.  The Client’s routing table is shown in [](#CSE548_Fig_5): Client's Routing Table below:

```{figure} images/CSE548_Fig_5.png
:label: CSE548_Fig_5
Client's Routing Table
```

In [](#CSE548_Fig_5): Client's Routing Table, we can see a entry for the default gateway whose IP address is 10.0.2.6.  The destination address for the default gateway routing table entry is 0.0.0.0, which means that any packet whose destination IP address is not on the local network (10.0.1.0) should be sent to the Gateway/Server.

The Gateway/Server was configured to be multi – homed, with two network interfaces.  The output of the ifconfig Linux command when executed on the Gateway/Server is shown in [](#CSE548_Fig_6): Gateway/Server's ifconfig Output.

```{figure} images/CSE548_Fig_6.png
:label: CSE548_Fig_6
Gateway/Server's *ifconfig* Output
```

As can be seen in [](#CSE548_Fig_6): Gateway/Server's ifconfig Output, the Gateway/Server is connected to both the 10.0.1.0 and 10.0.2.0 networks.
In order for the Gateway/Server to allow pings to the IP address 8.8.8.8, Network Address Translation (NAT) was implemented as shown in [](#CSE548_Fig_7): Gateway/Server's NAT Setup below:

```{figure} images/CSE548_Fig_7.png
:label: CSE548_Fig_7
Gateway/Server's NAT Setup
```

In [](#CSE548_Fig_7): Gateway/Server's NAT Setup, a Masquerade entry was added that allowed for network address translation for the reply pings coming back from the pinged IP address 8.8.8.8).  If this entry didn’t exist, then reply pings would never be received by the Client.
A simple web server was implemented on the Gateway/Server.  The web content for the server was the message “Welcome to Demo and Test!”.  This content was stored in an html file as shown in [](#CSE548_Fig_8): Gateway/Server's Web Content below:

```{figure} images/CSE548_Fig_8.png
:label: CSE548_Fig_8
Gateway/Server's Web Content
```

An Apache [^myref_2] webserver was started Gateway/Server.  The status of the webserver is shown in [](#CSE548_Fig_9): Apache Webserver's Status below:

```{figure} images/CSE548_Fig_9.png
:label: CSE548_Fig_9
Apache Webserver's Status
```

#### Project 2: SDN-Based Stateless Firewall

In Project 2, we setup a Software Defined Networking Stateless Firewall.  The firewall resided on an Open Virtual Switch that implements the OpenFlow protocol.  A POX [^myref_3]  instance acts as the controller for the Open Virtual Switch.  Containers are instantiated using Mininet to create four containers.  Layer 2 and Layer 3 firewall rules are applied to the controller using a firewall application running the application plane.  Various tests are performed in order to test the functionality of the firewall application.

The network setup for this Project is shown in [](#CSE548_Fig_10): Project 2 Network Setup below:

```{figure} images/CSE548_Fig_10.png
:label: CSE548_Fig_10
Project 2 Network Setup
```
[](#CSE548_Fig_10): Project 2 Network Setup shows the network topology.  The default IP addresses were changed such that the containers have the following IP addresses:

* Container 1: 192.168.2.10
* Container 2: 192.168.2.20
* Container 3: 192.168.2.30
* Container 4: 192.168.2.40

The default firewall rules did not prevent reachability between the containers.  Firewall rules were added per the Project instructions and tests were performed to check the functionality of the firewall with the new rules.

To setup the controller, the following POX command was issued as shown in [](#CSE548_Fig_11): POX Instantiation Command:

```{figure} images/CSE548_Fig_11.png
:label: CSE548_Fig_11
POX Instantiation Command
```

The POX instantiation command shown in [](#CSE548_Fig_11): POX Instantiation Command starts a POX controller using the OpenFlow protocol, using port 6655, with a Layer 2 learning firewall and a Layer 3 forwarding firewall.

To setup the Containers (Clients), the following Mininet [^myref_4] command was issued as shown in [](#CSE548_Fig_12): Host Network Configurations below:

```{figure} images/CSE548_Fig_12.png
:label: CSE548_Fig_12
Host Network Configurations
```

Issuing the command shown in [](#CSE548_Fig_12): Mininet Instantiation Command created four containers that attached themselves to the Open Virtual Switch listening on port 6655, with MAC (Media Access Control) functionality enabled.  The output of the command is shown in [](#CSE548_Fig_13): Output of Mininet Command below:

```{figure} images/CSE548_Fig_13.png
:label: CSE548_Fig_13
Output of Mininet Command
```

In the Mininet output shown in [](#CSE548_Fig_13): Output of Mininet Command, we can see that 4 hosts are created, and attached to switch s1.  Links were added between the hosts and s1.  Once the links were established, the hosts were configured with IP addresses and the Controller and Switch were started.

The default IP addesses given to the hosts were not in compliance with the Project requirements; therefore, their IP addresses were changed using the Linux *ifconfig* command.  The results of the issued *ifconfig* commands for each host are shown in the following figures ([](#CSE548_Fig_14a), [](#CSE548_Fig_14b), [](#CSE548_Fig_14c), [](#CSE548_Fig_14d)) below:

```{figure} images/CSE548_Fig_14a.png
:label: CSE548_Fig_14a
Host 1's *ifconfig* Output
```
```{figure} images/CSE548_Fig_14b.png
:label: CSE548_Fig_14b
Host 2's *ifconfig* Output
```
```{figure} images/CSE548_Fig_14c.png
:label: CSE548_Fig_14c
Host 3's *ifconfig* Output
```
```{figure} images/CSE548_Fig_14d.png
:label: CSE548_Fig_14d
Host 4's *ifconfig* Output
```

As can be seen in [](#CSE548_Fig_14a), [](#CSE548_Fig_14b), [](#CSE548_Fig_14c), [](#CSE548_Fig_14d): Host Network Configurations, every host’s IP address was changed from the default 10.0.0.0 network to the 192.168.2.0 network.

#### Project 3: SDN-Based DoS Attacks and Mitigation Project

The purpose of this project is to learn about Software Defined Networking and implementing Denial of Service (DoS) attack mitigation.  In this project an Open Virtual Switch is created that operates on the OpenFlow protocol.  A POX instance acts as the controller for the Open Virtual Switch.  Containers are instantiated using Mininet to create four containers.  The L3 firewall application was modified to detect DoS attacks and permanently block the offending MAC address.  Various tests are performed in order to test the functionality of the firewall application.
Setup for this Project is the same as for Project 2, except that the POX controller was now started with a Layer 3 learning firewall.  The initiation command for the POX controller is shown in [](#CSE548_Fig_18): Starting Layer 3 Learning Application through POX below:

```{figure} images/CSE548_Fig_18.png
:label: CSE548_Fig_18
Starting Layer 3 Learning Application through POX
```

The Layer 3 Learning application started using the command shown in Fig 15: Starting Layer 3 Learning Application through POX, instantiates a Open Virtual Switch whose Layer 3 firewall is defined in the pox.forwarding.l3_learning configuration file.  The Layer 3 configuration is defined in a Python script attached to this document [](L3Firewall.ipynb)

#### Project 4: Machine Learning-Based Anomaly Detection

The purpose of this Project is to use machine learning to spot abnormal patterns in network traffic and identify potential attacks from hackers.  Training data for the machine learning models is provided by the Course Team.  Two distinct models are trained and tested against three different test sets.  Testing / validation accuracy and loss are determined, as well as construction of a confusion matrix for the three separate testing conditions.  An assessment is made to determine the model with the most testing accuracy, and then to figure out why that model fares better than others.  This determination involves examining the training data and testing data to notice any particular patterns in the categories and subcategories of attacks. 

The analysis was performed in a Virtualbox Linux virtual machine (VM) guest running on a Windows 11 host.  The Linux system is Parrot OS.  The VM was assigned 12/16 processors and 24 Gbytes of RAM.  Unfortunately, Virtualbox does not support GPU passthrough to the guest and using the GPU for model training was not possible.  Model training was performed on the CPU with an average training time of about 2.5 hours per scenario.
The course team provided the bare-bones Python code necessary to make inroads into the Project.  Specifically, a data extractor script was provided to extract specific classes of attacks from the NSL-KDD standard cybersecurity dataset.  The data extractor script was migrated into a Jupyter Lab notebook running a Python 3.11 kernel.  The notebook is provided as an attachment to this Report [](dataExtractor.ipynb).  Migrating the data extractor script into Jupyter Lab provided a means of monitoring the operation of the script in logical sections.  The data extractor script was used to create training and testing data per the Project specifications.

After the training and testing datasets were extracted, the next script that was provided by the Course Team and migrated into Jupyter Lab was FNN_sample.py.  This script contained the bulk of the work necessary to be completed for the Project.  The script was modified to use the training and testing datasets per the Project specifications.  To facilitate reuse, a separate Jupyter Lab notebook file was create for each of the three scenarios.  These notebooks are provided as an attachment to this report [](FNN_Sample_SA.ipynb), [](FNN_Sample_SB.ipynb), [](FNN_Sample_SC.ipynb).

The Python Modules Keras [^myref_5] and Tensorflow [^myref_6] were the backends that provided the framework for training and testing the Feedforward Neural Networks.

The first step was to obtain the NSL-KDD [^myref_7] dataset per the Project instructions.  The dataset was obtained and examined within Jupyter Lab.  The first few lines of the dataset are shown in [](#CSE548_Fig_19): NSL-KDD Dataset Excerpt below:

```{figure} images/CSE548_Fig_19.png
:label: CSE548_Fig_19
NSL-KDD Dataset Excerpt
```

[](#CSE548_Fig_19): NSL-KDD Dataset Excerpt shows that the data is a CSV file with many rows and columns (only a few rows and columns are visible above).  A description is provided in an attached HTML file.  Task 2 of the Project instructions called out using the KDDTrain+.txt and KDDTest+.txt files, and obtaining attack classes and subclasses from them.  The KDDTrain+.csv and KDDTest+.txt raw data is opened in Jupyter Lab and shown in [](#CSE548_Fig_20): KDDTrain+.txt (partial) and [](#CSE548_Fig_21): KDDTest+.txt (partial) below:

```{figure} images/CSE548_Fig_20.png
:label: CSE548_Fig_20
KDDTrain+.txt (partial)
```
```{figure} images/CSE548_Fig_21.png
:label: CSE548_Fig_21
KDDTest+.txt (partial)
```

In [](#CSE548_Fig_20): KDDTrain+.txt (partial) and [](#CSE548_Fig_21): KDDTest+.txt (partial), we can see that the files contain large amounts of categorical and numerical data.  The class labels are at the second to last column (not shown for brevity).  	As denoted by their filenames, the data in KDDTrain+.txt will be used to train the machine learning model, and KDDTest+.txt will be used for testing the machine learning models.

Task 2 of the Project calls out the following scenarios shown in [](#CSE548_Table_1): Train / Test Scenarios:

:::{table} Train / Test Scenarios
:label: CSE548_Table_1
:align: center

| Datasets | Scenario A (SA) | Scenario B (SB) | Scenario C (SC) |
|----------|------------------|------------------|------------------|
| Training Dataset | A1, A3, N | A1, A2, N | A1, A2, N |
| Testing Dataset | A2, A4, N | A1, N | A1, A2, A3, N |

:::

We can see that there are three scenarios with different testing requirements, although scenario B and scenario C share a common training dataset.  This commonality greatly reduces the amount of model training time.

For Scenario A, the distribution of attack types is shown in [](#CSE548_Fig_22): A1 and A3 Training Dataset Distribution of Attack Types below:

```{figure} images/CSE548_Fig_22.png
:label: CSE548_Fig_22
A1 and A3 Training Dataset Distribution of Attack Types
```

Scenario B and C had the following attack distribution shown in [](#CSE548_Fig_23): A1 and A2 Training Dataset Distribution of Attack Types below:

```{figure} images/CSE548_Fig_23.png
:label: CSE548_Fig_23
A1 and A2 Training Dataset Distribution of Attack Types
```

Of particular interest is how the trained models would perfom when tested on data that is not included in their training data.  To that end, the test data for Scenario A is shown in [](#CSE548_Fig_24): A2 and A4 Testing Dataset Distribution of Attack Types.  

```{figure} images/CSE548_Fig_24.png
:label: CSE548_Fig_24
A2 and A4 Testing Dataset Distribution of Attack Types
```

We can see that in Scenario A, the model is trained on subclasses A1 and A3 but tested on A2 and A4.  A similar situtation was applied for Scenario B and C.  

A distribution of the attacks in the testing data for Scenario B is shown in [](#CSE548_Fig_25): A1 Testing Dataset Distribution of Attack Types. 

```{figure} images/CSE548_Fig_25.png
:label: CSE548_Fig_25
A1 Testing Dataset Distribution of Attack Types
```

Similarly, the testing data for Scenario C is shown in [](#CSE548_Fig_26): A1, A2 and A3 Testing Dataset Distribution of Attack Types.

```{figure} images/CSE548_Fig_26.png
:label: CSE548_Fig_26
A1, A2 and A3 Testing Dataset Distribution of Attack Types
```

##### Data Preparation: One - Hot Encoding
Since we will be training a neural network, all string objects in the dataset need to be processed into numeric values.  A convenient method is “one – hot encoding”, where each category gets its own column and a “1” for that particular category in the data row.  The categorical data was converted into numerical data by using One – Hot Encoding from the SKLearn [^myref_8] Python library.

##### Data Preparation: Feature Scaling
To improve accuracy of the neural network, it is important that features with large ranges do not swamp out the features with smaller ranges.  For this reason, all of the numerical data is normalized using SKLearn’s Standard Scaler.

##### Model Training
The models were then trained on the conditioned data.  These tasks are performed in the FNN_Sample_SX Jupyter Notebooks (where X is either A, B or C.  See attached Jupyter Notebooks).  Training a FNN is a very time consuming process; therefore, once trained, the network weights and biases were saved into a Keras format for later recall.  When saving the models training weights and biases, the loss history is not saved.  It was therefore recorded into JSON files for later recall.

The models were then reloaded into memory and a summary was viewed.  Keras provides a method to observe a summary of the trained model.  The summary for Scenario A is shown in [](#CSE548_Fig_27): Scenario A Trained Model Summary below:

```{figure} images/CSE548_Fig_27.png
:label: CSE548_Fig_27
Scenario A Trained Model Summary
```

Per [](#CSE548_Fig_27): Scenario A Trained Model Summary, the structure of the neural network is a dense layer of 6 input neurons, 6 inner neurons and one output neuron.  The output neuron outputted a value between 0 and 1, where a value greater than 0.9 was considered as an attack, and normal otherwise.  The number of epochs was 10 and the batch size was selected to be 10.  These values seemed to provide good (i.e.> 0.95) training accuracy and low (<0.1) loss for this particular neural network architecture and datasets.  Similar summaries are obtained for Scenario’s B and C.

### Explanation of Solution

#### Project 1: Packet Filter Firewall (iptables) Project

In order to meet the requirements of the Project, *iptables* rules were created such that network actions comply with the stipulations of the Project.  For example, the Client can not ping the Gateway/Server, etc.  The Gateway/Server’s *iptables* rules are shown in [](#CSE548_Fig_28): Gateway/Server's iptables Rules below:

```{figure} images/CSE548_Fig_28.png
:label: CSE548_Fig_28
Gateway/Server's *iptables* Rules
```

As can be seen in [](#CSE548_Fig_28): Gateway/Server's *iptables* Rules, the policy is of the “whitelist” type, where only allowed actions are authorized, and every other action is dropped.

#### Project 2: SDN-Based Stateless Firewall Project

New firewall rules were added to the Layer 3 and Layer 2 firewall configurations to container filtering rules per the Project instructions.  These are shown in [](#CSE548_Fig_29): Layer 3 Firewall Rules (rules 7 - 11 added) below:

```{figure} images/CSE548_Fig_29.png
:label: CSE548_Fig_29
Layer 3 Firewall Rules (rules 7 - 11 added)
```

[](#CSE548_Fig_29): Layer 3 Firewall Rules (rules 7 - 11 added) shows the Layer 3 firewall rules for the Open Virtual Switch.  To comply with the Project requirements, rules 7 through 11 were added.  These rules block:

* pinging beween Hosts 1 and 3
* pinging between Hosts 2 and 4
* block access to port 80 on Host 2
* block any TCP or UDP traffic between Hosts 10 and 20

Layer 2 firewall rules were also implemented per the Project requirements.  The configuration of the Layer 2 firewall is shown in [](#CSE548_Fig_30): Layer 2 Firewall Rules (rule 3 added) below:

```{figure} images/CSE548_Fig_30.png
:label: CSE548_Fig_30
Layer 2 Firewall Rules (rule 3 added)
```

The additional rule created in the Layer 2 firewall shown in [](#CSE548_Fig_30): Layer 2 Firewall Rules (rule 3 added), blocks traffic by MAC address from Host 2 to Host 4.

#### Project 3: SDN-Based DoS Attacks and Mitigation Project

The aim of this project was to detect DoS attacks.  The first item that needs to be established is how to differentiate between normal and DoS traffic.  For nice round numbers, I have decided to use 10 connections in a 3 second time window.  The L3Firewall.py application was modified to include these new constants as shown in [](#CSE548_Fig_31): L3Firewall.py DoS Detection Threshold Constants below:

```{figure} images/CSE548_Fig_31.png
:label: CSE548_Fig_31
L3Firewall.py DoS Detection Threshold Constants
```

When examining the provided L3Firewall.py, I noticed that there was a function called:

```{code} python
:label: CSE548_Code_1
replyToIP(self, packet, match, event, fwconfig)
```

and it contained the logic for processing IP packets.  I therefore decided that the logic to detect a DoS style attack should go into this function.  

The code that was added to the [replyToIP](#CSE548_Code_1) function is shown in [DoS Detection Logic](#CSE548_Code_2) below:

```{code} python
:label: CSE548_Code_2
# ************* DDOS Mods start here *******************
log.debug("[*] Entered DDOS in replyToIP")
current_time = time.time()

# Create a new entry to track the new connection for possible offense
if srcmac not in connection_counter:
    connection_counter[srcmac] = []
connection_counter[srcmac].append(current_time)

# Clean up connections that don't meet offensive threshold		
connection_counter[srcmac] = \
    [item for item in connection_counter[srcmac] if (current_time - item) <= BLOCK_TIME_WINDOW]

# If the number of connections from the same MAC address exceeds the offense threshold, block.
if len(connection_counter[srcmac]) > BLOCK_THRESHOLD:
    log.debug("[*] Blocking MAC address %s for DDOS " % srcmac)
    self.blockMAC(event, srcmac)
    return
# ************* DDOS Mods end here *******************
```

In the code snippet shown in [DoS Detection Logic](#CSE548_Code_2), an if statement checks whether or not a source MAC address is already in the *connection_counter* list of lists.  This list of lists contains a collection of MAC addresses that have not been seen before by the function and are now to be considered as possible DoS candidates.  If the source MAC is not in the *connection_counter* list of lists, then the current time is appended to the list corresponding to that source MAC address.

The next line is a list comprehension that removes any source MAC address whose connection time is greater than the *BLOCK_TIME_WINDOW* constant, which is 3 seconds.  This constant was chosen heuristically in order to achieve reasonable results during testing.  Connections that exceed the  *BLOCK_TIME_WINDOW* connection time are considered normal.

The next line is an if statement that checks if the length of the list for a particular source MAC address exceeds the *BLOCK_THRESHOLD* constant, which is 10 connection attempts.  If a particular source MAC address has 10 connections attempts, each lasting less than 3 seconds, then it is considered a source of DoS style attacks.  The source MAC is then sent to the [blockMAC()](#CSE548_Code_3) function, shown below:

```{code} python
:label: CSE548_Code_3
# ************* My mods start here *******************
# Create function to block offending MAC address
def blockMAC(self, event, mac_address):
    # Add a flow rule to block a MAC address permanently
    log.debug("[*] Entered blockMAC")
    msg = of.ofp_flow_mod()
    match = of.ofp_match()
    match.dl_src = EthAddr(mac_address)
    match.dl_type = pkt.ethernet.IP_TYPE
    msg.match = match
    msg.priority = 65535 # high priority
    msg.action = []
    event.connection.send(msg)
    log.debug("[*] Permanently blocked the MAC address %s" % mac_address)
    log.debug("[*] Exiting blockMAC")
# ************* My mods end here ********************
```

In the [blockMAC()](#CSE548_Code_3) function, code is present that sends a message to the OpenFlow controller’s firewall to add an entry for the offending source MAC.  When this message is sent to the controller’s firewall, the offending MAC address is blocked.

#### Project 4: Machine Learning-Based Anomaly Detection Project
In order to extract the specified scenarios from the provided training and testing datasets, a Python script called dataExtractor.py was provided by the course team.  This script was migrated into Jupyter Lab (see attachment [dataExtractor.ipynb](dataExtractor.ipynb)).  The script identifies the various attack classes and their associated subclasses as shown in [](#CSE548_Fig_32): Definition of Attack Subclasses below:

```{figure} images/CSE548_Fig_32.png
:label: CSE548_Fig_32
Definition of Attack Subclasses
```
	
The training and testing datasets were loaded in memory as Pandas [^myref_9] dataframes.  A Pandas [describe()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html) function was applied to the datasets to get an appreciation for their dimensions:

```{figure} images/CSE548_Fig_33.png
:label: CSE548_Fig_33
Training Dataset Characteristics (partial)
```

[](#CSE548_Fig_32): Training Dataset Characteristics (partial) shows that the training dataset contains 125,973 rows of data.

```{figure} images/CSE548_Fig_34.png
:label: CSE548_Fig_34
Testing Dataset Characteristics (partial)
```

[](#CSE548_Fig_34): Testing Dataset Characteristics (partial) shows that the testing dataset contains 22,544 rows of data.

Once the training and testing data are loaded into Pandas dataframes, they can be filtered for the desired training and testing data based on the three different scenarios as shown in [Scenario A Train / Test Configuration in Python](#CSE548_Cell_1), [Scenario B Train / Test Configuration in Python](#CSE548_Fig_36), [Scenario C Train / Test Configuration in Python](#CSE548_Fig_37):

```{embed} #CSE548_Cell_1
:remove-output: false
Scenario A Train / Test Configuration in Python
```
```{figure} images/CSE548_Fig_36.png
:label: CSE548_Fig_36
Scenario B Train / Test Configuration in Python
```
```{figure} images/CSE548_Fig_37.png
:label: CSE548_Fig_37
Scenario C Train / Test Configuration in Python
```

For each scenario, a *for* loop traverses the training and testing datasets and selects the desired attack classes.  Separated out training and testing datasets were then saved as CSV files for use in the next set of IPython [^myref_10] Notebooks that perform the actual training and testing of the machine learning models.  For the training datasets, this code cell is shown below in [Training A1 and A3 Dataset Generation](#CSE548_Code_4):

```{code} python
:label: CSE548_Code_4
:caption: Training A1 and A3 Dataset Generation
print("Creating training set.....\n")
setA_train = []

if (training_attack_class_list[0][0] != 0) and \
    (len(training_attack_class_list[0]) != num_attack_class):

    for i in range(len(X_train)):
        # exp., X_train[i, -2] is the label of attack subclass, and attacks_subClass[training_attack_class_list[0][j]-1] identify the selected attack class
        if str.lower(str(X_train[i,-2])) == 'normal':
            setA_train.append(X_train[i])

        for j in range(len(training_attack_class_list[0])):
            if str.lower(str(X_train[i, -2])) in attacks_subClass[training_attack_class_list[0][j]-1]:
                setA_train.append(X_train[i])

    trainingFileName="Training"

    for i in range(len(training_attack_class_list[0])):
        trainingFileName = trainingFileName + "-a" + str(training_attack_class_list[0][i])

    trainingFileName = trainingFileName + file_extension

    np.savetxt(trainingFileName, setA_train, delimiter=',', fmt="%s" )

    print("Files " + trainingFileName + " have been created in the same folder this script resides\n")

elif (len(training_attack_class_list[0]) == num_attack_class):
    print("No changes is needed for training dataset!\n")
else:
    print("No attack classes are chosen, thus no new training file is created!\n")
```

** Under Construction **

[^myref_1]: OpenFlow Switch Specification. (2021). Retrieved from https://opennetworking.org/
[^myref_2]: Apache HTTP Server. (2021). Retrieved from https://httpd.apache.org/
[^myref_3]: Using the POX SDN Controller. (2015). Retrieved from https://brianlinkletter.com/2015/04/using-the-pox-sdn-controller/
[^myref_4]: Mininet: An Instant Virtual Network on your Laptop (or other PC). (2021). Retrieved from http://mininet.org/
[^myref_5]: Keras. (2021). Retrieved from https://keras.io/
[^myref_6]: TensorFlow. (2021). Retrieved from https://www.tensorflow.org/
[^myref_7]: NSL-KDD Dataset. (2021). Retrieved from https://www.unb.ca/cic/datasets/nsl.html
[^myref_8]: Scikit-learn. (2021). Retrieved from https://scikit-learn.org/
[^myref_9]: Pandas. (2021). Retrieved from https://pandas.pydata.org/
[^myref_10]: IPython. (2021). Retrieved from https://ipython.org/





