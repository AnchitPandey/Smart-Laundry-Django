# Smart-Laundry-Django

## Components of the project

The image below shows the entire system of our project. It includes:
1. Custom Desiged PCB : This is the component that receives signals from Raspberry PI via the 40 pin connector and coverts it to electric high-low pulses on its pins and takes action (switches on machine OR sends status about a machine queried by raspberry pi). It has 12 ethernet jacks mounted to it which are connected to 12 different machines. We designed this board with Kicad software and mounted all the components.

2. Rasperry Pi: This device is used to receive user query data from our universitie's internal server and sets specific GPIO pins eventually trigerring the custom PCB to perform an action. The Raspberry pi continuously runs our socket programming code in Python to recieve data from server and perform action.

![hardware1](https://user-images.githubusercontent.com/40236708/106415564-4712e700-6404-11eb-853f-83886d091b95.jpg)


## Working of the System

The figure below shows the working of the system. Initially, the user interacts with the app and clicks a button to activate the machine. For example, if user clicks machine 5, then this AJAX request along with the data "5" is sent to the server. The API on the server extracts the data and sends a request to Raspbery pi. Our code on the raspberry pi 
converts 5 to the binary 0101. Specific GPIO pins on raspberry pi are set to 1 and that signal is then sent to the custom PCB via the 40 pin connector. The decoder mounted on the PCB decodes the signal and sends this to washing machine either getting the status of the machine or switching it on. 


![inside1](https://user-images.githubusercontent.com/40236708/106417009-c2c26300-6407-11eb-8b66-cf9a5185e314.PNG)

