import asyncio

from src.broker.broker_bridge import BrokerBridge


async def main():
    await BrokerBridge().consumer_process()

if __name__ == "__main__":
    asyncio.run(main())
