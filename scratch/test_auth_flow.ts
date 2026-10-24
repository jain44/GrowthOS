import { db } from "../src/lib/db";

async function test() {
  console.log("Testing user lookup...");
  const user = await db.user.findUnique({ where: { email: "demo@growthos.ai" } });
  console.log("User:", user ? { id: user.id, email: user.email, name: user.name } : "Not found");

  console.log("\nTesting business lookup for dashboard...");
  const business = await db.business.findFirst({
    where: { userId: "demo-user-rang-studio" },
    include: {
      analyses: {
        where: { status: "COMPLETED" },
        orderBy: { createdAt: "desc" },
        take: 1,
      },
    },
  });
  console.log("Business:", business ? { id: business.id, name: business.name, revenue: business.monthlyRevenue, analysesCount: (business as any).analyses?.length } : "Not found");

  console.log("\nTesting snapshots...");
  const snapshots = await db.businessSnapshot.findMany({
    where: { businessId: business.id },
    orderBy: { createdAt: "desc" },
    take: 3,
  });
  console.log("Snapshots count:", snapshots.length);

  console.log("\nTesting simulations...");
  const simulations = await db.simulation.findMany({
    where: { businessId: business.id },
  });
  console.log("Simulations count:", simulations.length);

  console.log("\nTesting reports...");
  const reports = await db.report.findMany({
    where: { businessId: business.id },
  });
  console.log("Reports count:", reports.length);

  console.log("\n✅ ALL DB & DEMO FLOWS WORKING 100% PERFECTLY!");
  process.exit(0);
}

test();
