"""Postmark email provider implementation"""

import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from postmarker.core import PostmarkClient
from postmarker.exceptions import PostmarkerException

logger = logging.getLogger(__name__)


class PostmarkProviderError(Exception):
    """Custom exception for Postmark provider errors"""

    pass


class PostmarkProvider:
    """Postmark email provider for sending emails via Postmark API"""

    def __init__(
        self,
        api_key: str,
        from_email: str,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        default_template_variables: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Postmark provider.

        Args:
            api_key (str): Postmark API server token
            from_email (str): Default sender email address
            from_name (str, optional): Default sender name. If not provided, only email is used.
            reply_to (str, optional): Default reply-to email address. Defaults to from_email.
            default_template_variables (dict, optional): Default template variables to include in all emails.
        """
        if not api_key:
            raise ValueError("Postmark API key is required")

        if not from_email:
            raise ValueError("From email address is required")

        self.api_key = api_key
        self.from_email = from_email
        self.from_name = from_name
        self.reply_to = reply_to or from_email
        self.default_template_variables = default_template_variables or {}
        self._client: Optional[PostmarkClient] = None

    @property
    def client(self) -> PostmarkClient:
        """Get or create Postmark client instance"""
        if self._client is None:
            self._client = PostmarkClient(server_token=self.api_key)
        return self._client

    def _get_from_address(self) -> str:
        """Get formatted from address"""
        if self.from_name:
            return f"{self.from_name} <{self.from_email}>"
        return self.from_email

    async def send_email(
        self,
        to: str,
        template_id: int,
        template_variables: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        reply_to: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sends an email using the Postmark API with the specified template.

        Args:
            to (str): The email address of the recipient.
            template_id (int): The ID of the email template to use.
            template_variables (dict, optional): A dictionary of variables to populate the email template.
            attachments (List[Dict], optional): List of attachments. Each attachment should be a dict with:
                - Name: The filename
                - Content: Base64 encoded content
                - ContentType: The MIME type (e.g., 'application/pdf')
            reply_to (str, optional): Reply-to email address. Defaults to provider's reply_to.
            from_email (str, optional): Override sender email address. Defaults to provider's from_email.
            from_name (str, optional): Override sender name. Defaults to provider's from_name.

        Returns:
            Dict: Response from Postmark API containing MessageID and other details

        Raises:
            PostmarkProviderError: If there's an error sending the email
            HTTPException: If there's a configuration or validation error

        Example with attachment:
            attachments = [
                {
                    "Name": "readme.txt",
                    "Content": "dGVzdCBjb250ZW50",
                    "ContentType": "text/plain"
                },
                {
                    "Name": "report.pdf",
                    "Content": "dGVzdCBjb250ZW50",
                    "ContentType": "application/octet-stream"
                }
            ]
        """
        try:
            # Determine from address
            if from_email:
                if from_name:
                    from_address = f"{from_name} <{from_email}>"
                else:
                    from_address = from_email
            else:
                from_address = self._get_from_address()

            # Merge template variables
            merged_variables = {
                **self.default_template_variables,
                **(template_variables or {}),
            }

            email_data = {
                "From": from_address,
                "To": to,
                "TemplateId": template_id,
                "TemplateModel": merged_variables,
                "ReplyTo": reply_to or self.reply_to,
            }

            if attachments:
                # Validate attachments format
                for attachment in attachments:
                    required_keys = ["Name", "Content", "ContentType"]
                    if not all(key in attachment for key in required_keys):
                        raise PostmarkProviderError(
                            f"Invalid attachment format. Required keys: {required_keys}"
                        )
                email_data["Attachments"] = attachments

            # Send email using Postmark API
            response = self.client.emails.send_with_template(**email_data)

            logger.info(
                "Email sent successfully via Postmark. Message ID: %s",
                response.get("MessageID"),
            )

            return response

        except PostmarkerException as e:
            # Handle Postmark-specific errors
            error_code = getattr(e, "error_code", None)
            error_message = str(e)

            logger.error("Postmark API error (code: %s): %s", error_code, error_message)

            # Map Postmark error codes to appropriate HTTP status codes
            if error_code in [100, 401]:
                raise HTTPException(
                    status_code=401, detail="Email service authentication failed"
                ) from e
            elif error_code in [300, 400, 401, 402, 406]:
                raise HTTPException(
                    status_code=422, detail=f"Email validation error: {error_message}"
                ) from e
            elif error_code == 500:
                raise HTTPException(
                    status_code=503, detail="Email service temporarily unavailable"
                ) from e
            else:
                raise PostmarkProviderError(f"Postmark error: {error_message}") from e

        except Exception as e:
            logger.error("Unexpected error sending email: %s", str(e))
            raise PostmarkProviderError(f"Failed to send email: {str(e)}") from e

    async def send_bulk_emails(
        self,
        emails: List[Dict[str, Any]],
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Sends multiple emails using Postmark's bulk email API.

        Args:
            emails (List[Dict]): List of email data dictionaries. Each should contain:
                - to: recipient email (required)
                - template_id: template ID (required)
                - template_variables: template variables dict (optional)
                - reply_to: reply-to email (optional)
            from_email (str, optional): Override sender email address. Defaults to provider's from_email.
            from_name (str, optional): Override sender name. Defaults to provider's from_name.

        Returns:
            List[Dict]: List of response data for each email

        Raises:
            PostmarkProviderError: If there's an error sending the emails
        """
        try:
            # Determine from address
            if from_email:
                if from_name:
                    from_address = f"{from_name} <{from_email}>"
                else:
                    from_address = from_email
            else:
                from_address = self._get_from_address()

            # Prepare bulk email data
            bulk_emails = []
            for email in emails:
                if "to" not in email or "template_id" not in email:
                    raise PostmarkProviderError(
                        "Each email must contain 'to' and 'template_id' fields"
                    )

                # Merge template variables with defaults
                template_variables = {
                    **self.default_template_variables,
                    **email.get("template_variables", {}),
                }

                email_data = {
                    "From": from_address,
                    "To": email["to"],
                    "TemplateId": email["template_id"],
                    "TemplateModel": template_variables,
                    "ReplyTo": email.get("reply_to") or self.reply_to,
                }
                bulk_emails.append(email_data)

            # Send bulk emails
            responses = self.client.emails.send_batch_with_templates(bulk_emails)

            logger.info("Bulk email sent successfully. Sent: %d emails", len(responses))
            return responses

        except PostmarkerException as e:
            logger.error("Postmark bulk email error: %s", str(e))
            raise PostmarkProviderError(f"Failed to send bulk emails: {str(e)}") from e
        except Exception as e:
            logger.error("Unexpected error sending bulk emails: %s", str(e))
            raise PostmarkProviderError(f"Failed to send bulk emails: {str(e)}") from e

    async def get_delivery_stats(self) -> Dict[str, Any]:
        """
        Get email delivery statistics from Postmark.

        Returns:
            Dict: Delivery statistics

        Raises:
            PostmarkProviderError: If there's an error fetching stats
        """
        try:
            stats = self.client.stats.get_outbound()

            logger.info("Retrieved Postmark delivery stats")
            return stats

        except PostmarkerException as e:
            logger.error("Postmark stats error: %s", str(e))
            raise PostmarkProviderError(
                f"Failed to get delivery stats: {str(e)}"
            ) from e
        except Exception as e:
            logger.error("Unexpected error getting delivery stats: %s", str(e))
            raise PostmarkProviderError(
                f"Failed to get delivery stats: {str(e)}"
            ) from e
