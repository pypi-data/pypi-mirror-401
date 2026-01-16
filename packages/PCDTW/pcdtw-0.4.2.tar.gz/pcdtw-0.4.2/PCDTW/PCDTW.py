#!/usr/bin/env python
# coding: utf-8

# In[1]:


#This performs a single peak MWHP conversion on an amino acid sequence
#NormType can be AbsMax or MinMax
def PCDTWConvert(x,PCProp1='Mass',PCProp2='HydroPho',normalize=True,NormType='MinMax'):
    BaseArray=NoteValueConverter(PCProp1,PCProp2,Normalize=normalize,NormType=NormType)

    #Create an empty list to hold the vectors produced from each run of the loop (JD).
    tempnamesLST=[]
    temptpLST=[]
    tempspLST=[]
  
    currentseq = x
    
    lengther=len(currentseq)   
    
    #Convert all of the charaters to upper before converting it to a list (JD)
    currentseq=currentseq.upper()
    
    #Convert the current sequence to a list (JD)
    currentseq=list(currentseq)
    
    #Loop through all of the characters and if any are not allowed amino acids, replace them with a 'G'(AK)
    for j in range(lengther):
            strAllowedChars = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L","M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"]
    
            if currentseq[j] not in strAllowedChars: 
                currentseq[j] = currentseq[j].replace(currentseq[j],'G')
    
    #Convert the list back to a string (JD)
    currentseq=''.join(currentseq)
   
    ##This block of code creates a vector containing only the notevalues representing the amino acid sequence (JD).    
    NoteVec=[]
    ender=currentseq[-1]
    currentseq="G"+currentseq+ender
    lengther=len(currentseq)
    
    for k in range(lengther):
        if k==lengther:
            NoteVec.append(BaseArray[currentseq[k-1]].NoteValue)
        else:
            NoteVec.append(BaseArray[currentseq[k]].NoteValue)
  
    ##This block of code converts a vector of NoteValues to a single-peak vector (JD)   
    lengther2=(len(NoteVec))-1
    SinglePeakOutVector=[]
    
    for l in range(lengther2):
        if l==0:
            Outvalue=((NoteVec[l]*2)+((NoteVec[l]+NoteVec[l+1])/2))/2
            SinglePeakOutVector.append(round(Outvalue,4))
        else:
            Outvalue=((NoteVec[l])+((NoteVec[l]+NoteVec[l+1])/2)+((NoteVec[l]+NoteVec[l-1])/2))/2  
            SinglePeakOutVector.append(round(Outvalue,4))

    return SinglePeakOutVector[1:], NoteVec

