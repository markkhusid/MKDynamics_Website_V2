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

**Abstract** — This report presents the outcomes of four projects conducted within the scope of the CSE548 Advanced Network Security course, which emphasize the integration of network security principles with practical implementations and machine learning techniques. The projects include:

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

In order to meet the requirements of the Project, `iptables` rules were created such that network actions comply with the stipulations of the Project.  For example, the Client can not ping the Gateway/Server, etc.  The Gateway/Server’s `iptables` rules are shown in [](#CSE548_Fig_28): Gateway/Server's iptables Rules below:

```{figure} images/CSE548_Fig_28.png
:label: CSE548_Fig_28
Gateway/Server's `iptables` Rules
```

As can be seen in [](#CSE548_Fig_28): Gateway/Server's `iptables` Rules, the policy is of the “whitelist” type, where only allowed actions are authorized, and every other action is dropped.

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

Once the training and testing data are loaded into Pandas dataframes, they can be filtered for the desired training and testing data based on the three different scenarios as shown below:

##### Scenario A Train / Test Configuration in Python
```{embed} #CSE548_Cell_1
:remove-output: false
```
```{embed} #CSE548_Cell_2
:remove-output: false
```

##### Scenario B Train / Test Configuration in Python
```{embed} #CSE548_Cell_3
:remove-output: false
```
```{embed} #CSE548_Cell_4
:remove-output: false
```

##### Scenario C Train / Test Configuration in Python
```{embed} #CSE548_Cell_5
:remove-output: false
```
```{embed} #CSE548_Cell_6
:remove-output: false
```

For each scenario, a *for* loop traverses the training and testing datasets and selects the desired attack classes.  Separated out training and testing datasets were then saved as CSV files for use in the next set of IPython [^myref_10] Notebooks that perform the actual training and testing of the machine learning models.  For the A1 and A3 training datasets, this code cell is shown below in [Training A1 and A3 Dataset Generation](#CSE548_Code_7):

```{embed} #CSE548_Code_7
:remove-output: false
```

Similar methods were used to create the other training and testing datasets with subclasses per [](#CSE548_Table_1): Train / Test Scenarios.

The created training and testing datasets were then imported into memory as Pandas dataframes.  Since the datasets contained both the features and labels, they needed to be further subdivided into training / testing features and labels.  The training features were extracted with the following code cell shown in [Model Training Features](#CSE548_Code_8) below:

```{embed} #CSE548_Code_8
:remove-output: false
```

The training labels were extracted with the following code cell shown in below: [Model Training Labels](#CSE548_Code_9):

```{embed} #CSE548_Code_9
:remove-output: false
```
```{embed} #CSE548_Code_10
:remove-output: false
```

We can see in [Model Training Labels Code](#CSE548_Code_10) that if the training label was ‘Normal’ a ‘0’ is appended; whereas if the label was a string other than ‘Normal’ (i.e. some kind of attack), a ‘1’ was appended.  Similar operations were performed for the testing data sets.  The training and testing features contained categorical data that needed to be converted into numeric data for model training and testing.  One – Hot Encoding was selected as the method to perform this operation.  For the training feature dataset, the following code cells illustrates this operation:

```{embed} #CSE548_Code_11
:remove-output: false
```

```{embed} #CSE548_Code_12
:remove-output: false
```

In addition to dealing with categorical data, scaling was necessary to prevent a particular feature from over – biasing the training data.  The [SKLearn StandardScaler() class](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) was selected for this operation.  The code cells [Perform Feature Scaling on Training Data Code](#CSE548_Code_13) and [Perform Feature Scaling on Testing Data Code Output](#CSE548_Code_14) show the results:

```{embed} #CSE548_Code_13
:remove-output: false
```

```{embed} #CSE548_Code_14
:remove-output: false
```

The training features are now normalized with a mean of zero.  A similar operation was performed for the testing data.

Once the training and testing data are cleaned and prepared, a Fully – connected Neural Network (FNN) can be constructed.  The FNN is defined as shown in the [Defining FNN Structure](#CSE548_Code_15) code cell below:

```{embed} #CSE548_Code_15
:remove-output: false
```

```{note} Additional Context from Copilot
In the [Defining FNN Structure](#CSE548_Code_15) code cell, we can see that the FNN has an input layer of 6 neurons, a hidden layer of 6 neurons and an output layer of one neuron.  The activation function for the hidden layer is ReLU (Rectified Linear Unit), and the activation function for the output layer is Sigmoid.
```

The model was compiled with the parameters as shown in the [Compilation of FNN](#CSE548_Code_16) code cell below:

```{embed} #CSE548_Code_16  
:remove-output: false
```

```{note} Website Referenced in [Defining FNN Structure](#CSE548_Code_15) and [Compilation of FNN](#CSE548_Code_16)
The code for defining and compiling the FNN was inspired by the following website:
https://machinelearningmastery.com
```

In [Compilation of FNN](#CSE548_Code_16), we can see that the FNN was compiled with the ADAM optimizer, a ‘binary_crossentropy’ loss function, and the metric is ‘accuracy’.  The choices for these hyperparameters were made based on the provided code from the Course team.

```{note} Additional Context from Copilot
- `ADAM` optimizer: an adaptive first‑and‑second‑moment SGD (momentum + RMSProp) optimizer (good default; typically uses lr=0.001) that speeds and stabilizes training.  
- `binary_crossentropy` loss: the log loss for binary targets; for a true label y∈{0,1} and predicted probability p, loss = $- \big(y\log p + (1-y)\log(1-p)\big)$. It's appropriate for a single-output sigmoid FNN.  
- `accuracy` metric: fraction of examples classified correctly (Keras uses a default 0.5 threshold on the sigmoid output).
```

The model was then fit and saved as a Keras file.  This was done to avoid retraining the model during code development since model trainnig takes a very long time. The code cell [Train Model](#CSE548_Code_17) [Save Model to Keras File](#CSE548_Code_18)shows the code cells that perform the training and saving of the traning history data.

```{embed} #CSE548_Code_17
:remove-output: false
```

```{embed} #CSE548_Code_18
:remove-output: false
```

```{note}
In the code cell [Train Model](#CSE548_Code_17), the command classifier.fit() is commented out to avoid retraining the model during code development.  The trained model is saved as shown in the code cell [Save Model to Keras File](#CSE548_Code_18) and is recalled from the Keras file in the code cell [Load Model from Keras File and Load Training History from JSON File](#CSE548_Code_19).
```

Once the model was trained, it can be reloaded at any time using the Keras load_model() function.  The model’s training history is loaded from a JSON file.  The following code cell in [Load Model from Keras File and Load Training History from JSON File](#CSE548_Code_19) displays this process:

```{embed} #CSE548_Code_19
:remove-output: false
```

```{note}
In the code cell [Load Model from Keras File and Load Training History from JSON File](#CSE548_Code_19), the commands are commented out to avoid overwriting the trained model and training history during code development.
```

Similar operations were performed for all Scenarios.  Now that the models are trained, they can be tested per the conditions described in [Table 1: Train / Test Scenarios](#CSE548_Table_1).

### Description of Results
#### Project 1: Packet Filter Firewall (iptables) Project

Once the webserver was setup on the Gateway/Server, accessing the webpage using the Linux command [curl](https://www.man7.org/linux/man-pages/man1/curl.1.html) from the client was possible.  This is shown in [](#CSE548_Fig_35): Accessing the Web Server on the Gateway/Server from the Client below: 

```{figure} images/CSE548_Fig_35.png
:label: CSE548_Fig_35
Accessing the Web Server on the Gateway/Server from the Client
```

In order to test proper functioning of the firewall, the following port scans were performed as shown in [](#CSE548_Fig_36): Client TCP Port Scan of Server and [](#CSE548_Fig_37): Client UDP Port Scan of Server:

##### Client TCP Port Scan of Server

```{figure} images/CSE548_Fig_36.png
:label: CSE548_Fig_36
Client TCP Port Scan of Server
```

##### Client UDP Port Scan of Server

```{figure} images/CSE548_Fig_37.png
:label: CSE548_Fig_37
Client UDP Port Scan of Server
```

In [](#CSE548_Fig_36): Client TCP Port Scan of Server we can see that because of the firewall (iptables) rules, the only TCP port the client can have access to is port 80 on the Gateway/Server.  [](#CSE548_Fig_37): Client UDP Port Scan of Server shows that all UDP ports on the Gateway/Server are closed to the Client as per Project Requirements.

##### Ping Tests to Verify Firewall Requirements

Another requirement of the Project is that the Client must be able to ping 8.8.8.8.  For this to work, the Gateway/Server needs to be setup as the default gateway on the Client, and the Gateway/Server must implement Network Address Translation to translate ICMP[^myref_11] send and receive packets from 8.8.8.8 to and from the Client, respectively.  The Client was able to send pings to 8.8.8.8 successfully and the results are shown in [](#CSE548_Fig_38): Client Ping to Internet Address 8.8.8.8 below:

```{figure} images/CSE548_Fig_38.png
:label: CSE548_Fig_38
Client Ping to Internet Address 8.8.8.8
```

A Project requirement is that the Client must not be able to ping to 8.8.4.4.  Since there is no explicit whitelist rule allowing pings to this address, the ICMP ping packets were dropped as required.  This is shown in [](#CSE548_Fig_39): Client Ping to Internet Address 8.8.4.4 below:

```{figure} images/CSE548_Fig_39.png
:label: CSE548_Fig_39
Client Ping to Internet Address 8.8.4.4
```

A Project requirement is that the Client must not be able to ping the Gateway/Server.  The firewall on the Gateway/Server was setup to drop ping packets from the Client.  Successful test results of this are shown in [](#CSE548_Fig_40): Client Ping of Gateway/Server below:

```{figure} images/CSE548_Fig_40.png
:label: CSE548_Fig_40
Client Ping of Gateway/Server
```

A Project requirement is that the Gateway/Server must not be able to ping the localhost.  ICMP packets that are sent from the Server and outside of the whitelist are successfully blocked as shown in [](#CSE548_Fig_41): Server Ping to Localhost below:

```{figure} images/CSE548_Fig_41.png
:label: CSE548_Fig_41
Server Ping to Localhost
```

A Project requirement is that the Gateway/Server must not be able to ping the Client.  ICMP packets that are sent from the Server and outside of the whitelist are successfully blocked as shown in [](#CSE548_Fig_42): Server Ping to Client below:

```{figure} images/CSE548_Fig_42.png
:label: CSE548_Fig_42
Server Ping to Client
```

#### Project 2: SDN-Based Stateless Firewall Project

Once the firewalls were setup on the Controller, pings were blocked per the Project requirements.  For example, when Host 1 tried to ping Host 3, the pings were dropped, as shown in [](#CSE548_Fig_43): Check Blocking ICMP Traffic from 192.168.2.10 to 192.168.2.30 below:

```{figure} images/CSE548_Fig_43.png
:label: CSE548_Fig_43
Check Blocking ICMP Traffic from 192.168.2.10 to 192.168.2.30
```

Note that in [](#CSE548_Fig_43): Check Blocking ICMP Traffic from 192.168.2.10 to 192.168.2.30, we can see that one ping did go through, but then the learning firewall learned the flow rule to block the remaining ping packets.  A similar successful test was performed for pings from Host 2 to Host 4 per Project requirements.  The results are shown in [](#CSE548_Fig_44): Check Blocking ICMP Traffic from 192.168.2.20 to 192.168.2.40 below:

```{figure} images/CSE548_Fig_44.png
:label: CSE548_Fig_44
Check Blocking ICMP Traffic from 192.168.2.20 to 192.168.2.40
```

A Project requirement is that HTTP traffic must be blocked from Host 2 to any requestor.  To test this flow rule, the [Python Simple Webserver](https://pythonbasics.org/webserver/) was started on Host 2 ([](#CSE548_Fig_45): HTTP Server Setup on Host 2).  A successful test of HTTP requests being blocked from the three other Hosts are shown in [](#CSE548_Fig_46): HTTP Requests to Node 2 Blocked below:

```{figure} images/CSE548_Fig_45.png
:label: CSE548_Fig_45
HTTP Server Setup on Host 2
```
```{figure} images/CSE548_Fig_46.png
:label: CSE548_Fig_46
HTTP Requests to Node 2 Blocked
```

A Project requirement is that MAC address filtering is performed from Host 2 to Host 4.  To perform this test, the Linux command [arping](https://linux.die.net/man/8/arping) was used.  A successful test showing the MAC address filtering from Host 2 to Host 4 was performed and the results are shown in [](#CSE548_Fig_47): Host 2 to Host 4 MAC Address Filtering below:

```{figure} images/CSE548_Fig_47.png
:label: CSE548_Fig_47
Host 2 to Host 4 MAC Address Filtering
```

It can be seen in [](#CSE548_Fig_47): Host 2 to Host 4 MAC Address Filtering that only one response is received from Node 4, while testing [arping](https://linux.die.net/man/8/arping) from Node 1 to Node 3 produced many responses.  This is taken as traffic from Node 2 to Node 4 is blocked based on MAC addresses, since the first reply is necessary for the Controller to learn the flow rule.

A Project requirement is that both TCP and UDP traffic are blocked from Host 1 to Host 2.  The [hping3](https://linux.die.net/man/8/hping3) Linux command was used to send both TCP and UDP packets.  A successful test of TCP packets being blocked when sent from Host 1 to Host 2 is shown in [](#CSE548_Fig_48): Check Blocking of TCP Traffic from Host 1 to Host 2 below:

```{figure} images/CSE548_Fig_48.png
:label: CSE548_Fig_48   
Check Blocking of TCP Traffic from Host 1 to Host 2
```

Likewise, for UDP traffic, a successful test showing that the UDP traffic from Host 1 to Host 2 is being blocked is shown in [](#CSE548_Fig_49): Check Blocking of UDP Traffic from Host 1 to Host 2 below:

```{figure} images/CSE548_Fig_49.png
:label: CSE548_Fig_49
Check Blocking of UDP Traffic from Host 1 to Host 2
```

As can be seen from [](#CSE548_Fig_48): Check Blocking of TCP Traffic from Host 1 to Host 2 and [](#CSE548_Fig_49): Check Blocking of UDP Traffic from Host 1 to Host 2, both TCP and UDP traffic was successfully blocked from Host 1 to Host 2.

#### Project 3: SDN-Based DoS Attacks and Mitigation Project

As a baseline, a DoS flood test was performed from Host 1 to 192.168.2.20 (Host 2) with a spoofed source address of 10.10.10.1.  The commands used to initiate the flood test are shown in [](#CSE548_Fig_50): Packet Flood Test from Host 1 to Host 2 with Spoofed Source IP Address 10.10.10.1 below:

```{figure} images/CSE548_Fig_50.png
:label: CSE548_Fig_50
Packet Flood Test from Host 1 to Host 2 with Spoofed Source IP Address
```

```{note} Explanation of hping3 Command by Copilot
The command used in [](#CSE548_Fig_50): Packet Flood Test from Host 1 to Host 2 with Spoofed Source IP Address is:
`hping3 10.0.0.2 -c 10000 -S --flood -a 10.10.10.1 -V`

- `10.0.0.2`: target IP.
- `-c 10000`: send (up to) 10,000 packets then exit.
- `-S`: set the TCP SYN flag (crafts SYN packets).
- `--flood`: send packets as fast as possible (no delays), i.e., a high‑rate send.
- `-a 10.10.10.1`: spoof the source IP address to 10.10.10.1.
- `-V`: verbose output (show packet headers/info).

Summary: this issues a high‑rate SYN flood (DoS-style) toward 10.0.0.2 while spoofing the source IP. It requires root privileges, can disrupt networks/hosts, and may be illegal or against policy if run against systems you do not own — do not run this on networks without explicit authorization.
```

As the flood of packets was happening, the OpenFlow switch’s flow entries were updating in real time as shown in [](#CSE548_Fig_51): OpenFlow Entries during Packet Flood below:

```{figure} images/CSE548_Fig_51.png
:label: CSE548_Fig_51
OpenFlow Entries during Packet Flood
```

The POX controller window was also displaying learned flow rules as shown in [](#CSE548_Fig_52): POX Controller Output during Packet Flood below: 

```{figure} images/CSE548_Fig_52.png
:label: CSE548_Fig_52
POX Controller Output during Packet Flood
```

We used the [iptraf-ng](https://github.com/iptraf-ng/iptraf-ng)[^myref_12] Linux application to monitor the amount of IP packets during the packet flood.  The output of [iptraf-ng](https://github.com/iptraf-ng/iptraf-ng) is shown in [](#CSE548_Fig_53): Iptraf-ng Output during Packet Flood below:

```{figure} images/CSE548_Fig_53.png
:label: CSE548_Fig_53
Iptraf-ng Output during Packet Flood
```

It can be seen from [](#CSE548_Fig_53): Iptraf-ng Output during Packet Flood that a huge amount of packets were being sent and a DoS attack was successful.

To mitigate the DoS attack, I swapped out the baseline L3Firewall.py for my modified version and restarted the POX controller.  Again, a DoS was started as shown in [](#CSE548_Fig_54): DoS Attack from Host 1 to Host 2 with Spoofed Source Address of 10.10.10.1 below:

```{figure} images/CSE548_Fig_54.png
:label: CSE548_Fig_54
DoS Attack from Host 1 to Host 2 with Spoofed Source Address of 10.10.10.1
```

As before, we observed the traffic flows on the OpenFlow switch.  The observation was performed using the Linux [watch](https://www.man7.org/linux/man-pages/man1/watch.1.html)[^myref_13] command, so as to be able to observe changes more easily without having to notice changes in a rapidly scrolling screen.  The results of the Linux [watch](https://www.man7.org/linux/man-pages/man1/watch.1.html) command are shown in [](#CSE548_Fig_55): Watch of OpenFlow Switch Traffic Flows.  We notice that a flow rule was added to drop packets from MAC address ending in 01 (i.e. the offending MAC address).

```{figure} images/CSE548_Fig_55.png
:label: CSE548_Fig_55
Watch of OpenFlow Switch Traffic Flows
```

The output of the POX controller indicates that a MAC address was blocked.  This is shown in [](#CSE548_Fig_56): POX Controller Output Indicating Offending MAC Address Permanently Blocked below:

```{figure} images/CSE548_Fig_56.png
:label: CSE548_Fig_56
POX Controller Output Indicating Offending MAC Address Permanently Blocked
```

Pinging between other hosts is still possible as the switch blocks the DoS attack from Host 1.  For example pinging from Host 4 to Host 3 is shown below in [](#CSE548_Fig_57): Pinging Allowed Between Host 4 and Host 3:

```{figure} images/CSE548_Fig_57.png
:label: CSE548_Fig_57
Pinging Allowed Between Host 4 and Host 3
```

However, pinging from Host 1 to any other host is blocked, as shown in [](#CSE548_Fig_58): Pings Blocked from Host 1 to Any Other Host, [](#CSE548_Fig_59): Pings Blocked from Host 1 to Any Other Host, and [](#CSE548_Fig_60): Pings Blocked from Host 1 to Any Other Host below:

```{figure} images/CSE548_Fig_58.png
:label: CSE548_Fig_58
Pings Blocked from Host 1 to Any Other Host
```
```{figure} images/CSE548_Fig_59.png
:label: CSE548_Fig_59
Pings Blocked from Host 1 to Any Other Host
```
```{figure} images/CSE548_Fig_60.png
:label: CSE548_Fig_60
Pings Blocked from Host 1 to Any Other Host
```

We can see from [](#CSE548_Fig_58), [](#CSE548_Fig_59), and [](#CSE548_Fig_60): Pings Blocked from Host 1 to Any Other Host, that pings from Host 1 to any other Host are effectively blocked by the firewall.

#### Project 4: Machine Learning-Based Anomaly Detection Project

Once the machine learning models were trained, the learned weights and biases were saved in the Keras[^myref_5] format.  The saving of the trained models prevents having to go through the very time – consuming training process during code development.  When saving the models, their training accuracy and loss histories were not preserved; therefore, their training accuracies and loss histories were saved as JSON files for later retrieval.  An example of the accuracy and loss history for Scenario A is shown in [](#CSE548_Fig_61): Scenario A Model Training Accuracy and Loss JSON File Contents below:

```{figure} images/CSE548_Fig_61.png
:label: CSE548_Fig_61
Scenario A Model Training Accuracy and Loss JSON File Contents
```

For Scenario A, the training accuracy and loss were then evaluated using the SKLearn [evaluate()](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html) function.  The results of the evaluation are shown in [](#CSE548_Fig_62): Evaluate Training Accuracy and Loss:

```{figure} images/CSE548_Fig_62.png
:label: CSE548_Fig_62
Evaluate Training Accuracy and Loss
```

We can see in [](#CSE548_Fig_62): Evaluate Training Accuracy and Loss, that the training accuracy is 0.9991 and the loss is 0.0036.  These are astonishingly great results, and may be an indication of overfitting.

We then evaluate the learned model on the testing dataset.  The results of this evaluation are shown in below:[](#CSE548_Fig_63): Evaluate Scenario A Test Accuracy and Loss:

```{figure} images/CSE548_Fig_63.png
:label: CSE548_Fig_63
Evaluate Scenario A Test Accuracy and Loss
```

Although the testing accuracy in [](#CSE548_Fig_63): Evaluate Scenario A Test Accuracy and Loss, is lower and the loss is higher than for training, the model does pretty well against a testing dataset that does not contain data from the same classes and subclasses.

For Scenario B, the training and testing accuracy and loss are shown in [](#CSE548_Fig_64): Scenario B Training and Testing Accuracy and Loss below:

```{figure} images/CSE548_Fig_64.png
:label: CSE548_Fig_64
Scenario B Training and Testing Accuracy and Loss
```

We can see from [](#CSE548_Fig_64): Scenario B Training and Testing Accuracy and Loss that although Scenario A has better training accuracy and lower training loss, Scenario B has better testing accuracy and lower testing loss.

For Scenario C, the training and testing accuracy and loss are shown in [](#CSE548_Fig_65): Scenario C Training and Testing Accuracy and Loss below:

```{figure} images/CSE548_Fig_65.png
:label: CSE548_Fig_65
Scenario C Training and Testing Accuracy and Loss
```

We can see from [](#CSE548_Fig_65): Scenario C Training and Testing Accuracy and Loss that Scenario C has lower training accuracy and training loss than scenario A, but it has better testing accuracy and lower testing loss than both scenario A and scenario B.

For Scenario A, we plot the training accuracy and loss as a function of training epoch.  The results are shown in [](#CSE548_Fig_66): Scenario A Model Training Accuracy and [](#CSE548_Fig_67): Scenario A Model Training Loss below:

```{figure} images/CSE548_Fig_66.png
:label: CSE548_Fig_66
Scenario A Model Training Accuracy
```

```{figure} images/CSE548_Fig_67.png
:label: CSE548_Fig_67
Scenario A Model Training Loss
```

For Scenario B, we plot the training accuracy and loss in [](#CSE548_Fig_68): Scenario B Model Training Accuracy and [](#CSE548_Fig_69): Scenario B Model Training Loss below:

```{figure} images/CSE548_Fig_68.png
:label: CSE548_Fig_68
Scenario B Model Training Accuracy
```

```{figure} images/CSE548_Fig_69.png
:label: CSE548_Fig_69
Scenario B Model Training Loss
```

For Scenario C, we have the following model training accuracy and loss as shown in [](#CSE548_Fig_70): Scenario C Model Training Accuracy and [](#CSE548_Fig_71): Scenario C Model Training Loss.  We can see that Scenario B and Scenario C have the same training accuracy and training loss curves since both scenarios used the same model parameters and training data.

```{figure} images/CSE548_Fig_70.png
:label: CSE548_Fig_70
Scenario C Model Training Accuracy
```

```{figure} images/CSE548_Fig_71.png
:label: CSE548_Fig_71
Scenario C Model Training Loss
```

##### Display Confusion Matrices and Scores

We now show the confusion matrices and scores for each Scenario.  For Scenario A, we have the following confusion matrix, shown in [](#CSE548_Fig_72): Scenario A Confusion Matrix below:

```{figure} images/CSE548_Fig_72.png
:label: CSE548_Fig_72
Scenario A Confusion Matrix
```

The confusion matrix in [](#CSE548_Fig_72): Scenario A Confusion Matrix indicates a large number of False Negatives (2352), which is not a good result for an attack detection model.

The model scores for Scenario A are shown in [](#CSE548_Fig_73): Scenario A Model Scores below:

```{figure} images/CSE548_Fig_73.png
:label: CSE548_Fig_73
Scenario A Model Scores
```

As can be seen in [](#CSE548_Fig_73): Scenario A Model Scores, the precision is 0.8 for the Normal Class and 0.88 for the Attack Class.  This means that of all of the positive predictions, 0.8 of the predictions are correct for the Normal Class, and 0.88 are correct for the Attack Class.

However, when considering the Recall (i.e. True Positive Rate), we see that of all of the actual positives, the model correctly identified 0.96 of the Normal Classes, but only 0.56 of the Attack Classes.  Therefore, we can say that the model struggles to correctly predict when an attack is occuring.  This is somewhat not surprising since the model was tested on subclasses that it was not trained on.

For Scenario B, we have the following confusion matrix shown in [](#CSE548_Fig_74): Scenario B Confusion Matrix below:

```{figure} images/CSE548_Fig_74.png
:label: CSE548_Fig_74
Scenario B Confusion Matrix
```

The confusion matrix shown in [](#CSE548_Fig_74): Scenario B Confusion Matrix indicates that Scenario B has a much lower amount of False Negatives (1558 vs 2352) than Scenario A.

The model scores for Scenario B are shown in [](#CSE548_Fig_75): Scenario B Model Scores below:

```{figure} images/CSE548_Fig_75.png
:label: CSE548_Fig_75
Scenario B Model Scores
```

We observe from [](#CSE548_Fig_75): Scenario B Model Scores, the precision is 0.85 for the Normal Class and 0.86 for the Attack Class.  This means that of all of the positive predictions, 0.85 of the predictions are correct for the Normal Class, and 0.86 are correct for the Attack Class.  The precision of the Scenario A model are just slightly better than the Scenario B model; however, the Scenario B model has drastically better recall (i.e. true positive rate) performance.

We can see from [](#CSE548_Fig_75): Scenario B Model Scores, that the model for Scenario B had a recall (i.e. true positive rate) of 0.9 for the Normal Class and a recall (i.e. true positive rate) of 0.79 for the Attack Class.  The model in Scenario B performs much better in identifying actual attacks when compared to the model in Scenario A (recall of 0.79 vs recall of 0.56).

For Scenario C, we have the following confusion matrix shown in [](#CSE548_Fig_76): Scenario C Confusion Matrix below:

```{figure} images/CSE548_Fig_76.png
:label: CSE548_Fig_76
Scenario C Confusion Matrix
```

The confusion matrix shown in [](#CSE548_Fig_76): Scenario C Confusion Matrix seems to indicate many False Negatives (2178); however, as a ratio to True Negatives (8939) and True Positives (7770), the model in this Scenario seems to perform better than the models in both Scenarios A and B.

The scores for the model in Scenario C are shown [](#CSE548_Fig_77): Scenario C Model Scores below:

```{figure} images/CSE548_Fig_77.png
:label: CSE548_Fig_77
Scenario C Model Scores
```

Observing the model score shown in [](#CSE548_Fig_77): Scenario C Model Scores, we see that the model in Scenario C has comparable precision (i.e. proportion of predicted positives that are correct) and recall (i.e. proportion of actual positives correctly identified) to the model in Scenario B, but has higher support (i.e. the number of actual occurrences of a class in the dataset) for those scores.  What is astonishing is that the model has such high precision and recall despite being tested on data that it has not been trained on (i.e. trained on subclasses A and B, tested on sublasses A, B and C).

It is observed that the model in Scenario A performed worse than the models in Scenario B and Scenario C when the testing subclasses differed from the training subclasses.  Astonishingly, even though scenario C was never training on attack subclass A3, it performed slightly better than scenario B.  Scenario B was trained on attack subclasses A1 and A2, but was tested on attack subclass A1.  Since it was already exposed to this attack subclass, it fared pretty well.  Scenario C was trained on attack subclasses A1 and A2, but not on A3.  Despite this, it still fared very well, even slightly better than scenario B.  This indicates that attack subclass A1 and A2 have some feature similarities to attack subclass C.

We can see from the bar charts in [](#CSE548_Fig_22): A1 and A3 Training Dataset Distribution of Attack Types and [](#CSE548_Fig_24): A2 and A4 Testing Dataset Distribution of Attack Types that for scenario A, there is no overlap in attack names.  The only commonality is the normal column.  Since the normal column magnitude is roughly an order of magnitude higher than the attacks, the model must be learning to recognize what is normal and using this to make a distinction.

For Scenario B, we can see from the bar charts in [](#CSE548_Fig_23): A1 and A2 Training Dataset Distribution of Attack Types and [](#CSE548_Fig_25): A1 Testing Dataset Distribution of Attack Types, that in addition to overlap on the normal class, there is significant overlap for the attack classes.

For Scenario C, we can see from the bar charts in [](#CSE548_Fig_23): A1 and A2 Training Dataset Distribution of Attack Types and [](#CSE548_Fig_26): A1, A2 and A3 Testing Dataset Distribution of Attack Types that in addition to significant normal class overlap, there is significant overlap in attack types, as well as additional attack types not seen in the training data.

We can get an even better idea of the performance of the model when observing the Receiver Operating Characteristic (ROC) Curve and Area Under the Curve (AUC).  For Scenario A, we have the following ROC and AUC shown in [](#CSE548_Fig_78): Scenario A Receiver Operating Characteristic Curve and Area Under the Curve below:

```{figure} images/CSE548_Fig_78.png
:label: CSE548_Fig_78
Scenario A Receiver Operating Characteristic Curve and Area Under the Curve
```

The ROC curve shown in [](#CSE548_Fig_78): Scenario A Receiver Operating Characteristic Curve and Area Under the Curve shows that it is difficult for this model to achieve a good True Positive Rate without starting to get unacceptably high False Positive rates.  The model is about 30 % (i.e. 0.79 - 0.5) better than random guessing as indicated by the Area Under Curve[^myref_14].

For Scenario B, we have the ROC and AUC shown in [](#CSE548_Fig_79): Scenario B Receiver Operating Characteristic Curve and Area Under the Curve.  The ROC curve for Scenario B shows that this model is much better at achieving a high True Positive rate without a high False Positive rate.  The model is about 40% (i.e. 0.89 - 0.5) better than random guessing as indicated by the Area Under Curve[^myref_14].

```{figure} images/CSE548_Fig_79.png
:label: CSE548_Fig_79
Scenario B Receiver Operating Characteristic Curve and Area Under the Curve
```

For Scenario C, we have the ROC and AUC shown in [](#CSE548_Fig_80): Scenario C Receiver Operating Characteristic Curve and Area Under the Curve.  Scenario C has a ROC and AUC similar to scenario B.  This makes sense, since they were trained on the same dataset.  What is astonishing is that scenario C is tested on a wider variety of data but still performs slightly better than scenario B as seen from the AUC (0.9 for Scenario C vs 0.89 for Scenario B).  The conclusion is that there were enough similarities in the training and test data so that the model in Scenario C performed well.

```{figure} images/CSE548_Fig_80.png
:label: CSE548_Fig_80
Scenario C Receiver Operating Characteristic Curve and Area Under the Curve
```

### Description of my Contributions to the Project

#### Project 1: Packet Filter Firewall (iptables) Project

For Project 1, I renamed the hostnames of the Virtual Machines (VMs) to ‘Client’ and ‘Server’ to enhance clarity of the report and prevent confusion as to which machine I am working with.  I figured out how to setup NAT networking on the two VMs so that they attached to the correct networks. 

Additionally, it may not be apparent in the report, but working with `iptables`[^myref_15] and chains is very complicated.  I had to redo this section of the Project many times to get the operation that was required.  My selected method was to add one iptables rule at a time and test functionality.  If things operate as expected, then I add another rule.  If things break, I delete the rule and retest.  Sometimes, the rule sets get entangled and it is worth starting over.  I also learned about adding a default route to the Client.  This was necessary since the OS on the Client would not know what to do with packets whose destination IP address is outside of the attached network.
I have been working with web server for many years, so I knew how to quickly setup an Apache webserver on the Gateway/Server, even though the Python simple webserver would have been sufficient.  I also used the `curl`[^myref_16] command to rapidly test whether the web server was working.

#### Project 2: SDN-Based Stateless Firewall Project

In Project 2, I used the Linux `Terminator`[^myref_17] terminal application to subdivide the terminal window into quadrants, so I can view the OpenFlow switch status, the POX controller status and the OpenFlow Switch’s traffic flows.  This greatly enhanced understanding of the operation of the components in real time.

#### Project 3: SDN-Based DoS Attacks and Mitigation Project

In Project 3, in order to see the DoS attack happening in real time, I used the `iptraf-ng`[myref_12] application to watch packet counters of packets on the network.  It was readily apparent that a packet flood was occurring since almost 4 million packets were sent by the offending Host, and the data rate was over 45 megabits/second.

In the code writing process for the [`L3Firewall.py`](L3Firewall.ipynb) application, I placed many debug output points that helped to figure out whether the code was operating as intended.

#### Project 4: Machine Learning-Based Anomaly Detection Project

In Project 4, I converted the provided Python scripts into `IPython`[^myref_10] Notebooks in the `Jupyter Lab`[^myref_18] environment.  I broke down the provided scripts into code cells according to logical divisions and made enhancements such as debug points as necessary.  This enabled understanding of exactly what the scripts were supposed to do.  I also added the ability to save the trained models into `Keras`[^myref_5] files, and the training accuracy and loss history into `JSON`[^myref_19] files.  This enabled development of the code without having to wait an extremely long time to retrain the models.

### Explanation of New Skills, Techniques, or Knowledge Acquired from the Project

#### Project 1: Packet Filter Firewall (iptables) Project

A lesson that I learned was that it was worth taking the time to enter the `iptables`[^myref_15] commands one at a time and checking the iptables chains using:

```{code} bash
iptables -L
```

I also learned how to fix errors by using the `–line-numbers` switch and the `-D` switch to delete mistakes.  `Iptables`[^myref_15] chains can become complicated, so it is worth to flush the entire chains and start over when things stop working.  I also learned that the `-A` switch will append a rule to the end, while the `-I` switch will insert a rule to the top.  The order of the rules matters, so that if there is a `DROP` before an `ACCEPT`, then the packet will be dropped.

#### Project 2: SDN-Based Stateless Firewall Project

An Open Virtual Switch[^mref_1] was set up and four containers were connected to it.  Firewall rules were set into place to provide security as per Project requirements.  The firewall was tested against various test conditions.  After performing the labs, the project was pretty straightforward.  I did learn about `hping`[^myref_20], which is a very powerful alternative to the standard Linux `ping`[^myref_21] command.

One thing that I did notice is that the firewall would stop working after a certain time.  After restarting the POX process, the firewall would work correctly.  I am not sure if this is a bug or proper behavior.  The network traffic that was examined with `Wireshark`[^myref_22] did not exhibit any anomalous behavior that precipitated the firewall shutting down.

#### Project 3: SDN-Based DoS Attacks and Mitigation Project

An Open Virtual Switch was set up and 4 containers were connected to it.  A DoS attack was performed that indicated that the baseline firewall configuration was susceptible to such attacks.  The [`L3Firewall.py`](L3Firewall.ipynb) application was modified to detect and permanently block the offending host by `MAC`[^myref_23] address.  Successful operation of the DoS mitigation was demonstrated.

I learned much about how the `Open Virtual Switch`[^myref_1] operates and deals with traffic flows by observing the addition of flow rules to the learning firewall.  When modifying the [`L3Firewall.py`](L3Firewall.ipynb) application, I learned about the format of the procedural calls and functions within the `Open Virtual Switch`[^myref_1] framework that examines flows and packets.  These procedural calls and functions can then be used to block traffic that matches the criteria of a DoS style attack.

#### Project 4: Machine Learning-Based Anomaly Detection Project

In Project 4, we were provided with lots of Python code to get started.  My favorite method of performing Data Science is to use `IPython Notebooks`[^myref_10] in the `Jupyter Lab`[^myref_18] environment.  I used the provided [`dataExtractor.py`](dataExtractor.ipynb) to create a `IPython Notebook`[^myref_10] based on this script to create the training subclass datasets.  Data label and preprocessing methods were taken out of the provided data_preprocessor.py and distinctLabelExtractor.py scripts and incorporated into more general Notebooks called [FNN_Sample_SA.ipynb](FNN_Sample_SA.ipynb), [FNN_Sample_SB.ipynb](FNN_Sample_SB.ipynb), [FNN_Sample_SC.ipynb](FNN_Sample_SC.ipynb).  It was decided to use three separate Notebooks to faciliate code reuse without having to rename general variable names.
Since the model training takes a very long time, I learned how to save the trained model into a `Keras`[^myref_5] file, as well as saving the training accuracy and loss histories into `JSON`[^myref_19] files for later recall.  At first glance, it was not trivial to identify the best performing model, since the model in Scenario A had such a high training accuracy.  Therefore, I had to learn to investigate the precision, recall, ROC and AUC characteristics of each model to get a better feel for which model peformed the best.

## CSE572 Data Mining: Portfolio Project Report

**Abstract** — Insulin Pump and Continuous Glucose Monitor sensor data were analyzed from three different vantage points in this study.  The first analysis resulted in an understanding of the amount time a patient dwells in a blood glucose classification level.  The second study looked at whether certain extracted features could be used to train a Support Vector Machine to classify whether a patient has eaten a meal or not.  Remarkably, the accuracy of the learned model was > 99%.  Finally, clustering was performed on the extracted features and compared to ground truth.

### 1. Introduction and Problem Statement

In this portfolio project report, we will be reviewing the results obtained from the three projects in this course.  The first project consisted of extracting glucose level time series data and its properties for a person using an artificial pancreas.  The second project consisted of training a machine model to assess whether the person has eaten a meal or not.  While the third project consisted of clustering the glucose data to determine the amount of carbohydrates the person has consumed in each meal.

The artificial pancreas used by the person is the Medtronic 670G[^myref_24] control system.  The system consists of a continuous glucose monitor (CGM), which is used to collect blood glucose measurements every five minutes.  Based on these readings a feedback control system delivers precise amounts of insulin to the person.  We will be analyzing the Insulin Pump and CGM Sensor data for the projects and this report.

### Explanation of the Solution

#### Project 1: Extracting Time Series Properties of Glucose Levels in Artificial Pancreas Project

Data for this project was provided as two separated Comma Separated Value (CSV) files.  The first CSV file contained CGM sensor data, while the second contained insuling pump data.  Both the CGM sensor data and insulin pump data were in reversed chronological order, meaning the latest data were the first rows of the files.  Additionally, the data from the CGM sensor and insulin pump were taken asynchronously from each other; therefore, synchronization would have to be performed.  The CGM sensor and insulin pump data also had many columns that added unecessary dimensionality that needed to be reduced.  Finally, there were many missing data points and over fifty – five thousand rows of data.  An effective strategy was required for dealing with the missing data points and the sheer number of rows.

The data for both the insulin pump and the CGM sensor were loaded into Pandas[^myref_9] dataframes.  In order to perform Exploratory Data Analysis (EDA) and plotting of the CGM sensor data, the data was reversed into proper chronological order and filtered to only include the date and time, Sensor Glucose reading in mg/dL, and raw sensor (ISIG) value columns.  The insulin pump data was reversed into proper chronological order and filtered to only include the date and time, and the alarm mode column.

To effectively synchronize the CGM sensor and insulin pump data, a *“datetime”* column was added to each dataset using the `datatime()`[^myref_25] method in the Pandas Python module.  The *"datetime"* column is a concatenation of the date and time columns within the datasets.

The project required knowledge of when the insulin pump was set to Auto Mode.  A reading of “AUTO MODE ACTIVE PLGM OFF” in the Alarm column of the insulin pump dataset indicates the start of the date and time for when Auto Mode is activated.  Once in Auto Mode, the insulin pump can not go back to manual mode without a reset.  With the datasets both having a datetime column, a search can be made from when the insulin pump was set to Auto Mode.  The corresponding data point with the closest time stamp in the CGM sensor dataset was then found.  A “Sensor Mode” column was added CGM sensor dataframe and each row was then assigned whether it is data from Manual Mode or Auto Mode.

To find the daily averages, it is necessary to know the number of data points per day.  Since each data point corresponds to a 5 minute increment, simple arithmetic provides that there are 288 data points per 24 hour period.  Note that this number may include missing data points.  To find the overall averages required for the project, day numbers were added to the CGM dataframe.  Day numbers were simply derived as 24 – hour periods from the datetime column.  The maximum day number can then be used to calculate the overall averages that were required in this project.  The number of days of data per this methodology turned out to be 203.  The rows were then characterized as either day time or overnight by looking at the hour in the datetime column and assigning 6AM to 12AM as “daytime” and 12AM to 6AM as “overnight”.

Handling missing data is an extremely critical part of data cleaning and preparation.  For this stage of the Project, the Pandas’ linear interpolation method was used on the CGM Sensor Glucose column without further consideration for correctness;  with the assumption being that glucose levels should follow an orderly change from a last known reading.

Lastly, classification of glucose levels was required by the project as shown in [](#CSE572_Table_1): Glucose Classification Levels.

```{table} Glucose Classification Levels
:label: CSE572_Table_1
| Glucose Level [mg/dL] | Classification Level |
|-----------------------|----------------------|
| level > 250 | Hyperglycemia Critical |
| level > 180 | Hyperglycemia |
| 70 <= level <= 180 | Normal |
| 70 <= level <= 150 | Secondary |
| 54 < level < 70 | Hypoglycemia Level 1 |
| level <= 54 | Hypoglycemia Level 2 |
```

Now that the dataframes were cleaned and prepared, calculations of daily and overall means for the various categories could be performed.  The project required calculation of means for 18 different categories.  This number is arrived by realizing that there are 6 classification levels given in [](#CSE572_Table_1): Glucose Classification Levels, and each classification level is to be averaged over the overnight, day time and whole day time periods.  Additionally, these 18 categories are to be evaluated for both when the insulin pump is in Manual Mode or Auto Mode, for a total of 36 separate mean calculations.

An example of a mean calculation would be to select from the overall data the appropriate categorical conditions, group that data by day and count the number of data items.  This effectively gives the amount of time the person’s blood glucose levels were in a specific range category per day.  A per day mean and a mean for the entire dataset can then be calculated.

#### Project 2: Machine Model Training Project

The goal of this project is to train a machine to differentiate between the person eating a meal versus not eating a meal given the person’s CGM sensor’s time series data.  As in Project 1, insulin pump and CGM sensor data were provided; however, for this project two sets of data were available.

The datasets had similar problems that occurred in Project 1; however, Project 2’s insulin pump datasets had the additional issue of non – uniform date and time recording.  This necessitated an additional step of pre – processing of the date and time columns within the datasets.  As in Project 1, the now cleaned date and time columns were combined into a “datetime” column using the `to_datetime()`[^myref_27] method provided by the Pandas Python module.

To train a machine learning model, rows from the datasets had to be extracted that corresponded to the person eating a meal.  It was assumed that an occurrence of a non – NaN and positive entry in the “BWZ Carb Input (grams)” column corresponds to the start of a meal.  The time stamps for each of these rows were saved into a sub – dataframe for further processing.

A meal window was defined as a 2 hour time period from when there is an entry in the meal start time sub – dataframe.  If that window was empty, then the corresponding CGM sensor data for time period of meal time – 30 minute to meal time + 2 hours was added to a separate agglomerated dataset.  The adding of meal data to the separate agglomerated dataset was somewhat complicated by the fact that meals might occur within the 2 hour meal window.  In that case the meal occurs within the window is ignored.  If a meal occurs exactly at the end of the 2 hour window, then data from meal time – 1 hour and meal time + 4 hours is used.

Since the CGM sensor provides data at 5 minute intervals, a time period of 2.5 hours results in 30 CGM sensor data points.  Sometimes, due to missing data from the CGM sensor, less than 30 data points are available.  It was decided to drop any rows that contained less than 30 data points, as there was sufficient data available to train the machine.  The separate agglomerated CGM sensor readings data were then converted into a Numpy[^myref_28] matrix to facilitate use of Sklearn’s[myref_8] machine learning Python Modules.

For the no – meal data, a similar procedure was followed except that the post – absorbtive window was defined as a meal time + 2 hours to meal time + 4 hours.  If there were any meals in this post – absorbtive period, then data for that period was ignored.  However, if the post – absorbtive window had any 0 or NaN data points, the 0’s or NaN’s were ignored and data for that post – absorbtive stretch was added into the agglomerated sub – datasets.  

Since the post – absorbtive window is 2 hours, CGM sensor data at 5 minute interval results in 24 data points.  Any rows that had less than 24 data points were dropped since there was sufficient data to train the machine.
Even though rows with less than 30 data points in the meal data and rows with less than 24 data points in the no – meal data were excluded, the intra – row data might still contain NaN’s.  

It was decided to use [imputation](https://grokipedia.com/page/Imputation_(statistics)) to handle these missing data points.  The problem is that if the amount of missing data points is too high, then imputation would provide erroneous results.  A heuristic threshold of 10% missing data points was chosen as a drop threshold.  From the rows that were left, the missing data points were handled with Sklearn’s[^myref_8] KNN (K – Nearest Neighbor) Imputer[^myref_29].  The K used for the KNN Imputer was 7.  This value was chosen based on a heuristic estimate.

```{note} Additional Context from Copilot
K in KNN (k‑Nearest Neighbors)

- K = number of nearest training instances used to make a prediction.
- Classification: predicted class = majority vote among the K nearest neighbors (ties often broken by using odd K or tie‑breaker rule).  
- Regression: predicted value = average (or distance‑weighted average) of the K neighbors' values.
- Effect:
  - small K → low bias, high variance (sensitive to noise, more overfitting)
  - large K → high bias, low variance (smoother decision boundary, may underfit)
- Choosing K: use cross‑validation; ensure K ≤ number of training samples; common practice uses odd K for binary classification.
```

Now that the meal and no – meal datasets were cleaned and imputed, features can be extracted that are used to train the machine learning model.  The eight features that were selected were:
- Mean for the row
- Standard deviation for the row
- Maximum value for the row
- Minimum value for the row
- Mean first derivative for the row
- Mean second derivative for the row
- Area of the curve (AUC) for the row
- Time to reach the peak for the row

These features were then extracted for each row using a feature extractor function.

Since it is known which data corresponds to a meal or not, class labels were then added to the meal data and no – meal data feature matrices.  A class label of 1 was added to the meal data feature matrix and a class label of 0 was added to the no – meal feature matrix.  The meal and no meal feature matrices were then vertically stacked using Numpy’s[^myref_28] `vstack`[^myref_30] method.  The training data was then sliced off and labeled as “X”, while the class labels were sliced off and labeled as “y” following machine learning conventions.

Sklearn’s[^myref_8] `train_test_split`[^myref_31] was then used to split the data into a training sub – dataset and a testing sub – dataset with a 80% / 20% ratio, respectively.  The training and testing datasets were then normalized using Sklearn’s[^myref_8] `StandardScaler`[^myref_32] class.

For this Project, it was decided to employ a `Support Vector Machine (SVM)`[^myref_33] machine learning model, although a `Decision Tree`[^myref_34] machine learning model would have also been a good choice for this binary classification problem.  A linear kernel was chosen since the dimensionality of eight is rather high, but the features have linearly seperable charactersitics.  To prevent overfitting (low bias, high variance), a Regularization Parameter (C) of 0.1 was chosen.

```{note} Additional Context from Copilot
SVM kernels and the regularization parameter C — concise guide

- Kernel concept  
  - Kernel k(x,y)=⟨φ(x),φ(y)⟩ lets SVM operate in a transformed feature space without explicit mapping (kernel trick). Choose based on assumed decision-boundary shape.

- Common kernels (form + when to use)
  - Linear: k(x,y)=x·y  
    - Use when data is (nearly) linearly separable or #features ≫ #samples; fast and interpretable.
  - Polynomial: k(x,y)=(γ x·y + coef0)^degree  
    - Captures feature interactions; degree controls complexity (degree=2 or 3 typical). Can overfit at high degree.
  - RBF / Gaussian: k(x,y)=exp(-γ ||x-y||^2)  
    - Default choice for many problems. γ controls influence radius: small γ → smooth boundary (underfit); large γ → localized, complex boundary (overfit).
  - Sigmoid: k(x,y)=tanh(γ x·y + coef0)  
    - Behaves like a two‑layer neural net; less commonly used and may not satisfy Mercer conditions for all params.
  - Custom kernels: allowed but must be positive semi‑definite (Mercer) for SVM guarantees.

- Kernel hyperparameters to tune  
  - `degree` (polynomial), `gamma` (RBF/poly/sigmoid), `coef0` (poly/sigmoid). Defaults (e.g., `gamma='scale'`) are common but cross‑validate.

- Regularization parameter C (intuition + effect)  
  - SVM objective (soft‑margin): minimize 1/2 ||w||^2 + C Σ ξ_i  subject to margin constraints.  
  - C controls trade‑off between margin width and training errors:
    - Large C → penalize slack heavily → narrower margin, fewer training errors (low bias, higher variance / potential overfit).
    - Small C → allow more slack → wider margin, more regularization (higher bias, lower variance / potential underfit).
  - Practical rule: grid‑search C on log scale (e.g., 1e-3 … 1e3).

- Practical tips
  - Always scale/normalize features before kernel SVM.  
  - If data is high‑dimensional and linear performance is acceptable, use linear SVM for speed (or LinearSVC).  
  - Start with RBF + CV over {C, γ}; if that fails, try polynomial or custom kernels informed by domain knowledge.
```

The SVM model was then trained on the normalized training data and an accuracy of 99.71% was the result.  Additionally, the F1 score was calculated to be 1.00.  

```{note} Additional Context from Copilot
F1 score = harmonic mean of precision and recall:

- Formula: $$F_1 = 2\cdot\frac{\text{precision}\cdot\text{recall}}{\text{precision}+\text{recall}}$$
- Precision:
$$\text{precision} = \frac{TP}{TP + FP}$$
- Recall:
$$\text{recall} = \frac{TP}{TP + FN}$$
- Purpose: balances precision and recall into a single metric (better than arithmetic mean when values differ).  
- Range: 0–1 (higher is better). Use when you need a single measure that penalizes extreme imbalance between precision and recall.

What the extremes mean:
- F1 = 0: occurs when `TP = 0` (so precision = 0 and/or recall = 0). The model makes no correct positive predictions or misses all positives.  
- F1 = 1: occurs when `FP = 0` and `FN = 0` (so precision = 1 and recall = 1). The model perfectly identifies all positives with no false alarms.
```

The high accuracy and high F1 score led me to believe that the model exhibited overfitting.  Altering the kernel of Regularization parameter reduced the F1 score, but not by much.  It was therefore surmized that the choice of features were perhaps optimal for differentiating between a mean and no – meal.  `Principle Component Analysis (PCA)`[^myref_35], a `Confusion Matrix Heatmap`[^myref_36], and `Pairwise Plotting`[^myref_37] were then used to visualize the outputs of the SVM model.

#### Project 3: Cluster Validation Project

In this Project, the person’s carborhydrate input provided Insulin Pump dataset is separated into bins and an unsupervised clustering algorithm is used to cluster the data and compare it to the binned ground truth.

Using techniques similar to Projects 1 and 2, the Insulin Pump data and the CGM sensor data were extracted to find the carbohydrates ingested and blood glucose levels.  The minimum and maximum carbohydrates ingested were then used as the binning limits and a bin size of 20 resulted in 6 bins.  Binning was easily accomplished using Numpy’s[^myref_28] `digitize`[^myref_38] method on the resulting carbohydrate input data from the Insulin Pump.  As in Project 2, the CGM sensor data was cleaned, missing data imputed, features extracted and normalized.

Two methods of clustering were employed: `K-Means`[^myref_39] and `DBSCAN`[^myref_40] clustering.  For K-Means, the K parameter was set to the number of bins, which was six.  

```{note} Additional Context from Copilot
K in K‑means = the number of clusters the algorithm will find.

- Role: K specifies how many centroids are created; each datapoint is assigned to the nearest centroid and centroids are updated to minimize within‑cluster sum of squared distances.  
- Effect: small K → few/large clusters (high bias, underfit); large K → many/small clusters (low bias, high variance, possible overfit).  
- How chosen: domain knowledge or heuristics such as the elbow method (plot total within‑cluster SSE vs K), silhouette score, gap statistic, or stability/consensus clustering; try multiple K and validate.  
- Practical tips: scale features, use KMeans++ initialization and multiple random restarts to avoid poor local minima, and inspect cluster interpretability, not just numeric scores.
```

The Features Matrix was then sent through the `K-Means`[^myref_39] clustering algorithm.  For visualization, since the feature data has 8 dimensions, `PCA`[^myref_35] was used to find the primary two features to plot the clusters against.  In order to also visualize and compare the results of the `K-Means` clustering to the ground truth, each bin entry was plotted for each Features Matrix row.  Additionally, each K-Means clustering result was plotted for each Features Matrix row.  The `Sum of Squared Errors` were then computed.

```{note} Additional Context from Copilot
Sum of Squared Errors (SSE) in K‑means clustering:
- Definition: SSE = Σ (distance between each point and its assigned cluster centroid)². It quantifies how tightly data points are clustered around their centroids.
- Role: SSE is the objective function that K‑means aims to minimize during clustering. Lower SSE indicates more compact clusters.
- Effect of K: As K increases, SSE typically decreases because more centroids allow points to be closer to their assigned centroid. However, too high K can lead to overfitting (each point its own cluster).
- Choosing K: The "elbow method" involves plotting SSE vs K and looking for a point where the decrease in SSE starts to level off (the "elbow"). This suggests a good trade‑off between cluster compactness and model simplicity.
```

For `DBSCAN`[^myref_40], a similar process was taken; however, the `DBSCAN` algorithm assigns a “-1” to noise points.  These had to be handled so as to make a comparison to the results of the `K-Means`[^myref_39] clustering and the ground truth.  Finally, entropy and purity were computed for each cluster and for the overall clustering results.

```{note} Additional Context from Copilot
Entropy and Purity in Clustering:
- Entropy:
  - Definition: Entropy measures the disorder or uncertainty in cluster assignments. For a cluster C with classes {c1, c2, ..., cn}, entropy is calculated as:
    $$Entropy(C) = - \sum_{i=1}^{n} p(c_i) \log_2 p(c_i)$$
    where p(ci) is the proportion of points in cluster C that belong to class ci.
  - Role: Lower entropy indicates that a cluster is more homogeneous (i.e., contains mostly points from a single class). Higher entropy indicates more mixed classes within the cluster.
- Purity:
  - Definition: Purity measures the extent to which clusters contain a single class. For a cluster C, purity is calculated as:
    $$Purity(C) = \frac{1}{|C|} \max_{i} |c_i|$$
    where |C| is the size of cluster C and |ci| is the number of points in C that belong to class ci.
  - Role: Higher purity indicates that a cluster is more homogeneous. Purity ranges from 0 to 1, with 1 indicating that all points in the cluster belong to the same class.
- Overall Measures:
  - Overall Entropy: Weighted average of entropies of all clusters.
  - Overall Purity: Weighted average of purities of all clusters.
- Use Cases: Both metrics are used to evaluate clustering quality when ground truth class labels are available.
```

### Description of Results

#### Project 1: Extracting Time Series Properties of Glucose Levels in Artificial Pancreas Project

The insulin pump dataset contained 41,434 rows, many of which contained missing data.  The CGM sensor dataset contained 55,343 rows of data, of which 51,175 rows contained non-null Sensor Glucose information.  
In the insulin pump dataset, the time stamp for when Auto Mode was activated shown in [](#CSE572_Fig_1): Insulin Pump Auto Mode Data Row:

```{figure} images/CSE572_Fig_1.png
:label: CSE572_Fig_1
Insulin Pump Auto Mode Data Row
```

The corresponding data point with the closest time stamp in the CGM sensor dataset is shown in [](#CSE572_Fig_2): Corresponding CGM Sensor Auto Mode Data Row:

```{figure} images/CSE572_Fig_2.png
:label: CSE572_Fig_2
Corresponding CGM Sensor Auto Mode Data Row
```

In order to visualize the CGM sensor data, a plot was made using Pandas.  On the x – axis we have the row number, and on the y – axis we have the sensor glucose output in [mg/dL] as shown in [](#CSE572_Fig_3): Plot of CGM Data vs Row Number.

```{figure} images/CSE572_Fig_3.png
:label: CSE572_Fig_3
Plot of CGM Data vs Row Number
```

Not much can be seen from the plot in [](#CSE572_Fig_3): Plot of CGM Data vs Row Number at this point, except for maybe the minimums and maximums.  

The CGM data was processed and placed into a `Pandas`[^myref_9] `Dataframe`[^myref_41] shown in [](#CSE572_Fig_4): Processed CGM Dataframe:

```{figure} images/CSE572_Fig_4.png
:label: CSE572_Fig_4
Processed CGM Dataframe
```

To obtain the averages required for the Project, sub – dataframes were selected from the main dataframe shown in [](#CSE572_Fig_4): Processed CGM Dataframe based on the required mean.  For example, Manual Mode, Overnight Percentage of Time in Hyperglycemia range.  There were 166 CGM entries spanning 7 distinct days.  This data was aggregated by day using the `Pandas`[^myref_9] `groupby`[^myref_42] function and counted to obtain the quantity in hyperglycemia for that day.  This is shown in [](#CSE572_Fig_5): Manual Mode / Overnight / Hyperglycemia.

```{figure} images/CSE572_Fig_5.png
:label: CSE572_Fig_5
Manual Mode / Overnight / Hyperglycemia
```

The percentage mean for the day was computed by dividing each row in [](#CSE572_Fig_5): Manual Mode / Overnight / Hyperglycemia by 288 and multiplying by 100.  An overall mean for this set of conditions was obtained by averaging the percentage mean for each day out of the total number of days in the the dataset.  Similar methodoly was undertaken for the 35 other combinations.  The results of all of the means for the 36 combinations are given in [Project 1 Results - Table of Calculated Percentage Means: Overnight](#CSE572_Code_1), [Project 1 Results - Table of Calculated Percentage Means: Daytime](#CSE572_Code_2) and [Project 1 Results - Table of Calculated Percentage Means: Whole Day](#CSE572_Code_3):

```{embed} #CSE572_Code_1
:remove-output: false
```

```{embed} #CSE572_Code_2
:remove-output: false
```

```{embed} #CSE572_Code_3
:remove-output: false
```

It can be seen from [Project 1 Results - Table of Calculated Percentage Means: Overnight](#CSE572_Code_1), [Project 1 Results - Table of Calculated Percentage Means: Daytime](#CSE572_Code_2) and [Project 1 Results - Table of Calculated Percentage Means: Whole Day](#CSE572_Code_3) that the person spent a majority of their time in either the normal or secondary ranges while in Auto Mode.  The numbers were non – sensical for Manual Mode, perhaps because the person was not recording data.

#### Project 2: Machine Model Training Project

The Meal and No Meal Data Matrices were extracted from the CGM sensor datasets.  A heatmap of the cleaned, imputed meal data matrix is shown in [](#CSE572_Fig_6): Heatmap of Meal Data Matrix 1:

```{figure} images/CSE572_Fig_6.png
:label: CSE572_Fig_6
Heatmap of Meal Data Matrix 1
```

Features were extracted from the Meal Data Matrix using a [feature extractor](#CSE572_Code_4) function:

```{embed} #CSE572_Code_4
:remove-output: false
```

A moving average visulization of the row Maximum, Average, Minimum and Standard Deviation are shown in [](#CSE572_Fig_7): Moving Average of  the Maximum, Mean, Standard Deviation and Minimum of the Meal Features Matrix Rows.

```{figure} images/CSE572_Fig_7.png
:label: CSE572_Fig_7
Moving Average of  the Maximum, Mean, Standard Deviation and Minimum of the Meal Features Matrix Rows
```

The `Seaborn`[^myref_43] `Pandas`[^myref_9] module was used to produce a `pairwise plot`[^myref_37] of the eight extrated features.  This plot is shown in [](#CSE572_Fig_8): Pairwise Plot of Meal Features Matrix.

```{figure} images/CSE572_Fig_8.png
:label: CSE572_Fig_8
Pairwise Plot of Meal Features Matrix
```

It can be seen in [](#CSE572_Fig_8): Pairwise Plot of Meal Features Matrix that there is a strong positive linear correlation between Feature 1 (row mean) and Feature 7 (area under curve).

For the No Meal Features Matrix, features were extracted from the using the same feature extractor function.  A moving average visulization of the row Maximum, Average, Minimum and Standard Deviation are shown in [](#CSE572_Fig_9): Moving Average of  the Maximum, Mean, Standard Deviation and Minimum of the No Meal Features Matrix Rows.

```{figure} images/CSE572_Fig_9.png
:label: CSE572_Fig_9
Moving Average of  the Maximum, Mean, Standard Deviation and Minimum of the No Meal Features Matrix Rows
```

At first glance it appears that it would be difficult to visually discern whether a meal has occurred when comparing [](#CSE572_Fig_7): Moving Average of the Maximum, Mean, Standard Deviation and Minimum of the Meal Features Matrix Rows and [](#CSE572_Fig_9): Moving Average of  the Maximum, Mean, Standard Deviation and Minimum of the No Meal Features Matrix Rows.  As for the Meal Features Matrix, a `pairwise plot`[^myref_37] was created for the No Meal Features Matrix, shown in [](#CSE572_Fig_10): Pairwise Plot of No Meal Features Matrix.

```{figure} images/CSE572_Fig_10.png
:label: CSE572_Fig_10
Pairwise Plot of No Meal Features Matrix
```

In [](#CSE572_Fig_10): Pairwise Plot of No Meal Features Matrix, we again observe a strong positive linear  correlation between Feature 1 (row mean) and Feature 7 (area under curve).

The meal and no meal feature matrices were vertically stacked, normalized and class lables were appended. A Sklearn[^myref_8] `Support Vector Machine (SVM)`[^myref_33] machine learning model was then trained on the features data using a train / test split ratio of 80% / 20%, respectively.

The `SVM`[^myref_33] model was then tested on the test data and surprisingly had a test accuracy of 99.71%, with an [F1 score](https://grokipedia.com/page/F-score) of 1.00.  A visual representation of the model’s prediction accuracy was generated by using `Principle Component Analysis (PCA)`[^myref_35] on the scaled test data.  The results are shown in [](#CSE572_Fig_11): SVM Classification Results: Correct vs Incorrect Predictions on Test Data.

```{figure} images/CSE572_Fig_11.png
:label: CSE572_Fig_11
SVM Classification Results: Correct vs Incorrect Predictions on Test Data
```

The reason for this remarkable result is thought to be the selection of features that enabled the SVM machine to definitively differentiate between a meal and a no meal data sample.  To test this theory, a Seaborn pair plot was generated on the features data and the predicted class.  This plot is shown in [](#CSE572_Fig_12): Pair Plot of SVM Classification Results.

```{figure} images/CSE572_Fig_12.png
:label: CSE572_Fig_12
Pair Plot of SVM Classification Results
```

The pair plot in [](#CSE572_Fig_12): Pair Plot of `SVM`[^myref_33] Classification Results again shows a strong positive linear correlation between Feature 1 (row mean) and Feature 7 (area under curve).  The plot also shows that for Feature 7 (area under curve), there is substantial non – overlap of the histogram distributions.  This allows the `SVM` machine to accurately predict whether the features data object is a meal or a non – meal data object.

Lastly, a `Confusion Matrix Heatmap`[^myref_35] was created to visualize the `SVM` machine's [`accuracy`](https://grokipedia.com/page/Machine_learning#evaluation-and-validation), [`recall`](https://grokipedia.com/page/Precision_and_recall), [`precision`](https://grokipedia.com/page/Precision_and_recall) and [`F1 score`](https://grokipedia.com/page/Machine_learning#evaluation-and-validation).  These results are shown in [](#CSE572_Fig_13): Confusion Matrix Heatmap of Test Data:

```{figure} images/CSE572_Fig_13.png
:label: CSE572_Fig_13
Confusion Matrix Heatmap of Test Data
```

#### Project 3: Cluster Validation Project

A method similar to Project 2 was used to extract the meal carbohydrate ingestion data from the Insulin Pump dataset.  The extracted carbohydrate amounts were then binned into six bins that were bounded by the minimum and maximum carbohydrate ingestion amounts.  This resulted in the “ground truth” that will be later employed for cluster validation.

Addtionally, using methods similar to Project 2, the meal blood glucose levels were extracted from the CGM sensor dataset.  The data was then cleaned and missing data items were [imputed](https://grokipedia.com/page/Imputation_(statistics)) using Sklearn’s[^myref_8] `KNN Imputer`[^myref_29].  Features were then extracted from the meal blood glucose sensor readins in a manner similar to what was employed in Project 2.  The features were then normalized to facilitate accurate clustering.

`K-Means Clustering`[^myref_39] was employed first.  The clustering results were plotted against two [Principle Components](https://grokipedia.com/page/Principal_component_analysis) features that were obtained using [`Principle Component Analysis (PCA)`](https://grokipedia.com/page/Principal_component_analysis)[^myref_35] from `Sklearn’s`[^myref_8] `PCA`[^myref_44] class.  The plotted results are shown in [](#CSE572_Fig_14): K - Means Clusters vs PCA Components:

```{figure} images/CSE572_Fig_14.png
:label: CSE572_Fig_14
K - Means Clusters vs PCA Components
```

In order to assess the validity of the clustering, a dual plot was generated of the original bins and the results of the K – Means clustering.  The result is shown in [](#CSE572_Fig_15): Original Bins and K - Means Clustering Bins:

```{figure} images/CSE572_Fig_15.png
:label: CSE572_Fig_15
Original Bins and K - Means Clustering Bins
```

It can be seen from [](#CSE572_Fig_15): Original Bins and K - Means Clustering Bins heavily mis – clustered bins 1 and 4.  The `Sum of the Squared Error (SSE)`[^myref_45] for the `K – Means Clustering`[^myref_39] result is shown in  [K - Means SSE Result](#CSE572_Code_5).

```{embed} #CSE572_Code_5
:remove-output: false
```

DBSCAN clustering was then performed.  A plot of the `DBSCAN`[^myref_40] clustering results were plotted against two [Principle Components](https://grokipedia.com/page/Principal_component_analysis) of the features matrix and shown side – by – side with the `K – Means Clustering`[^myref_39] results for comparison.  This is shown in [](#CSE572_Fig_16): DBSCAN Clustering and K - Means Clustering Results:

```{figure} images/CSE572_Fig_16.png
:label: CSE572_Fig_16
DBSCAN Clustering and K - Means Clustering Results
```

Notably, the `DBSCAN`[^myref_40] clustering results shown in [](#CSE572_Fig_16) are very different than the `K – Means Clustering`[^myref_39] results.  This can be explained because `DBSCAN` works off of data density rather than distance to the initially guessed [`centroid`](https://grokipedia.com/page/K-means_clustering#k--means-clustering) as in `K – Means Clustering`.  To assess whether the `DBSCAN` clustering was able to properly cluster the features data, a dual plot was generated of the original bins and the results of the `DBSCAN` clustering.  The result is shown in [](#CSE572_Fig_17): Original Bins and DBSCAN Clustering Bins:

```{figure} images/CSE572_Fig_17.png
:label: CSE572_Fig_17
Original Bins and DBSCAN Clustering Bins
```

It can be seen from [](#CSE572_Fig_17): Original Bins and DBSCAN Clustering Bins heavily mis – clustered bins 1 and 4.  The `Sum of the Squared Error (SSE)`[^myref_45] for the `DBSCAN`[^myref_40] clustering result is shown in [DBSCAN Clustering SSE](#CSE572_Code_6).

```{embed} #CSE572_Code_6
:remove-output: false
```

The cluster and overall [`Total Entropy and Purity`](https://towardsdatascience.com/evaluation-metrics-for-clustering-models-5dde821dd6cd/) were computed for both the `K – Means Clustering`[^myref_39] and `DBSCAN`[^myref_40] clustering results.  The results are shown in [K - Means Clustering Total Entropy](#CSE572_Code_7), [DBSCAN Clustering Total Entropy](#CSE572_Code_8), [K - Means Clustering Total Purity](#CSE572_Code_9), and [DBSCAN Clustering Total Purity](#CSE572_Code_10).

```{embed} #CSE572_Code_7
:remove-output: false
```

```{embed} #CSE572_Code_8
:remove-output: false
```

```{embed} #CSE572_Code_9
:remove-output: false
```

```{embed} #CSE572_Code_10
:remove-output: false
```

From [K - Means Clustering Total Entropy](#CSE572_Code_7), [DBSCAN Clustering Total Entropy](#CSE572_Code_8), [K - Means Clustering Total Purity](#CSE572_Code_9), and [DBSCAN Clustering Total Purity](#CSE572_Code_10), we can observe that the DBSCAN entropy is lower than the K – Means entropy, while the K – Means purity is higher than the DBSCAN purity.

```{note} Additional Context from Copilot
Interpreting Entropy and Purity Results in Clustering:

Entropy measures the impurity or randomness in a cluster. Lower entropy indicates more homogeneous clusters.
Purity measures the dominance of a single class within a cluster. Higher purity indicates more homogeneous clusters.

In this case, DBSCAN has lower entropy (more homogeneous clusters) but lower purity (less dominance of a single class), while K-Means has higher purity (more dominance of a single class) but higher entropy (less homogeneous clusters).

- What the numbers mean
  - Lower DBSCAN entropy → on average DBSCAN clusters have less class‑mix (more homogeneous class distributions) — good.
  - Higher K‑Means purity → K‑Means clusters contain a larger fraction of the dominant (most common) class per cluster — also “good” but measures a different aspect.

- Why they can disagree
  - Entropy and purity capture different things: entropy measures full class distribution within clusters (penalizes mixed clusters); purity only looks at the largest class in each cluster (ignores how the remainder is distributed) and is sensitive to cluster sizes and splits.
  - K‑Means can produce many small, single‑class clusters that inflate purity but leave some large mixed clusters that raise entropy.  
  - DBSCAN can leave ambiguous points as noise or merge dense regions into relatively homogeneous clusters, lowering entropy but (depending on cluster sizes/noise handling) yielding lower overall purity.
```

#### Description of My Contributions to the Project

My experience with `Python`, `Jupyter Lab` and `Data Science` has enabled me to probe a bit further than the strict requirements of the three Projects.  In addition to writing the baseline code to fullfill the Project requirements, I have thought about and implemented various visualizations to get a better understanding of the data and extracted features.  There were many more visualizations that I could have included, but for the sake of brevity, only the most salient visualizations were included.

#### Explanation of New Skills, Techniques, or Knowledge Acquired from the Project

In neither my engineering employement nor Data Science studies, have I ever encountered a dataset with so many columns and rows.  This presented a unique challenge when it came to [`Exploratory Data Analysis (EDA)`](https://grokipedia.com/page/Exploratory_data_analysis) and [`Data Cleaning`](https://grokipedia.com/page/Data_cleansing).  For example, it was meaningless to display small snippets of the CGM Sensor `dataframe`[^myref_41].  Dealing with missing values was definitely an interesting learning point, because this is somewhat an arbitrary decision that has profound effects on the accuracy of the analysis, particularly in Project 1’s calculation of the distinct means, and Project 3’s cluster validation.

For high – dimensional data, I learned to use [`Principle Component Analysis (PCA)`](https://grokipedia.com/page/Principal_component_analysis) to extract the two features with the most [`variance`](https://grokipedia.com/page/Variance).  These two features can then be used to make two – dimensional visualizations that assist in understanding the data and results.  I also learned about creating the “ground truth” prior to performing data clustering.  Comparison to ground truth makes allot more sense than an `SSE`[^myref_45], [entropy or purity calculations](https://towardsdatascience.com/evaluation-metrics-for-clustering-models-5dde821dd6cd/).


[^myref_1]: OpenFlow Switch Specification. https://opennetworking.org/
[^myref_2]: Apache HTTP Server. https://httpd.apache.org/
[^myref_3]: Using the POX SDN Controller. https://brianlinkletter.com/2015/04/using-the-pox-sdn-controller/
[^myref_4]: Mininet: An Instant Virtual Network on your Laptop (or other PC). http://mininet.org/
[^myref_5]: Keras. https://keras.io/
[^myref_6]: TensorFlow. https://www.tensorflow.org/
[^myref_7]: NSL-KDD Dataset. https://www.unb.ca/cic/datasets/nsl.html
[^myref_8]: Scikit-learn. https://scikit-learn.org/
[^myref_9]: Pandas. https://pandas.pydata.org/
[^myref_10]: IPython. https://ipython.org/
[^myref_11]: Internet Control Message Protocol (ICMP). https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol, https://tools.ietf.org/html/rfc792
[^myref_12]: `iptraf-ng` is an ncurses-based IP LAN monitor that generates various network statistics including TCP info, UDP counts, ICMP   and OSPF information, Ethernet load info, node stats, IP checksum errors, and others.  If the `iptraf-ng` command is issued without any command-line options, the program comes up in interactive mode, with the various facilities accessed through the main menu. https://www.man7.org/linux/man-pages/man8/iptraf-ng.8.html, https://github.com/iptraf-ng/iptraf-ng
[^myref_13]: `watch` runs command repeatedly, displaying its output and errors (the first screenful). This allows you to watch the program output change over time. By default, command is run every 2 seconds and `watch` will run until interrupted.  A header informs of the start and running time of command as well as its exit code. https://www.man7.org/linux/man-pages/man1/watch.1.html
[^myref_14]: https://en.wikipedia.org/wiki/Receiver_operating_characteristic
[^myref_15]: `Iptables` is a user-space utility program that allows a system administrator to configure the IP packet filter rules of the Linux kernel firewall, implemented as different Netfilter modules. https://netfilter.org/projects/iptables/index.html
[^myref_16]: `curl` is a command-line tool for transferring data specified with URL syntax. https://curl.se/docs/manpage.html
[^myref_17]: `Terminator` is a terminal emulator for Linux which allows users to arrange multiple terminal windows in a grid. https://terminator-gtk3.readthedocs.io/en/latest/
[^myref_18]: `JupyterLab` is an open-source web-based interactive development environment for Jupyter notebooks, code, and data. https://jupyter.org/
[^myref_19]: `JSON` (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write, and easy for machines to parse and generate. https://www.json.org/json-en.html
[^myref_20]: `hping` is a command-line oriented TCP/IP packet assembler/analyzer. The interface is inspired to the ping(8) Unix command, but hping isn’t only able to send ICMP echo requests. It supports TCP, UDP, ICMP and RAW-IP protocols, has a traceroute mode, the ability to send files between a covered channel, and many other features. https://en.wikipedia.org/wiki/Hping, https://www.hping.org/wiki-sub/index/
[^myref_21]: `ping` is a computer network administration utility used to test the reachability of a host on an Internet Protocol (IP) network. It measures the round-trip time for messages sent from the originating host to a destination computer that are echoed back to the source. https://en.wikipedia.org/wiki/Ping_(networking_utility)
[^myref_22]: `Wireshark` is a free and open-source packet analyzer. It is used for network troubleshooting, analysis, software and communications protocol development, and education. https://www.wireshark.org/
[^myref_23]: A `Media Access Control address (MAC address)` is a unique identifier assigned to a network interface controller (NIC) for use as a network address in communications within a network segment. https://en.wikipedia.org/wiki/MAC_address
[^myref_24]: Medtronic 670G Hybrid Closed Loop System. https://www.medtronicdiabetes.com/products/minimed-670g-insulin-pump-system
[^myref_25]: The `datetime` module supplies classes for manipulating dates and times in both simple and complex ways. While date and time arithmetic is supported, the focus of the implementation is on efficient attribute extraction for output formatting and manipulation. https://docs.python.org/3/library/datetime.html
[^myref_27]: The `to_datetime()` function in the Pandas Python module is used to convert a string or a list of strings to datetime objects. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
[^myref_28]: `NumPy` is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays. https://numpy.org/
[^myref_29]: The `KNNImputer` class in the Sklearn Python module provides imputation for completing missing values using the k-Nearest Neighbors approach. https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html
[^myref_30]: The `vstack()` function in the Numpy Python module is used to stack arrays in sequence vertically (row wise). https://numpy.org/doc/stable/reference/generated/numpy.vstack.html
[^myref_31]: The `train_test_split()` function in the Sklearn Python module is used to split arrays or matrices into random train and test subsets. https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
[^myref_32]: The StandardScaler class in the Sklearn Python module is used to standardize features by removing the mean and scaling to unit variance. https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
[^myref_33]: A `Support Vector Machine (SVM)` is a supervised machine learning model that uses classification algorithms for two-group classification problems. After giving an SVM model sets of labeled training data for each category, they’re able to categorize new text. https://en.wikipedia.org/wiki/Support_vector_machine
[^myref_34]: `Decision Tree` learning is a supervised learning approach used in statistics, data mining and machine learning. In this formalism, a classification or regression decision tree is used as a predictive model to draw conclusions about a set of observations. https://en.wikipedia.org/wiki/Decision_tree_learning
[^myref_35]: `Principal Component Analysis (PCA)` is a statistical procedure that uses an orthogonal transformation to convert a set of observations of possibly correlated variables into a set of values of linearly uncorrelated variables called principal components. https://en.wikipedia.org/wiki/Principal_component_analysis
[^myref_36]: A `Confusion Matrix Heatmap` is a visualization tool used to evaluate the performance of a classification model by displaying the counts of true positive, true negative, false positive, and false negative predictions in a matrix format, often enhanced with color gradients to represent the magnitude of each count. https://en.wikipedia.org/wiki/Confusion_matrix
[^myref_37]: `Pairwise Plotting` is a data visualization technique that involves creating scatter plots for every possible pair of variables in a dataset, allowing for the examination of relationships and correlations between multiple variables simultaneously. https://seaborn.pydata.org/generated/seaborn.pairplot.html
[^myref_38]: The `digitize()` function in the Numpy Python module is used to return the indices of the bins to which each value in input array belongs. https://numpy.org/doc/stable/reference/generated/numpy.digitize.html
[^myref_39]: `K-Means` is an unsupervised machine learning algorithm used for clustering data into K distinct groups based on feature similarity. https://en.wikipedia.org/wiki/K-means_clustering
[^myref_40]: `DBSCAN` (Density-Based Spatial Clustering of Applications with Noise) is an unsupervised machine learning algorithm used for clustering data points based on their density, allowing it to identify clusters of varying shapes and sizes while effectively handling noise and outliers. https://en.wikipedia.org/wiki/DBSCAN
[^myref_41]: A `DataFrame` is a two-dimensional, size-mutable, and potentially heterogeneous tabular data structure provided by the Pandas Python module, which allows for easy data manipulation, analysis, and storage in rows and columns. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
[^myref_42]: The `groupby()` function in the Pandas Python module is used to split data into groups based on some criteria, allowing for aggregation, transformation, or filtration of the data within each group. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
[^myref_43]: `Seaborn` is a Python data visualization library based on Matplotlib that provides a high-level interface for creating attractive and informative statistical graphics. https://seaborn.pydata.org/
[^myref_44]: The `PCA` class in the Sklearn Python module is used to perform Principal Component Analysis, a dimensionality reduction technique that transforms data into a new coordinate system by identifying the directions (principal components) that maximize variance. https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
[^myref_45]: The `Sum of Squared Errors (SSE)` is a statistical measure used to quantify the total deviation of predicted values from the actual values in a dataset, calculated by summing the squares of the differences between each predicted value and its corresponding actual value. https://en.wikipedia.org/wiki/Residual_sum_of_squares









