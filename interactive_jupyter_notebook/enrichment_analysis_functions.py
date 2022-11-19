"""
This module defines the functions used for
the Enrichment Analsysis scripts using KnetMiner knowledge graphs
"""

# import the python script containing the common queries
import common_queries as cq

# Import pandas, numpy, matplotlib, scipy, HTML, importlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import base64
from IPython.display import HTML
import importlib

# Import ipywidgets for interactive interface
import ipywidgets as widgets
from ipywidgets import interact, interact_manual

# Import SPARQLWrapper library to use the SPARQL endpoint
from SPARQLWrapper import SPARQLWrapper2

# create variable for SPARQL endpoint
sparql = SPARQLWrapper2 ("http://knetminer-data.cyverseuk.org/lodestar/sparql")



# ---------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- General Functions ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------- #


# A function to create list for the concepts
def get_concepts():
    concepts = ['Trait', 'BioProcess']
    return concepts


# A function to create dataframe for Tax IDs and their names
def df_taxID():
    """This function creates a dataframe for Tax IDs and their names."""

    dframe_taxID = pd.DataFrame({'Tax IDs': ['4565', '3702', '4530'],
                                'Tax Names': ['Triticum aestivum (wheat)',
                                            'Arabidopsis thaliana (thale cress)',
                                            'Oryza sativa (rice)'],
                                'Database URL': ['https://knetminer.com/ws/wheatknet/',
                                            'https://knetminer.com/ws/araknet/',
                                            'https://knetminer.com/ws/riceknet/']})
    return dframe_taxID


# create dataframe for evidence meaning
def df_evidence():
    """This function creates a dataframe for evidence meaning."""

    dframe_evidence = pd.DataFrame({'Evidence Code': ['TM_0-0', 'TM_0-1', 'TM_1-0', 'TM_1-1',
                                                  'GWAS_0-0', 'GWAS_0-1', 'GWAS_1-0', 'GWAS_1-1'],
                               'Evidence Type': ['Text Mining (TM)', 'Text Mining', 'Text Mining', 'Text Mining',
                                                'Genetic Study (GWAS)', 'Genetic Study', 'Genetic Study', 'Genetic Study'],
                               'Homology': [0, 0, 1, 1, 0, 0, 1, 1],
                               'Interaction': [0, 1, 0, 1, 0, 1, 0, 1]})

    return dframe_evidence


# create a function to flatten a list of lists into a single list
def flatten(xss):
    """This function flattens a list of lists into a single list."""

    return [x for xs in xss for x in xs]


# A function to create download link to save datafarames as csv files
# refrence: https://www.codegrepper.com/code-examples/python/download+csv+file+from+jupyter+notebook

def create_download_link(df, filename, title):
    """This function creates a download link to save datafarames as csv files."""

    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload,title=title,filename=filename)
    return HTML(html)



# ---------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------  Display Functions for Checkboxes and RadioButtons ------------------------------------------ #
# ---------------------------------------------------------------------------------------------------------------------------------- #


# refrence: https://stackoverflow.com/questions/57219796/ipywidgets-dynamic-creation-of-checkboxes-and-selection-of-data

def display_checkboxes(data):
    """This function creates and displays checkboxes for a list of data."""

    checkboxes = [widgets.Checkbox(value=False, description=label) for label in data]
    output = widgets.VBox(children=checkboxes)
    display(output)
    
    return checkboxes

def get_checkboxes_selection(checkboxes):
    """This function gets the selections of the checkboxes."""

    selected_data = []
    for i in range(0, len(checkboxes)):
        if checkboxes[i].value == True:
            selected_data = selected_data + [checkboxes[i].description]
    
    return selected_data


def display_radiobuttons(data):
    """This function creates and displays radio buttons for a list of data."""

    radiobuttons = widgets.RadioButtons(options = data, value = None)
    display(radiobuttons)

    return radiobuttons



# ---------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Function to get database files ------------------------------------------------------ #
# ---------------------------------------------------------------------------------------------------------------------------------- #


