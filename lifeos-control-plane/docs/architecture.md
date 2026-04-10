# Architecture

The MVP uses a single FastAPI deployment with logical microservices:
- orchestration
- policy engine
- simulation engine
- observability/trace
- memory service
- connector service
- evaluations service

Control flow:
1) request intake -> 2) planning -> 3) policy review -> 4) simulation -> 5) approval gate -> 6) execution -> 7) trace + metrics.

Trace model captures stage, event type, message, metadata, and timestamp per workflow.
Memory model is editable per user with confidence and source.
