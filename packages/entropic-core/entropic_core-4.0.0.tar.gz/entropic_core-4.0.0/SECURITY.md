# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### Private Disclosure

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please email us at: **security@entropic-core.org**

Include the following information:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** of the vulnerability
4. **Affected versions** (if known)
5. **Suggested fix** (if you have one)

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

### Security Update Process

1. We will confirm the vulnerability
2. We will develop and test a fix
3. We will release a security patch
4. We will publicly disclose the vulnerability (after fix is released)

### Severity Levels

**Critical**: Remote code execution, data breach, privilege escalation
**High**: Authentication bypass, significant data exposure
**Medium**: Denial of service, limited data exposure
**Low**: Information disclosure with minimal impact

## Security Best Practices

When using Entropic Core:

### 1. Keep Dependencies Updated

```bash
pip install --upgrade entropic-core
```

### 2. Use Environment Variables

Never hardcode sensitive data:

```python
import os
api_key = os.getenv('API_KEY')  # Good
api_key = "sk-xxx"  # Bad
```

### 3. Validate Input

Always validate agent inputs:

```python
from entropic_core import EntropyBrain

brain = EntropyBrain()
if brain.validate_agent(agent):  # Validate first
    brain.connect([agent])
```

### 4. Run with Least Privilege

Use non-root users in production:

```dockerfile
USER entropic  # Non-root user
```

### 5. Monitor System Health

Enable health monitoring:

```python
from entropic_core.utils import HealthMonitor

monitor = HealthMonitor()
if monitor.check_system_health()['status'] != 'healthy':
    # Take action
    pass
```

### 6. Use HTTPS

Always use secure connections:

```python
dashboard_config = {
    'ssl_cert': '/path/to/cert.pem',
    'ssl_key': '/path/to/key.pem'
}
```

## Known Security Considerations

### Database Connections

- Use parameterized queries (we do this by default)
- Never store passwords in plain text
- Use connection pooling with limits

### API Endpoints

- Rate limiting is enabled by default
- Authentication required for sensitive endpoints
- Input validation on all user data

### File System Access

- Restricted to designated data directories
- No arbitrary file access
- Path traversal protection

## Security Checklist for Contributors

When contributing code:

- [ ] No hardcoded secrets or credentials
- [ ] Input validation for all user-supplied data
- [ ] Proper error handling (no information leakage)
- [ ] SQL injection prevention (use parameterized queries)
- [ ] XSS prevention (sanitize outputs)
- [ ] CSRF protection (for web endpoints)
- [ ] Rate limiting for APIs
- [ ] Proper authentication and authorization
- [ ] Secure random number generation when needed
- [ ] No use of `eval()` or `exec()` on user input

## Disclosure Policy

We follow coordinated vulnerability disclosure:

1. Security researcher reports vulnerability privately
2. We confirm and develop a fix
3. We release the fix in a security update
4. After 90 days (or when fix is widely deployed), we publicly disclose
5. We credit the researcher (if they wish)

## Bug Bounty

We currently do not have a formal bug bounty program, but we deeply appreciate security researchers who help us improve. We will publicly acknowledge contributors (if desired) and may offer rewards for significant findings on a case-by-case basis.

## Contact

- **Security Issues**: security@entropic-core.org
- **General Questions**: hello@entropic-core.org
- **GitHub Issues**: For non-security bugs only

Thank you for helping keep Entropic Core secure!