# Function to get all of the selected concept related to the genes
def get_database_csv(taxID, database, concept):
    """This function gets the chosen concept related to the genes from the database."""

    # import the python script containing the queries for the concept
    moduleName = f'{concept}_queries'
    concept_qu = importlib.import_module(moduleName)

    # create an empty list to append the results of each loop
    final_result = []

    # loop over the pathways
    for pathway in concept_qu.pathways:
        query = concept_qu.query_subset1%taxID + pathway + concept_qu.query_subset2
        # run the query
        sparql.setQuery (query)
        result = sparql.query().bindings
        result = [ [ r['geneAcc'].value, r['geneName'].value, r['ontologyTerm'].value,
                    r['preferredName'].value, r['evidence'].value] for r in result ]
        final_result += result


    # Render into a dataframe
    dframe_GeneTrait = pd.DataFrame (final_result, columns = ["Gene Accession", "Gene Name",
                                                               "Ontology Term", "Preferred Name",
                                                               "Evidence"])

    # remove repeated rows
    dframe_GeneTrait = dframe_GeneTrait.drop_duplicates()
    

    ##### editing the BioProc files for multiple accession #####
    if concept == 'BioProcess':
        for x, row in dframe_GeneTrait.iterrows():

            # edit Gene Accessions
            geneAccs = row['Gene Accession']
            # split if there are more than one accession, and take the first accession
            geneAcc1 = geneAccs.split(";")[0]
            # replace the gene accession with that one accession number
            row['Gene Accession'] = geneAcc1

            # edit Ontology Term accessions
            ontoTerms = row['Ontology Term']
            # split the terms
            ontoTermsList = ontoTerms.split(";")
            ontoTermsList.sort()
            # replace the ontology accession with the first GO term
            for acc in ontoTermsList:
                if acc.startswith('GO'):
                    row['Ontology Term'] = acc
                    break
    ##### END of editing the BioProc files #####

    
    ##### add the urls for the knowledge graph pathway (gene--concept)
    urls = []
    for x, row in dframe_GeneTrait.iterrows():
        # get Gene Accession
        geneAcc = row['Gene Accession']

        # Get Ontology Accession number
        ontoTerm = row['Ontology Term']
        # split if there are more than one accession, and take the first accession
        first_term = ontoTerm.split(";")[0]
        if "_" in first_term:
            term_split = first_term.split("_")
            onto_acc = term_split[0] + ":" + term_split[1]
        else:
            onto_acc = first_term
        
        # create the url and append it to the list
        url = f'{database}genepage?list={geneAcc}&keyword=%22{onto_acc}%22'
        urls.append(url)
        
    # add urls to dataframe
    dframe_GeneTrait['Network URL'] = urls

    # get CSV download link for the dataframe
    csv_link = create_download_link(dframe_GeneTrait, f'Gene{concept}Table_{taxID}.csv',
                                    f'Download Gene{concept}Table_{taxID}.csv file')
    display(csv_link)

    return csv_link




# ---------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Functions for Genes ----------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------- #


# Create a function to get the count of genes in the database for a species tax ID.
def get_gene_count(taxID):
    """This function gets the count of genes in the database for a species tax ID."""

    # run the query
    sparql.setQuery(cq.query_count_genes%taxID)
    result = sparql.query().bindings
    result = [ [ r['Count'].value] for r in result ]
    total_db_genes = int(result[0][0])
    
    return total_db_genes



# Use the study/user list of genes to extract their rows from the dframe_GeneTrait
def get_df_GeneTrait_filtered(dframe_GeneTrait, total_DEXgenes):
    """This function uses the study/user list of genes to extract their rows from the dframe_GeneTrait."""

    # Extract the rows containg the genes list from the first dataframe (dframe_GeneTrait)
    dframe_GeneTrait_filtered = dframe_GeneTrait[dframe_GeneTrait['Gene Accession'].isin(total_DEXgenes)]

    # Sort dframe_GeneTrait_filtered 
    dframe_GeneTrait_filtered = dframe_GeneTrait_filtered.sort_values(['Ontology Term', 'Gene Name', 'Evidence'],
                                                                    ascending = [True, True, True])

    # update the dataframe index
    dframe_GeneTrait_filtered = dframe_GeneTrait_filtered.reset_index(drop=True)

    return dframe_GeneTrait_filtered



# ---------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Functions for Enrichment Analysis --------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------- #


# Create a function to calculate adjusted p-values (or Q-values) using numpy
# refrence: https://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python

# p is p-values, q is adjusted p-values
def p_adjust_bh(p):
    """This function uses Benjamini-Hochberg p-value correction for multiple hypothesis testing."""

    p = np.asfarray(p) # Return an array converted to a float type
    by_descend = p.argsort()[::-1] # order by descending order
    steps = float(len(p)) / np.arange(len(p), 0, -1)
    q = np.minimum(1, np.minimum.accumulate(steps * p[by_descend]))
    return by_descend, q


