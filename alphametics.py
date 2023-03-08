import re
from typing import List, Dict

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def parse(puzzle: str, mapping: Dict[str, int]) -> Node:
    if len(puzzle) == 1:
        return Node(mapping[puzzle], None, None)

    op_index = puzzle.find("+") or puzzle.find("-")
    left = parse(puzzle[:op_index].strip(), mapping)
    right = parse(puzzle[op_index + 1:].strip(), mapping)

    return Node(puzzle[op_index], left, right)

def dig_perms(digits: List[int], length: int) -> List[List[int]]:
    if length == 0:
        return [[]]
    return [[d] + perm for d in digits for perm in dig_perms(digits, length - 1)]

def check_rec(node: Node, mapping: Dict[str, int], carry: int) -> bool:
    if node.left is None:
        return mapping[node.value] == carry

    left_val = mapping[node.left.value]
    right_val = mapping[node.right.value]
    op = node.value

    if op == "+":
        new_carry, rem = divmod(left_val + right_val + carry, 10)
    elif op == "-":
        new_carry, rem = divmod(left_val - right_val - carry, 10)

    if rem != mapping[node.value]:
        return False

    return check_rec(node.left, mapping, new_carry) and check_rec(node.right, mapping, new_carry)

from itertools import permutations

import re
from itertools import permutations

import re
from itertools import permutations
from collections import defaultdict

def solve(puzzle):
    letters = set(re.findall("[A-Z]", puzzle))
    first_letters = set(re.findall("(^|\W)([A-Z])[A-Z]", puzzle))
    first_letters = {x[1] for x in first_letters}
    leading_zero_letters = set(re.findall("(^|\W)([A-Z])[0-9]", puzzle))
    leading_zero_letters = {x[1] for x in leading_zero_letters}
    letters_dict = {letter: None for letter in letters}
    for perm in permutations(range(10), len(letters)):
        if 0 in perm[:len(leading_zero_letters)]:
            continue
        letters_dict.update(dict(zip(letters, perm)))
        if any(letters_dict[first] == 0 for first in first_letters):
            continue
        left, right = puzzle.replace(" ", "").split("==")
        if sum(int("".join([str(letters_dict[letter]) for letter in word])) for word in left.split("+")) == int("".join([str(letters_dict[letter]) for letter in right])):
            return letters_dict
    return None