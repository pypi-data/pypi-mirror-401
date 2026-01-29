import numpy as np
from dataclasses import dataclass, field
import pint

ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

@dataclass
class Compound:
    """Chemical compound with thermophysical properties."""
    
    # Identifiers (no units)
    No: int = 0
    """ Unique compound number """
    Formula: str = ''
    """ Empirical formula """
    Name: str = ''
    """ Unique compound name """
    
    # Basic properties with units
    Molwt: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.g / ureg.mol)
    """ Molecular weight """
    
    # Temperature properties
    Tfp: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.K)
    """ Triple point temperature """
    Tb: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.K)
    """ Boiling point temperature """
    Tc: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.K)
    """ Critical temperature """
    
    # Critical properties
    Pc: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.bar)
    """ Critical pressure """
    Vc: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.m**3 / ureg.mol)
    """ Critical volume """
    
    # Dimensionless properties
    Zc: float = 0.0
    """ Critical compressibility """
    Omega: float = 0.0
    """ Acentric factor """
    Dipm: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.debye)
    """ Dipole moment """

    # Heat capacity coefficients (stored as floats in standard basis)
    # Cp = CpA + CpB*T + CpC*T^2 + CpD*T^3 where T is in K, result in J/(mol*K)
    CpA: float = 0.0
    """ Ideal gas heat capacity coeff (J/(mol*K)) """
    CpB: float = 0.0
    """ Ideal gas heat capacity coeff (J/(mol*K^2)) """
    CpC: float = 0.0
    """ Ideal gas heat capacity coeff (J/(mol*K^3)) """
    CpD: float = 0.0
    """ Ideal gas heat capacity coeff (J/(mol*K^4)) """
    
    # Formation properties
    dHf: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.J / ureg.mol)
    """ Ideal gas enthalpy of formation at 298.15 K """
    dGf: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.J / ureg.mol)
    """ Ideal gas Gibbs energy of formation at 298.15 K """
    
    # Vapor pressure equation (dimensionless coefficients)
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
    Tmin: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.K)
    """ Vapor pressure temperature range min """
    Tmax: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.K)
    """ Vapor pressure temperature range max """
    
    # Liquid density
    Lden: float = 0.0
    """ Liquid density at Tden """
    Tden: pint.Quantity = field(default_factory=lambda: 0.0 * ureg.K)
    """ Temperature at which liquid density is measured """
    
    charge: int = 0
    """ Net charge of the compound (not in input properties set unless encoded in Formula) """
    atomset: set = field(default_factory=set)
    """ Set of unique atom names in empirical formula """
    atomdict: dict = field(default_factory=dict)
    """ Dictionary of atomname:count items representing empirical formula """
    metadata: dict = field(default_factory=dict)
    """ Dictionary for storing any additional metadata passed from the database """

    def get_Cp_coeffs(self) -> dict[str, float]:
        """
        Get ideal gas heat capacity coefficients as dict.
        
        Returns coefficients for: Cp = a + b*T + c*T^2 + d*T^3
        where Cp is in J/(mol*K) and T is in K (dimensionless values).
        """
        return {'a': self.CpA, 'b': self.CpB, 'c': self.CpC, 'd': self.CpD}
    
    def __repr__(self):
        return f"Compound(No={self.No}, Name='{self.Name}', Formula='{self.Formula}')"

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

    def Cp_ideal_gas(self, T: pint.Quantity) -> pint.Quantity:
        """
        Calculate ideal gas heat capacity at temperature T.
        
        Parameters
        ----------
        T : Quantity
            Temperature
            
        Returns
        -------
        Quantity
            Heat capacity in J/(mol-K)
        """
        T_K = T.m_as('K')
        Cp_val = self.CpA + self.CpB*T_K + self.CpC*T_K**2 + self.CpD*T_K**3
        return Cp_val * ureg.J / (ureg.mol * ureg.K)

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