# Perform Enrichment Analysis using SciPy and calculate adjusted p-value
def get_df_Ftest_sorted(dframe_GeneTrait, total_DEXgenes, total_db_genes):
    """This function performs enrichment analysis and calculates adjusted p-value."""

    # get dframe_GeneTrait_filtered
    dframe_GeneTrait_filtered = get_df_GeneTrait_filtered(dframe_GeneTrait, total_DEXgenes)

    # create dataframe to add the odd ratio and p-value
    df_Ftest = pd.DataFrame (columns = ["Ontology Term", "Preferred Name", "odds ratio", "exact p-value",
                                        "Reference Genes", "User/Study Genes"])

    # create list to add the Trait Accessions numbers
    traits =  []

    ### for each trait, calculate odds ratio, exact p-value and number of related genes in database and list ###

    for x, row in dframe_GeneTrait_filtered.iterrows():
        trait_acc = row['Ontology Term']
        
        if trait_acc not in traits:
            
            traits.append(trait_acc)
            trait_name = row['Preferred Name']
            
            # 1a. Get the complete set of genes linked to the trait in the gene list
            select_trait = dframe_GeneTrait_filtered.loc[dframe_GeneTrait_filtered['Ontology Term'] == trait_acc]
            
            # 1b. Get the distinct list of genes linked to the trait in the gene list
            trait_DEXgenes = set(select_trait['Gene Accession'].unique())
            
            
            # 2a. Get the complete set of genes linked to the trait in the database (dframe_GeneTrait)
            select_Totaltrait = dframe_GeneTrait.loc[dframe_GeneTrait['Ontology Term'] == trait_acc]
            
            # 2b. Get the distinct list of genes linked to the trait in dframe_GeneTrait
            total_TraitGenes = set(select_Totaltrait['Gene Accession'].unique())
            
            
            # 3. Calculate the odds ratio and p-value using scipy
            a= len(trait_DEXgenes)
            b= len(total_DEXgenes)-len(trait_DEXgenes)
            c= len(total_TraitGenes)-len(trait_DEXgenes)
            d= total_db_genes-a-b-c
            data = [[a, b], [c, d]]
            oddsratio, pvalue = stats.fisher_exact(data)
            
            # 4. Add the data to the df_Ftest table
            df = {'Ontology Term': trait_acc, 'Preferred Name': trait_name, 'odds ratio': oddsratio, 'exact p-value': pvalue,
                'Reference Genes': len(total_TraitGenes), 'User/Study Genes': a}
            df_Ftest = df_Ftest.append(df, ignore_index = True)


    ### calculate adjusted p-value ###

    # Get the list of p-values from the dataframe
    pvalues = df_Ftest['exact p-value'].tolist()

    # get by_descend and adj_pvalues
    by_descend, q = p_adjust_bh(pvalues)

    # sort the table by the indecies (used in the formula)
    df_Ftest_sorted = df_Ftest.reindex(by_descend)

    # add column to dataframe
    df_Ftest_sorted.insert(4, 'adj p-value', q)

    # sort the dataframe according to adjusted p-value and update the dataframe index
    df_Ftest_sorted = df_Ftest_sorted.sort_values(by=['adj p-value']).reset_index(drop=True)
    

    ### create download links for final tables and show first 10 rows of each table ###

    # gene-trait table:
    print("\nThe gene-concept table below has " + str(dframe_GeneTrait_filtered.shape[0]) +
    " rows.\nTo view the whole table, see the 'View whole tables section' or click on the download link below:")
    display(create_download_link(dframe_GeneTrait_filtered, "GeneConcept_filtered_table.csv", "Download gene-concept table CSV file"))

    # copy the head of the dataframe to avoid editing and changing data type of the original
    df_GeneTrait_filtered = dframe_GeneTrait_filtered[:].copy()
    df_GeneTrait_filtered = df_GeneTrait_filtered.head(10)
    # display gene-trait table by rendering the HTML to clickable
    s = "View Network"
    df_GeneTrait_filtered['Network URL'] = df_GeneTrait_filtered['Network URL'].apply(lambda x: f'<a href="{x}">{s}</a>')
    display(HTML(df_GeneTrait_filtered.to_html(render_links=True, escape=False)))

    # Trait enrichment table:
    print("\nThe enrichment table below has " + str(df_Ftest_sorted.shape[0]) +
    " rows.\nTo view the whole table, see the 'View whole tables section' or click on the download link below:")
    display(create_download_link(df_Ftest_sorted, "enrichment_table.csv", "Download enrichment table CSV file"))
    display(df_Ftest_sorted.head(10))

    return dframe_GeneTrait_filtered, df_Ftest_sorted



# ---------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Functions for GXA studies ----------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------- #

