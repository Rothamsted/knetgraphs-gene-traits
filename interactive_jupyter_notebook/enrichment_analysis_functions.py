# Import SPARQLWrapper library to use the SPARQL endpoint, pandas, scipy, np, and HTML
from SPARQLWrapper import SPARQLWrapper2

import pandas as pd

import scipy.stats as stats

import numpy as np

import base64
from IPython.display import HTML

# create variable for SPARQL endpoint
sparql = SPARQLWrapper2 ( "http://knetminer-data.cyverseuk.org/lodestar/sparql" )


# create a function to flatten a list of lists into a single list
def flatten(xss):
    return [x for xs in xss for x in xs]


# A function to create download link to save datafarames as csv files
# refrence: https://www.codegrepper.com/code-examples/python/download+csv+file+from+jupyter+notebook

def create_download_link(df, filename, title):
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload,title=title,filename=filename)
    return HTML(html)


# A function to create dataframe for Tax IDs and their names
def df_taxID():
    dframe_taxID = pd.DataFrame({'Tax IDs': ['4565', '3702', '4530'],
                                'Tax Names': ['Triticum aestivum (wheat)', 'Arabidopsis thaliana (thale cress)',
                                           'Oryza sativa (rice)'],
                                'Database URL': ['https://knetminer.com/ws/wheatknet/', 'https://knetminer.com/ws/araknet/',
                                    'https://knetminer.com/ws/riceknet/']})
    return dframe_taxID


# create dataframe for evidence meaning
def df_evidence():
    dframe_evidence = pd.DataFrame({'Evidence Code': ['TM_0-0', 'TM_0-1', 'TM_1-0', 'TM_1-1',
                                                  'GWAS_0-0', 'GWAS_0-1', 'GWAS_1-0', 'GWAS_1-1'],
                               'Evidence Type': ['Text Mining (TM)', 'Text Mining', 'Text Mining', 'Text Mining',
                                                'Genetic Study (GWAS)', 'Genetic Study', 'Genetic Study', 'Genetic Study'],
                               'Homology': [0, 0, 1, 1, 0, 0, 1, 1],
                               'Interaction': [0, 1, 0, 1, 0, 1, 0, 1]})

    return dframe_evidence


# Create a function to get the count of genes in the database for a species tax ID.
def get_gene_count(taxID):
    query_count = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT (count(*) as ?Count)
    {
      ?gene a bk:Gene;
        bka:TAXID '%s'.
    } """%(taxID)

    # run the query
    sparql.setQuery ( query_count )
    result = sparql.query().bindings
    result = [ [ r['Count'].value] for r in result ]
    total_db_genes = int(result[0][0])
    
    print("Total Number of Genes = " + str(total_db_genes))
    return total_db_genes


# Create a function to get the list of studies for each species
def get_study_list(taxID):
    query_study_list = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX agri: <http://agrischemas.org/>
    PREFIX bioschema: <http://bioschemas.org/>
    PREFIX schema: <http://schema.org/>

    SELECT DISTINCT ?studyAcc ?studyTitle
    WHERE {
        ?gene a bk:Gene;
            bka:TAXID '%s'.

        ?gene bioschema:expressedIn ?condition.

        ?expStatement a rdfs:Statement;
            rdf:subject ?gene;
            rdf:predicate bioschema:expressedIn;
            rdf:object ?condition;
            agri:evidence ?study.

        ?study
            dc:title ?studyTitle;
            schema:identifier ?studyAcc.
    } """%(taxID)

    # run the query
    sparql.setQuery ( query_study_list )
    result = sparql.query().bindings
    final_result_study = [ [ r['studyAcc'].value, r['studyTitle'].value] for r in result ]

    # Render into a table
    dframe_study_list = pd.DataFrame ( final_result_study, columns = ["Study Accession", "Study Title"] )

    return dframe_study_list


