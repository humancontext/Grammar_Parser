from nltk.grammar import FeatureGrammar
from nltk import FeatureChartParser
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
    ugrammar = FeatureGrammar.fromstring(rules)
    uparser = FeatureChartParser(ugrammar)
    index = 0
    for sent in text:
        index += 1
        print_tree(sent, uparser, index)
    print "Input testing sentece or the number of the above one: (q to quit)"
    str = sys.stdin.readline().strip()
    while str != "q":
        try:
            index = int(str)
            print_tree(text[index], uparser, index)
        except IndexError:
            print "Index out of range. Please check."
        except ValueError:
            print_tree(str, uparser, -1)
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
    # The extension lexicon
    "Bart likes drinking milk",
    "Lisa may have drunk milk",
    "Lisa may have seen Bart drinking milk",
    "Lisa may not have seen Bart drinking milk",
    ]

# Unification grammar rules
rules = """\
    #### Sentences
    S -> NP VP[SUBCAT=nil, FORM=pret]
    S -> NP VP[SUBCAT=nil, FORM=static]
    S -> NP[NUM=sing, PER=3] VP[SUBCAT=nil, FORM=vbz]
    S -> NP[PER=1] VP[SUBCAT=nil, FORM=base]
    S -> NP[PER=2] VP[SUBCAT=nil, FORM=base]
    S -> NP[NUM=plur, PER=3] VP[SUBCAT=nil, FORM=base]
    S -> AdvClause S    |S AdvClause
    QS -> NP VP[SUBCAT=nil, FORM=base]

    ### WH-Questions
    S -> Wh-adv VP
    S -> Wh-noun AuxP   | Wh-noun NP AuxP

    ### Imperative sentence
    S -> VP[FORM=base]


    ### Adverbial Clauses
    AdvClause -> Wh-adv S

    #### Arguments
    ARG[CAT=np]             -> NP
    ARG[CAT=pp]             -> PP
    ARG[CAT=s]              -> S
    ARG[CAT=vp, FORM=?f]    -> VP[FORM=?f]
    ARG[CAT=qs]             -> QS

    #### Noun Phrases
    NP[NUM=?n, PER=3]       -> Det[NUM=?n] Nom[NUM=?n]|Nom[NUM=?n]  |ProperNoun[NUM=?n]
    NP[NUM=sing, PER=3]     -> V[FORM=prespart]     |V[FORM=prespart] NP
    NP[NUM=plur, PER=?p]    -> NP Conj NP[PER=?p]
    NP[NUM=?n, PER=?p]      -> Pron[NUM=?n, PER=?p]

    #### Preposition Phrases
    PP -> Prep NP

    #### Verbs Phrases
    VP[SUBCAT=?rest, FORM=?f]   -> VP[SUBCAT=[HEAD=?arg, TAIL=?rest], FORM=?f] ARG[CAT=?arg]
    VP[SUBCAT=?args, FORM=?f]   -> V[SUBCAT=?args, FORM=?f]|Adv V[SUBCAT=?args, FORM=?f]|VP[SUBCAT=?args, FORM=?f] PP
    VP[SUBCAT=?rest, FORM=?f]   -> Aux[SUBCAT=[HEAD=vp, TAIL=?rest], HAVE=false, FORM=?f] ARG[CAT=vp, FORM=base]
    VP[SUBCAT=?rest, FORM=?f]   -> Aux[SUBCAT=[HEAD=vp, TAIL=?rest], HAVE=false, FORM=?f] Adv ARG[CAT=vp, FORM=base]
    VP[SUBCAT=?rest]            -> Aux[SUBCAT=[HEAD=vp, TAIL=?rest]] ARG[CAT=qs]
    VP[SUBCAT=?rest, FORM=?f]   -> Aux[SUBCAT=[HEAD=?arg, TAIL=?rest], HAVE=true, FORM=?f] ARG[CAT=vp, FORM=pastpart]
    VP[SUBCAT=?rest, FORM=?f]   -> Aux[SUBCAT=[HEAD=?arg, TAIL=?rest], HAVE=true, FORM=?f] Adv ARG[CAT=vp, FORM=pastpart]
    VP[SUBCAT=?args, FORM=?f]   -> Aux[FORM=?f, HAVE=true] VP[SUBCAT=[HEAD=?arg, TAIL=?rest], FORM=?f]

    #### Verbs
    ### Intransitive Verbs
    V[SUBCAT=nil, FORM=base]        -> 'laugh'
    V[SUBCAT=nil, FORM=vbz]         -> 'laughs'
    V[SUBCAT=nil, FORM=pret]        -> 'laughed'
    V[SUBCAT=nil, FORM=pastpart]    -> 'laughed'
    V[SUBCAT=nil, FORM=prespart]    -> 'laughing'
    ### Transitive Verbs with PP and NP as arguments
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]], FORM=base]        -> 'put'    |'see'
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]], FORM=vbz]         -> 'puts'   |'sees'
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]], FORM=pret]        -> 'put'    |'saw'
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]], FORM=pastpart]    -> 'put'    |'seen'
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]], FORM=prespart]    -> 'putting'|'seeing'
    ### Transitive Verbs with only NP as argument
    V[SUBCAT=[HEAD=np, TAIL=nil], FORM=base]        -> 'drink'      |'wear'     |'serve'    |'like'     |'know'
    V[SUBCAT=[HEAD=np, TAIL=nil], FORM=vbz]         -> 'drinks'     |'wears'    |'serves'   |'likes'    |'knows'
    V[SUBCAT=[HEAD=np, TAIL=nil], FORM=pret]        -> 'drank'      |'wore'     |'served'   |'liked'    |'knew'
    V[SUBCAT=[HEAD=np, TAIL=nil], FORM=pastpart]    -> 'drunk'      |'worn'     |'served'   |'liked'    |'known'
    V[SUBCAT=[HEAD=np, TAIL=nil], FORM=prespart]    -> 'drinking'   |'wearing'  |'serving'  |'liking'   |'knowing'
    ### Verbs with Two NP Arguments
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]], FORM=base]        -> 'serve'  |'give'     |'see'
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]], FORM=vbz]         -> 'serves' |'gives'    |'sees'
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]], FORM=pret]        -> 'served' |'gave'     |'saw'
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]], FORM=pastpart]    -> 'served' |'given'    |'seen'
    V[SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]], FORM=prespart]    -> 'serving'|'giving'   |'seeing'
    ### Clause Verbs
    V[SUBCAT=[HEAD=s, TAIL=nil], FORM=base]     -> 'think'
    V[SUBCAT=[HEAD=s, TAIL=nil], FORM=vbz]      -> 'thinks'
    V[SUBCAT=[HEAD=s, TAIL=nil], FORM=pret]     -> 'thought'
    V[SUBCAT=[HEAD=s, TAIL=nil], FORM=pastpart] -> 'thought'
    V[SUBCAT=[HEAD=s, TAIL=nil], FORM=prespart] -> 'thinking'
    ### Auxiliary Verbs
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=base,      HAVE=false] -> 'do'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=vbz,       HAVE=false] -> 'does'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=pret,      HAVE=false] -> 'did'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=pastpart,  HAVE=false] -> 'done'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=prespart,  HAVE=false] -> 'doing'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=static,    HAVE=false] -> 'can'|'could'|'may'|'might'|'shall'|'should'|'will'|'would'|'must'
    ## Auxiliary Verbs (have)
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=base,      HAVE=true] -> 'have'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=vbz,       HAVE=true] -> 'has'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=pret,      HAVE=true] -> 'had'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=pastpart,  HAVE=true] -> 'had'
    Aux[SUBCAT=[HEAD=vp, TAIL=nil], FORM=prespart,  HAVE=true] -> 'having'
    ## Auxiliary Verbs (be)
    BeVerb[FORM=base, PER=1]    -> 'am'
    BeVerb[FORM=base, PER=2]    -> 'are'
    BeVerb[FORM=pret, PER=1]    -> 'was'
    BeVerb[FORM=pret, PER=2]    -> 'were'
    BeVerb[FORM=pret, PER=3]    -> 'was'
    BeVerb[FORM=base, PER=3]    -> 'is'
    BeVerb[FORM=base, NUM=plur] -> 'are'
    BeVerb[FORM=pret, NUM=plur] -> 'were'
    BeVerb[FORM=pastpart]       -> 'been'
    BeVerb[FORM=prespart]       -> 'being'

    ### Nominals
    Nom[NUM=?n] -> Noun[NUM=?n]     |Adj Nom[NUM=?n]
    ### Nouns
    Noun[NUM=sing] -> 'milk'    |'salad'    |'kitchen'  |'midnight' |'table'    |'shoe'
    Noun[NUM=plur] -> 'salads'  |'kitchens' |'tables'   |'shoes'
    ### Proper Nouns
    ProperNoun[NUM=sing] -> 'Homer' |'Bart' |'Lisa'
    ### Pronouns
    Pron[NUM=sing, PER=1] ->  'I'       |'me'
    Pron[NUM=plur, PER=1] ->  'we'      |'us'
    Pron[NUM=sing, PER=2] ->  'you'
    Pron[NUM=plur, PER=2] ->  'you'
    Pron[NUM=sing, PER=3] ->  'he'      |'she'     |'it'    |'him'  |'her'
    Pron[NUM=plur, PER=3] ->  'they'    |'them'


    ### WH- adverbs and nouns
    Wh-adv  -> 'when'   |'where'    |'why'      |'how'
    Wh-noun -> 'who'    |'whom'     |'which'    |'what'

    ### Conjunctions
    Conj -> 'and'

    ### Adjectives
    Adj -> 'blue'   |'green'    |'healthy'

    ### Determiners
    Det -> 'the'
    Det[NUM=sing] -> 'a'    |'an'   |'this' |'that'
    Det[NUM=plur] -> 'these'|'those'

    ### Adverbs
    Adv -> 'always'     |'never'    |'not'

    ### Prepositions
    Prep -> 'in'        |'before'   |'on'   |'at'   |'around' 
    """
if __name__ == "__main__": main()