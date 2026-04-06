// Simple API client for workflow backend
export async function fetchWorkflows() {
  const resp = await fetch('/api/workflows');
  if (!resp.ok) throw new Error('Failed to fetch workflows');
  return resp.json();
}

export async function createWorkflow(data) {
  const resp = await fetch('/api/workflows', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!resp.ok) throw new Error('Failed to create workflow');
  return resp.json();
}

// Add more API methods as needed (update, delete, etc.)
