import nats
from nats.aio.client import Client
from nats.js import JetStreamContext


async def connect_to_nats(servers: list[str]) -> tuple[Client, JetStreamContext]:
    nc: Client = await nats.connect(
        servers,
        connect_timeout=10,
        reconnect_time_wait=1,
    )
    js: JetStreamContext = nc.jetstream(timeout=20)

    return nc, js
