# Message Queuing Telemetry Transport (MQTT) vs Representational State Transfer (REST) Architecture

## 1. Introduction
- MQTT and REST are to different communication approches that are used in distributed systems and both are used widely. They serve different purposes and therefore we will need to know the advantages and disadvantages of both those methods and what our projects need in order to make the right choice between the two.   

## 2. Message Queuing Telemetry Transport (MQTT)
- Definition
  + "MQTT (Message Queuing Telemetry Transport) is a lightweight, publish-subscribe network protocol designed for low-bandwidth, high-latency, or unreliable networks, making it the standard for IoT and Machine-to-Machine (M2M) communication. It enables resource-constrained devices to send data to a central broker, which distributes it to authorized subscribers." - (Defitnition given by Google AI)

- Pros
1. It is efficient and requires low consumption.
2. It provides the comunication between two ore more devices through a broker which also helps with decoupling of the devices.
3. It is reliable even when the network is not stable.
4. It provides data without the need to "ask for it".
- Cons
1. Tt requires a "handshake" to establish a connection which creates more overhead. 
2. It reliys on the broker to keep the entire communication system working.
3. It becomes harder and harder to manage the brokers memory as the number of connected devices increases.

- Example
A common real-world example of MQTT in action is a Smart Home Temperature System. In this scenario, multiple devices communicate through a central Broker (like Mosquitto) using specific Topics.

## 3. Representational State Transfer (REST) Architecture
- Definition
  +"REST (Representational State Transfer) is a software architectural style that defines a set of constraints for building distributed systems, most notably the World Wide Web and modern web APIs. It emphasizes simple, stateless, and scalable communication using standard protocols, primarily HTTP." - (Defitnition given by Google AI) 

- Pros
1. It does not store the state of of the devices therefore it can handle large volumes of request efficiently. 
2. It improves performance by storing the frequently requested data localy.
3. It supports multiple data formats from which the developers can choose in order to satisfy their clients needs.
- Cons
1. It returns a fixed data structure which can lead to a client that can receive too much or not enough information.
2. It is not a protocol therefore it leads to incosistent implementation.
3. It always requires a request from the client in order to sent data. 

- Example
A common real-life example of a REST API in action is a Weather Application on your smartphone. When you open the app to check the forecast, it doesn't store all the world's weather data locally; instead, it uses a REST API to "pull" exactly what it needs for your location.


## 4. What does our project need ?
- The project will involve a large number of distributed sensors sending telemetry data continously to the system. Therefore, the comunication layer should be able to handle high-frequency data transmission, support asynchronous processing, provide reliable service even under unstable network and provide decoupling. 

# 5. Which is the right choice ?
- Both MQTT and REST serve different purposes but that doesn`t mean we have to choose either one or the other. REST is very good for the communication between the sensors and the system. It provides a simple, standard and testable way to send data into the platform.
- REST however is not the good at handling high-throughput, continous data. This is where MQTT is needed as its publish-subscribe model enables efficient decoupling between services and ensures better performance under load.
- Therefore the chosen approach is to combine both. I will use REST to be used as the entry point to incoming data and MQTT for internal communication between services.
