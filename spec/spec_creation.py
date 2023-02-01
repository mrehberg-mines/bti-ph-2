# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 20:39:03 2023

@author: mrehberg
"""

import pandas as pd
import os

global defined_terms

def escapeLatex(text, link):
    text = text.replace('$', '\$')
    text = text.replace('_', '\_')
    text = text.replace('%', '\%')
    text = text.replace('#', ' ')
    if link:
        text = createLink(text)
    return text

def createLink(text):
    text = text.replace('{ref:', '\\nameref{ref:')
    for key in defined_terms:
        value = defined_terms[key]
        term = '{term:'+key+'}'
        label = 'term:' + key
        link = '\hyperref['+label+']{'+value+'}'
        text = text.replace(term, link)
    return text

df = pd.read_excel('Requirements.xlsx', sheet_name='Spec', header=2, usecols=lambda x: 'Unnamed' not in x,).fillna('')
df = df[df.columns[0:4]]
defined_terms=dict()


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
            f.write(r'\subsubsection{{{}}}'.format(escapeLatex(sub, False)))
            f.write('\n')
        prev_sub = sub
        
        
       
        
        # If the value is a defined term, add it to the defined term dictionary
        if section == 'Defined Term':
            defined_terms.update({sub:text})
            f.write('\label{{term:{}}}'.format(escapeLatex(sub, False)))
        else:
            f.write('\label{{ref:{}}}'.format(escapeLatex(sub, False)))
        
        
        f.write('\n')
        f.write('{}'.format(escapeLatex(text, True)))
        f.write('\n')
    
  
for i in range(3):
    os.system("pdflatex bti-spec.tex")
