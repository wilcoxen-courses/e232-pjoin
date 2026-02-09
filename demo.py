"""
demo.py
Spring 2023 PJW

Demonstrate an inner join and a few other features of Pandas.
"""

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 300

#
#  Set up a dictionary to keep all the FIPS codes in both files as
#  strings when the files are being read. Use a dictionary comprehension
#  for convenience
#

fips_vars = ['Region','Division','State','STATEFP']
fips_cols = {col:str for col in fips_vars}

#
#  Read the data. OK to use the fips_cols for both since it's not
#  a problem for it to contain entries for variables that aren't in
#  a dataset.
#

name_data = pd.read_csv('state_name.csv',dtype=fips_cols)
pop_data = pd.read_csv('state_pop.csv',dtype=fips_cols)

#%%

#
#  Look at the state codes present in each file. Use set variables
#  to get lists of unique entries.
#

name_states = set( name_data['State'] )
pop_states = set( pop_data['STATEFP'] )

#  What's in name_data?

print( f"\nRaw state codes in name data ({len(name_data)}):" )
print( name_data['State'].to_list() )

print( f"\nUnique state codes in name data ({len(name_states)}):" )
print( sorted(name_states) )

#  What's in pop_data?

print( f"\nUnique state codes in pop data ({len(pop_states)}):" )
print( sorted(pop_states) )

#  Where do they differ?

print( "\nState codes in name_data not in pop data:" )
print( name_states - pop_states )

print( "\nState codes in pop_data not in pop data:" )
print( pop_states - name_states )

#%%
#
#  But wait, there's more: works with sets of tuples, too
#

tset1 = set( [ (1,2), (2,3), (1,3), (2,3)      ] )
tset2 = set( [        (2,3), (1,3),       (2,4)] )

print( "\nTuple set 1:", tset1 )
print( "Difference from set 2:", tset1 - tset2 )

#%%
#
#  Do an inner join of the population data onto the name data. Will keep only
#  the rows for states and DC since the population file doesn't have populations
#  for Census regions. Also drops Puerto Rico, which is in the population data
#  but isn't in the state name file.
#

merged = name_data.merge(pop_data,left_on="State",right_on="STATEFP",how='inner')

#%%
#
#  Set the index to the state's Division. The index in Pandas doesn't need
#  to be unique except in certain circumstances.
#

merged = merged.set_index('Division')

#  Use the .head() method to print out the first few rows

print( '\n', merged.head() )

#  Use the .loc[] operation to print out the data for Division 8

print( '\n', merged.loc["8"] )

#%%
#
#  Aggregate the population by Census division
#

group_by_div = merged.groupby('Division')
div_pop = group_by_div['pop'].sum()

print(div_pop)

#%%
#
#  Compute each state's percentage of its division population. Pandas
#  automatically lines up the data by Division using the indexes of
#  merged and div_pop.
#

merged['percent'] = 100*merged['pop']/div_pop
merged['percent'] = merged['percent'].round(3)

#%%
#
#  Sort the output file by STATEFP and then write it out
#

merged = merged.sort_values('STATEFP')
merged.to_csv('demo-merged.csv')

#%%
#
#  Look over three of the divisions via a loop. More convenient
#  and scalable than writing out separate plot statements for each
#  figure.
#

div_info = [
    ("3","East North Central"),
    ("5","South Atlantic"),
    ("8","Mountain")
    ]

for number,name in div_info:

    sel = merged.loc[number]

    print( f'\n{name} Division:\n' )
    print( sel )
    print( '\nCheck:', round(sel['percent'].sum(),2) )

    fig,ax = plt.subplots()
    fig.suptitle(f"Census Division: {name}")
    sel = sel.sort_values('percent')
    sel.plot.barh(x='Name',y='percent',ax=ax,legend=None)
    ax.set_ylabel(None)
    ax.set_xlabel('Percent of division')
    if number=='5':
        fig.savefig(f'div{number}-1before.png')
    fig.tight_layout()
    if number=='5':
        fig.savefig(f'div{number}-2after.png')
