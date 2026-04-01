# Monolithic vs Microservice Architecture

## 1. Introduction
The project introduces a dilema whether which architectural aproach should we use. Should we use Monolithic or Microservice Architecture. 
First we have to understand what is each one of them and then look at what the project asks us to do in order to deciede for the right method.  

## 2. Monolithic Architecture
- Definition
"Monolithic architecture is a traditional software development model where an entire application is built, deployed, and managed as a single, unified unit. Components are tightly coupled, sharing the same codebase and database. While simple to develop, test, and deploy initially, it lacks flexibility and scales poorly." - (Defitnition given by Google AI)

- Pros
1. It is easy and simple. (especially for small, simple applications.)
2. It is faster bacause it reduces daley between modules when they comunicate with each other. 
3. It is easier to monitor everything when you only have to work with only one codebase.
- Cons
1. It is a very rigid strucutre as it cannot grow or expand dynamicly.
2. It is very bad at adapting to change. You have to redo the application which is costly and time consuming.
3. It becomes increasingly complex with weach new feature added which also lead to the system slowing down and underperforming.
- Example
A lot of the top companies today use Microservice Architecture but in their early startups they used monolithic ones in order to lauch fast and gain popularity. It also helped that they were small companies back then and that is why today small start up companies also use Monolithic Architecture for sake of simplicity.

## 3. Microservice Architecture
- Definition
"Microservices architecture is an architectural style that structures an application as a collection of small, independent, and loosely coupled services. Each service focuses on a single business capability—such as user authentication, payment processing, or inventory management—and can be developed, deployed, and scaled independently." - (Defitnition given by Google AI) 
- Pros
1. It can push updates and deploy them independently.
2. It fixes problems localy without affecting the rest of the services.
3. It allows for severel developers to work on the same time without messing with eachothers work. 
- Cons
1. It expands increasingly which requires the need for high level orchestration which may not be sustainable for small teams.
2. It can be harder to trace and correct mistakes or bugs as thesystem gets more complex.
3. It makes it harder and harder for consistancy accros different dtabases to be maintained.  
- Example
Real-world examples of microservices architecture are found in nearly every major tech giant today, including Netflix, Amazon, Uber, and Spotify. These companies transitioned from monolithic structures to microservices to solve critical bottlenecks in scalability, deployment speed, and reliability as their user bases grew. 

## 4. What does our project need ?
Our project involves the digestion of data sent from thousands of dummy sensores that will cause a lot of overload in the system. The dummy sensores will be sending data at all times and continuosly so, and the system should be able to receive, orchestrate, and dsitribute it. It will have to deal with overload but also delays and bugs that can affect several servers at the same time. Therefore we will need an architecture that can deal with a lot of data simultanously, fixing problems localy without causing drop in performance.

# 5. Which is the right choice ?

A monolithic approach will not be able to handle the shear amount of throughput data so we will use a microservice architecture that will be able to deal with a huge amount of data at the same time, minimize delays and be very adaptable to change making the systam dynamic and expandable something that the monolithic approach would not allow for.