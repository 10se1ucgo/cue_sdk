class CorsairError(Exception):
    """
    Base exception from which all Corsair SDK errors inherit from
    """


class ServerNotFound(CorsairError):
    """
    CUE is not running or was shut down or third-party control is disabled in CUE settings (runtime error)
    """


class NoControl(CorsairError):
    """
    if some other client has or took over exclusive control (runtime error)
    """


class ProtocolHandshakeMissing(CorsairError):
    """
    if developer did not perform protocol handshake (developer error)
    """


class IncompatibleProtocol(CorsairError):
    """
    if developer is calling the function that is not supported by the server
    (either because protocol has broken by server or client or because the function is new and server is too old.
    Check CorsairProtocolDetails for details) (developer error)
    """


class InvalidArguments(CorsairError):
    """
    if developer supplied invalid arguments to the function (for specifics look at function descriptions).
    (developer error)
    """
