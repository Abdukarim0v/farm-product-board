import { createClient } from "redis";

const REDIS_HOST = process.env.REDIS_HOST || "redis";
const REDIS_PORT = process.env.REDIS_PORT || "6379";
const QUEUE_NAME = process.env.QUEUE_NAME || "order_events";

const client = createClient({
    url: `redis://${REDIS_HOST}:${REDIS_PORT}`
});

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

async function run() {
    await client.connect();
    console.log("Notifier started. Waiting for orders...");

    while (true) {
        const res = await client.blPop(QUEUE_NAME, 5);
        if (!res) continue;

        const order = JSON.parse(res.element);
        console.log(
            `[NOTIFY] To: ${order.to} | Order ${order.orderId} | ${order.product} x${order.qty} | Buyer: ${order.buyer}`
        );

        await sleep(200);
    }
}

run().catch(err => {
    console.error("Notifier error:", err);
    process.exit(1);
});
