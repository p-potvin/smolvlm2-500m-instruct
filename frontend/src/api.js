// Simple API client for workflow backend

export async function fetchWorkflows() {
  const res = await fetch('/api/workflows');
  if (!res.ok) throw new Error('Failed to fetch workflows');
  return res.json();
}

export async function createWorkflow({ name, category }) {
  const res = await fetch('/api/workflows', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, category })
  });
  if (!res.ok) throw new Error('Failed to create workflow');
  return res.json();
}
// Add more API methods as needed (update, delete, etc.)
