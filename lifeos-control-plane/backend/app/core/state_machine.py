from app.core.enums import WorkflowStatus


ALLOWED_TRANSITIONS: dict[WorkflowStatus, set[WorkflowStatus]] = {
    WorkflowStatus.CREATED: {WorkflowStatus.PLANNING, WorkflowStatus.CANCELLED},
    WorkflowStatus.PLANNING: {WorkflowStatus.POLICY_REVIEW, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED},
    WorkflowStatus.POLICY_REVIEW: {WorkflowStatus.SIMULATING, WorkflowStatus.BLOCKED, WorkflowStatus.CANCELLED},
    WorkflowStatus.SIMULATING: {WorkflowStatus.WAITING_FOR_APPROVAL, WorkflowStatus.APPROVED_FOR_EXECUTION, WorkflowStatus.CANCELLED},
    WorkflowStatus.WAITING_FOR_APPROVAL: {WorkflowStatus.APPROVED_FOR_EXECUTION, WorkflowStatus.REJECTED, WorkflowStatus.CANCELLED},
    WorkflowStatus.APPROVED_FOR_EXECUTION: {WorkflowStatus.EXECUTING, WorkflowStatus.CANCELLED},
    WorkflowStatus.EXECUTING: {WorkflowStatus.COMPLETED, WorkflowStatus.PARTIALLY_COMPLETED, WorkflowStatus.FAILED},
    WorkflowStatus.COMPLETED: set(),
    WorkflowStatus.PARTIALLY_COMPLETED: set(),
    WorkflowStatus.FAILED: set(),
    WorkflowStatus.BLOCKED: set(),
    WorkflowStatus.REJECTED: set(),
    WorkflowStatus.CANCELLED: set(),
}


def can_transition(current: WorkflowStatus, target: WorkflowStatus) -> bool:
    return target in ALLOWED_TRANSITIONS[current]
