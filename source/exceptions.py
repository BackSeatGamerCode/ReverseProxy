class ReverseProxyException(Exception):
    pass


class FailedToConnectException(ReverseProxyException):
    pass


class ReturnToHomeException(ReverseProxyException):
    pass
