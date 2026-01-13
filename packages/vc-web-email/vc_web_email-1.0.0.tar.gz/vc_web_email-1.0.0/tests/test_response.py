"""
Tests for EmailResponse.
"""

import pytest
from datetime import datetime
from vc_web_email.response import EmailResponse, BulkEmailResponse, EmailStatus


class TestEmailResponse:
    """Tests for EmailResponse class."""
    
    def test_success_response_factory(self):
        response = EmailResponse.success_response(
            message_id='msg-123', provider='smtp', recipients=['user@example.com']
        )
        assert response.success is True
        assert response.message_id == 'msg-123'
        assert response.status == EmailStatus.SENT
    
    def test_failure_response_factory(self):
        response = EmailResponse.failure_response(
            error='Connection failed', provider='smtp', error_code='CONN_ERR'
        )
        assert response.success is False
        assert response.error == 'Connection failed'
        assert response.status == EmailStatus.FAILED
    
    def test_is_successful_property(self):
        success = EmailResponse.success_response('msg-1', 'smtp')
        failure = EmailResponse.failure_response('Error', 'smtp')
        assert success.is_successful is True
        assert failure.is_successful is False
    
    def test_to_dict(self):
        response = EmailResponse.success_response('msg-123', 'smtp')
        result = response.to_dict()
        assert result['success'] is True
        assert result['message_id'] == 'msg-123'


class TestBulkEmailResponse:
    """Tests for BulkEmailResponse class."""
    
    def test_create_bulk_response(self):
        responses = [
            EmailResponse.success_response('msg-1', 'smtp'),
            EmailResponse.failure_response('Error', 'smtp'),
        ]
        bulk = BulkEmailResponse(total=2, successful=1, failed=1, responses=responses)
        assert bulk.total == 2
        assert bulk.success_rate == 0.5
    
    def test_all_successful(self):
        bulk = BulkEmailResponse(total=3, successful=3, failed=0)
        assert bulk.all_successful is True
    
    def test_get_failed_responses(self):
        responses = [
            EmailResponse.success_response('msg-1', 'smtp'),
            EmailResponse.failure_response('Error', 'smtp'),
        ]
        bulk = BulkEmailResponse(total=2, successful=1, failed=1, responses=responses)
        failed = bulk.get_failed_responses()
        assert len(failed) == 1