#Conversion function that takes any two PC properties and converts them to a notevalue list
#NormType can be AbsMax or MinMax
def NoteValueConverter(PropA,PropB,Normalize=True,NormType='MinMax'):
    
    import pandas as pd
    
    #The values in this dataframe were taken from DOI:10.1371/journal.pone.0147 and vary slightly from the values used in
    #The MWHP algorithm used in Dixson and Azad 2021.  Zero values were treated as 0.001 here except for hydrophobicity
    #where they were set to 1 as in the original algorithm.  The values for hydrophobicity are mostly from Monera 1995 except for 
    #proline that was not included in that publication.  The value for proline was set at -46 in accordance with the chart at
    #https://www.sigmaaldrich.com/US/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart?srsltid=AfmBOop298sG6HwDyQ7tvsDFLsBOA2B9f8MQMalLOrTFF3h3_fC7iqZC
    #which includes the values from Monera et al 1995.

    
    PCPropertiesRaw=pd.DataFrame.from_dict({'HydroPho':[1,41,97,74,100,97,-23,-10,-31,-5,-46,76,99,49,63,8,-14,-28,-55,13],
                                    'HydroPhIl':[0.001,-0.5,-1.8,-1.3,-2.5,-3.4,3,0.2,3,0.3,0.001,-1.5,-1.8,-1,-2.3,-0.5,3,2,3,-0.4],
                                    'Hbond':[2,2,2,2,2,3,2,4,4,4,2,2,2,2,3,4,4,4,4,4],
                                    'SideVol':[0.001,27.5,93.5,94.1,115.5,145.5,100,80.7,62,29.3,41.9,71.5,93.5,44.6,117.3,79,105,58.7,40,51.3],
                                    'Polarity':[9,8.1,4.9,5.7,5.2,5.4,11.3,10.5,12.3,9.2,8,5.9,5.2,5.5,6.2,10.4,10.5,11.6,13,8.6],
                                    'Polarizability':[0.001,0.046,0.186,0.221,0.29,0.409,0.219,0.18,0.151,0.062,0.131,0.14,0.186,0.128,0.298,0.23,0.18,0.134,0.105,0.108],
                                    'SASA':[0.881,1.181,1.931,2.034,2.228,2.663,2.258,1.932,1.862,1.298,1.468,1.645,1.81,1.461,2.368,2.025,1.932,1.655,1.587,1.525],
                                    'NCI':[0.179052,0.007187,0.051672,0.002683,0.037552,0.037977,0.017708,0.049211,0.006802,0.004627,0.239531,0.057004,0.021631,-0.03661,0.023599,-0.01069,0.049211,0.005392,-0.02382,0.003352],
                                    'Mass':[57.05,71.08,113.16,131.2,147.18,186.22,128.18,128.13,129.12,87.08,97.12,99.13,113.16,103.15,163.18,137.14,156.19,114.11,115.09,101.11],
                                    'None':[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]},
                                    orient='index', columns=['G','A','L','M','F','W','K','Q','E','S','P','V','I','C','Y','H','R','N','D','T'])
    
    PCPropertiesNorm=pd.DataFrame()
    PCProperties=pd.DataFrame()

    def absolute_maximum_scale(series):
        return series / series.abs().max()

    def min_maximum_scale(series):
        # Correct Min-Max Scaling: (x - min) / (max - min)
        min_val = series.min()
        max_val = series.max()
        
        # Check for division by zero (e.g., if all values are the same)
        if (max_val - min_val) == 0:
            return series.copy() # Or return a series of a single value like 1 or 0
        
        return (series - min_val) / (max_val - min_val)

    PCPropertiesNorm=PCPropertiesRaw.transpose()

    for col in PCPropertiesNorm.columns:
        if NormType=="AbsMax":
            PCPropertiesNorm[col] = absolute_maximum_scale(PCPropertiesNorm[col])
        elif NormType=="MinMax":
            PCPropertiesNorm[col] = min_maximum_scale(PCPropertiesNorm[col])
        
    PCPropertiesNorm=PCPropertiesNorm.transpose() 
    
    if Normalize is True:
        PCProperties=PCPropertiesNorm
    else:
        PCProperties=PCPropertiesRaw
     
    PreNotesA=PCProperties.loc[PropA].tolist()
    PreNotesB=PCProperties.loc[PropB].tolist()
    
    MaxNoteA=max(PreNotesA)
    
    outNoteslst=[]
    
    for i in range(20):
        R=PCProperties.loc[PropA].tolist()[i]
        G=max(PreNotesA)
        H=PCProperties.loc[PropB].tolist()[i]
        V=round(((R/G)*H),4)
        outNoteslst.append(V)
        
    BaseArray=pd.DataFrame.from_dict({
        'NoteValue': outNoteslst},
    orient='index', columns=['G','A','L','M','F','W','K','Q','E','S','P','V','I','C','Y','H','R','N','D','T'])
   
    return BaseArray



# In[2]:


