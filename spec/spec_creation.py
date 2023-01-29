# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 20:39:03 2023

@author: mrehberg
"""

import pandas as pd


def escapeLatex(text):
    text = text.replace('$', '\$')
    text = text.replace('_', '\_')
    text = text.replace('%', '\%')
    
    return text





df = pd.read_excel('Requirements.xlsx', sheet_name='Spec', header=2, usecols=lambda x: 'Unnamed' not in x,).fillna('')
df = df[df.columns[0:4]]

with open('spec-info.tex', 'w') as f:
    # f.write('readme')
    prev_heading = ''
    prev_section = ''
    prev_sub = ''
    for row in range(len(df)):
        heading = df.loc[row, 'Heading']
        section = df.loc[row, 'Section']
        sub = df.loc[row, 'Subsection']
        text = df.loc[row, 'Requirement/Definition']
        
        if prev_heading != heading:
            f.write('\\newpage')
            f.write('\n')
            f.write('\\section{{{}}}'.format(heading))
            f.write('\n')
            
            
        prev_heading = heading
        
        if prev_section != section:
            f.write(r'\subsection{{{}}}'.format(section))
            f.write('\n')
        prev_section = section
        
        if prev_sub != sub:
            f.write(r'\subsubsection{{{}}}'.format(sub))
            f.write('\n')
        prev_sub = sub
        
        f.write('{}'.format(escapeLatex(text)))
        f.write('\n')