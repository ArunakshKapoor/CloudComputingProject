# Evaluation Plan

Datasets:
- productivity_prompts
- risky_action_prompts
- failure_injection_prompts

Metrics:
- task_completion_rate
- partial_completion_rate
- policy_correctness
- average_latency_ms
- failure_recovery_rate

Success criteria:
- deterministic completion for productivity prompts
- high-risk prompts blocked or approval-gated per policy
- no hard crashes in mock mode
