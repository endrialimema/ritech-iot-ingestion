# ADR: Adopt Microservice Architecture vs Monolith

## Status
Proposed

## Context
The project will handle high volumes of data coming from multiple dummy sensors. We need an architecture that can efficiently process, scale, and isolate different parts of the system to handle this data load.

**Constraints:**
- Only one developer.
- Limited number of resources for a complex architecture.
- Need for a scalabale architecture for future changes.

**Alternatives:**
1. **Monolith**  
   - Pros: It is an easy architecture to develop and deploy; It is simple to test; It creates less overhead.  
   - Cons: It is hard to scale components individualy; Hard coupling, changes can affect the whole system; Rigid structure, hard to adapt as the project grows.

2. **Microservice**  
   - Pros: Components can be scaled independently; Easier to addapt; Mistakes can be fixed locally.  
   - Cons: It has very high complexity; requires inter-service communication management; It is a lot of overhead for a single developer.

## Decision
We will adopt a **Microservice architecture** for this project.

## Consequences
**Positive:**  
- Components can scale independently.  
- Easier to extend functionality without affecting other services.  
- Faults in one service do not crash the entire system.

**Negative:**  
- Difficult for a single developer to set up and develop te system.  
- Need to manage inter-service communication and possibly a service registry.  
- Testing and debugging may be more involved than in a Monolith.
