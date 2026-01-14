# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by emailing security@example.com.

Please include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes

We will acknowledge receipt within 48 hours and provide a detailed response within 7 days.

## Security Best Practices

When using this SDK:

1. **Never hardcode API keys** - Use environment variables or secure configuration files
2. **Use HTTPS** - The SDK defaults to HTTPS for all API calls
3. **Keep dependencies updated** - Regularly update to get security patches
4. **Validate input** - Always validate data before passing to the SDK
5. **Handle errors securely** - Don't expose sensitive information in error messages
