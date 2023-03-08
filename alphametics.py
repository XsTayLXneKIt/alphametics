from itertools import permutations

def dig_perms(digits, non_zero_letters, zero_letters):
    # Generate all possible permutations of the digits
    all_perms = permutations(digits)

    # Filter out permutations that violate the constraints
    valid_perms = []
    for perm in all_perms:
        # Check if any non-zero letter is assigned to 0
        if any(perm.index(letter) == 0 for letter in non_zero_letters):
            continue
        # Replace 0 with each zero letter and check if the resulting permutation is valid
        for letter in zero_letters:
            zero_index = perm.index(letter)
            if zero_index == 0 and letter not in non_zero_letters:
                continue
            perm_with_zero = list(perm)
            perm_with_zero[zero_index] = '0'
            if ''.join(perm_with_zero) == '0' and any(letter in zero_letters for letter in digits):
                continue
            valid_perms.append(tuple(perm_with_zero))

    return valid_perms

def check_rec(node, carry=0):
    # Check if the node is a leaf (i.e., a digit)
    if isinstance(node, int):
        return (node + carry) % 10, (node + carry) // 10

    # Recursively evaluate the left and right sub-trees
    left_value, left_carry = check_rec(node.left, carry)
    right_value, right_carry = check_rec(node.right, left_carry)

    # Compute the result and the new carry value
    result = left_value + right_value
    new_carry = right_carry + (result // 10)

    return result % 10, new_carry
    

def solve(puzzle):
    # Split the puzzle into words and the result
    words = puzzle.split(" + ")
    result = words.pop()

    # Get the set of all letters in the puzzle
    letters = set(result)
    for word in words:
        letters |= set(word)

    # Get the set of letters that cannot be assigned to 0
    non_zero_letters = set(word[0] for word in words) | set(result[0])

    # Generate all possible permutations of digits for the given letters
    digit_perms = dig_perms('0123456789', non_zero_letters, letters-non_zero_letters)

    # Try each digit permutation until a valid solution is found
    for digits in digit_perms:
        # Create a dictionary mapping letters to digits
        mapping = dict(zip(letters, digits))

        # Check if the mapping has unique values for each letter
        if len(set(mapping.values())) != len(mapping):
            continue

        # Evaluate the expression using the current mapping
        expression_value = 0
        for word in words:
            word_value = int(''.join(mapping[letter] for letter in word))
            expression_value += word_value
        result_value = int(''.join(mapping[letter] for letter in result))

        # Check if the current mapping is a valid solution
        if expression_value == result_value:
            return mapping

    # If no valid solution was found, return None
    return None