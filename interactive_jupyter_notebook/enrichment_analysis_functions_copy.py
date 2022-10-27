"""
This module defines the functions used for
the Enrichment Analsysis scripts using KnetMiner knowledge graphs
"""

# import the python script containing the common queries
import common_queries as cq

# Import SPARQLWrapper library to use the SPARQL endpoint
from SPARQLWrapper import SPARQLWrapper2

# Import pandas, numpy, matplotlib, scipy and HTML
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import base64
from IPython.display import HTML


# create variable for SPARQL endpoint
sparql = SPARQLWrapper2 ("http://knetminer-data.cyverseuk.org/lodestar/sparql")



# ---------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- General Functions ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------- #


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



# ---------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Function to get database files ------------------------------------------------------ #
# ---------------------------------------------------------------------------------------------------------------------------------- #

# Function to get all of the selected concept related to the genes
def get_database_csv(taxID, database,concept_qu):
    """This function gets all the traits related to the genes from the database."""

    # import the python script containing the trait queries
    import trait_queries as concept_qu
    
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
    
    
    # add the urls for the knowledge graph pathway (gene--trait)
    urls = []
    for x, row in dframe_GeneTrait.iterrows():
        # get Gene Accession
        geneAcc = row['Gene Accession']

        # Get Trait Accession
        ontoTerm = row['Ontology Term']
        # split if there are two trait accessions, and take the first accession
        first_term = ontoTerm.split(";")[0]
        # split the "TO" and the accession number
        if "_" in first_term:
            term_split = first_term.split("_")
        else:
            term_split = first_term.split(":")

        # condition in case there is only accession number without "TO" or "GO"
        onto = ''
        acc = ''
        if len(term_split) == 2:
            onto = term_split[0]+":"
            acc = term_split[1]
        else:
            acc = term_split[0]

        onto_acc = onto + acc

        url = f'{database}genepage?list={geneAcc}&keyword=%22{onto_acc}%22'

        urls.append(url)
        
    # add urls to dataframe
    dframe_GeneTrait['Network URL'] = urls

    # get CSV download link for the dataframe
    csv_link = create_download_link(dframe_GeneTrait, f'GeneTraitTable_{taxID}.csv',
                                    f'Download GeneTraitTable_{taxID}.csv file')
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
    
    print("Total Number of Genes = " + str(total_db_genes))
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

    # sort the dataframe according to adjusted p-value
    df_Ftest_sorted = df_Ftest_sorted.sort_values(by=['adj p-value'])

    # update the dataframe index
    df_Ftest_sorted = df_Ftest_sorted.reset_index(drop=True)
    

    ### create download links for final tables and show first 10 rows of each table ###

    # gene-trait table:
    print("\nThe gene-trait table below has " + str(dframe_GeneTrait_filtered.shape[0]) +
    " rows.\nTo view the whole table, see the 'View whole tables section' or click on the download link below:")
    display(create_download_link(dframe_GeneTrait_filtered, "GeneTrait_filtered_table.csv", "Download gene-trait table CSV file"))

    # copy the head of the dataframe to avoid editing and changing data type of the original
    df_GeneTrait_filtered = dframe_GeneTrait_filtered[:].copy()
    df_GeneTrait_filtered = df_GeneTrait_filtered.head(10)
    # display gene-trait table by rendering the HTML to clickable
    s = "View Network"
    df_GeneTrait_filtered['Network URL'] = df_GeneTrait_filtered['Network URL'].apply(lambda x: f'<a href="{x}">{s}</a>')
    display(HTML(df_GeneTrait_filtered.to_html(render_links=True, escape=False)))

    # Trait enrichment table:
    print("\nThe trait enrichment table below has " + str(df_Ftest_sorted.shape[0]) +
    " rows.\nTo view the whole table, see the 'View whole tables section' or click on the download link below:")
    display(create_download_link(df_Ftest_sorted, "trait_enrichment_table.csv", "Download trait enrichment table CSV file"))
    display(df_Ftest_sorted.head(10))

    return dframe_GeneTrait_filtered, df_Ftest_sorted
    