#This performs a single peak MWHP alignment
#If you want to use only one PC property then you need to set PCProp2='None'
def PCDTWPWAlign(inputseq1str,inputseq2str,PCProp1='Mass',PCProp2='HydroPho',Penalty=0,Window=3,GAP='Lower'):#GAP can be 'Lower' or "Gap"
    
    
    from dtaidistance import dtw
    import numpy as np

    vector1=PCDTWConvert(inputseq1str,PCProp1,PCProp2)[0]
    vector2=PCDTWConvert(inputseq2str,PCProp1,PCProp2)[0]

    path=dtw.warping_path(vector1, vector2,penalty=Penalty,window=Window)
    
    #Split the path into two lists that represent index values of the original sequence.
    vector1indexlst, vector2indexlst = zip(*path)
    
    alignedseq1=""
    alignedseq2=""
    
    h=0
    while h <(len(vector1indexlst)):
        looker1=vector1indexlst[h]
        temp1counter=vector1indexlst.count(looker1)
        if temp1counter==1:
            alignedseq1=alignedseq1+(list(inputseq1str))[vector1indexlst[h]]
            h+=temp1counter
            
        elif temp1counter>1:
            
            if GAP=='Lower':
                gapper=((list(inputseq1str))[vector1indexlst[h]]).lower()
                for l in range(temp1counter):
                    alignedseq1=alignedseq1+gapper
                h+=temp1counter
                
            elif GAP=='Gap':
                alignedseq1=alignedseq1+(list(inputseq1str))[vector1indexlst[h]]
                for l in range(temp1counter-1):
                    alignedseq1=alignedseq1+"-"                  
                h+=temp1counter
    
    
    j=0
    while j <(len(vector2indexlst)):
        looker2=vector2indexlst[j]
        temp2counter=vector2indexlst.count(looker2)
        if temp2counter==1:
            alignedseq2=alignedseq2+(list(inputseq2str))[vector2indexlst[j]]
            j+=temp2counter
            
        elif temp2counter>1:
            
            if GAP=='Lower':
                gapper=((list(inputseq2str))[vector2indexlst[j]]).lower()
                
                for l in range(temp2counter):
                    alignedseq2=alignedseq2+gapper
                j+=temp2counter
                    
            elif GAP=='Gap':
                alignedseq2=alignedseq2+(list(inputseq2str))[vector2indexlst[j]]
                for l in range(temp2counter-1):
                    alignedseq2=alignedseq2+"-"
                j+=temp2counter
            
            
###########################GET THE ALIGNED VECTORS########################################
    alignedvec1=[]
    alignedvec2=[]
    
    h=0
    while h <(len(vector1indexlst)):
        looker1=vector1indexlst[h]
        temp1counter=vector1indexlst.count(looker1)
        if temp1counter==1:
            alignedvec1.append(vector1[vector1indexlst[h]])
            h+=temp1counter
        elif temp1counter>1:
            alignedvec1.append(vector1[vector1indexlst[h]])
            for l in range(temp1counter-1):
                alignedvec1.append(vector1[vector1indexlst[h]])
            h+=temp1counter
    
    
    j=0
    while j <(len(vector2indexlst)):
        looker2=vector2indexlst[j]
        temp2counter=vector2indexlst.count(looker2)
        if temp2counter==1:
            alignedvec2.append(vector2[vector2indexlst[j]])
            j+=temp2counter
        elif temp2counter>1:
            alignedvec2.append(vector2[vector2indexlst[j]])
            for l in range(temp2counter-1):
                alignedvec2.append(vector2[vector2indexlst[j]])
            j+=temp2counter
    outp1arr=np.array(alignedvec1)
    outp2arr=np.array(alignedvec2)
    ConsensusVector=(outp1arr+outp2arr)/2
            
###########################GET THE ALIGNED VECTORS########################################
    
    
    GAPS=(alignedseq1+alignedseq2).count('-')
    Seq1Alignstr=alignedseq1
    Seq2Alignstr=alignedseq2
    
    counter=0
    for i in range(len(Seq1Alignstr)):
        if Seq1Alignstr[i]==Seq2Alignstr[i]:
            counter=counter+1
    identity=(int((counter/len(Seq1Alignstr))*100))
    
    midalignstr=''
    for i in range(len(Seq1Alignstr)):
        if Seq1Alignstr[i]==Seq2Alignstr[i]:
            midalignstr=midalignstr+'|'
        else:
            midalignstr=midalignstr+' '
    FullAlignment= Seq1Alignstr+'\n'+midalignstr+'\n'+Seq2Alignstr
    
    #Full list of variables that could be returned
    PCDTWAlnResult={
        'Seq1AlignedString':Seq1Alignstr,
        'Seq2AlignedString':Seq2Alignstr,
        'FullAlignment':FullAlignment,
        'Identity':identity,
        'ConsensusVector':ConsensusVector       
                   }

    return PCDTWAlnResult


# In[3]:


