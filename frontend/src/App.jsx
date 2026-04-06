
import './tailwind.css';
import { WorkflowList } from './WorkflowList';
import { Sidebar } from './Sidebar';

import { useEffect } from 'react';
import { fetchWorkflows } from './api';
import { useDispatch, useSelector } from 'react-redux';
import { setWorkflows, setLoading, setError } from './store';


import { useState } from 'react';

function App() {
  const dispatch = useDispatch();
  const workflows = useSelector((state) => state.workflows.items);
  const loading = useSelector((state) => state.workflows.loading);
  const error = useSelector((state) => state.workflows.error);
  const [category, setCategory] = useState('All');

  useEffect(() => {
    dispatch(setLoading(true));
    fetchWorkflows()
      .then((data) => dispatch(setWorkflows(data)))
      .catch((err) => dispatch(setError(err.message)))
      .finally(() => dispatch(setLoading(false)));
  }, [dispatch]);

  // Example categories (replace with dynamic if available)
  const categories = ['All', 'Data', 'ML', 'Reporting'];

  // Filter workflows by category if not 'All' (placeholder logic)
  const filtered = category === 'All' ? workflows : workflows.filter(wf => wf.category === category);

  return (
    <div className="min-h-screen bg-gradient-to-br from-vault-100 via-vault-50 to-gray-50 dark:from-vault-900 dark:via-gray-900 dark:to-gray-950">
      <header className="p-4 border-b border-vault-200 dark:border-vault-700 bg-vault-50 dark:bg-vault-900">
        <h1 className="text-3xl font-bold text-vault-900 dark:text-vault-100 font-vault">Workflow Manager</h1>
      </header>
      <div className="flex flex-col md:flex-row max-w-5xl mx-auto">
        <Sidebar categories={categories} onSelect={setCategory} selected={category} />
        <main className="flex-1 py-4 md:py-8">
          {loading ? (
            <div className="text-vault-500">Loading workflows...</div>
          ) : error ? (
            <div className="text-red-500">Error: {error}</div>
          ) : (
            <WorkflowList workflows={filtered} />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
