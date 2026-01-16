# Author: Cameron F. Abrams <cfa22@drexel.edu>

import pandas as pd
import numpy as np

import argparse as ap
from difflib import SequenceMatcher
from importlib.resources import files

from .compound import Compound

class PropertiesDatabase:
    resources_root = files('sandlerprops') / 'resources'
    """ Root directory for resource files. """
    data_dir = resources_root / 'data'
    """ Directory for data files. """
    datafile_path = data_dir / 'properties_database.csv'
    """ Path to the properties database CSV file. """
    def __init__(self):
        D = pd.read_csv(self.datafile_path, header=0, index_col=None)
        self.D = D.rename(columns={
            'Tfp (K)': 'Tfp',
            'Tb (K)': 'Tb',
            'Tc (K)': 'Tc',
            'Pc (bar)': 'Pc'})
        if self._swap_zeros_for_Os_in_Formulas() > 0:
            raise ValueError('Some formulas had 0 replaced with O; please verify correctness.')
        unitlist = [
            '', # no. (unique)
            '', # formula
            '', # name (unique)
            'g/mol', # molecular weight
            'K', # triple point temperature
            'K', # boiling point temperature
            'K', # critical temperature
            'bar', # critical pressure
            'm3/mol', # critical volume
            '', # critical compressibility
            '', # acentric factor
            '', # DIPM
            'J/mol-K', # ideal gas heat capacity coeff 1
            'J/mol-K2', # ideal gas heat capacity coeff 2
            'J/mol-K3', # ideal gas heat capacity coeff 3
            'J/mol-K4', # ideal gas heat capacity coeff 4
            'J/mol', # ideal gas enthalpy of formation at 298.15 K
            'J/mol', # ideal gas entropy of formation at 298.15 K   
            '', # vapor pressure equation type number
            '', # vapor pressure coeff 1
            '', # vapor pressure coeff 2
            '', # vapor pressure coeff 3
            '', # vapor pressure coeff 4
            'K', # vapor pressure temperature range min
            'K', # vapor pressure temperature range max
            '', # liquid density at Tden
            ''] # liquid density temperature for reference
        descriptions = [
            'Unique compound number',
            'Empirical formula',
            'Unique compound name',
            'Molecular weight in g/mol',
            'Triple point temperature in K',
            'Boiling point temperature in K',
            'Critical temperature in K',
            'Critical pressure in bar',
            'Critical volume in m3/mol',
            'Critical compressibility',
            'Acentric factor',
            'DIPM',
            'Ideal gas heat capacity coeff 1',
            'Ideal gas heat capacity coeff 2',
            'Ideal gas heat capacity coeff 3',
            'Ideal gas heat capacity coeff 4',
            'Ideal gas enthalpy of formation at 298.15 K',
            'Ideal gas entropy of formation at 298.15 K   ',
            'Vapor pressure equation type number',
            'Vapor pressure coeff 1',
            'Vapor pressure coeff 2',
            'Vapor pressure coeff 3',
            'Vapor pressure coeff 4',
            'Vapor pressure temperature range min',
            'Vapor pressure temperature range max',
            'Liquid density at Tden',
            'Temperature at which liquid density is measured'
        ]
        formatters = [
            '{:<10d}', # no. (unique)
            '{:<s}', # formula
            '{:<s}', # name (unique)
            '{:< 10.3f}', # molecular weight
            '{:< 10.1f}', # triple point temperature
            '{:< 10.1f}', # boiling point temperature
            '{:< 10.1f}', # critical temperature
            '{:< 10.2f}', # critical pressure
            '{:< 10.3f}', # critical volume
            '{:< 10.3f}', # critical compressibility
            '{:< 10.3f}', # acentric factor
            '{:<10g}', # DIPM
            '{:< 10.2f}', # ideal gas heat capacity coeff 1
            '{:< 10.4f}', # ideal gas heat capacity coeff 2
            '{:< 10.4e}', # ideal gas heat capacity coeff 3
            '{:< 10.4e}', # ideal gas heat capacity coeff 4
            '{:< 10.1f}', # ideal gas enthalpy of formation at 298.15 K
            '{:< 10.1f}', # ideal gas entropy of formation at 298.15 K   
            '{:<10d}', # vapor pressure equation type number
            '{:< 10.5f}', # vapor pressure coeff 1
            '{:< 10.5f}', # vapor pressure coeff 2
            '{:< 10.5f}', # vapor pressure coeff 3
            '{:< 10.5f}', # vapor pressure coeff 4
            '{:< 10.1f}', # vapor pressure temperature range min
            '{:< 10.1f}', # vapor pressure temperature range max
            '{:< 10.3f}', # liquid density at Tden
            '{:< 10.1f}'] # liquid density temperature for reference
        self.properties = list(self.D.columns)
        self.metadata = {}
        for p, u, f, d in zip(self.properties, unitlist, formatters, descriptions):
            self.metadata[p] = {
                'unit': u,
                'formatter': f,
                'description': d
            }

    def _swap_zeros_for_Os_in_Formulas(self):
        """
        Internal method to replace zeros with capital 'O's in the Formula column of the DataFrame.
        However, we can only do this if either of these conditions are met:
        1. The zero is the first character in the Formula
        2. The zero is preceded by a letter (not another digit)
        """
        num_corrections = 0
        formulas = self.D['Formula'].to_list()
        for i, formula in enumerate(formulas):
            trigger = False
            new_formula_chars = []
            for j, char in enumerate(formula):
                if char == '0':
                    if j == 0 or (j > 0 and not formula[j-1].isdigit()):
                        trigger = True
                        new_formula_chars.append('O')
                    else:
                        new_formula_chars.append('0')
                else:
                    new_formula_chars.append(char)
            new_formula = ''.join(new_formula_chars)
            if trigger:
                num_corrections += 1
                print(f'Corrected Formula from {formula} to {new_formula}')
            self.D.at[i, 'Formula'] = new_formula
        return num_corrections
    
    def show_properties(self, args: ap.Namespace = None):
        """ 
        Subcommand handler that displays the list of available properties with their units.
        
        Parameters
        ----------
        args : argparse.Namespace, optional
            Not used; present for compatibility since this is a subcommand handler.
        """
        header = ['Property', 'Units', 'Description']
        print(f'{header[0]:>10s} {header[1]:>10s}   {header[2]}')
        print('-'*50)
        for p in self.properties:
            unit = self.metadata[p]['unit']
            description = self.metadata[p]['description']
            print(f'{p:>10s} {unit:>10s}   {description}')

    def find_compound(self, args: ap.Namespace):
        """
        Subcommand handler that looks for a compound by name and displays if found.
        
        Parameters
        ----------
        args : argparse.Namespace
            Must contain attribute 'compound_name' with the name of the compound to find.
        """
        compound_name = args.compound_name
        record = self.get_compound(compound_name)
        if record.No != 0:
            print(f'Found exact match: {record.Name} (index {record.No})')

    def show_compound_properties(self, args: ap.Namespace):
        """
        Subcommand handler that displays all properties of a specified compound.
        
        Parameters
        ----------
        args : argparse.Namespace
            Must contain attribute 'compound_name' with the name of the compound to display.    
        """
        compound_name = args.compound_name
        record = self.get_compound(compound_name)
        if record is not None:
            print(f'Properties of {record.Name} (index {record.No}):')
            print('-'*40)
            for p in self.properties:
                value = getattr(record, p)
                unit = self.metadata[p]['unit']
                formatter = self.metadata[p]['formatter']
                formatted_value = formatter.format(value)
                if unit:
                    print(f'  {p:<10s}: {formatted_value} {unit}')
                else:
                    print(f'  {p:<10s}: {formatted_value}')

    def get_compound(self, name: str, near_matches: int = 10):
        """ 
        Retrieves a **Compound** by name. If not found, suggests similar names and returns
        an unpopulated **Compound** object with name and Formula set to input name.
        
        Parameters
        ----------
        name : str
            Name of the compound to retrieve
        near_matches : int
            Number of similar names to suggest if exact match not found
        
        Returns
        -------
        **Compound**
            The **Compound** object if found, else an empty **Compound** with name and Formula set.
        """
        row = self.D[self.D['Name'] == name]
        if not row.empty:
            d = row.to_dict('records')[0]
            return Compound(**d)
        else:
            print(f'{name} not found.  Here are similars:')
            scores = []
            for n in self.D['Name']:
                scores.append(SequenceMatcher(None, name, n).ratio())
            scores = np.array(scores)
            si = np.argsort(scores)
            sorted_names = np.array(self.D['Name'])[si]
            top_sorted_names = sorted_names[-near_matches:][::-1]
            for n in top_sorted_names:
                print(n)
        return Compound(Name=name, Formula=name)

_instance = None

def get_database():
    """
    Get or create the singleton database instance.
    
    Returns
    -------
    **PropertiesDatabase**
        The singleton instance of the properties database.
    """
    global _instance
    if _instance is None:
        _instance = PropertiesDatabase()
    return _instance