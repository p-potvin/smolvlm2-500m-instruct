import { requirePrisma } from "../db/prisma.js";

const prisma = requirePrisma();

const workflows = await prisma.workflow.findMany({
  take: 5,
  orderBy: { name: "asc" },
});

console.log({ count: workflows.length, workflows });

