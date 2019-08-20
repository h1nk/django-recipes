import msgpack

__all__ = (
    'MsgPackSerializer',
)


class MsgPackSerializer:
    """
    Simple wrapper for MsgPack to be used in :meth:`signing.dumps <django.core.signing.dumps>` and
    :meth:`signing.loads <django.core.signing.dumps>`.
    """

    @staticmethod
    def dumps(obj):
        return msgpack.dumps(obj)

    @staticmethod
    def loads(data):
        return msgpack.loads(data)
