from modules.application.errors import ApplicationError
from modules.comment.types import CommentErrorCode


class CommentError(ApplicationError):
    pass


class CommentNotFoundError(CommentError):
    def __init__(self, *, comment_id: str) -> None:
        super().__init__(
            error_code=CommentErrorCode.NOT_FOUND,
            message=f"Comment with id {comment_id} not found",
            status_code=404,
        )


class CommentBadRequestError(CommentError):
    def __init__(self, message: str) -> None:
        super().__init__(
            error_code=CommentErrorCode.BAD_REQUEST,
            message=message,
            status_code=400,
        )


class CommentTaskNotFoundError(CommentError):
    def __init__(self, *, task_id: str) -> None:
        super().__init__(
            error_code=CommentErrorCode.TASK_NOT_FOUND,
            message=f"Task with id {task_id} not found",
            status_code=404,
        )