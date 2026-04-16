\# Evaluation Plan



\## 1. Purpose



The goal of the evaluation layer is to assess how well \*\*LifeOS Control Plane\*\* performs as a \*\*governed Personal Assistant-as-a-Service system\*\*, rather than as a standalone chatbot.



Instead of evaluating text responses, the system evaluates:



\- workflow decomposition

\- policy correctness

\- execution outcomes

\- system robustness under different prompt types



The evaluation is \*\*workflow-engine based\*\*, meaning prompts are run through the actual planning, policy, simulation, and execution pipeline.



\---



\## 2. Evaluation Approach



For each prompt in a dataset, the system performs:



1\. \*\*Planning\*\*  

&#x20;  Generate structured workflow steps using the planner.



2\. \*\*Policy evaluation\*\*  

&#x20;  Assign risk levels and decisions (ALLOWED / BLOCKED / APPROVAL\_REQUIRED).



3\. \*\*Simulation\*\*  

&#x20;  Estimate latency and cost, and preview expected outputs.



4\. \*\*Execution (mock-safe mode)\*\*  

&#x20;  Execute steps through connectors using structured payloads.



5\. \*\*Outcome classification\*\*  

&#x20;  Determine whether the workflow is:

&#x20;  - COMPLETED

&#x20;  - PARTIALLY\_COMPLETED



6\. \*\*Metric computation\*\*  

&#x20;  Compute evaluation metrics based on actual workflow behavior.



This pipeline ensures that evaluation reflects \*\*system behavior\*\*, not just static scoring.



\---



\## 3. Evaluation Datasets



The system includes three datasets:



\### 3.1 Productivity Prompts

Focus: normal assistant tasks



Examples:

\- drafting emails

\- suggesting meeting slots

\- creating task checklists

\- summarizing GitHub issues



Expected behavior:

\- most steps should be allowed

\- workflows should complete successfully



\---



\### 3.2 Risky Action Prompts

Focus: governance and safety



Examples:

\- sending emails

\- creating calendar events

\- performing side-effect actions



Expected behavior:

\- high-risk actions should be:

&#x20; - blocked, or

&#x20; - approval-required

\- workflows may end as partially completed



This dataset is critical for evaluating \*\*policy correctness\*\*.



\---



\### 3.3 Failure Injection Prompts

Focus: robustness and resilience



Examples:

\- ambiguous requests

\- incomplete instructions

\- edge-case phrasing



Expected behavior:

\- system should not crash

\- workflow should degrade gracefully

\- trace should still be recorded



\---



\## 4. Metrics



The evaluation layer computes the following metrics:



\### 4.1 Task Completion Rate

Fraction of workflows that reach `COMPLETED`.



task\_completion\_rate = completed\_workflows / total\_workflows



\--



\### 4.2 Partial Completion Rate

Fraction of workflows that reach `PARTIALLY\_COMPLETED`.



partial\_completion\_rate = partially\_completed\_workflows / total\_workflows



This metric is particularly meaningful for \*\*risky datasets\*\*, where some actions are intentionally blocked.



\---



\### 4.3 Policy Correctness

Measures whether policy decisions align with expected behavior.



Examples:

\- `email.send` → should be BLOCKED

\- `calendar.create\_event` → should require APPROVAL



Policy correctness is evaluated per prompt based on:

\- presence of expected action types

\- correctness of policy decisions



\---



\### 4.4 Average Latency (ms)

Average estimated latency from simulation.



average\_latency\_ms = mean(simulated\_latency\_per\_workflow)



This reflects system complexity rather than real network latency.



\---



\### 4.5 Failure Recovery Rate

Measures robustness against execution failures.



failure\_recovery\_rate = 1 - (hard\_failures / total\_workflows)



A hard failure is defined as:

\- unhandled exception during execution

\- system crash for a prompt



\---



\## 5. Interpretation of Metrics



Metrics should be interpreted \*\*relative to dataset type\*\*:



| Dataset | Expected outcome |

|--------|--------|

| Productivity | High completion rate |

| Risky actions | Higher partial completion rate |

| Failure injection | High recovery rate |



Important:

\- A high partial completion rate is \*\*not necessarily bad\*\*

\- It can indicate correct enforcement of policy constraints



\---



\## 6. Limitations of Current Evaluation



The current evaluation is \*\*prototype-grade\*\*, with several limitations:



\- execution is mostly mock-safe (no full real-world side effects)

\- GitHub is the only connector with optional live-readonly mode

\- planner is deterministic rather than LLM-based

\- grading logic is rule-based rather than learned or statistical

\- datasets are small and manually curated



As a result, the evaluation should be interpreted as:



> a validation of system behavior and architecture, not a production benchmark



\---



\## 7. Why This Evaluation is Still Meaningful



Despite limitations, the evaluation is useful because it tests:



\- workflow decomposition quality

\- policy enforcement correctness

\- system stability under varied inputs

\- execution behavior across services

\- traceability and observability



This aligns directly with the project goal of demonstrating:



> a governed, simulation-first PA-as-a-Service system



\---



\## 8. Future Improvements



Potential improvements include:



\- LLM-based grading and semantic evaluation

\- larger and more diverse datasets

\- real integration testing (calendar, email draft)

\- connector-specific evaluation metrics

\- exportable evaluation reports for analysis

\- statistical benchmarking across multiple runs



\---



\## 9. Evaluation Positioning



This evaluation layer should be understood as:



> a workflow-level evaluation framework for governed assistant systems



rather than a traditional NLP benchmark.



Its primary purpose is to demonstrate that the system:



\- behaves correctly under policy constraints

\- handles risky actions safely

\- produces traceable and interpretable outcomes







