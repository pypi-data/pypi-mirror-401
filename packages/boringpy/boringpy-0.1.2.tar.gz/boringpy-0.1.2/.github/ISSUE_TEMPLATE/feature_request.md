---
name: Feature Request
about: Suggest an idea for BoringPy
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## 🚀 Feature Description

A clear and concise description of the feature you'd like to see.

## 💡 Motivation

Why do you need this feature? What problem does it solve?

**Example:**
> I often need to generate APIs with authentication, and setting it up manually each time is time-consuming.

## 📝 Proposed Solution

How would you like this feature to work?

**Example:**
```bash
boringpy generate api my_api --auth jwt
```

## 🔄 Alternatives Considered

What alternatives have you considered?

## 📸 Examples / Mock-ups

If applicable, provide examples of how this would look:

```python
# Example code
from app.core.auth import require_auth

@router.get("/protected")
@require_auth
async def protected_route():
    return {"message": "Protected"}
```

## 🎯 Use Cases

Who would benefit from this feature?

- [ ] Solo developers
- [ ] Small teams
- [ ] Large organizations
- [ ] Specific industry/use case: ___

## 📊 Priority

How important is this to you?

- [ ] Critical - I can't use BoringPy without it
- [ ] High - Would significantly improve my workflow
- [ ] Medium - Nice to have
- [ ] Low - Just an idea

## 🤝 Contribution

Would you be willing to contribute to implementing this feature?

- [ ] Yes, I can implement it with guidance
- [ ] Yes, I can help with testing/documentation
- [ ] Maybe, depending on complexity
- [ ] No, but I can provide feedback

## 🔗 Related Issues

Are there any related issues or feature requests?

- #123
- #456

## 📚 Additional Context

Any other information that might be helpful.
