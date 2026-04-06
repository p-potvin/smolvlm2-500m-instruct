
import './tailwind.css';
import { WorkflowList } from './components/ui/WorkflowList';
import { Sidebar } from './components/ui/Sidebar';
import { Modal } from './components/ui/Modal';
import { ImageTools } from './components/features/ImageTools';
import { ImageCaptioning } from './components/features/ImageCaptioning';
import LoRATraining from './components/features/LoRATraining';

import { useEffect } from 'react';
import { fetchWorkflows, createWorkflow } from './api';
import { useDispatch, useSelector } from 'react-redux';
import { setWorkflows, setLoading, setError } from './store';


import { useState } from 'react';
import { workflowSchema } from './validation';
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    // Optionally log error to a service
  }
  render() {
    if (this.state.hasError) {
      return <div className="p-8 text-red-600">Something went wrong: {this.state.error?.message || 'Unknown error'}</div>;
    }
    return this.props.children;
  }
}

function App() {
  const dispatch = useDispatch();
  const workflows = useSelector((state) => state.workflows.items);
  const loading = useSelector((state) => state.workflows.loading);
  const error = useSelector((state) => state.workflows.error);
  const [category, setCategory] = useState('All');
  const [showCreate, setShowCreate] = useState(false);
  const [newName, setNewName] = useState('');
  const [newCategory, setNewCategory] = useState('');
  const [formError, setFormError] = useState('');

  const loadWorkflows = () => {
    dispatch(setLoading(true));
    fetchWorkflows()
      .then((data) => dispatch(setWorkflows(data)))
      .catch((err) => dispatch(setError(err.message)))
      .finally(() => dispatch(setLoading(false)));
  };
  useEffect(() => {
    loadWorkflows();
  }, [dispatch]);

  // Example categories (replace with dynamic if available)
  const categories = ['All', 'Data', 'ML', 'Reporting'];

  // Filter workflows by category if not 'All' (placeholder logic)
  const filtered = category === 'All' ? workflows : workflows.filter(wf => wf.category === category);

  const handleCreate = async () => {
    setFormError('');
    const result = workflowSchema.safeParse({ name: newName, category: newCategory });
    if (!result.success) {
      setFormError(result.error.errors[0]?.message || 'Invalid input');
      return;
    }
    try {
      await createWorkflow({ name: newName, category: newCategory });
      setShowCreate(false);
      setNewName('');
      setNewCategory('');
      loadWorkflows();
    } catch (err) {
      setFormError(err.message);
    }
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-vault-100 via-vault-50 to-gray-50 dark:from-vault-900 dark:via-gray-900 dark:to-gray-950">
      <header className="p-4 border-b border-vault-200 dark:border-vault-700 bg-vault-50 dark:bg-vault-900">
        <h1 className="text-3xl font-bold text-vault-900 dark:text-vault-100 font-vault">Workflow Manager</h1>
      </header>
      <div className="flex flex-col md:flex-row max-w-5xl mx-auto">
        <Sidebar categories={categories} onSelect={setCategory} selected={category} />
        <main className="flex-1 py-4 md:py-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Workflows</h2>
            <button
              className="px-4 py-2 rounded bg-vault-900 dark:bg-vault-100 text-white dark:text-vault-900 font-bold shadow hover:bg-vault-800 dark:hover:bg-vault-200"
              onClick={() => setShowCreate(true)}
            >
              + Create Workflow
            </button>
          </div>
          {loading ? (
            <div className="text-vault-500">Loading workflows...</div>
          ) : error ? (
            <div className="text-red-500">Error: {error}</div>
          ) : (
            <WorkflowList workflows={filtered} />
          )}

          {/* Image Tools Section */}
          <ImageTools />

          {/* Image Captioning/Tagging Section */}
          <ImageCaptioning />

          {/* LoRA Training Section */}
          <LoRATraining />
        </main>
      </div>
      <Modal open={showCreate} onClose={() => setShowCreate(false)} title="Create Workflow">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Name:</label>
          <input
            className="w-full border rounded px-2 py-1 dark:bg-gray-900 dark:text-gray-100"
            value={newName}
            onChange={e => setNewName(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Category:</label>
          <input
            className="w-full border rounded px-2 py-1 dark:bg-gray-900 dark:text-gray-100"
            value={newCategory}
            onChange={e => setNewCategory(e.target.value)}
          />
        </div>
        {formError && <div className="text-red-500 mb-2">{formError}</div>}
        <div className="flex justify-end space-x-2">
          <button className="px-4 py-1 rounded bg-vault-200 dark:bg-vault-700 text-vault-900 dark:text-vault-100" onClick={() => setShowCreate(false)}>Cancel</button>
          <button
            className="px-4 py-1 rounded bg-vault-900 dark:bg-vault-100 text-white dark:text-vault-900 font-bold"
            onClick={handleCreate}
            disabled={!newName.trim()}
          >
            Create
          </button>
        </div>
      </Modal>
      </div>
    </ErrorBoundary>
  );
}

export default App;
