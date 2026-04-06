import { z } from 'zod';

export const workflowSchema = z.object({
  name: z.string().min(2, 'Name is required'),
  // Add more fields as needed
});