# ---------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Functions for a GXA study ----------------------------------------------------------- #
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

    return dframe_study_list


# Get the differentially expressed genes in a study
def get_study_DEXgenes(studyAcc):
    """This function gets the differentially expressed genes in a study."""

    # run the query
    sparql.setQuery (cq.query_DEXgenes_in_study%studyAcc)
    result = sparql.query().bindings
    final_result_study = [ [ r['geneAcc'].value] for r in result ]
    final_result_study = flatten(final_result_study)
    total_DEXgenes = set(final_result_study)

    print("Number of genes in study is: " + str(len(total_DEXgenes)))
    return total_DEXgenes


# Get the number of differentially expressed genes in a study
def get_StudyGeneCount(studyAcc):
    """This function gets the count of genes in a study."""

    # run the query
    sparql.setQuery(cq.query_CountStudyGenes%studyAcc)
    result = sparql.query().bindings
    result = [ [ r['Count'].value] for r in result ]
    StudyGeneCount = int(result[0][0])
    
    print("Total Number of Genes in study = " + str(StudyGeneCount))
    return StudyGeneCount


# Show a histogram for the p-values or a bar graph for ordical TPM, for the differentially expressed genes in a study
def get_StudyPvalues(studyAcc):
    """This function gets the p-values for the genes in a study or their ordidinal TPM
    and plots a histogram or a bar graph respectively."""

    # run the query
    sparql.setQuery (cq.query_StudyPvalues%studyAcc)
    result = sparql.query().bindings

    # if the study results are from Differential experiments, it will have p-values
    if 'pvalue' in result[0]:
        StudyPvalues = [ [ r['pvalue'].value] for r in result ]
        # flatten the list of lists into a list
        StudyPvalues = flatten(StudyPvalues)
        # change the string number into float
        StudyPvalues = [float(x) for x in StudyPvalues]
        # sort the pvalues in ascending order
        StudyPvalues.sort(key=None, reverse=False)

        # plot the p-values in a histogram using matplotlib
        plt.hist(StudyPvalues, edgecolor='black', bins=[0, 0.01, 0.02, 0.03, 0.04, 0.05])
        plt.grid(axis='y', linestyle='--')
        plt.xlabel('p-values', fontweight='bold')
        plt.ylabel('density', fontweight='bold')
        plt.title('P-values Histogram', fontweight='bold')
        plt.show()

    # if the study results are from Baseline experiments, it will have TPM
    # and we want to obtain the ordinal TPM as low, medium and high
    else:
        StudyTPM = [ [ r['ordinalTpm'].value] for r in result ]
        # flatten the list of lists into a list
        StudyTPM = flatten(StudyTPM)
        # Render into a dataframe
        df_StudyTPM = pd.DataFrame (StudyTPM, columns = ['StudyTPM'])
        # get the counts of the orders
        df_StudyTPM_count = df_StudyTPM['StudyTPM'].value_counts().rename_axis('ordinalTpm').reset_index(name='counts')

        from pandas.api.types import CategoricalDtype
        # create a custom category type
        cat_order = CategoricalDtype(['low', 'medium', 'high'], ordered=True)
        # cast the ordinalTpm column to the custom category type
        df_StudyTPM_count['ordinalTpm'] = df_StudyTPM_count['ordinalTpm'].astype(cat_order)
        # sort values according to ordinalTpm
        df_StudyTPM_count = df_StudyTPM_count.sort_values('ordinalTpm')

        # plot the ordinalTpm in a bar graph using matplotlib
        plt.bar(range(len(df_StudyTPM_count)), list(df_StudyTPM_count['counts']), align='center', edgecolor='black')
        plt.xticks(range(len(df_StudyTPM_count)), list(df_StudyTPM_count['ordinalTpm']))
        plt.grid(axis='y', linestyle='--')
        plt.xlabel('\nordinal TPM', fontweight='bold')
        plt.ylabel('counts', fontweight='bold')
        plt.title('Ordinal TPM Bar Graph', fontweight='bold')
        for i, v in enumerate(df_StudyTPM_count['counts']):
            plt.text(i-0.10, v, str(v), color='red') #fontweight='bold'
        plt.show()