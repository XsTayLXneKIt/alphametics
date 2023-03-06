from itertools import permutations

def solve(puzzle):
    # Extract the words and result from the puzzle
    words = puzzle.split(' = ')[0].split(' + ')
    result = puzzle.split(' = ')[1]
    
    # Extract the unique letters from the puzzle
    letters = set(''.join(words) + result)
    
    # Generate all possible permutations of the digits
    for digits in permutations(range(10), len(letters)):
        # Assign each digit to its corresponding letter
        mapping = {letter: digit for letter, digit in zip(letters, digits)}
        
        # Check if the mapping satisfies the puzzle conditions
        if all(mapping[word[0]] != 0 for word in words + [result]) and \
           sum(int(''.join(str(mapping[letter]) for letter in word)) for word in words) == \
           int(''.join(str(mapping[letter]) for letter in result)):
            return mapping
    
    # No solution found
    return None