#This returns the dtw distance per residue.  Default is single peak vector (i.e. one peak per residue)
def PCDTWDist(Seq1,Seq2,PCProp1='Mass',PCProp2='HydroPho',PeaksPerRes=1,Penalty=0,Window=3):
    from dtaidistance import dtw
    Vec1=PCDTWConvert(Seq1,PCProp1,PCProp2)[0]
    Vec2=PCDTWConvert(Seq2,PCProp1,PCProp2)[0]
    
    DTWDistance = dtw.distance(Vec1, Vec2, penalty=Penalty, window=Window)
    DTWDistance=DTWDistance/(len(Vec1)*PeaksPerRes)
    DTWDistance=round(DTWDistance,3)

    return DTWDistance


# In[4]:


#Function to evolve a sequence with the objective of minimizing the physicochemical change (2 properties) while maximizing the sequence level change.
#The sequences output from this function will vary slightly from those Dixson et. al. 2025 because the hydrophobicity values have been updated
#This change is discussed further in the NoteValueConverter function comments above.

def PCEvolve(Seq='GALM', PCProp1='Mass', PCProp2='HydroPho', BaseName='ProtX'):
    import pandas as pd
    NoteVector = (PCDTWConvert(x=Seq, PCProp1=PCProp1, PCProp2=PCProp2, normalize=False))[1]
    NoteVector=NoteVector[:-1]
    NoteVector=NoteVector[1:]

    #Create an empty dataframe to hold the top three residues that match the input sequence
    MatchedRes=pd.DataFrame()      
    
    # #Creat lists to hold the residues and the notevalue for each residue
    NoteResLst=(NoteValueConverter(PropA=PCProp1,PropB=PCProp2,Normalize=False)).columns.tolist()  
    NoteValLst=(NoteValueConverter(PropA=PCProp1,PropB=PCProp2,Normalize=False)).iloc[0].tolist()

    #Put the Notevalues into a dict
    NoteDict = dict(zip(NoteResLst, NoteValLst))

    #Convert the input sequence to a vector of note values
    NoteValues = [NoteDict[char] for char in Seq if char in NoteDict]

    #Find the closest fully divergent sequence to the input NoteValues
    FullDivSeq = []
    for value in NoteValues:
        closest_key = None
        min_difference = float('inf')
        
        for key, dict_value in NoteDict.items():
            difference = abs(dict_value - value)
            
            if difference < min_difference and dict_value != value:
                min_difference = difference
                closest_key = key
        
        if closest_key is not None:
            FullDivSeq.append(closest_key)

    #Iterate through the NoteValues 20 times with a step of 0.05 difference so that a residue is only replaced if it is the step percentage value
    #or less different than the original sequence
    fasta_output = ""
    threshold = 0  # Starts at 0% for identical sequence
    previous_seq = Seq  # Initialize with original sequence to exclude it
    seq_number = 1  # Output sequence numbering
    
    for i in range(20):
        new_seq = ""
    
        for j, char in enumerate(Seq):
            if char in NoteDict:
                original_value = NoteDict[char]
                alternative_value = NoteDict.get(FullDivSeq[j], original_value)  # Alternative or original value
                percent_difference = abs(alternative_value - original_value) / original_value * 100
    
                # Final iteration: Apply 95% threshold and include all values exceeding it
                if i == 19 and percent_difference > 95:
                    new_seq += FullDivSeq[j]
                elif percent_difference <= threshold and alternative_value != original_value:
                    new_seq += FullDivSeq[j]
                else:
                    new_seq += char
            else:
                new_seq += char  # Preserve unchanged if not in dictionary
    
        # Append sequence only if it's different from the previous one AND not the original Seq
        if new_seq != previous_seq:
            fasta_output += f">{BaseName}_{'SimHomolog_'}{seq_number}\n{new_seq}\n"
            previous_seq = new_seq  # Update sequence tracker
            seq_number += 1  # Increment naming only for unique sequences
    
        # Increase threshold by 5% per iteration, stopping at 95% for the final loop
        threshold = min(threshold + 5, 95)
       
    return fasta_output


# In[5]:


#Function to take a fasta file of protein sequences, convert them to PC vectors, calculate a PCDTW distance matrix and output a newick dedrogram

