# FastAPI Provider Postmark

A Postmark email provider package for FastAPI projects that provides a clean, class-based interface for sending emails via the Postmark API.

## Features

- 📧 **Email Sending**
  - Send templated emails using Postmark templates
  - Support for attachments
  - Customizable sender information
  - Default template variables

- 📦 **Bulk Email**
  - Send multiple emails in a single API call
  - Efficient batch processing

- 📊 **Statistics**
  - Retrieve email delivery statistics
  - Monitor email performance

- 🛡️ **Error Handling**
  - Comprehensive error handling
  - HTTP exception mapping
  - Detailed logging

## Installation

Using UV:

```bash
uv add fastapi-provider-postmark
```

Or using pip:

```bash
pip install fastapi-provider-postmark
```

## Quick Start

### Basic Usage

```python
from fastapi import FastAPI
from fastapi_provider_postmark import PostmarkProvider

app = FastAPI()

# Initialize the provider
postmark = PostmarkProvider(
    api_key="your-postmark-api-key",
    from_email="support@example.com",
    from_name="My App",
    reply_to="support@example.com",
    default_template_variables={
        "product_url": "https://example.com",
        "product_name": "My App",
        "support_email": "support@example.com",
    }
)

@app.post("/send-email")
async def send_email():
    await postmark.send_email(
        to="user@example.com",
        template_id=123456,
        template_variables={
            "user_name": "John Doe",
            "action_url": "https://example.com/verify",
        }
    )
    return {"message": "Email sent successfully"}
```

### With Environment Variables

```python
import os
from fastapi_provider_postmark import PostmarkProvider

postmark = PostmarkProvider(
    api_key=os.getenv("POSTMARK_API_KEY"),
    from_email=os.getenv("POSTMARK_FROM_EMAIL", "noreply@example.com"),
    from_name=os.getenv("POSTMARK_FROM_NAME", "My App"),
    reply_to=os.getenv("POSTMARK_REPLY_TO", "support@example.com"),
    default_template_variables={
        "product_url": os.getenv("PRODUCT_URL", "https://example.com"),
        "product_name": os.getenv("PRODUCT_NAME", "My App"),
    }
)
```

### Sending Emails with Attachments

```python
attachments = [
    {
        "Name": "document.pdf",
        "Content": "base64_encoded_content_here",
        "ContentType": "application/pdf"
    }
]

await postmark.send_email(
    to="user@example.com",
    template_id=123456,
    template_variables={"user_name": "John Doe"},
    attachments=attachments
)
```

### Sending Bulk Emails

```python
emails = [
    {
        "to": "user1@example.com",
        "template_id": 123456,
        "template_variables": {"user_name": "User 1"}
    },
    {
        "to": "user2@example.com",
        "template_id": 123456,
        "template_variables": {"user_name": "User 2"}
    }
]

responses = await postmark.send_bulk_emails(emails)
```

### Getting Delivery Statistics

```python
stats = await postmark.get_delivery_stats()
print(f"Sent: {stats.get('Sent')}")
print(f"Bounced: {stats.get('Bounced')}")
```

### Using with Dependency Injection

```python
from fastapi import Depends
from fastapi_provider_postmark import PostmarkProvider

def get_postmark_provider() -> PostmarkProvider:
    return PostmarkProvider(
        api_key=os.getenv("POSTMARK_API_KEY"),
        from_email=os.getenv("POSTMARK_FROM_EMAIL"),
        from_name=os.getenv("POSTMARK_FROM_NAME"),
    )

@app.post("/send-email")
async def send_email(
    postmark: PostmarkProvider = Depends(get_postmark_provider)
):
    await postmark.send_email(
        to="user@example.com",
        template_id=123456,
        template_variables={"user_name": "John Doe"}
    )
    return {"message": "Email sent"}
```

## API Reference

### PostmarkProvider

#### `__init__`

Initialize the Postmark provider.

**Parameters:**
- `api_key` (str, required): Postmark API server token
- `from_email` (str, required): Default sender email address
- `from_name` (str, optional): Default sender name
- `reply_to` (str, optional): Default reply-to email address. Defaults to `from_email`
- `default_template_variables` (dict, optional): Default template variables to include in all emails

#### `send_email`

Send an email using a Postmark template.

**Parameters:**
- `to` (str, required): Recipient email address
- `template_id` (int, required): Postmark template ID
- `template_variables` (dict, optional): Template variables
- `attachments` (List[Dict], optional): List of attachments
- `reply_to` (str, optional): Override reply-to address
- `from_email` (str, optional): Override sender email
- `from_name` (str, optional): Override sender name

**Returns:** Dict containing Postmark API response

#### `send_bulk_emails`

Send multiple emails in a batch.

**Parameters:**
- `emails` (List[Dict], required): List of email dictionaries
- `from_email` (str, optional): Override sender email
- `from_name` (str, optional): Override sender name

**Returns:** List of response dictionaries

#### `get_delivery_stats`

Get email delivery statistics from Postmark.

**Returns:** Dict containing delivery statistics

## Error Handling

The provider includes comprehensive error handling:

- `PostmarkProviderError`: Custom exception for provider errors
- `HTTPException`: Raised for authentication and validation errors
- Automatic mapping of Postmark error codes to HTTP status codes

## Development

### Setup

1. Clone the repository
2. Install dependencies:
```bash
uv sync
```

## License

MIT License - see LICENSE file for details

