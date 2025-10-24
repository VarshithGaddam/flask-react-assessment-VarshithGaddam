from modules.comment.comment_service import CommentService
from modules.comment.errors import CommentNotFoundError, CommentTaskNotFoundError
from modules.comment.types import (
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    UpdateCommentParams,
)
from modules.application.common.types import PaginationParams
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentService(BaseTestComment):
    def test_create_comment_success(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        
        # Test
        comment = CommentService.create_comment(
            params=CreateCommentParams(
                account_id=account.id,
                task_id=task.id,
                content="Test comment content"
            )
        )
        
        # Assertions
        assert comment.id is not None
        assert comment.task_id == task.id
        assert comment.account_id == account.id
        assert comment.content == "Test comment content"
        assert comment.created_at is not None
        assert comment.updated_at is not None

    def test_create_comment_task_not_found(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        
        # Test & Assert
        try:
            CommentService.create_comment(
                params=CreateCommentParams(
                    account_id=account.id,
                    task_id=fake_task_id,
                    content="Test comment content"
                )
            )
            assert False, "Expected CommentTaskNotFoundError"
        except CommentTaskNotFoundError:
            pass

    def test_get_comment_success(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        created_comment = self.create_test_comment(account.id, task.id, "Original content")
        
        # Test
        retrieved_comment = CommentService.get_comment(
            params=GetCommentParams(
                account_id=account.id,
                task_id=task.id,
                comment_id=created_comment.id
            )
        )
        
        # Assertions
        assert retrieved_comment.id == created_comment.id
        assert retrieved_comment.task_id == task.id
        assert retrieved_comment.account_id == account.id
        assert retrieved_comment.content == "Original content"

    def test_get_comment_not_found(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        # Test & Assert
        try:
            CommentService.get_comment(
                params=GetCommentParams(
                    account_id=account.id,
                    task_id=task.id,
                    comment_id=fake_comment_id
                )
            )
            assert False, "Expected CommentNotFoundError"
        except CommentNotFoundError:
            pass

    def test_get_comment_task_not_found(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        fake_comment_id = "507f1f77bcf86cd799439012"
        
        # Test & Assert
        try:
            CommentService.get_comment(
                params=GetCommentParams(
                    account_id=account.id,
                    task_id=fake_task_id,
                    comment_id=fake_comment_id
                )
            )
            assert False, "Expected CommentTaskNotFoundError"
        except CommentTaskNotFoundError:
            pass

    def test_get_paginated_comments_success(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comments = self.create_multiple_test_comments(account.id, task.id, 5)
        
        # Test
        pagination_result = CommentService.get_paginated_comments(
            params=GetPaginatedCommentsParams(
                account_id=account.id,
                task_id=task.id,
                pagination_params=PaginationParams(page=1, size=10, offset=0)
            )
        )
        
        # Assertions
        assert len(pagination_result.items) == 5
        assert pagination_result.total_count == 5
        assert pagination_result.pagination_params.page == 1
        assert pagination_result.pagination_params.size == 10

    def test_get_paginated_comments_task_not_found(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        
        # Test & Assert
        try:
            CommentService.get_paginated_comments(
                params=GetPaginatedCommentsParams(
                    account_id=account.id,
                    task_id=fake_task_id,
                    pagination_params=PaginationParams(page=1, size=10, offset=0)
                )
            )
            assert False, "Expected CommentTaskNotFoundError"
        except CommentTaskNotFoundError:
            pass

    def test_update_comment_success(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id, "Original content")
        
        # Test
        updated_comment = CommentService.update_comment(
            params=UpdateCommentParams(
                account_id=account.id,
                task_id=task.id,
                comment_id=comment.id,
                content="Updated content"
            )
        )
        
        # Assertions
        assert updated_comment.id == comment.id
        assert updated_comment.content == "Updated content"
        assert updated_comment.updated_at != comment.updated_at

    def test_update_comment_not_found(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        # Test & Assert
        try:
            CommentService.update_comment(
                params=UpdateCommentParams(
                    account_id=account.id,
                    task_id=task.id,
                    comment_id=fake_comment_id,
                    content="Updated content"
                )
            )
            assert False, "Expected CommentNotFoundError"
        except CommentNotFoundError:
            pass

    def test_update_comment_task_not_found(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        fake_comment_id = "507f1f77bcf86cd799439012"
        
        # Test & Assert
        try:
            CommentService.update_comment(
                params=UpdateCommentParams(
                    account_id=account.id,
                    task_id=fake_task_id,
                    comment_id=fake_comment_id,
                    content="Updated content"
                )
            )
            assert False, "Expected CommentTaskNotFoundError"
        except CommentTaskNotFoundError:
            pass

    def test_delete_comment_success(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id)
        
        # Test
        deletion_result = CommentService.delete_comment(
            params=DeleteCommentParams(
                account_id=account.id,
                task_id=task.id,
                comment_id=comment.id
            )
        )
        
        # Assertions
        assert deletion_result.success is True
        assert deletion_result.comment_id == comment.id
        assert deletion_result.deleted_at is not None
        
        # Verify comment is soft deleted
        try:
            CommentService.get_comment(
                params=GetCommentParams(
                    account_id=account.id,
                    task_id=task.id,
                    comment_id=comment.id
                )
            )
            assert False, "Expected CommentNotFoundError after deletion"
        except CommentNotFoundError:
            pass

    def test_delete_comment_not_found(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        # Test & Assert
        try:
            CommentService.delete_comment(
                params=DeleteCommentParams(
                    account_id=account.id,
                    task_id=task.id,
                    comment_id=fake_comment_id
                )
            )
            assert False, "Expected CommentNotFoundError"
        except CommentNotFoundError:
            pass

    def test_delete_comment_task_not_found(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        fake_comment_id = "507f1f77bcf86cd799439012"
        
        # Test & Assert
        try:
            CommentService.delete_comment(
                params=DeleteCommentParams(
                    account_id=account.id,
                    task_id=fake_task_id,
                    comment_id=fake_comment_id
                )
            )
            assert False, "Expected CommentTaskNotFoundError"
        except CommentTaskNotFoundError:
            pass