from random import getrandbits
from ipaddress import ip_address

from django.core import signing
from django.test import TestCase

from django_recipes import MsgPackSerializer


class TestMsgPackSerializer(TestCase):
    def test_msgpack_serializer_for_signing(self):
        data = [getrandbits(64), int(ip_address(getrandbits(32)))]

        msgpack_data = signing.dumps(data, serializer=MsgPackSerializer)
        msgpack_data = msgpack_data.replace(':', '.')

        json_data = signing.dumps(data)

        self.assertLessEqual(len(msgpack_data), len(json_data))
        self.assertEqual(data, signing.loads(msgpack_data.replace('.', ':'), serializer=MsgPackSerializer))
