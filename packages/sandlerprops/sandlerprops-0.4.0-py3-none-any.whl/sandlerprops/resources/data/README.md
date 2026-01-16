# Pure Component Properties Database

I extracted this database (`properties_database.csv`) from the Microsoft Access database provided in the CDROM that accompanied _Chemical, Biochemical, and Engineering Thermodynamics_, 4th ed. by Stan Sandler.

A few corrections to note:

1.  The empirical formula for phosgene was incorrectly listed as `CCl20`. I corrected this to `CCl2O` manually (zero to upper-case "O").
2.  The empirical formula for trifluoroacetic acid was incorrectly listed as `C2CHF3O2`.  I corrected this to `C2HF3O2` manually (got rid of extra carbon atom).
3. The empirical formula for dichloromethane was incorrectly listed as `CH2CL2`.  I corrected this to `CH2Cl2` manually. (upper-case "L" to lower-case "l")
4. The empirical formula for ammonia was weirdly listed as `H3N`.  I manually changed this to the better-looking `NH3` and enforce no atom name reordering.