def PCDTWTree(FastaFile='Your_File_Location.fasta',PCProp1='Mass', PCProp2='HydroPho'):

    def get_newick(node, parent_dist, leaf_names, newick=""):

        if node.is_leaf():
            return f"{leaf_names[node.id]}:{parent_dist - node.dist}{newick}"
        else:
            if len(newick) > 0:
                newick = f"):{parent_dist - node.dist}{newick}"
            else:
                newick = ");"
            newick = get_newick(node.get_left(), node.dist, leaf_names, newick=newick)
            newick = get_newick(node.get_right(), node.dist, leaf_names, newick=f",{newick}")
            newick = f"({newick}"
        return newick

    #Open the FASTA file
    from Bio import SeqIO
    records = list(SeqIO.parse(FastaFile, "fasta"))

    #Convert the sequences into vectors and put them into a dataframe
    import pandas as pd
    import numpy as np
    nameslst=[]
    vectorlst=[]
    for i in range(len(records)):
        nameslst.append(records[i].description)
        x=records[i].seq
        vector=PCDTWConvert(x,PCProp1=PCProp1,PCProp2=PCProp2,normalize=True)[0]
        vectorlst.append(np.array(vector))
    vectorsDF=pd.DataFrame({"NAME": nameslst, "VECTOR": vectorlst})
   
    #Create a PCDTW distance matrix
    from dtaidistance import dtw

    distanceMatrix = dtw.distance_matrix_fast(vectorlst,compact=True)
    
    #Perform UPGMA hierarchical cluster
    from scipy.cluster.hierarchy import average, dendrogram, linkage
    outDND=average(distanceMatrix) 

    #Perform UPGMA Hierarchical clustering and output the tree in newick format.
    from scipy.cluster import hierarchy

    tree = hierarchy.to_tree(outDND, False)
  
    newickOutput = get_newick(tree, tree.dist, nameslst)
    
    import matplotlib.pyplot as plt
    from Bio import Phylo
    from io import StringIO

    print("Trees will only be drawn as .png if there are 100 sequences or less in your input file.\nThe newick format tree will be "\
          "included regardless of the number of sequences input.")

    def show_newick_tree(newick_str):

        tree = Phylo.read(StringIO(newick_str), "newick")
    
        # Create figure with flexible size
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # Remove axis frame (bounding box)
        ax.set_frame_on(False)
    
        # Remove axes (x and y)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
    
        # Draw tree without extra constraints
        Phylo.draw(tree, axes=ax)
    
        # Adjust spacing dynamically
        plt.subplots_adjust(left=0.2, right=0.8, top=0.95, bottom=0.05)
    
        plt.show()


    if len(nameslst)<101:
        show_newick_tree(newickOutput)


    return newickOutput



    


# In[6]:


#MSA function.  Original version written by Tanmayi Akasapu and Jamie Dixson. Optimized by Jamie Dixson
# import PCDTW
import numpy as np
from Bio import SeqIO
from joblib import Parallel, delayed

