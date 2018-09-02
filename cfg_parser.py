from nltk import CFG, ChartParser
import sys

# Method used to print the tree
def print_tree(sent, parser, index):
    parses = parser.parse(sent.split())
    amb = 0
    for tree in parses:
        amb += 1
    if index >0:
        print "#%d has %d possible tree(s)" %(index,amb)
    else:
        print "This sentence has %d possible tree(s)" %(amb)
    print sent
    parses = parser.parse(sent.split())
    for tree in parses:
        print tree
    print
    print "================================================================"


# The main method including a simple commandline UI
def main():
    cfparser = ChartParser(cfg)
    index = 0
    for sent in text:
        index += 1
        print_tree(sent, cfparser, index)
    print "Input testing sentece or the number of the above one: (q to quit)"
    str = sys.stdin.readline().strip()
    while str != "q":
        try:
            index = int(str)
            print_tree(text[index], cfparser, index)
        except IndexError:
            print "Index out of range. Please check."
        except ValueError:
            print_tree(str, cfparser, -1)
        print "Input testing sentece or the number of the above one: (q to quit)"
        str = sys.stdin.readline().strip()

# Lexicon
text = [
    # The basic lexicon
    "Bart laughs",
    "Homer laughed",
    "Bart and Lisa drink milk",
    "Bart wears blue shoes",
    "Lisa serves Bart a healthy green salad",
    "Homer serves Lisa",
    "Bart always drinks milk",
    "Lisa thinks Homer thinks Bart drinks milk",
    "Homer never drinks milk in the kitchen before midnight",
    "when Homer drinks milk Bart laughs",
    "when does Lisa drink the milk on the table",
    "when do Lisa and Bart wear shoes",
    # The incorrect sentences
    "Bart laugh",
    "when do Homer drinks milk",
    "Bart laughs the kitchen",
    ]

# CFG rules
cfg = CFG.fromstring("""\
    #### Sentences
    S -> NP VP
    S -> AdvClause S
    S -> Wh-adv Aux S

    ### Clauses
    AdvClause -> Wh-adv S


    ### Phrases
    NP -> ProperNoun|ProperNoun Conj ProperNoun         |Nom            |NP PP
    VP -> V         |V NP              |V NP NP       |Adv VP         |V S        |VP PP
    PP -> Prep NP 
    Nom -> Noun     | Adj Nom           |Det Nom    

    #### Terminals
    Noun        -> 'milk'   |'shoes'    |'salad'    |'kitchen'  |'midnight' |'table'
    V           -> 'laughs' |'runs'     |'laughed'  |'drink'    |'drinks'   |'wears'    |'likes'
    V           -> 'serves' |'thinks'   |'does'     |'do'       |'wear'     |'laugh'
    Conj        -> 'and'    |'or'       |'but'
    Adj         -> 'blue'   |'healthy'  |'green'
    Adv         -> 'always' |'never'    |'when'
    Prep        -> 'in'     |'before'   |'on'
    ProperNoun  -> 'Homer'  |'Bart'     |'Lisa'
    Wh-adv      -> 'when'
    Det         -> 'a'      |'the'
    Aux         -> 'do'     |'does'     |'did'
    """)
if __name__ == "__main__": main()