# Function to get all the traits related to the genes
def get_database_csv(taxID, database):
    
    # Create the query
    query_subset1 = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
    PREFIX bkg: <http://knetminer.org/data/rdf/resources/graphs/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT *
    FROM bkg:poaceae
    WHERE {
      ?gene1 a bk:Gene;
          bka:TAXID '%s';
          bk:prefName ?geneName;
          dcterms:identifier ?geneAcc.

        """%(taxID)

    query_subset2 = """

      ?trait a bk:Trait;
          bk:prefName ?traitName;
          dcterms:identifier ?traitAcc.
    } """

    pathways = [
        """?gene1 bk:cooc_wi|^bk:cooc_wi ?trait. BIND ("TM_0-0" AS ?evidence)""",

        """?gene1 bk:has_variation ?snp.
        ?snp bk:associated_with ?phenotype.
        ?phenotype a bk:Phenotype.
        ?phenotype bk:part_of ?trait.
        BIND ("GWAS_0-0" AS ?evidence)""",

        """{ ?gene1 bk:homoeolog|^bk:homoeolog ?gene2. BIND ("TM_1-0" AS ?evidence) }
        UNION { ?gene1 (bk:regulates|bk:genetic|bk:physical|^bk:regulates|^bk:genetic|^bk:physical) ?gene2.
        BIND ("TM_0-1" AS ?evidence) }
        ?gene2 bk:cooc_wi|^bk:cooc_wi ?trait.""",

        """{ ?gene1 bk:homoeolog|^bk:homoeolog ?gene2. BIND ("GWAS_1-0" AS ?evidence) }
        UNION { ?gene1 (bk:regulates|bk:genetic|bk:physical|^bk:regulates|^bk:genetic|^bk:physical) ?gene2.
        BIND ("GWAS_0-1" AS ?evidence) }
        ?gene2 bk:has_variation ?snp.
        ?snp bk:associated_with ?phenotype.
        ?phenotype a bk:Phenotype.
        ?phenotype bk:part_of ?trait.""",

        """?gene1 bk:enc ?protein1.
        ?protein1 (bk:h_s_s|bk:xref|^bk:h_s_s|^bk:xref) ?protein2.
        ?protein2 bk:cooc_wi|^bk:cooc_wi ?trait.
        BIND ("TM_1-0" AS ?evidence) """,

        """?gene1 bk:enc ?protein1.
        ?protein1 bk:ortho|^bk:ortho ?protein2.
        ?protein2 ^bk:enc ?gene2.
              { ?gene2 bk:cooc_wi|^bk:cooc_wi ?trait. BIND ("TM_1-0" AS ?evidence) }
        UNION { ?gene2 (bk:genetic|bk:physical|^bk:genetic|^bk:physical) ?gene3.
                ?gene3 bk:cooc_wi|^bk:cooc_wi ?trait. BIND ("TM_1-1" AS ?evidence) }""",

        """?gene1 bk:enc ?protein1.
        ?protein1 bk:ortho|^bk:ortho ?protein2.
        ?protein2 ^bk:enc ?gene2.
              { ?gene2 bk:has_variation ?snp.  BIND ("GWAS_1-0" AS ?evidence) }
        UNION { ?gene2 (bk:genetic|bk:physical|^bk:genetic|^bk:physical) ?gene3.
                ?gene3 bk:has_variation ?snp. BIND ("GWAS_1-1" AS ?evidence) }
        ?snp bk:associated_with ?phenotype.
        ?phenotype a bk:Phenotype.
        ?phenotype bk:part_of|^bk:part_of ?trait."""]
    
    
    # create an empty list to append the results of each loop
    final_result = []

    # loop over the pathways
    for pathway in pathways:
        query = query_subset1 + pathway + query_subset2
        # run the query
        sparql = SPARQLWrapper2 ( "http://knetminer-data.cyverseuk.org/lodestar/sparql" )
        sparql.setQuery ( query )
        result = sparql.query().bindings
        result = [ [ r['geneAcc'].value, r['geneName'].value, r['traitAcc'].value, r['traitName'].value,
                    r['evidence'].value] for r in result ]
        final_result += result


    # Render into a dataframe
    dframe_GeneTrait = pd.DataFrame ( final_result, columns = ["Gene Accession", "Gene Name",
                                                               "Trait Accession", "Trait Name", "Evidence"] )

    # remove repeated rows
    dframe_GeneTrait = dframe_GeneTrait.drop_duplicates()
    
    
    # add the urls for the knowledge graph pathway (gene--trait)
    urls = []
    for x, row in dframe_GeneTrait.iterrows():
        # get Gene Accession
        geneAcc = row['Gene Accession']

        # Get Trait Accession
        traitAcc = row['Trait Accession']
        first_trait = traitAcc.split(";")[0] # split if there are two trait accessions, and take the first accession
        trait_split = first_trait.split("_") # split the "TO" and the accession number

        # condition in case there is only accession number without "TO"
        to = ''
        acc = ''
        if len(trait_split) == 2:
            to = trait_split[0]+":"
            acc = trait_split[1]
        else:
            acc = trait_split[0]

        to_acc = to + acc

        url = f'{database}genepage?list={geneAcc}&keyword=%22{to_acc}%22'

        urls.append(url)
        
    # add urls to dataframe
    dframe_GeneTrait['Network URL'] = urls

    # get CSV download link for the dataframe
    csv_link = create_download_link(dframe_GeneTrait, f'GeneTraitTable_{taxID}.csv', f'Download GeneTraitTable_{taxID}.csv file')
    display(csv_link)
    
    return csv_link


# Get the differentially expressed genes in the study
def get_study_DEXgenes(studyAcc):
    query_study = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX agri: <http://agrischemas.org/>
    PREFIX bioschema: <http://bioschemas.org/>
    PREFIX schema: <http://schema.org/>

    SELECT *
    WHERE {
        ?gene a bk:Gene;
            dcterms:identifier ?geneAcc.

        ?gene bioschema:expressedIn ?condition.

        ?expStatement a rdfs:Statement;
            rdf:subject ?gene;
            rdf:predicate bioschema:expressedIn;
            rdf:object ?condition;
            agri:evidence ?study.

        ?study
            dc:title ?studyTitle;
            schema:identifier '%s'.
    } """%(studyAcc)

    # run the query
    sparql.setQuery ( query_study )
    result = sparql.query().bindings
    final_result_study = [ [ r['geneAcc'].value] for r in result ]
    final_result_study = flatten(final_result_study)
    total_DEXgenes = set(final_result_study)

    print("Number of genes in study is: " + str(len(total_DEXgenes)))
    return total_DEXgenes


