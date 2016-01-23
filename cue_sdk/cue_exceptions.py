class ServerNotFound(Exception):
    """
    CUE is not running or was shut down or third-party control is disabled in CUE settings (runtime error)
    """
    pass


class NoControl(Exception):
    """
    if some other client has or took over exclusive control (runtime error)
    """
    pass


class ProtocolHandshakeMissing(Exception):
    """
    if developer did not perform protocol handshake (developer error)
    """
    pass


class IncompatibleProtocol(Exception):
    """
    if developer is calling the function that is not supported by the server
    (either because protocol has broken by server or client or because the function is new and server is too old.
    Check CorsairProtocolDetails for details) (developer error)
    """
    pass


class InvalidArguments(Exception):
    """
    if developer supplied invalid arguments to the function (for specifics look at function descriptions).
    (developer error)
    """
    pass
