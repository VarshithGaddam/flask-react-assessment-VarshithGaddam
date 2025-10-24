from modules.comment.types import CommentErrorCode
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentApi(BaseTestComment):
    
    # CREATE COMMENT TESTS
    
    def test_create_comment_success(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment_data = {"content": "This is a test comment"}
        
        # Test
        response = self.make_authenticated_request(
            "POST", account.id, task.id, token, data=comment_data
        )
        
        # Assertions
        assert response.status_code == 201
        self.assert_comment_response(
            response.json, 
            task_id=task.id, 
            account_id=account.id, 
            content="This is a test comment"
        )

    def test_create_comment_missing_content(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment_data = {}
        
        # Test
        response = self.make_authenticated_request(
            "POST", account.id, task.id, token, data=comment_data
        )
        
        # Assertions
        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

    def test_create_comment_empty_content(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment_data = {"content": ""}
        
        # Test
        response = self.make_authenticated_request(
            "POST", account.id, task.id, token, data=comment_data
        )
        
        # Assertions
        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

    def test_create_comment_no_request_body(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        
        # Test
        response = self.make_authenticated_request(
            "POST", account.id, task.id, token, data=None
        )
        
        # Assertions
        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

    def test_create_comment_task_not_found(self):
        # Setup
        account, token = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        comment_data = {"content": "This is a test comment"}
        
        # Test
        response = self.make_authenticated_request(
            "POST", account.id, fake_task_id, token, data=comment_data
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.TASK_NOT_FOUND)

    def test_create_comment_unauthenticated(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment_data = {"content": "This is a test comment"}
        
        # Test
        response = self.make_unauthenticated_request(
            "POST", account.id, task.id, data=comment_data
        )
        
        # Assertions
        assert response.status_code == 401

    def test_create_comment_cross_account_access(self):
        # Setup
        account1, token1 = self.create_account_and_get_token("user1@test.com")
        account2, _ = self.create_account_and_get_token("user2@test.com")
        task = self.create_test_task(account2.id)
        comment_data = {"content": "This is a test comment"}
        
        # Test
        response = self.make_cross_account_request(
            "POST", account2.id, task.id, token1, data=comment_data
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.TASK_NOT_FOUND)

    # GET SINGLE COMMENT TESTS
    
    def test_get_comment_success(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id, "Test comment content")
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, task.id, token, comment_id=comment.id
        )
        
        # Assertions
        assert response.status_code == 200
        self.assert_comment_response(response.json, expected_comment=comment)

    def test_get_comment_not_found(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, task.id, token, comment_id=fake_comment_id
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_get_comment_task_not_found(self):
        # Setup
        account, token = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        fake_comment_id = "507f1f77bcf86cd799439012"
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, fake_task_id, token, comment_id=fake_comment_id
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.TASK_NOT_FOUND)

    def test_get_comment_unauthenticated(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id)
        
        # Test
        response = self.make_unauthenticated_request(
            "GET", account.id, task.id, comment_id=comment.id
        )
        
        # Assertions
        assert response.status_code == 401

    # GET PAGINATED COMMENTS TESTS
    
    def test_get_paginated_comments_success(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comments = self.create_multiple_test_comments(account.id, task.id, 3)
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, task.id, token
        )
        
        # Assertions
        assert response.status_code == 200
        self.assert_pagination_response(
            response.json, 
            expected_items_count=3, 
            expected_total_count=3
        )

    def test_get_paginated_comments_with_pagination(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comments = self.create_multiple_test_comments(account.id, task.id, 5)
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, task.id, token, query_params="page=1&size=2"
        )
        
        # Assertions
        assert response.status_code == 200
        self.assert_pagination_response(
            response.json, 
            expected_items_count=2, 
            expected_total_count=5,
            expected_page=1,
            expected_size=2
        )

    def test_get_paginated_comments_empty_result(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, task.id, token
        )
        
        # Assertions
        assert response.status_code == 200
        self.assert_pagination_response(
            response.json, 
            expected_items_count=0, 
            expected_total_count=0
        )

    def test_get_paginated_comments_invalid_page(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, task.id, token, query_params="page=0"
        )
        
        # Assertions
        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

    def test_get_paginated_comments_invalid_size(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, task.id, token, query_params="size=0"
        )
        
        # Assertions
        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

    def test_get_paginated_comments_task_not_found(self):
        # Setup
        account, token = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        
        # Test
        response = self.make_authenticated_request(
            "GET", account.id, fake_task_id, token
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.TASK_NOT_FOUND)

    def test_get_paginated_comments_unauthenticated(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        
        # Test
        response = self.make_unauthenticated_request(
            "GET", account.id, task.id
        )
        
        # Assertions
        assert response.status_code == 401

    # UPDATE COMMENT TESTS
    
    def test_update_comment_success(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id, "Original content")
        update_data = {"content": "Updated content"}
        
        # Test
        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=comment.id, data=update_data
        )
        
        # Assertions
        assert response.status_code == 200
        self.assert_comment_response(
            response.json, 
            id=comment.id,
            content="Updated content"
        )

    def test_update_comment_missing_content(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id)
        update_data = {}
        
        # Test
        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=comment.id, data=update_data
        )
        
        # Assertions
        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

    def test_update_comment_empty_content(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id)
        update_data = {"content": ""}
        
        # Test
        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=comment.id, data=update_data
        )
        
        # Assertions
        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

    def test_update_comment_no_request_body(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id)
        
        # Test
        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=comment.id, data=None
        )
        
        # Assertions
        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

    def test_update_comment_not_found(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"
        update_data = {"content": "Updated content"}
        
        # Test
        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=fake_comment_id, data=update_data
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_update_comment_task_not_found(self):
        # Setup
        account, token = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        fake_comment_id = "507f1f77bcf86cd799439012"
        update_data = {"content": "Updated content"}
        
        # Test
        response = self.make_authenticated_request(
            "PATCH", account.id, fake_task_id, token, comment_id=fake_comment_id, data=update_data
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.TASK_NOT_FOUND)

    def test_update_comment_unauthenticated(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id)
        update_data = {"content": "Updated content"}
        
        # Test
        response = self.make_unauthenticated_request(
            "PATCH", account.id, task.id, comment_id=comment.id, data=update_data
        )
        
        # Assertions
        assert response.status_code == 401

    # DELETE COMMENT TESTS
    
    def test_delete_comment_success(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id)
        
        # Test
        response = self.make_authenticated_request(
            "DELETE", account.id, task.id, token, comment_id=comment.id
        )
        
        # Assertions
        assert response.status_code == 204
        
        # Verify comment is deleted
        get_response = self.make_authenticated_request(
            "GET", account.id, task.id, token, comment_id=comment.id
        )
        self.assert_error_response(get_response, 404, CommentErrorCode.NOT_FOUND)

    def test_delete_comment_not_found(self):
        # Setup
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        # Test
        response = self.make_authenticated_request(
            "DELETE", account.id, task.id, token, comment_id=fake_comment_id
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_delete_comment_task_not_found(self):
        # Setup
        account, token = self.create_account_and_get_token()
        fake_task_id = "507f1f77bcf86cd799439011"
        fake_comment_id = "507f1f77bcf86cd799439012"
        
        # Test
        response = self.make_authenticated_request(
            "DELETE", account.id, fake_task_id, token, comment_id=fake_comment_id
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.TASK_NOT_FOUND)

    def test_delete_comment_unauthenticated(self):
        # Setup
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment = self.create_test_comment(account.id, task.id)
        
        # Test
        response = self.make_unauthenticated_request(
            "DELETE", account.id, task.id, comment_id=comment.id
        )
        
        # Assertions
        assert response.status_code == 401

    def test_delete_comment_cross_account_access(self):
        # Setup
        account1, token1 = self.create_account_and_get_token("user1@test.com")
        account2, _ = self.create_account_and_get_token("user2@test.com")
        task = self.create_test_task(account2.id)
        comment = self.create_test_comment(account2.id, task.id)
        
        # Test
        response = self.make_cross_account_request(
            "DELETE", account2.id, task.id, token1, comment_id=comment.id
        )
        
        # Assertions
        self.assert_error_response(response, 404, CommentErrorCode.TASK_NOT_FOUND)