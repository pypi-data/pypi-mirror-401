---
name: code-review-assistant
description: Helps review Python code following best practices and team conventions
tags: [python, code-review, best-practices]
requires: [python-linter]
---

# Code Review Assistant

This skill helps Claude review Python code with a focus on quality, maintainability, and team conventions.

## When to Use

Activate this skill when:
- User asks for a code review
- User submits a pull request for feedback
- User wants to improve code quality

## Review Checklist

1. **Readability**: Is the code easy to understand?
2. **Naming**: Are variables and functions descriptive?
3. **Structure**: Is the code well-organized?
4. **Error Handling**: Are exceptions handled properly?
5. **Testing**: Are there appropriate tests?

## Example

Given this code:
```python
def f(x):
    return x*2
```

Suggest:
```python
def double_value(number: int) -> int:
    """Return the input number multiplied by two."""
    return number * 2
```

## Guidelines

- Be constructive, not critical
- Explain the "why" behind suggestions
- Prioritize impactful changes over nitpicks
