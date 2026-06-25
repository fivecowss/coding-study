# Week 3 Day 1: Basic Stack

## Today's Goals

- Understand stack as a Last-In, First-Out data structure.
- Use Python list as a stack with append, pop, and stack[-1].
- Solve Valid Parentheses using a stack.
- Implement MinStack with O(1) getMin.

---

## 1. Stack Basics

A stack follows Last-In, First-Out order.

Python stack operations:

```python
stack = []

stack.append(x)   # push
stack[-1]         # peek
stack.pop()       # pop
```

## Day 2: Expression Stack and Monotonic Stack

### Evaluate Reverse Polish Notation

Pattern:
- Use stack to store numbers.
- If token is a number, push it.
- If token is an operator, pop two numbers.
- Apply the operator.
- Push the result back.

Important:
```python
b = stack.pop()
a = stack.pop()
```