def PCDTWMSAlign(FASTALoc, PCProp1='Mass', PCProp2='HydroPho', n_jobs=-1):

    # Read the input sequences from a fasta file
    if isinstance(FASTALoc, str):
        records = list(SeqIO.parse(FASTALoc, "fasta"))
        seqs = [str(record.seq) for record in records]
        names = [record.id for record in records]
    elif isinstance(FASTALoc, list):
        seqs = [str(seq) for seq in FASTALoc]
        names = [f"seq{i+1}" for i in range(len(seqs))]
    else:
        raise ValueError("FASTALoc must be a file path (str) or a list of sequences")

    seqs_len = len(seqs)
    if seqs_len < 2:
        raise ValueError("At least two sequences are required for MSA")

    # Compute pairwise distance matrix to find the star sequence
    asym_mat = np.zeros((seqs_len, seqs_len), dtype=np.float64)
    indices = [(i, j) for i in range(seqs_len) for j in range(i + 1, seqs_len)]
    distances = Parallel(n_jobs=n_jobs)(
        delayed(lambda i, j: PCDTWDist(seqs[i], seqs[j], PCProp1=PCProp1, PCProp2=PCProp2))(i, j)
        for i, j in indices
    )
    for k, (i, j) in enumerate(indices):
        asym_mat[i, j] = distances[k]
        asym_mat[j, i] = distances[k] 

    # Make the distance matrix symetric
    sym_matrix = (asym_mat + asym_mat.T) / 2
    np.fill_diagonal(sym_matrix, 0)

    # Find the star sequence index
    star_idx = np.argmin(np.sum(sym_matrix, axis=1))
    star_seq = seqs[star_idx]
    non_star_seqs = seqs[:star_idx] + seqs[star_idx + 1:]
    non_star_indices = list(range(star_idx)) + list(range(star_idx + 1, seqs_len))

    # Perform pairwise alignments to star sequence
    alignments = Parallel(n_jobs=n_jobs)(
        delayed(lambda seq: (
            PCDTWPWAlign(star_seq, seq, PCProp1=PCProp1, PCProp2=PCProp2, Penalty=0, Window=3, GAP='Gap')
        ))(seq) for seq in non_star_seqs
    )
    alignments = [
        (aln['Seq1AlignedString'].replace('\n', '').replace('\r', ''),
         aln['Seq2AlignedString'].replace('\n', '').replace('\r', ''))
        for aln in alignments
    ]

    # Initialize MSA with the first pairwise alignment
    star0, other0 = alignments[0]
    msa = np.array([list(star0), list(other0)], dtype=np.dtype('U1'))
    seq_counter = 1
    names_dict = {0: 'star', 1: 'seq1'}

    # Merge the remaining alignments
    for aln_star, aln_other in alignments[1:]:
        seq_counter += 1
        aln_star = np.array(list(aln_star), dtype=np.dtype('U1'))
        aln_other = np.array(list(aln_other), dtype=np.dtype('U1'))
        
        # Pre-allocate new MSA with enough space
        max_len = msa.shape[1] + len(aln_star)
        new_msa = np.full((msa.shape[0] + 1, max_len), '-', dtype=np.dtype('U1'))
        new_msa[:msa.shape[0], :msa.shape[1]] = msa
        i = j = k = 0

        # Merge the sequences
        while i < msa.shape[1] or j < len(aln_star):
            a = msa[0, i] if i < msa.shape[1] else None
            b = aln_star[j] if j < len(aln_star) else None

            if a is not None and b is not None and a == b:
                new_msa[:-1, k] = msa[:, i]
                new_msa[-1, k] = aln_other[j]
                i += 1
                j += 1
            elif a == '-' and (b != '-' or b is None):
                new_msa[:-1, k] = msa[:, i]
                new_msa[-1, k] = '-'
                i += 1
            elif b == '-' and (a != '-' or a is None):
                new_msa[:-1, k] = '-'
                new_msa[-1, k] = aln_other[j]
                j += 1
            elif a is None and b is not None:
                new_msa[:-1, k] = '-'
                new_msa[-1, k] = aln_other[j]
                j += 1
            elif b is None and a is not None:
                new_msa[:-1, k] = msa[:, i]
                new_msa[-1, k] = '-'
                i += 1
            k += 1

        # Trim excess columns
        msa = new_msa[:, :k]
        names_dict[msa.shape[0] - 1] = f"seq{seq_counter}"

    # Prepare a list of aligned sequences as output
    keys_order = ['star'] + [f"seq{i+1}" for i in range(seq_counter)]
    aligned_seqs = [''.join(msa[i]) for i in range(msa.shape[0])]
    name_mapping = {names_dict[i]: names[star_idx if i == 0 else non_star_indices[i-1]] for i in range(msa.shape[0])}
    
    # Format the output string so it is in fasta format
    output_str = ""
    for key in keys_order:
        output_str += f">{name_mapping[key]}\n{aligned_seqs[keys_order.index(key)]}\n"

    return aligned_seqs, output_str


# In[10]:


#Import libraries and open the dataframe
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import PCDTW

