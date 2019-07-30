import difflib
import keyword
import numpy as np
import pandas as pd
import tokenize


# Constants
BEGIN="<BOF>"
COMMENT="<COMMENT>"
VARIABLE="<VARIABLE>"
NEWLINE="<NEWLINE>"
NL="<NL>"
STRING="<STRING>"
INDENT="<INDENT>"
DEDENT="<DEDENT>"
NUMBER="<NUMBER>"
END="<EOF>"

constants_dict = {}
_name=""
_value=""
for _name, _value in globals().items():
    if type(_value) is type("") and not _name.startswith('_'):
        constants_dict[_name] = _value

del _name, _value

py_vocab = keyword.kwlist.copy()
py_vocab.extend(('.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '@', 
    '->', '=', '*', '**', '+=', '-=', '*=', '@=', '/=', '%=', '&=', '|=', 
    '^=', '<<=', '>>=', '**=', '//=', '...', '<', '>', '==', '>=', '<=', 
    '<>', '!=', '^', '|', '&', '<<', '>>', '+', '-', '/', '%', '//', '~'))
py_vocab.extend(list(constants_dict.values()))


def deduplicate(vector):
    """ Given a vector of tokens, returns a new vector of pruned tokens.
    Particularly, this function removes the multiple-line comments
    and the compound variables (i.e., <variable>.<variable> = <variable>)
    """
    new_vector = []
    new_vector.append(vector[0])
    for i in range(1, len(vector)):
        if vector[i] == NL:
            pass
        elif vector[i] == COMMENT and new_vector[-1] == COMMENT:
            pass
        elif (vector[i] == "." and new_vector[-1] == VARIABLE):
            pass
        elif (vector[i] == VARIABLE and new_vector[-1] == VARIABLE):
            pass
        else:
            new_vector.append(vector[i])
    return new_vector


def tokens2seq(vector,
               vocabulary):
    """ Converts a vector of text tokens into a vector of numbers,
    using the vocabulary to translate
    """
    new_vector = []
    for tok in vector:
        new_vector.append(vocabulary.index(tok))
    return new_vector


def mark_defects(defective_vector,
                 corrected_vector):
    """ Returns a binary vector that identifies the defective lines. Specifically,
    for each line of code (i.e., sequence of tokens terminating with a new line) 
    that is deleted or modified in the defective vector, the position of new line
    is marked with a 1.
    """
    defective_pos = []
    diff = difflib.unified_diff(defective_vector, corrected_vector, n=0)
    pos = None
    for line in diff:
        if line.startswith("@@"):
            defective_pos.append( -1*int(line.replace(",", " ").split(" ")[1]) - 1 )
            pop = True
        elif NEWLINE in line:
            # In the case a line is added we can not assume that
            # the sorrounding lines were defective
            if pop:
                defective_pos.pop()
            # Prevent multiple pop in one change
            pop = False
        ## TODO: should we care about (+|-)NL exclusive changes?
    defective_tok = [0] * len(defective_vector)
    for pos in defective_pos:
        nl_pos = defective_vector.index(NEWLINE, pos)
        defective_tok[nl_pos] = 1
    return defective_tok


def py2vector(filename):
    """ Loads a python source file and build a vector of text tokens.
    It also replaces comments, variables, strings, and numbers with
    anonymous tokens.
    """
    vector = []
    with open(filename, 'rb') as f:
        tokens = list(tokenize.tokenize(f.readline))
    for toknum, tokval, _, _, _ in tokens:
        if toknum == tokenize.ENCODING:
            vector.append(BEGIN)
        elif toknum == tokenize.COMMENT:
            vector.append(COMMENT)
        elif toknum == tokenize.NAME and tokval not in keyword.kwlist:
            vector.append(VARIABLE)
        elif toknum == tokenize.NEWLINE:
            vector.append(NEWLINE)
        elif toknum == tokenize.NL:
            vector.append(NL)
        elif toknum == tokenize.STRING:
            vector.append(STRING)
        elif toknum == tokenize.INDENT:
            vector.append(INDENT)
        elif toknum == tokenize.DEDENT:
            vector.append(DEDENT)
        elif toknum == tokenize.NUMBER:
            vector.append(NUMBER)
        elif toknum == tokenize.ENDMARKER:
            vector.append(END)
        else:
            vector.append(tokval)
    if vector[-1] != END:
        vector.append(END)
    return vector


def seq2df(sequence,
           class_seq,
           seq_names=None,
           class_names=None):
    """ Returns a DataFrame with the one hot encoded version of the sequence
    and the one hot version of the class vector.
    """
    temp_seq = np.zeros((len(sequence), np.max(sequence)+1))
    temp_seq[np.arange(len(sequence)), sequence] = 1
    temp_class = np.zeros((len(class_seq), np.max(class_seq)+1))
    temp_class[np.arange(len(class_seq)), [0] + class_seq[:-1]] = 1
    df = pd.DataFrame(np.concatenate((temp_seq, temp_class), axis=1))
    if (seq_names is not None and class_names is not None):
        df.columns = seq_names + class_names
    return df
