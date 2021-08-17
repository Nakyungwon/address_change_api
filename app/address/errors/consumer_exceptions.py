class ConsumerException(AssertionError):
    status: bool
    code: str
    msg: str
    detail: str
    ex: AssertionError

    def __init__(
        self,
        *,
        msg: str = None,
        status: bool = False,
        ex: AssertionError = None,
    ):
        self.status = status
        self.msg = msg
        self.ex = ex
        super().__init__(ex)


class SiteEnterException(ConsumerException):
    def __init__(self, msg: str = "사이트 진입 실패", ex: AssertionError = None):
        super().__init__(
            msg=msg,
            ex=ex
        )


class LoginException(ConsumerException):
    def __init__(self, ex: AssertionError = None):
        super().__init__(
            msg="로그인 실패",
            ex=ex
        )
