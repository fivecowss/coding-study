
# ============================================================
# Problem: LeetCode 150. Evaluate Reverse Polish Notation
# Pattern: Stack
# Key idea:
#   - Push numbers into stack.
#   - When we see an operator, pop two numbers.
#   - Apply the operator.
#   - Push the result back.
# ============================================================


def eval_rpn(tokens: list[str]) -> int:
    """
    Evaluate an arithmetic expression in Reverse Polish Notation.

    Args:
        tokens: list of strings such as ["2", "1", "+", "3", "*"]

    Returns:
        Final integer result.
    """

    # --------------------------------------------------------
    # Step 1. Create an empty stack.
    # This stack stores numbers that are waiting to be used.
    # --------------------------------------------------------
    stack = []


    # --------------------------------------------------------
    # Step 2. Define the set of operators.
    # This helps us distinguish numbers from operators.
    # --------------------------------------------------------
    operators = {"+", "-", "*", "/"}

    # --------------------------------------------------------
    # Step 3. Loop through each token.
    # token can be either a number string or an operator.
    # --------------------------------------------------------
    for token in tokens:

        # ----------------------------------------------------
        # Case 1. token is a number.
        # Convert it to int and push it into stack.
        # ----------------------------------------------------
        if token not in operators:
            # TODO: push int(token) into stack
            stack.append(int(token))
        

        # ----------------------------------------------------
        # Case 2. token is an operator.
        # Pop two numbers and apply the operator.
        # ----------------------------------------------------
        else:
            # TODO: pop right operand first
            b = stack.pop()
            # TODO: pop left operand second
            a = stack.pop()
            # TODO: handle +
            if token == "+":
                stack.append(a + b)
            # TODO: handle -
            elif token == "-":
                stack.append(a - b)
            # TODO: handle *
            elif token == "*":
                stack.append(a * b)
            # TODO: handle /
            else:
                stack.append(int(a / b))
        


    # --------------------------------------------------------
    # Step 4. At the end, stack has exactly one number.
    # Return that number.
    # --------------------------------------------------------
    # TODO: return final result
    return stack[-1]


if __name__ == "__main__":
    print(eval_rpn(["2", "1", "+", "3", "*"]))       # 9
    print(eval_rpn(["4", "13", "5", "/", "+"]))      # 6
    print(eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]))  # 22