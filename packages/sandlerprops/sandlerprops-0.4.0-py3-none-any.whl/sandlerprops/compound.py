import numpy as np
from dataclasses import dataclass, field

@dataclass
class Compound:
    No: int = 0
    """ Unique compound number """
    Formula: str = ''
    """ Empirical formula """
    Name: str = ''
    """ Unique compound name """
    Molwt: float = 0.0
    """ Molecular weight in g/mol """
    Tfp: float = 0.0
    """ Triple point temperature in K """
    Tb: float = 0.0
    """ Boiling point temperature in K """
    Tc: float = 0.0
    """ Critical temperature in K """
    Pc: float = 0.0
    """ Critical pressure in **bar** """
    Vc: float = 0.0
    """ Critical volume in m3/mol """
    Zc: float = 0.0
    """ Critical compressibility """
    Omega: float = 0.0
    """ Acentric factor """
    Dipm: float = 0.0
    """ DIPM """
    CpA: float = 0.0
    """ Ideal gas heat capacity coeff 1 """
    CpB: float = 0.0
    """ Ideal gas heat capacity coeff 2 """
    CpC: float = 0.0
    """ Ideal gas heat capacity coeff 3 """
    CpD: float = 0.0
    """ Ideal gas heat capacity coeff 4 """
    dHf: float = 0.0
    """ Ideal gas enthalpy of formation at 298.15 K """
    dGf: float = 0.0
    """ Ideal gas entropy of formation at 298.15 K   """
    Eq: int = 0
    """ Vapor pressure equation type number """
    VpA: float = 0.0
    """ Vapor pressure coeff 1 """
    VpB: float = 0.0
    """ Vapor pressure coeff 2 """
    VpC: float = 0.0
    """ Vapor pressure coeff 3 """
    VpD: float = 0.0
    """ Vapor pressure coeff 4 """
    Tmin: float = 0.0
    """ Vapor pressure temperature range min """
    Tmax: float = 0.0
    """ Vapor pressure temperature range max """
    Lden: float = 0.0
    """ Liquid density at Tden """
    Tden: float = 0.0
    """ Temperature at which liquid density is measured """
    charge: int = 0
    """ Net charge of the compound (not in input properties set unless encoded in Formula) """
    atomset: set = field(default_factory=set)
    """ Set of unique atom names in empirical formula """
    atomdict: dict = field(default_factory=dict)
    """ Dictionary of atomname:count items representing empirical formula """

    def __post_init__(self):
        """ dictionary of atomname:count items representing empirical formula """
        efc = self.Formula.split('^')
        ef_neutral = efc[0]
        self.charge = 0
        if len(efc) > 1:
            expo = efc[1]
            if expo[0] == '{' and expo[-1] == '}':
                self.charge = int(expo[1:-1])
            else:
                raise ValueError(f'Error: malformed charge {efc[1]}')

        self.atomdict = parse_empirical_formula(ef_neutral)
        self._reorder_elements()
        self.atomset = set(self.atomdict.keys())

    @property
    def Cp(self):
        """ Returns ideal gas heat capacity coefficients as a numpy array """
        return np.array([self.CpA, self.CpB, self.CpC, self.CpD])

    def _reorder_elements(self):
        leave_these_alone = ['NH3', 'CH3OH', 
                             'Fe','He','Li','Be','Ne','Na','Mg','Al','Si','Cl','Ar','Ca','Sc',
                             'Ti','Cr','Mn','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr',
                             'Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In',
                             'Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm',
                             'Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re',
                             'Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra',
                             'Ac','Th','Pa','U']
        if self.Formula in leave_these_alone:
            return
        my_order_preference = ['C', 'H', 'O', 'N', 'Na', 'K', 'Ca', 'F', 'Cl', 'Br', 'I']
        A = self.atomdict.copy()
        ef = ''
        for a in my_order_preference:
            if a in A:
                c = '' if A[a] == 1 else str(A[a])
                ef += f'{a}{c}'
                del A[a]
        for e, c in A.items():
            c = '' if c == 1 else str(c)
            ef += f'{e}{c}'
        self.Formula = ef


def _push(obj: any, l: list, depth: int):
    """
    push an object onto a nested list at a given depth 
    (source: https://stackoverflow.com/users/5079316/olivier-melan%c3%a7on)
    
    Parameters
    ----------
    obj : any
        object to push
    l : list
        list to push onto
    depth : int
        depth at which to push
    """
    while depth:
        l = l[-1]
        depth -= 1
    l.append(obj)

