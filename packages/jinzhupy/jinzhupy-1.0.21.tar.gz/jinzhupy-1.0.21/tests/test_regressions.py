import asyncio
import json
import unittest
from unittest.mock import AsyncMock, patch

from jinzhupy.amqplib.defs import RabbitMQConnectionConfig
from jinzhupy.amqplib.rabbitmq import AsyncRabbitMQClient
from jinzhupy.redis import RedisManger
from jinzhupy.tools.query_builder import GenericQueryBuilder


class TestQueryBuilder(unittest.TestCase):
    def test_add_time_range_allows_zero(self):
        builder = GenericQueryBuilder()
        builder.add_time_range(0, 0, "ts")
        self.assertIn("1970", builder.year_specific_conditions)
        conditions = builder.year_specific_conditions["1970"]
        self.assertEqual(1, len(conditions))
        self.assertEqual((0, 0), conditions[0].value)


class TestRedisManager(unittest.IsolatedAsyncioTestCase):
    @patch("jinzhupy.redis.__init__.aredis.ConnectionPool")
    @patch("jinzhupy.redis.__init__.aredis.StrictRedis")
    async def test_connect_uses_connection_pool(self, strict_redis, pool_cls):
        pool = object()
        pool_cls.return_value = pool
        manager = RedisManger()
        manager.connect({"host": "localhost", "port": 6379, "password": ""})
        strict_redis.assert_called_once()
        _, kwargs = strict_redis.call_args
        self.assertIn("connection_pool", kwargs)
        self.assertIs(pool, kwargs["connection_pool"])

    async def test_srem_normalizes_items(self):
        manager = RedisManger()
        manager.redis_con = AsyncMock()
        await manager.srem("key", [b"a", "b", 1])
        manager.redis_con.srem.assert_awaited_once()
        args, _ = manager.redis_con.srem.call_args
        self.assertEqual(b"a", args[1])
        self.assertEqual(b"b", args[2])
        self.assertEqual(b"1", args[3])


class TestRabbitMQClient(unittest.IsolatedAsyncioTestCase):
    async def test_ensure_connection_retries_with_limit(self):
        client = AsyncRabbitMQClient(RabbitMQConnectionConfig())
        client.close = AsyncMock()
        client.connect = AsyncMock(side_effect=RuntimeError("boom"))
        client.setup_infrastructure = AsyncMock()
        with self.assertRaises(RuntimeError):
            await client.ensure_connection()
        self.assertEqual(3, client.connect.call_count)

    @patch("jinzhupy.amqplib.rabbitmq.uuid.uuid4", return_value="fixed-id")
    async def test_rpc_call_consumes_with_ack(self, _uuid4):
        client = AsyncRabbitMQClient(RabbitMQConnectionConfig())
        client.ensure_connection = AsyncMock()
        client.publish = AsyncMock()

        callback_queue = AsyncMock()
        callback_queue.name = "cb"

        consumed = {}

        async def consume_side_effect(callback, no_ack=False, consumer_tag=None):
            consumed["no_ack"] = no_ack
            class FakeMessage:
                correlation_id = "fixed-id"
                content_type = "application/json"
                body = json.dumps({"ok": True}).encode()
                ack = AsyncMock()

            await callback(FakeMessage())

        callback_queue.consume.side_effect = consume_side_effect

        client._channel = AsyncMock()
        client._channel.declare_queue = AsyncMock(return_value=callback_queue)

        result = await client.rpc_call("ex", "rk", {"ping": 1}, timeout=1)
        self.assertEqual({"ok": True}, result)
        self.assertFalse(consumed.get("no_ack"))


if __name__ == "__main__":
    unittest.main()
