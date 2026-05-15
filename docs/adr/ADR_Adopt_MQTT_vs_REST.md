# ADR: Adopt MQTT vs REST

## Status
Proposed

## Context
The project will handle communication between sensores and system and communtication between multple servers within the system . We need a method that can provide good and reliable communication.

**Constraints:**
- Only one developer.
- Frequent data messaged.
- Need for minimal delay.
- Need to handle freaquent messaging.

**Alternatives:**
1. **MQTT**  
   - Pros: It is an easy architecture to develop and deploy; It is simple to test; It creates less overhead.  
   - Cons: It is hard to scale components individualy; Hard coupling, changes can affect the whole system; Rigid structure, hard to adapt as the project grows.

2. **REST**  
   - Pros: It is easy to use and implement. It is standard and easy to correct mistakes.
   - Cons: Not very efficient for real time data. Works only on request.

## Decision
We will use **MQTT** for sensor data communication.

## Consequences
**Positive:**  
- Efficient, lightweight protocol suitable for frequent sensor updates.  
- Supports publish/subscribe, making it easier to scale or add new consumers.  
- Low latency communication suitable for real-time monitoring.  

**Negative:**  
- Requires maintaining an MQTT broker.  
- Slightly higher complexity in setup compared to REST.  
- Debugging and testing messages can be harder than simple HTTP requests.
