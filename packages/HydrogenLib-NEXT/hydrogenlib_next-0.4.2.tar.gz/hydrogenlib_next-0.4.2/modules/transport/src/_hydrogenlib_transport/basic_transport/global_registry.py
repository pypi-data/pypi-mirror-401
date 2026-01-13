registry = {}


def register_socket_protocol(proto: str):
    def decorator(cls):
        registry[proto] = cls
        return cls
    return decorator


def get_protocol(proto: str):
    return registry.get(proto)
