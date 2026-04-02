# Message Queuing Telemetry Transport (MQTT) vs Representational State Transfer (REST) Architecture

## 1. Introduction
- 

## 2. Message Queuing Telemetry Transport (MQTT)
- Definition
"MQTT (Message Queuing Telemetry Transport) is a lightweight, publish-subscribe network protocol designed for low-bandwidth, high-latency, or unreliable networks, making it the standard for IoT and Machine-to-Machine (M2M) communication. It enables resource-constrained devices to send data to a central broker, which distributes it to authorized subscribers." - (Defitnition given by Google AI)

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
"REST (Representational State Transfer) is a software architectural style that defines a set of constraints for building distributed systems, most notably the World Wide Web and modern web APIs. It emphasizes simple, stateless, and scalable communication using standard protocols, primarily HTTP." - (Defitnition given by Google AI) 

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
The project need 

# 5. Which is the right choice ?

