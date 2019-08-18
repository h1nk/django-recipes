import msgpack


class MsgPackSerializer:
    """Simple wrapper for MsgPack to be used in ``signing.dumps`` and ``signing.loads``."""

    @staticmethod
    def dumps(obj):
        return msgpack.dumps(obj)

    @staticmethod
    def loads(data):
        return msgpack.loads(data)
