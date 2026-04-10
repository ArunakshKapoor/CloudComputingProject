import { API_BASE } from "./constants";

async function req(path: string, init?: RequestInit) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}

export const api = {
  createWorkflow: (payload: { request_text: string; user_id?: string; mode?: string }) => req("/workflows", { method: "POST", body: JSON.stringify(payload) }),
  listWorkflows: () => req("/workflows"),
  getWorkflow: (id: string) => req(`/workflows/${id}`),
  planWorkflow: (id: string) => req(`/workflows/${id}/plan`, { method: "POST" }),
  simulateWorkflow: (id: string) => req(`/workflows/${id}/simulate`, { method: "POST" }),
  executeWorkflow: (id: string) => req(`/workflows/${id}/execute`, { method: "POST" }),
  listMemory: () => req(`/memory?user_id=demo-user`),
  listPolicies: () => req(`/policies`),
  listConnectors: () => req(`/connectors`),
  listApprovals: (id: string) => req(`/workflows/${id}/approvals`),
  decideApproval: (stepId: string, status: string) => req(`/approvals/${stepId}`, { method: "POST", body: JSON.stringify({ status }) }),
  trace: (id: string) => req(`/workflows/${id}/trace`),
  runEval: (dataset: string) => req("/evaluations/run", { method: "POST", body: JSON.stringify({ dataset }) }),
};
