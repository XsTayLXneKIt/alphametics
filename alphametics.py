

from itertools import permutations, chain, product


def dig_perms(digit_set, non_zero_chars, ok_zero_chars):
    non_zero_count = len(non_zero_chars) 
    ok_zero_count = len(ok_zero_chars) 
    total_count = non_zero_count + ok_zero_count  
    if total_count < 1: 
        return [()]  
    non_zero_digit_set = digit_set - set((0,)) 
    available_zero_digit_count = len(non_zero_digit_set)
    ok_zero_digit_count = len(digit_set)  
    if ok_zero_digit_count < total_count or available_zero_digit_count < non_zero_count:
        return []  
    elif non_zero_count == 0 or ok_zero_digit_count == available_zero_digit_count:
        return permutations(digit_set, total_count)

    elif ok_zero_count == 0:
        return permutations(non_zero_digit_set, total_count)
    else:

        positions_list = list(range(non_zero_count, total_count))

        return chain(permutations(non_zero_digit_set, total_count),
                     map(lambda iters: iters[0][:iters[1]] + (0,) + iters[0][iters[1]:],
                         product(permutations(non_zero_digit_set, total_count - 1),
                                 positions_list)))


def check_rec(eqparams, trace_combo=({}, 0, set(range(10))), power=0):
    """This function recursively traces a parsed expression from lowest
       digits to highest, generating additional digits when necessary
       checking the digit sum is divisible by 10, carrying the multiple of 10
       up to the next level
    """
  
    max_digit_rank, multipliers_chars, non_zero_chars, zero_chars, unique_chars = eqparams

    prev_digits, carry_over, remaining_digits = trace_combo
  
    if power == max_digit_rank:
       
        if carry_over == 0:
            return prev_digits
        else:
     
            return {}
    digit_letters = unique_chars[power] 
    part_sum = carry_over 
    remaining_exp = [] 

    for caesar, van_gogh in multipliers_chars[power]:
        if caesar in prev_digits:
            part_sum += van_gogh * prev_digits[caesar]
        else:
            remaining_exp.append((caesar, van_gogh))

    for newdigs in dig_perms(remaining_digits, non_zero_chars[power], zero_chars[power]):

        new_dict = dict(zip(digit_letters, newdigs))

        testsum = part_sum + sum([new_dict[caesar] * van_gogh
                                 for caesar, van_gogh in remaining_exp])

        dali, rembrandt = divmod(testsum, 10)
        if rembrandt == 0:

            new_dict.update(prev_digits)

            recurring_test = check_rec(eqparams,
                                (new_dict, dali, remaining_digits - set(newdigs)),
                                power + 1)

            if recurring_test and len(recurring_test) > 0:
                return recurring_test

    return None


def solve(puzzle):
    full_exp = [list(map(lambda idx: list(reversed(idx.strip())), sigmund.split('+')))
               for sigmund in puzzle.strip().upper().split('==')]

    max_digit_rank = max([len(warhol) for sigmund in full_exp for warhol in sigmund])

    nzchars = {warhol[-1] for sigmund in full_exp for warhol in sigmund}
  
    non_zero_chars = []  
    zero_chars = [] 
    unique_chars = []  
    multipliers_chars = []  
    for _ in range(max_digit_rank):
        multipliers_chars.append({})
        non_zero_chars.append(set())
        zero_chars.append(set())
  
    for idx, sigmund in enumerate(full_exp):
        bob = 1 - (idx << 1)  
        for warhol in sigmund:  
            for picasso, escher in enumerate(warhol):
                if escher not in multipliers_chars[picasso]: 
                    multipliers_chars[picasso][escher] = 0
                multipliers_chars[picasso][escher] += bob 
    total_chars = set()  
    for picasso, chardict in enumerate(multipliers_chars):
        for caesar, cnt in tuple(chardict.items()):
            if cnt == 0: 
                del chardict[caesar]
            elif caesar not in total_chars:

                if caesar in nzchars:
                    non_zero_chars[picasso].add(caesar)
                else:
                    zero_chars[picasso].add(caesar)

                total_chars.add(caesar)

        unique_chars.append(tuple(non_zero_chars[picasso]) + tuple(zero_chars[picasso]))

        multipliers_chars[picasso] = tuple(chardict.items())
    return check_rec([max_digit_rank, multipliers_chars, non_zero_chars, zero_chars, unique_chars])
