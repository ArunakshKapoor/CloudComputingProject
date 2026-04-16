\# Architecture



\## 1. System Overview



LifeOS Control Plane is a \*\*simulation-first, governed Personal Assistant-as-a-Service prototype\*\*.



The system is designed around the idea that a personal assistant should not directly execute opaque actions. Instead, it should:



1\. accept a natural-language request

2\. decompose it into structured service steps

3\. assign risk and policy decisions

4\. simulate likely outputs and side effects

5\. require approval for sensitive actions

6\. execute allowed steps

7\. produce a traceable audit trail



The system is implemented as a \*\*single deployable FastAPI application\*\* with \*\*logical microservices\*\* and a separate \*\*Next.js frontend\*\*.



\---



\## 2. Design Goals



The architecture is built around five main goals:



\### 2.1 Governed orchestration

The system should not behave like a single black-box chatbot. It should expose planning, policy, simulation, and execution as distinct stages.



\### 2.2 Simulation before side effects

Before execution, the system should preview likely outputs, estimate latency/cost, and indicate whether approval is required.



\### 2.3 Service decomposition

Assistant capabilities should be decomposed into logical services:

\- orchestration

\- policy

\- simulation

\- memory

\- connectors

\- observability

\- evaluation



\### 2.4 Traceability

Every important workflow stage should generate structured trace events for inspection and debugging.



\### 2.5 Safe extensibility

The prototype should support richer integrations over time while remaining stable in mock-safe mode.



\---



\## 3. Deployment Model



\### 3.1 Frontend

\- \*\*Framework:\*\* Next.js + TypeScript + Tailwind CSS

\- \*\*Responsibility:\*\* request composition, workflow inspection, approvals, trace, connectors, evaluations, and settings UI



\### 3.2 Backend

\- \*\*Framework:\*\* FastAPI

\- \*\*Responsibility:\*\* orchestration, planning, policy review, simulation, execution, observability, memory retrieval, connector access, and evaluation



\### 3.3 Data layer

\- \*\*Default database:\*\* SQLite

\- \*\*Compatibility:\*\* PostgreSQL-compatible via `DATABASE\_URL`



The backend uses one application process and one database, but the code is structured as a \*\*logical microservice architecture\*\*.



\---



\## 4. Logical Services



\## 4.1 Orchestration Service

\*\*Purpose:\*\* Convert user requests into structured multi-step workflows.



\*\*Responsibilities:\*\*

\- accept workflow requests

\- retrieve scoped memory context

\- call the planner provider

\- create structured workflow steps

\- coordinate simulation and execution



\*\*Key modules:\*\*

\- `planner.py`

\- `provider.py`

\- `executor.py`

\- `workflows.py`



The current planner is a \*\*richer deterministic planner\*\*, not yet a full LLM-backed planner.



\---



\## 4.2 Policy Engine

\*\*Purpose:\*\* Decide whether an action is allowed, blocked, or approval-required.



\*\*Responsibilities:\*\*

\- assign risk levels

\- enforce action-level policy rules

\- support safe-by-default behavior for risky actions



\*\*Examples:\*\*

\- `email.draft` → medium / allowed

\- `email.send` → high / blocked by default

\- `calendar.create\_event` → high / approval required



\*\*Key modules:\*\*

\- `engine.py`

\- `rule\_loader.py`



\---



\## 4.3 Simulation Service

\*\*Purpose:\*\* Perform a dry run before execution.



\*\*Responsibilities:\*\*

\- produce step previews

\- estimate latency

\- estimate cost

\- summarize side effects

\- indicate approval-gated steps



\*\*Key module:\*\*

\- `simulator.py`



The current simulation layer is prototype-grade and uses lightweight preview logic, but it is still useful for demonstrating simulation-first execution.



\---



\## 4.4 Connector Services

\*\*Purpose:\*\* Wrap external or mock-safe capabilities behind stable interfaces.



\*\*Current connectors:\*\*

\- GitHub

\- Email

\- Calendar

\- Task



\*\*Responsibilities:\*\*

\- expose `health\_check()`

\- expose `simulate()`

\- expose `execute()`



\*\*Current connector modes:\*\*

\- GitHub: mock by default, optional live-readonly mode when token is available

\- Email draft: mock-safe

\- Email send: blocked by policy by default

\- Calendar: mock-safe

\- Task: mock-safe



\*\*Key modules:\*\*

\- `base.py`

\- `github\_connector.py`

\- `email\_connector.py`

\- `calendar\_connector.py`

\- `task\_connector.py`



\---



