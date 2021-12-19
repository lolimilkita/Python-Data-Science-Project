import pandas as pd
import streamlit as st
import altair as alt

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

row1_1, row1_2 = st.columns((1,3))

with row1_1:
    st.title("Perhitungan Sederhana DNA Nucleotide")

with row1_2:
    st.write(
    """
    ##
    DNA is a long chain of other chemicals and the most important are the four nucleotides, adenine, cytosine, guanine and thymine. A single DNA chain can contain billions of these four nucleotides and the order in which they occur is important! We call the order of these nucleotides in a bit of DNA a "DNA sequence".
    \n
    We represent a DNA sequence as an ordered collection of these four nucleotides and a common way to do that is with a string of characters such as "ATTACG" for a DNA sequence of 6 nucleotides. 'A' for adenine, 'C' for cytosine, 'G' for guanine, and 'T' for thymine.
     [Sumber](https://exercism.org/tracks/julia/exercises/nucleotide-count)
    \n
    Aplikasi ini menghitung komposisi nucleotide dari sebuah kueri DNA! [contoh rumus](https://rosalind.info/problems/dna/)
    """)

st.write("""
***
""")

st.header('Masukkan DNA sequence')

sequence_input = ">DNA Query Tiga\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area("Sequence input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:] # Skips the sequence name (first line)
sequence = ''.join(sequence) # Concatenates list to string

st.write("""
***
""")

st.header('INPUT (DNA Query)')

st.code("Gabungan DNA!\n" + sequence)

st.header('OUTPUT (DNA Nucleotide Count)')

def DNA_nucleotide_count(seq):
    d = dict([
                ('A',seq.count('A')),
                ('T',seq.count('T')),
                ('G',seq.count('G')),
                ('C',seq.count('C'))
                ])
    return d

X = DNA_nucleotide_count(sequence)

#X_label = list(X)
#X_values = list(X.values())


# Membuat kolom
row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,2))

with row2_1:
    st.write('Hasil dictionary')
    X

with row2_2:
    st.write('Hasil DataFrame')
    df = pd.DataFrame.from_dict(X, orient='index')
    df = df.rename({0: 'count'}, axis='columns')
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'nucleotide'})
    st.write(df)

with row2_3:
    st.write('Hasil text')
    st.write('Ada  ' + str(X['A']) + ' adenine (A)')
    st.write('Ada  ' + str(X['T']) + ' thymine (T)')
    st.write('Ada  ' + str(X['G']) + ' guanine (G)')
    st.write('Ada  ' + str(X['C']) + ' cytosine (C)')
    

with row2_4:
    st.write('Hasil Bar chart')
    p = alt.Chart(df).mark_bar().encode(
        x='nucleotide',
        y='count'
    )
    
    p = p.properties(
        width=alt.Step(80)
    )
    
    st.write(p)