# Create a function to get the list of studies for each species
def get_study_list(taxID):
    """This function gets the list of studies for each species."""

    # run the query
    sparql.setQuery (cq.query_study_list%taxID)
    result = sparql.query().bindings
    final_result_study = [ [ r['studyAcc'].value, r['studyTitle'].value] for r in result ]

    # Render into a table
    dframe_study_list = pd.DataFrame ( final_result_study, columns = ["Study Accession", "Study Title"] )
    dframe_study_list = dframe_study_list.sort_values("Study Accession").reset_index(drop=True)
    dframe_study_list["Accession_Title"] = dframe_study_list["Study Accession"] + ": " + dframe_study_list["Study Title"]

    return dframe_study_list


# Get the differentially expressed genes in a study
def get_study_DEXgenes(studyAcc, filter=False, pvalue=0):
    """This function gets the differentially expressed genes in a study."""

    # run the query
    if filter == False:
        sparql.setQuery (cq.query_DEXgenes_in_study%studyAcc)
    else:
        sparql.setQuery (cq.query_FilterByPvalues%(pvalue, studyAcc))
    
    # get the results
    result = sparql.query().bindings
    final_result_study = [ [ r['geneAcc'].value] for r in result ]
    final_result_study = flatten(final_result_study)
    total_DEXgenes = set(final_result_study)

    return total_DEXgenes


# Get the number of differentially expressed genes in a study
def get_StudyGeneCount(studyAcc):
    """This function gets the count of genes in a study."""

    # run the query
    sparql.setQuery(cq.query_CountStudyGenes%studyAcc)
    result = sparql.query().bindings
    result = [ [ r['Count'].value] for r in result ]
    StudyGeneCount = int(result[0][0])

    return StudyGeneCount


# Get a datafarme for the pvalues in a study and the respective number of cumulative genes
def get_StudyPvalues(studyAcc):
    """This function gets the p-values for the genes in a study and the cumulative number of genes at each pvalue."""

    # run the query
    sparql.setQuery (cq.query_StudyPvalues%studyAcc)
    result = sparql.query().bindings
    StudyPvalues = [ [ r['pvalue'].value] for r in result ]
    # flatten the list of lists into a list
    StudyPvalues = flatten(StudyPvalues)
    # change the string number into float
    StudyPvalues = [float(x) for x in StudyPvalues]
    # sort the pvalues in ascending order
    StudyPvalues.sort(key=None, reverse=False)
    # Render into a dataframe
    df_StudyPvalues = pd.DataFrame (StudyPvalues, columns = ['StudyPvalues'])

    # get the counts(frequency) of the pvalues
    df_StudyPvalues_count = df_StudyPvalues['StudyPvalues'].value_counts().rename_axis('pvalues').reset_index(name='frequency')
    # sort the dataframe according to pvalues and reset the index
    df_StudyPvalues_count = df_StudyPvalues_count.sort_values('pvalues').reset_index(drop=True)
    # get the cumulative frequeny
    df_StudyPvalues_count['Cumulative Frequency'] = df_StudyPvalues_count['frequency'].cumsum()

    return df_StudyPvalues_count


# Show a cumulative frequency for the p-values for the differentially expressed genes in a study
def plot_pvalues(df_StudyPvalues_count, pvalues=0):
    """This function plots the cumulative number of genes against the p-values."""

    if pvalues==0:
        df_StudyPvalues_count.plot.line(x = 'pvalues', y = 'Cumulative Frequency', legend=False)
        plt.grid(axis='y', linestyle='--')
        plt.grid(axis='x', linestyle='--')
        plt.xlabel('p-values', fontweight='bold')
        plt.ylabel('cumulative gene frequency', fontweight='bold')
        plt.title('P-values Cumulative Frequency', fontweight='bold')
        plt.show()

    else:
        pvalue = df_StudyPvalues_count[df_StudyPvalues_count['pvalues'] <= pvalues].iloc[-1]['pvalues']
        geneNum = df_StudyPvalues_count[df_StudyPvalues_count['pvalues'] <= pvalues].iloc[-1]['Cumulative Frequency']

        df_StudyPvalues_count.plot.line(x = 'pvalues', y = 'Cumulative Frequency', legend=False)
        plt.grid(axis='y', linestyle='--')
        plt.grid(axis='x', linestyle='--')
        plt.xlabel('p-values', fontweight='bold')
        plt.ylabel('cumulative gene frequency', fontweight='bold')
        plt.axhline(y= geneNum, color='k', lw=0.8, ls='--')
        plt.axvline(x= pvalue, color='k', lw=0.8, ls='--')
        plt.text(0.04, 0, 'x=%1.4f, y=%1.0f' % (pvalue, geneNum), fontdict=None)
        plt.title('P-values Cumulative Frequency', fontweight='bold')
        plt.show()