\## 4.5 Memory Service

\*\*Purpose:\*\* Provide user-specific context to planning and execution.



\*\*Responsibilities:\*\*

\- store memory items per user

\- retrieve relevant memory for a request

\- support memory-aware planning

\- support payload-aware execution



\*\*Examples of memory-backed values:\*\*

\- preferred meeting time

\- default email recipient

\- configured repository

\- default event title



\*\*Key modules:\*\*

\- `manager.py`

\- `scorer.py`



The current memory retrieval is lightweight and deterministic, but memory is now used to influence planning and connector payloads.



\---



\## 4.6 Observability Service

\*\*Purpose:\*\* Make workflow behavior inspectable.



\*\*Responsibilities:\*\*

\- record lifecycle events

\- store event metadata

\- support trace inspection

\- support simple execution metrics



\*\*Trace captures:\*\*

\- stage

\- event type

\- message

\- metadata

\- timestamp



\*\*Key modules:\*\*

\- `tracer.py`

\- `event\_logger.py`

\- `metrics.py`



\---



\## 4.7 Evaluation Service

\*\*Purpose:\*\* Run benchmark prompts through the workflow engine.



\*\*Responsibilities:\*\*

\- load dataset prompts

\- run the workflow pipeline in mock-safe mode

\- grade outcomes

\- summarize metrics



\*\*Current datasets:\*\*

\- `productivity\_prompts`

\- `risky\_action\_prompts`

\- `failure\_injection\_prompts`



\*\*Current metrics:\*\*

\- task completion rate

\- partial completion rate

\- policy correctness

\- average latency

\- failure recovery rate



\*\*Key modules:\*\*

\- `dataset\_runner.py`

\- `graders.py`

\- `report\_generator.py`



The evaluation layer is now workflow-engine based, but it is still prototype-grade rather than research-grade.



\---



\## 5. End-to-End Control Flow



The current control flow is:



1\. \*\*Request intake\*\*  

&#x20;  User submits a natural-language request from the dashboard.



2\. \*\*Memory retrieval\*\*  

&#x20;  The backend retrieves and scopes relevant memory for the request.



3\. \*\*Planning\*\*  

&#x20;  The planner generates structured steps with service names and action types.



4\. \*\*Policy review\*\*  

&#x20;  Each step is assigned a risk level and policy decision.



5\. \*\*Simulation\*\*  

&#x20;  The workflow is dry-run to estimate latency/cost and preview outputs.



6\. \*\*Approval gate\*\*  

&#x20;  Risky actions that require approval are routed through the Approval Center.



7\. \*\*Execution\*\*  

&#x20;  Approved or allowed steps are executed through the connector layer.



8\. \*\*Trace + metrics\*\*  

&#x20;  Trace events are recorded throughout the workflow lifecycle.



\---



\## 6. Memory-Aware Planning



One of the important architectural upgrades is that planning is no longer based only on raw request text.



The planner can now use scoped memory context to improve step generation.



Examples:

\- remembered repository name → more specific GitHub step naming

\- remembered email recipient → more specific email drafting

\- remembered preferred meeting time → more contextual calendar planning

\- remembered event title → more specific event creation labels



This makes the PA behavior feel more personalized while keeping the planner deterministic and stable.



\---



\## 7. Payload-Aware Execution



Another important architectural improvement is that connectors no longer execute with empty payloads.



Structured execution payloads can include:

\- request text

\- repo name

\- meeting preferences

\- email subject/body/recipient

\- event title/time hint

\- memory context



This matters because it makes the connector layer a more realistic service abstraction and prepares the architecture for selective live integrations.



\---



\## 8. Governance Model



The core architectural differentiator of this project is \*\*governed execution\*\*.



The system does not simply decide “what to do.” It also decides:



\- whether an action is low/medium/high risk

\- whether it should be allowed immediately

\- whether it should be blocked

\- whether it should require approval first



\### Example governance behavior

\- `email.draft` → allowed

\- `email.send` → blocked by default

\- `calendar.create\_event` → approval required



This makes the system better suited for realistic personal-assistant scenarios, where side effects must be controlled.



\---



\## 9. Evaluation Architecture



The evaluation engine is designed to test the workflow system, not just a model response.



For each dataset prompt, the backend can:

1\. generate a plan

2\. apply policy decisions

3\. simulate execution

4\. execute allowed steps in mock-safe mode

5\. compute aggregate metrics



This is useful even without full live integrations, because it evaluates:

\- workflow correctness

\- policy correctness

\- completion behavior

\- resilience against hard failure



