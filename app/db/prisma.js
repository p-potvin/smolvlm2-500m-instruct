import "dotenv/config";

import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../generated-prisma-client/index.js";

const prismaEnabled = process.env.PRISMA_ENABLED === "1";
const connectionString = process.env.DATABASE_URL?.trim();

/**
 * Optional Prisma client (off by default).
 * - Enable with `PRISMA_ENABLED=1` and a valid `DATABASE_URL`.
 * - When disabled, exports `null`.
 */
const prisma =
  prismaEnabled && connectionString
    ? new PrismaClient({ adapter: new PrismaPg({ connectionString }) })
    : null;

function requirePrisma() {
  if (!prisma) {
    throw new Error(
      "Prisma is disabled. Set PRISMA_ENABLED=1 and DATABASE_URL, then run `npm run prisma:generate`.",
    );
  }
  return prisma;
}

export { prisma, requirePrisma };

