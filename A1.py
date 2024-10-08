import os
from typing import Union, List, Optional

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """
    # TODO
    lines = []
    file = open(fp, "r")
    for line in file:
        lines.append(line)
    return lines


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    # TODO
    if not (s[0] in alphabet_chars): #check first element is a letter
        return False   
    for l in s:
        if not (l in var_chars):   
            return False   
    return True


class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
        self.children = []


    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)


class ParseTree:
    """
    A full parse tree, with nodes
    Attributes:
        root: the root of the tree
    """
    def __init__(self, root):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        # TODO
        print("")



def parse_tokens(s_: str, association_type: Optional[str] = None) -> Union[List[str], bool]:
    """
    Gets the final tokens for valid strings as a list of strings, only for valid syntax,
    where tokens are (no whitespace included)
    \\ values for lambdas
    valid variable names
    opening and closing parenthesis
    Note that dots are replaced with corresponding parenthesis
    :param s_: the input string
    :param association_type: If not None, add brackets to make expressions non-ambiguous
    :return: A List of tokens (strings) if a valid input, otherwise False
    """

    s = s_[:]  #  Don't modify the original input string
    #PART 1: ERROR HANDLING
    #split all elements into terminal elements (variables, \, (), .)
    elements = []
    for i in range(len(s)):
        if s[i] in var_chars: #alphanumeric, should be a variable
            if (s[i-1] in var_chars) and (i-1>=0):
                #ideally, if the previous token was alphanumeric, we would have already processed it as a variable, so we shouldn't need to worry about this character
                continue
            var_len_counter = 1
            j = i
            while s[i+1] in var_chars and ((i+2)<len(s)):
                var_len_counter += 1
                i += 1
            var = s[j:j+var_len_counter]
            elements.append(var)
        else:
            elements.append(s[i])


    #check for errors in the elements
    bracket_counter = 0
    for i in range(len(elements)):
        #invalid character (ex. +, -)
        if elements[i] not in all_valid_chars:
            if len(elements[i]) > 1:
                #multiple character variable encountered, check that it's a valid name
                if not is_valid_var_name(elements[i]):
                    print("invalid variable name starting at index",i)
                    return False
            elif elements[i] == " " or elements[i] == "\n":
                continue
            else:
                print("Invalid token \""+elements[i]+"\" at index",i)
                return False
        
        #backslash errors
        elif elements[i] == "\\":
            if i+1 == len(elements):
                print("invalid lambda at index",i)
                return False
            elif elements[i+1] == " ":
                print("Invalid space after lambda at index",i)
                return False
            elif not is_valid_var_name(elements[i+1]):
                print("lambda must be followed by a valid variable at index",(i+1))
                return False
            elif (elements[i+2] != "(") and (elements[i+2] != ".") and (elements[i+2] != " "):
                #the element two spaces away from the lambda must be either a space, a dot, or an opening bracket
                print("invalid lambda expression at",i)
                return False

        
        #open bracket
        elif elements[i] == "(":
            bracket_counter += 1
            if i+1 == len(elements):
                print("expression cannot end with opening bracket at index",i)
                return False
            elif elements[i+1] == ")":
                print("missing expression at index",i)
                return False
            
        # dot encountered
        elif elements[i] == ".":
            if i == 0:
                print("Dot encountered at invalid index 0")
                return False
            elif not is_valid_var_name(elements[i-1]):
                print("must have variable before . at index",(i-1))
                return False

        elif elements[i] == ")":
            bracket_counter -= 1
    
    if bracket_counter > 0:
        print("bracket ( is not matched with a closing bracket")
        return False
    elif bracket_counter < 0:
        print("bracket ) is not matched with an opening bracket")
        return False
    # IF NO ERRORS: RETURN LIST OF TOKENS
    tokens = []
    bracket_counter = 0
    for i in range(len(s)):
        if s[i] == " ":
            continue # disregard whitespace
        #check for \
        if s[i] == "\\" :
            tokens.append(s[i])

        elif s[i] == "(":
            tokens.append("(")
            bracket_counter += 1
        elif s[i] == ")":
            tokens.append(")")
            bracket_counter -= 1

        #check for dot (if next character is a bracket, start counter and continue)
        elif s[i] == ".": 
            tokens.append("(")
            bracket_counter += 1
        elif s[i] in var_chars: #alphanumeric, should be a variable
            if s[i-1] in var_chars:
                #ideally, if the previous token was alphanumeric, we would have already processed it as a variable, so we shouldn't need to worry about this character
                continue
            var_len_counter = 1
            j = i
            while s[i+1] in var_chars:
                var_len_counter += 1
                i += 1
            var = s[j:j+var_len_counter]
            if is_valid_var_name(var):
                tokens.append(var)

    #once all characters have been tokenized, append appropriate number of closing brackets to the end
    while bracket_counter > 0:
        tokens.append(")")
        bracket_counter -= 1
    
    # TODO

    return tokens


def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param lines: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")



def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()


def add_associativity(s_: List[str], association_type: str = "left") -> List[str]:
    """
    :param s_: A list of string tokens
    :param association_type: a string in [`left`, `right`]
    :return: List of strings, with added parenthesis that disambiguates the original expression
    """

    # TODO Optional
    s = s_[:]  # Don't modify original string
    return []




def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree
    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """

    #TODO
    return Node()


def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":





    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    #read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("\n\nChecking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)
    '''
    # Optional
    print("\n\nAssociation Examples:")
    sample = ["a", "b", "c"]
    print("Right association")
    associated_sample_r = add_associativity(sample, association_type="right")
    print(associated_sample_r)
    print("Left association")
    associated_sample_l = add_associativity(sample, association_type="left")
    print(associated_sample_l)
    '''
    
    
    
    