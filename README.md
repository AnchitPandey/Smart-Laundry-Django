# Smart-Laundry-Django

## Components of the project

The image below shows the entire system of my project. It includes:
1. Custom Desiged PCB : This is the component that receives signals from Raspberry PI via the 40 pin connector and coverts it to electric high-low pulses on its pins and takes action (switches on machine OR sends status about a machine queried by raspberry pi). It has 12 ethernet jacks mounted to it which are connected to 12 different machines. We designed this board with Kicad software and mounted all the components.

2. Rasperry Pi: This device is used to receive user query data from our universitie's internal server and sets specific GPIO pins eventually trigerring the custom PCB to perform an action. The Raspberry pi continuously runs our socket programming code in Python to recieve data from server and perform action.

![hardware1](https://user-images.githubusercontent.com/40236708/106415564-4712e700-6404-11eb-853f-83886d091b95.jpg)


## Working of the System

