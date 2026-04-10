export type Workflow = {
  id: string;
  status: string;
  request_text: string;
  estimated_cost_usd: number;
  estimated_latency_ms: number;
  steps: any[];
};
