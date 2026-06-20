class OdeError(Exception):
    pass


class GuardRejectedError(OdeError):
    pass


class HttpError(OdeError):
    def __init__(self, status: int, url: str) -> None:
        super().__init__(f"HTTP {status} while requesting {url}.")
        self.status = status
        self.url = url


class ConnectionError(OdeError):
    def __init__(self, url: str, detail: str | None = None) -> None:
        message = f"Unable to reach {url}."
        if detail:
            message = f"{message} {detail}"
        super().__init__(message)
        self.url = url


class UnexpectedResponseError(OdeError):
    pass