#Function to determine which PC properties are most conserved among a group of homologous proteins.
def FindConservation(FASTALoc):
    #Initialize the summary stats lists
    pairlst=[]
    dimlst=[]
    meanlst=[]
    madlst=[]
    

    #Take a fasta file as input
    records = list(SeqIO.parse(FASTALoc, "fasta"))
    
    #Convert the fasta sequences into 45D vectors
    PCCombinations=[('HydroPho', 'HydroPhIl'), ('HydroPho', 'Hbond'), ('HydroPho', 'SideVol'), ('HydroPho', 'Polarity'), ('HydroPho', 'Polarizability'), ('HydroPho', 'SASA'), ('HydroPho', 'NCI'), ('HydroPho', 'Mass'), ('HydroPho', 'None'), ('HydroPhIl', 'Hbond'), ('HydroPhIl', 'SideVol'), ('HydroPhIl', 'Polarity'), ('HydroPhIl', 'Polarizability'), ('HydroPhIl', 'SASA'), ('HydroPhIl', 'NCI'), ('HydroPhIl', 'Mass'), ('HydroPhIl', 'None'), ('Hbond', 'SideVol'), ('Hbond', 'Polarity'), ('Hbond', 'Polarizability'), ('Hbond', 'SASA'), ('Hbond', 'NCI'), ('Hbond', 'Mass'), ('Hbond', 'None'), ('SideVol', 'Polarity'), ('SideVol', 'Polarizability'), ('SideVol', 'SASA'), ('SideVol', 'NCI'), ('SideVol', 'Mass'), ('SideVol', 'None'), ('Polarity', 'Polarizability'), ('Polarity', 'SASA'), ('Polarity', 'NCI'), ('Polarity', 'Mass'), ('Polarity', 'None'), ('Polarizability', 'SASA'), ('Polarizability', 'NCI'), ('Polarizability', 'Mass'), ('Polarizability', 'None'), ('SASA', 'NCI'), ('SASA', 'Mass'), ('SASA', 'None'), ('NCI', 'Mass'), ('NCI', 'None'), ('Mass', 'None')]

    #Create 45D vector for each sequence in the fasta file
    Vector45lst=[]
    for i in range(len(records)):

        sequence=records[i].seq

        full45Dvector=PCDTW45DConvert(sequence)

            
        Vector45lst.append(np.round(np.array(full45Dvector),decimals=4))

    for j in range(len(Vector45lst[0])):  # dimensions
        proplbl1=PCCombinations[j][0]
        proplbl2=PCCombinations[j][1]
        analyzeVec = []
        for k in range(len(Vector45lst)):  # sequences
            analyzeVec.append(Vector45lst[k][j])  


        # 1. Find the length of the longest vector
        max_len = max(len(v) for v in analyzeVec)

        resampled_vectors = []

        # 2. Stretch and resample all vectors
        for vec in analyzeVec:
            if len(vec) < 2:
                print(f"Warning: Skipping vector with length less than 2: {vec}")
                continue

            # Create x-coordinates for the original vector
            x_orig = np.linspace(0, 1, len(vec))
            # Create x-coordinates for the resampled vector
            x_new = np.linspace(0, 1, max_len)

            # Use linear interpolation to resample
            f = interp1d(x_orig, vec, kind='linear')
            resampled_vec = f(x_new)
            resampled_vectors.append(resampled_vec)

        if not resampled_vectors:
            print("No valid vectors to process.")
            return None, None

        num_vectors = len(resampled_vectors)
        num_points = resampled_vectors[0].size

        # 3. Calculate pairwise distances for each point
        all_distances = np.zeros(num_points)
        num_pairs = 0

        for l in range(num_vectors):
            for m in range(l + 1, num_vectors):
                # Calculate the absolute difference (distance) at each point
                distances_at_points = np.abs(resampled_vectors[l] - resampled_vectors[m])
                all_distances += distances_at_points
                num_pairs += 1

        # 4. Calculate the average distance for each point
        if num_pairs > 0:
            average_distances = all_distances / num_pairs
        else:
            # If there's only one vector, there are no pairs.
            average_distances = np.zeros(num_points)

        if average_distances is not None:
            # Plot the average distance
            point_indices=range(1,len(average_distances)+1)
            plt.figure(figsize=(30, 6))
            plt.plot(point_indices, average_distances, marker='o')
            plt.title(f'Mean Absolute Pairwise Difference Among Stretched/Resampled Vectors (Dimension {j}) ({proplbl1}|{proplbl2})',fontsize=24)
            plt.xlabel('Vector Position',fontsize=24)
            plt.ylabel('Mean Absolute Difference',fontsize=24)
            plt.grid(True)
            plt.minorticks_on()
            plt.grid(which='both', linestyle='-', linewidth=0.5, alpha=0.5)
            plt.ylim(top=0.75)
            plt.show()
            
        #Compile the summary stats
        pairlst.append(proplbl1+"|"+proplbl2)
        dimlst.append(str(j))
        mean_diff=round((np.mean(average_distances)),4)
        meanlst.append(mean_diff)
        madlst.append(round((np.mean(np.abs(average_distances - mean_diff))),4))
    
    #Create a dataframe that shows the summary stats for the stretching of vectors to make them all the same length
    #using uniform stretching of the entire vector along with resampling.
    
    resultdf=pd.DataFrame()
    resultdf['PCPropPair']=pairlst
    resultdf['Dimension']=dimlst
    resultdf['Mean']=meanlst
    resultdf['MAD']=madlst

    resultdf = resultdf.sort_values(by=['Mean', 'MAD'], ascending=[True, True]).reset_index(drop=True)
    print("""
    ────────────────────────────────────────────────────────────
    NOTE: Uniform Vector Dataframe Sorting Explanation
    ────────────────────────────────────────────────────────────

      The dataframe below is sorted ascending by:
        • Mean (first) 
        • MAD (second)

      This means the top record represents the dimension with:
        • Least average pairwise distance
        • Highest uniformity along the sequence

      Recommendation:
        Use this top dimension or one of the top dimensions when:
          – Aligning protein family members
          – Searching for unknown homologs

    ────────────────────────────────────────────────────────────
    """)
    return resultdf
        

            
            


