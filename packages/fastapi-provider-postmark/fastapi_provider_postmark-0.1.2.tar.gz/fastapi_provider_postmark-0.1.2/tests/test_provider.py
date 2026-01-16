"""Tests for PostmarkProvider"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from postmarker.exceptions import PostmarkerException

from fastapi_provider_postmark import PostmarkProvider, PostmarkProviderError


class TestPostmarkProviderInit:
    """Tests for PostmarkProvider initialization"""

    def test_init_with_all_parameters(self):
        """Test initialization with all parameters"""
        provider = PostmarkProvider(
            api_key="test-api-key",
            from_email="test@example.com",
            from_name="Test App",
            reply_to="support@example.com",
            default_template_variables={"key": "value"},
        )

        assert provider.api_key == "test-api-key"
        assert provider.from_email == "test@example.com"
        assert provider.from_name == "Test App"
        assert provider.reply_to == "support@example.com"
        assert provider.default_template_variables == {"key": "value"}

    def test_init_with_minimal_parameters(self):
        """Test initialization with minimal required parameters"""
        provider = PostmarkProvider(
            api_key="test-api-key",
            from_email="test@example.com",
        )

        assert provider.api_key == "test-api-key"
        assert provider.from_email == "test@example.com"
        assert provider.from_name is None
        assert provider.reply_to == "test@example.com"  # Should default to from_email
        assert provider.default_template_variables == {}

    def test_init_without_api_key_raises_error(self):
        """Test that initialization without API key raises ValueError"""
        with pytest.raises(ValueError, match="Postmark API key is required"):
            PostmarkProvider(
                api_key="",
                from_email="test@example.com",
            )

    def test_init_without_from_email_raises_error(self):
        """Test that initialization without from_email raises ValueError"""
        with pytest.raises(ValueError, match="From email address is required"):
            PostmarkProvider(
                api_key="test-api-key",
                from_email="",
            )

    def test_get_from_address_with_name(self):
        """Test _get_from_address with from_name"""
        provider = PostmarkProvider(
            api_key="test-api-key",
            from_email="test@example.com",
            from_name="Test App",
        )
        assert provider._get_from_address() == "Test App <test@example.com>"

    def test_get_from_address_without_name(self):
        """Test _get_from_address without from_name"""
        provider = PostmarkProvider(
            api_key="test-api-key",
            from_email="test@example.com",
        )
        assert provider._get_from_address() == "test@example.com"

    def test_client_property_creates_client(self):
        """Test that client property creates PostmarkClient"""
        provider = PostmarkProvider(
            api_key="test-api-key",
            from_email="test@example.com",
        )
        with patch(
            "fastapi_provider_postmark.provider.PostmarkClient"
        ) as mock_client_class:
            client = provider.client
            mock_client_class.assert_called_once_with(server_token="test-api-key")
            assert client is not None

    def test_client_property_caches_client(self):
        """Test that client property caches the client"""
        provider = PostmarkProvider(
            api_key="test-api-key",
            from_email="test@example.com",
        )
        with patch(
            "fastapi_provider_postmark.provider.PostmarkClient"
        ) as mock_client_class:
            client1 = provider.client
            client2 = provider.client
            mock_client_class.assert_called_once()
            assert client1 is client2


class TestSendEmail:
    """Tests for send_email method"""

    @pytest.mark.asyncio
    async def test_send_email_success(self, postmark_provider):
        """Test successful email sending"""
        mock_response = {
            "MessageID": "test-message-id",
            "SubmittedAt": "2024-01-01T00:00:00Z",
            "To": "recipient@example.com",
        }

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(return_value=mock_response)
        postmark_provider._client = mock_client

        result = await postmark_provider.send_email(
            to="recipient@example.com",
            template_id=123456,
            template_variables={"user_name": "John Doe"},
        )

        assert result == mock_response
        mock_client.emails.send_with_template.assert_called_once()
        call_args = mock_client.emails.send_with_template.call_args[1]
        assert call_args["From"] == "Test App <test@example.com>"
        assert call_args["To"] == "recipient@example.com"
        assert call_args["TemplateId"] == 123456
        assert call_args["TemplateModel"]["user_name"] == "John Doe"
        assert call_args["TemplateModel"]["product_name"] == "Test App"
        assert call_args["ReplyTo"] == "support@example.com"

    @pytest.mark.asyncio
    async def test_send_email_with_attachments(self, postmark_provider):
        """Test sending email with attachments"""
        mock_response = {"MessageID": "test-message-id"}

        attachments = [
            {
                "Name": "document.pdf",
                "Content": "base64encodedcontent",
                "ContentType": "application/pdf",
            }
        ]

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(return_value=mock_response)
        postmark_provider._client = mock_client

        result = await postmark_provider.send_email(
            to="recipient@example.com",
            template_id=123456,
            template_variables={},
            attachments=attachments,
        )

        assert result == mock_response
        call_args = mock_client.emails.send_with_template.call_args[1]
        assert call_args["Attachments"] == attachments

    @pytest.mark.asyncio
    async def test_send_email_with_invalid_attachment_format(self, postmark_provider):
        """Test sending email with invalid attachment format"""
        invalid_attachments = [
            {
                "Name": "document.pdf",
                # Missing Content and ContentType
            }
        ]

        with pytest.raises(PostmarkProviderError, match="Invalid attachment format"):
            await postmark_provider.send_email(
                to="recipient@example.com",
                template_id=123456,
                template_variables={},
                attachments=invalid_attachments,
            )

    @pytest.mark.asyncio
    async def test_send_email_with_custom_from(self, postmark_provider):
        """Test sending email with custom from address"""
        mock_response = {"MessageID": "test-message-id"}

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(return_value=mock_response)
        postmark_provider._client = mock_client

        await postmark_provider.send_email(
            to="recipient@example.com",
            template_id=123456,
            template_variables={},
            from_email="custom@example.com",
            from_name="Custom Name",
        )

        call_args = mock_client.emails.send_with_template.call_args[1]
        assert call_args["From"] == "Custom Name <custom@example.com>"

    @pytest.mark.asyncio
    async def test_send_email_with_custom_reply_to(self, postmark_provider):
        """Test sending email with custom reply-to"""
        mock_response = {"MessageID": "test-message-id"}

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(return_value=mock_response)
        postmark_provider._client = mock_client

        await postmark_provider.send_email(
            to="recipient@example.com",
            template_id=123456,
            template_variables={},
            reply_to="custom-reply@example.com",
        )

        call_args = mock_client.emails.send_with_template.call_args[1]
        assert call_args["ReplyTo"] == "custom-reply@example.com"

    @pytest.mark.asyncio
    async def test_send_email_merges_template_variables(self, postmark_provider):
        """Test that template variables are merged with defaults"""
        mock_response = {"MessageID": "test-message-id"}

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(return_value=mock_response)
        postmark_provider._client = mock_client

        await postmark_provider.send_email(
            to="recipient@example.com",
            template_id=123456,
            template_variables={"user_name": "John", "product_name": "Override"},
        )

        call_args = mock_client.emails.send_with_template.call_args[1]
        template_model = call_args["TemplateModel"]
        assert template_model["user_name"] == "John"
        assert template_model["product_name"] == "Override"  # Should override default
        assert (
            template_model["product_url"] == "https://example.com"
        )  # Should keep default

    @pytest.mark.asyncio
    async def test_send_email_postmark_authentication_error(self, postmark_provider):
        """Test handling of Postmark authentication error"""
        error = PostmarkerException("Authentication failed")
        error.error_code = 401

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(side_effect=error)
        postmark_provider._client = mock_client

        with pytest.raises(HTTPException) as exc_info:
            await postmark_provider.send_email(
                to="recipient@example.com",
                template_id=123456,
                template_variables={},
            )

        assert exc_info.value.status_code == 401
        assert "authentication failed" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_send_email_postmark_validation_error(self, postmark_provider):
        """Test handling of Postmark validation error"""
        error = PostmarkerException("Invalid email address")
        error.error_code = 400  # 400 is handled as validation error

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(side_effect=error)
        postmark_provider._client = mock_client

        with pytest.raises(HTTPException) as exc_info:
            await postmark_provider.send_email(
                to="invalid-email",
                template_id=123456,
                template_variables={},
            )

        assert exc_info.value.status_code == 422
        assert "validation error" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_send_email_postmark_server_error(self, postmark_provider):
        """Test handling of Postmark server error"""
        error = PostmarkerException("Server error")
        error.error_code = 500

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(side_effect=error)
        postmark_provider._client = mock_client

        with pytest.raises(HTTPException) as exc_info:
            await postmark_provider.send_email(
                to="recipient@example.com",
                template_id=123456,
                template_variables={},
            )

        assert exc_info.value.status_code == 503
        assert "temporarily unavailable" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_send_email_generic_postmark_error(self, postmark_provider):
        """Test handling of generic Postmark error"""
        error = PostmarkerException("Unknown error")
        error.error_code = 999

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(side_effect=error)
        postmark_provider._client = mock_client

        with pytest.raises(PostmarkProviderError, match="Postmark error"):
            await postmark_provider.send_email(
                to="recipient@example.com",
                template_id=123456,
                template_variables={},
            )

    @pytest.mark.asyncio
    async def test_send_email_unexpected_error(self, postmark_provider):
        """Test handling of unexpected errors"""
        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_with_template = MagicMock(
            side_effect=Exception("Unexpected error")
        )
        postmark_provider._client = mock_client

        with pytest.raises(PostmarkProviderError, match="Failed to send email"):
            await postmark_provider.send_email(
                to="recipient@example.com",
                template_id=123456,
                template_variables={},
            )


class TestSendBulkEmails:
    """Tests for send_bulk_emails method"""

    @pytest.mark.asyncio
    async def test_send_bulk_emails_success(self, postmark_provider):
        """Test successful bulk email sending"""
        mock_responses = [
            {"MessageID": "msg-1", "To": "user1@example.com"},
            {"MessageID": "msg-2", "To": "user2@example.com"},
        ]

        emails = [
            {
                "to": "user1@example.com",
                "template_id": 123456,
                "template_variables": {"user_name": "User 1"},
            },
            {
                "to": "user2@example.com",
                "template_id": 123456,
                "template_variables": {"user_name": "User 2"},
            },
        ]

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_batch_with_templates = MagicMock(
            return_value=mock_responses
        )
        postmark_provider._client = mock_client

        result = await postmark_provider.send_bulk_emails(emails)

        assert result == mock_responses
        mock_client.emails.send_batch_with_templates.assert_called_once()
        call_args = mock_client.emails.send_batch_with_templates.call_args[0][0]
        assert len(call_args) == 2
        assert call_args[0]["To"] == "user1@example.com"
        assert call_args[0]["TemplateModel"]["user_name"] == "User 1"
        assert call_args[1]["To"] == "user2@example.com"
        assert call_args[1]["TemplateModel"]["user_name"] == "User 2"

    @pytest.mark.asyncio
    async def test_send_bulk_emails_merges_template_variables(self, postmark_provider):
        """Test that bulk emails merge template variables with defaults"""
        mock_responses = [{"MessageID": "msg-1"}]

        emails = [
            {
                "to": "user1@example.com",
                "template_id": 123456,
                "template_variables": {"user_name": "User 1"},
            }
        ]

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_batch_with_templates = MagicMock(
            return_value=mock_responses
        )
        postmark_provider._client = mock_client

        await postmark_provider.send_bulk_emails(emails)

        call_args = mock_client.emails.send_batch_with_templates.call_args[0][0]
        template_model = call_args[0]["TemplateModel"]
        assert template_model["user_name"] == "User 1"
        assert template_model["product_name"] == "Test App"

    @pytest.mark.asyncio
    async def test_send_bulk_emails_missing_required_fields(self, postmark_provider):
        """Test that bulk emails require 'to' and 'template_id' fields"""
        emails = [
            {
                "to": "user1@example.com",
                # Missing template_id
            }
        ]

        with pytest.raises(
            PostmarkProviderError, match="must contain 'to' and 'template_id'"
        ):
            await postmark_provider.send_bulk_emails(emails)

    @pytest.mark.asyncio
    async def test_send_bulk_emails_with_custom_reply_to(self, postmark_provider):
        """Test bulk emails with custom reply-to per email"""
        mock_responses = [{"MessageID": "msg-1"}]

        emails = [
            {
                "to": "user1@example.com",
                "template_id": 123456,
                "reply_to": "custom@example.com",
            }
        ]

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_batch_with_templates = MagicMock(
            return_value=mock_responses
        )
        postmark_provider._client = mock_client

        await postmark_provider.send_bulk_emails(emails)

        call_args = mock_client.emails.send_batch_with_templates.call_args[0][0]
        assert call_args[0]["ReplyTo"] == "custom@example.com"

    @pytest.mark.asyncio
    async def test_send_bulk_emails_with_custom_from(self, postmark_provider):
        """Test bulk emails with custom from address"""
        mock_responses = [{"MessageID": "msg-1"}]

        emails = [
            {
                "to": "user1@example.com",
                "template_id": 123456,
            }
        ]

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_batch_with_templates = MagicMock(
            return_value=mock_responses
        )
        postmark_provider._client = mock_client

        await postmark_provider.send_bulk_emails(
            emails,
            from_email="custom@example.com",
            from_name="Custom Name",
        )

        call_args = mock_client.emails.send_batch_with_templates.call_args[0][0]
        assert call_args[0]["From"] == "Custom Name <custom@example.com>"

    @pytest.mark.asyncio
    async def test_send_bulk_emails_postmark_error(self, postmark_provider):
        """Test handling of Postmark errors in bulk emails"""
        error = PostmarkerException("Bulk email error")
        error.error_code = 422

        emails = [
            {
                "to": "user1@example.com",
                "template_id": 123456,
            }
        ]

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_batch_with_templates = MagicMock(side_effect=error)
        postmark_provider._client = mock_client

        with pytest.raises(PostmarkProviderError, match="Failed to send bulk emails"):
            await postmark_provider.send_bulk_emails(emails)

    @pytest.mark.asyncio
    async def test_send_bulk_emails_unexpected_error(self, postmark_provider):
        """Test handling of unexpected errors in bulk emails"""
        emails = [
            {
                "to": "user1@example.com",
                "template_id": 123456,
            }
        ]

        mock_client = MagicMock()
        mock_client.emails = MagicMock()
        mock_client.emails.send_batch_with_templates = MagicMock(
            side_effect=Exception("Unexpected")
        )
        postmark_provider._client = mock_client

        with pytest.raises(PostmarkProviderError, match="Failed to send bulk emails"):
            await postmark_provider.send_bulk_emails(emails)


class TestGetDeliveryStats:
    """Tests for get_delivery_stats method"""

    @pytest.mark.asyncio
    async def test_get_delivery_stats_success(self, postmark_provider):
        """Test successful retrieval of delivery stats"""
        mock_stats = {
            "Sent": 1000,
            "Bounced": 10,
            "SpamComplaints": 2,
            "Tracked": 800,
        }

        mock_client = MagicMock()
        mock_client.stats = MagicMock()
        mock_client.stats.get_outbound = MagicMock(return_value=mock_stats)
        postmark_provider._client = mock_client

        result = await postmark_provider.get_delivery_stats()

        assert result == mock_stats
        mock_client.stats.get_outbound.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_delivery_stats_postmark_error(self, postmark_provider):
        """Test handling of Postmark errors when getting stats"""
        error = PostmarkerException("Stats error")
        error.error_code = 500

        mock_client = MagicMock()
        mock_client.stats = MagicMock()
        mock_client.stats.get_outbound = MagicMock(side_effect=error)
        postmark_provider._client = mock_client

        with pytest.raises(PostmarkProviderError, match="Failed to get delivery stats"):
            await postmark_provider.get_delivery_stats()

    @pytest.mark.asyncio
    async def test_get_delivery_stats_unexpected_error(self, postmark_provider):
        """Test handling of unexpected errors when getting stats"""
        mock_client = MagicMock()
        mock_client.stats = MagicMock()
        mock_client.stats.get_outbound = MagicMock(side_effect=Exception("Unexpected"))
        postmark_provider._client = mock_client

        with pytest.raises(PostmarkProviderError, match="Failed to get delivery stats"):
            await postmark_provider.get_delivery_stats()