def _parse_parentheses(s: str) -> list:
    """
    byte-wise de-nestify a string with parenthesis
    (source: https://stackoverflow.com/users/5079316/olivier-melan%c3%a7on)

    Parameters
    ----------
    s : str
        string to de-nestify

    Returns
    -------
    list
        nested list representing the de-nestified string
    """
    groups = []
    depth = 0
    try:
        i = 0
        while i < len(s):
            char = s[i]
            if char == '(':
                _push([], groups, depth)
                depth += 1
            elif char == ')':
                depth -= 1
            else:
                _push(char, groups, depth)
            i += 1
    except IndexError:
        raise ValueError('Parentheses mismatch')
    if depth != 0:
        raise ValueError('Parentheses mismatch')
    else:
        return groups

def bankblock(B: list, b: list):
    """
    bank a block into the list of blocks if it is non-empty
    (source: https://stackoverflow.com/users/5079316/olivier-melan%c3%a7on)

    Parameters
    ----------
    B : list
        list of blocks
    b : list
        block to bank
    """
    if len(b[0]) > 0: # bank this block
        if not any(isinstance(i, list) for i in b[0]):
            b[0] = ''.join(b[0])
        nstr = ''.join(b[1])
        b[1] = 1 if len(nstr) == 0 else int(nstr)
        B.append(b)

def blockify(bl: list) -> list:
    """
    parse the byte_levels returned from the byte-wise de-nester into blocks, where
    a block is a two-element list, where first element is a block and second is 
    an integer subscript >= 1.  A "primitive" block is one in which the first
    element is not a list, but instead a string that indentifies a chemical element.
    (source: https://stackoverflow.com/users/5079316/olivier-melan%c3%a7on)

    Parameters
    ----------
    bl : list
        byte_levels list to parse

    Returns
    -------
    list
        list of blocks
    """
    blocks = []
    curr_block = [[], []]
    for b in bl:
        if len(b) == 1:
            if b.isalpha():
                if b.isupper(): # new block
                    bankblock(blocks, curr_block)
                    curr_block = [[b], []]
                else: # still building this block's elem name
                    curr_block[0].append(b)
            elif b.isdigit():
                curr_block[1].append(b)
        else:
            bankblock(blocks, curr_block)
            curr_block = [blockify(b), []]
    bankblock(blocks, curr_block)
    return blocks

def flattify(B: list) -> None:
    """
    recursively flatten nested blocks in place
    (source: https://stackoverflow.com/users/5079316/olivier-melan%c3%a7on)

    Parameters
    ----------
    B : list
        list of blocks to flattify
    """
    for b in B:
        if isinstance(b[0], str) or b[1] == 1: # already flat
            pass
        else:
            m = b[1]
            b[1] = 1
            for bb in b[0]:
                bb[1] *= m
                flattify(b[0])

def my_flatten(L: list, size: tuple = (2)):
    """
    recursively flatten a nested list of blocks into a flat list of element:number pairs
    (source: https://stackoverflow.com/users/5079316/olivier-melan%c3%a7on)

    Parameters
    ----------
    L : list
        nested list of blocks to flatten
    size : tuple, optional
        size of the element:number pairs, by default (2)

    Returns
    -------
    list
        flat list of element:number pairs
    """
    flatlist = []
    for i in L:
        if not isinstance(i[0], list):
            flatlist.append(i)
        else:
            newlist = my_flatten(i[0])
            flatlist.extend(newlist)
    return flatlist

def reduce(L: list) -> dict:
    """ 
    reduce a flat list of element:number pairs into a dictionary of element:number items
    (source: https://stackoverflow.com/users/5079316/olivier-melan%c3%a7on)
    
    Parameters
    ----------
    L : list
        flat list of element:number pairs

    Returns
    -------
    dict
        dictionary of element:number items
    """
    result_dict = {}
    for i in L:
        if i[0] in result_dict:
            result_dict[i[0]] += i[1]
        else:
            result_dict[i[0]] = i[1]
    return result_dict

def parse_empirical_formula(ef: str) -> dict:
    """
    parse an empirical formula into a dictionary of element:number items
    (source: https://stackoverflow.com/users/5079316/olivier-melan%c3%a7on)

    Parameters
    ----------
    ef : str
        empirical formula string

    Returns
    -------
    dict
        dictionary of element:number items
    """
    block_levels = blockify(_parse_parentheses(ef))
    flattify(block_levels)
    return reduce(my_flatten(block_levels))
