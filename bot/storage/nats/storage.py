from __future__ import annotations

from typing import Any, Optional, Callable

import orjson
from aiogram.filters.state import StateType
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    DefaultKeyBuilder,
    KeyBuilder,
    StorageKey,
)
from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.api import KeyValueConfig, StorageType
from nats.js.errors import NotFoundError
from nats.js.kv import KeyValue


class NatsStorage(BaseStorage):
    nc: Client
    js: JetStreamContext
    _key_builder: KeyBuilder
    fsm_states_bucket: str
    fsm_data_bucket: str
    kv_states: KeyValue
    kv_data: KeyValue
    loads: Callable[[bytes], Any | None]
    dumps: Callable[[Any], bytes]

    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            key_builder: Optional[KeyBuilder] = None,
            fsm_states_bucket: str = 'fsm_states_aiogram',
            fsm_data_bucket: str = 'fsm_data_aiogram',
            loads=orjson.loads,
            dumps=orjson.dumps,
            decode_error=orjson.JSONDecodeError
    ) -> None:

        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.nc = nc
        self.js = js
        self.fsm_states_bucket = fsm_states_bucket
        self.fsm_data_bucket = fsm_data_bucket
        self._key_builder = key_builder
        self.loads = loads
        self.dumps = dumps
        self.decode_error = decode_error

    @staticmethod
    async def init(
            nc: Client,
            js: JetStreamContext,
            key_builder: Optional[KeyBuilder] = None,
            fsm_states_bucket: str = 'fsm_states_aiogram',
            fsm_data_bucket: str = 'fsm_data_aiogram',
            loads=orjson.loads,
            dumps=orjson.dumps,
    ) -> NatsStorage:
        self = NatsStorage(nc, js, key_builder, fsm_states_bucket, fsm_data_bucket, loads, dumps)

        self.kv_states = await self._get_kv_states()  # type: ignore
        self.kv_data = await self._get_kv_data()  # type: ignore

        return self

    async def _get_kv_states(self) -> KeyValue:
        return await self.js.create_key_value(
            config=KeyValueConfig(
                bucket=self.fsm_states_bucket,
                # history=5,
                storage=StorageType.FILE
            )
        )

    async def _get_kv_data(self) -> KeyValue:
        return await self.js.create_key_value(
            config=KeyValueConfig(
                bucket=self.fsm_data_bucket,
                # history=5,
                storage=StorageType.FILE
            )
        )

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        state = state.state if isinstance(state, State) else state
        await self.kv_states.put(
            self._key_builder.build(key), self.dumps(state)
        )

    async def get_state(self, key: StorageKey) -> Optional[str]:
        try:
            entry = await self.kv_states.get(self._key_builder.build(key))
            data = self.loads(entry.value)  # type: ignore
        except (NotFoundError, self.decode_error):
            return None
        return data

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        await self.kv_data.put(self._key_builder.build(key), self.dumps(data))

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        try:
            entry = await self.kv_data.get(self._key_builder.build(key))
            return self.loads(entry.value)  # type: ignore
        except (NotFoundError, self.decode_error):
            return {}

    async def close(self) -> None:
        await self.nc.close()
