import nltk
import sys
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | VP Conj VP
NP -> N | Det N | AP NP | P NP | Det AP N
VP -> V | VP NP| N V NP | N VP | N Adv V NP | VP Adv | V Adv NP | V Adv
AP -> Adj | AP Adj
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # print(f"sentence: {sentence}")
    # You should use nltk’s word_tokenize function to perform tokenization.
    words = word_tokenize(sentence)
    lowercase_words = [word.lower() for word in words]
    # print(f"lower_case_list: {lowercase_words}")

    alphabetic_words = ["".join(char for char in word if char.isalpha()) for word in lowercase_words if word]

    filtered_list = [string for string in alphabetic_words if string]
    
    # print(f"filtered_strings: {filtered_list}")

    return filtered_list

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    subtrees = tree.subtrees()
    # 1) get all NPs
    list = []
    for subtree in subtrees:
        if subtree.label() == "NP":
            list.append(subtree)

    # 2) identify repeats and eliminate
    for subtree1 in list:
        print(f"subtree1: {subtree1.leaves()}")
        for subtree2 in list:
            leave1 = subtree1.leaves()
            leave2 = subtree2.leaves()
            if (set(leave1) <= set(leave2)) and (leave1 != leave2) and (subtree1 in list):
                # print(f"    ENTERED IF\n    subtree1 leaves: {leave1} \n    subtree2 leaves: {leave2} \n")
                list.remove(subtree1)

    return list


if __name__ == "__main__":
    main()

    # WORKS
    # formatted_tree = nltk.Tree.fromstring(str(tree))
    # list = []
    # for subtree in formatted_tree.subtrees():
    #     if subtree.label() == "NP" and subtree not in list:
    #         list.append(subtree)

    # filtered_strings = []
    # result = []
    # for s1 in list:
    #     keep = True
    #     for s2 in list:
    #         if s1 != s2 and s2 in s1:
    #             keep = False
    #             break
    #     if keep:
    #         result.append(s1)
    # return result

    # TRY #1
    # print(f"subtrees: {tree.subtrees()}")
    # list = []
    # def get_np_chunks(tree):
    #     for subtree in tree:
    #         # print(f"subtree: {subtree}")
    #         # print(f"    subtree length: {subtree.height()}")
    #         # print(f"    subtree label: {subtree.label()}")

    #         if subtree.height() > 3:
    #             get_np_chunks(subtree)
    #         if subtree.height() == 3:
    #             # print(f"    subtree label: {subtree.label()}")
    #             if str(subtree.label()) == 'NP':
    #                 # print(f"    NP subtree: {subtree}")
    #                 # print(f"        NP leaves: {subtree.leaves()}")

    #                 list.append(subtree)
    #                 # print(f"    list: {list}")


    # get_np_chunks(tree)
    # for subtree in tree:
    #     print(f"branch: {subtree}")
    #     print(f"length: {len(subtree)}")
    # print(f"np_chunks: {list}")

    # TRY #2
    # parent = nltk.tree.ParentedTree.convert(tree)
    # # print(f"parent: {parent}")
    # for subtree in parent.subtrees():
    #     # print(f"    subtree: {subtree}")
    #     if subtree.label() == "N" and subtree.parent:
    #         list.append(subtree.parent())