# Use the study/user list of genes to extract their rows from the dframe_GeneTrait
def get_df_GeneTrait_filtered(dframe_GeneTrait, total_DEXgenes):
    # Extract the rows containg the genes list from the first dataframe (dframe_GeneTrait)
    dframe_GeneTrait_filtered = dframe_GeneTrait[dframe_GeneTrait['Gene Accession'].isin(total_DEXgenes)]

    # Sort dframe_GeneTrait_filtered 
    dframe_GeneTrait_filtered = dframe_GeneTrait_filtered.sort_values(['Trait Accession', 'Gene Name', 'Evidence'],
                                                                    ascending = [True, True, True])

    # update the dataframe index
    dframe_GeneTrait_filtered = dframe_GeneTrait_filtered.reset_index(drop=True)

    return dframe_GeneTrait_filtered


# Create a function to calculate adjusted p-values (or Q-values) using numpy
# refrence: https://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python

# p is p-values , q is adjusted p-values
def p_adjust_bh(p):
    """Benjamini-Hochberg p-value correction for multiple hypothesis testing."""
    p = np.asfarray(p) # Return an array converted to a float type
    by_descend = p.argsort()[::-1]
    steps = float(len(p)) / np.arange(len(p), 0, -1)
    q = np.minimum(1, np.minimum.accumulate(steps * p[by_descend]))
    return by_descend, q


# Perform Enrichment Analysis using SciPy and calculate adjusted p-value
def get_df_Ftest_sorted(dframe_GeneTrait, total_DEXgenes, total_db_genes):

    # get dframe_GeneTrait_filtered
    dframe_GeneTrait_filtered = get_df_GeneTrait_filtered(dframe_GeneTrait, total_DEXgenes)

    # create dataframe to add the odd ratio and p-value
    df_Ftest = pd.DataFrame (columns = ["Trait Accession", "Trait Name", "odds ratio", "exact p-value",
                                    "Total number of related genes in database",
                                        "Number of related genes in user/study list"])

    # create list to add the Trait Accessions numbers
    traits =  []

    ### for each trait, calculate odds ratio, exact p-value and number of related genes in database and list ###

    for x, row in dframe_GeneTrait_filtered.iterrows():
        trait_acc = row['Trait Accession']
        
        if trait_acc not in traits:
            
            traits.append(trait_acc)
            trait_name = row['Trait Name']
            
            # 1a. Get the complete set of genes linked to the trait in the gene list
            select_trait = dframe_GeneTrait_filtered.loc[dframe_GeneTrait_filtered['Trait Accession'] == trait_acc]
            
            # 1b. Get the distinct list of genes linked to the trait in the gene list
            trait_DEXgenes = set(select_trait['Gene Accession'].unique())
            
            
            # 2a. Get the complete set of genes linked to the trait in the database (dframe_GeneTrait)
            select_Totaltrait = dframe_GeneTrait.loc[dframe_GeneTrait['Trait Accession'] == trait_acc]
            
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
            df = {'Trait Accession': trait_acc, 'Trait Name': trait_name, 'odds ratio': oddsratio, 'exact p-value': pvalue,
                'Total number of related genes in database': len(total_TraitGenes),
                'Number of related genes in user/study list': a}
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
    print("\nThe gene-trait table below has " + str(dframe_GeneTrait_filtered.shape[0]) + " rows.\nTo view the whole table click on the download link below:")
    display(create_download_link(dframe_GeneTrait_filtered, "GeneTrait_filtered_table.csv", "Download gene-trait table CSV file"))

    # copy the head of the dataframe to avoid editing and changing data type of the original
    df_GeneTrait_filtered = dframe_GeneTrait_filtered[:].copy()
    df_GeneTrait_filtered = df_GeneTrait_filtered.head(10)
    # display gene-trait table by rendering the HTML to clickable
    s = "View Network"
    df_GeneTrait_filtered['Network URL'] = df_GeneTrait_filtered['Network URL'].apply(lambda x: f'<a href="{x}">{s}</a>')
    display(HTML(df_GeneTrait_filtered.to_html(render_links=True, escape=False)))

    # Trait enrichment table:
    print("\nThe trait enrichment table below has " + str(df_Ftest_sorted.shape[0]) + " rows.\nTo view the whole table click on the download link below:")
    display(create_download_link(df_Ftest_sorted, "trait_enrichment_table.csv", "Download trait enrichment table CSV file"))
    display(df_Ftest_sorted.head(10))

    return dframe_GeneTrait_filtered, df_Ftest_sorted
    