# In[8]:


import PCDTW
import numpy as np

#This 45D converter needs to be incorporated into the PCDTW package.
def PCDTW45DConvert(seq1, normalize=True, NormType='MinMax'):
    # All property pairs
    PCPropPairs = [
        ('HydroPho', 'HydroPhIl'), ('HydroPho', 'Hbond'), ('HydroPho', 'SideVol'),
        ('HydroPho', 'Polarity'), ('HydroPho', 'Polarizability'), ('HydroPho', 'SASA'),
        ('HydroPho', 'NCI'), ('HydroPho', 'Mass'), ('HydroPhIl', 'Hbond'),
        ('HydroPhIl', 'SideVol'), ('HydroPhIl', 'Polarity'), ('HydroPhIl', 'Polarizability'),
        ('HydroPhIl', 'SASA'), ('HydroPhIl', 'NCI'), ('HydroPhIl', 'Mass'),
        ('Hbond', 'SideVol'), ('Hbond', 'Polarity'), ('Hbond', 'Polarizability'),
        ('Hbond', 'SASA'), ('Hbond', 'NCI'), ('Hbond', 'Mass'), ('SideVol', 'Polarity'),
        ('SideVol', 'Polarizability'), ('SideVol', 'SASA'), ('SideVol', 'NCI'),
        ('SideVol', 'Mass'), ('Polarity', 'Polarizability'), ('Polarity', 'SASA'),
        ('Polarity', 'NCI'), ('Polarity', 'Mass'), ('Polarizability', 'SASA'),
        ('Polarizability', 'NCI'), ('Polarizability', 'Mass'), ('SASA', 'NCI'),
        ('SASA', 'Mass'), ('NCI', 'Mass'), ('HydroPho', 'None'), ('HydroPhIl', 'None'),
        ('Hbond', 'None'), ('SideVol', 'None'), ('Polarity', 'None'),
        ('Polarizability', 'None'), ('SASA', 'None'), ('NCI', 'None'), ('Mass', 'None')
    ]

    # Preprocess sequence once
    seq = seq1.upper()
    allowed = set(["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"])
    seq = ''.join([c if c in allowed else 'G' for c in seq])
    seq = "G" + seq + seq[-1]

    results = []
    for pcprop1, pcprop2 in PCPropPairs:
        # Build BaseArray for this property pair
        BaseArray = PCDTW.NoteValueConverter(pcprop1, pcprop2, Normalize=normalize, NormType=NormType)

        # Convert to NoteVec
        NoteVec = [BaseArray[c].NoteValue for c in seq]

        # Convert to SinglePeakOutVector
        SinglePeakOutVector = []
        for i in range(len(NoteVec)-1):
            if i == 0:
                val = ((NoteVec[i]*2) + ((NoteVec[i]+NoteVec[i+1])/2)) / 2
            else:
                val = (NoteVec[i] + ((NoteVec[i]+NoteVec[i+1])/2) + ((NoteVec[i]+NoteVec[i-1])/2)) / 2
            SinglePeakOutVector.append(round(val,4))

        results.append(SinglePeakOutVector[1:])  # skip first element

    return results

