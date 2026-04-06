import { configureStore, createSlice } from '@reduxjs/toolkit';

const workflowsSlice = createSlice({
  name: 'workflows',
  initialState: {
    items: [],
    loading: false,
    error: null,
  },
  reducers: {
    setWorkflows(state, action) {
      state.items = action.payload;
    },
    setLoading(state, action) {
      state.loading = action.payload;
    },
    setError(state, action) {
      state.error = action.payload;
    },
  },
});

export const { setWorkflows, setLoading, setError } = workflowsSlice.actions;

export const store = configureStore({
  reducer: {
    workflows: workflowsSlice.reducer,
  },
});
