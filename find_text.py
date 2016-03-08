def ch_pos_in_str(ch, s):
    """ returns list of all positions of character ch in string s"""
    return [i for i, letter in enumerate(s) if letter == ch]


def find_substr_pos_in_str(sub, s):
    """ returns list of all positions of substring sub in string s"""
    import re
    starts = [match.start() for match in re.finditer(re.escape(sub), s)]
    return starts
