# Import SPARQLWrapper library to use the SPARQL endpoint, pandas, scipy, np
from SPARQLWrapper import SPARQLWrapper2

import pandas as pd

import scipy.stats as stats

import numpy as np


# create variable for SPARQL endpoint
sparql = SPARQLWrapper2 ( "http://knetminer-data.cyverseuk.org/lodestar/sparql" )


# create a function to flatten a list of lists into a single list
def flatten(xss):
    return [x for xs in xss for x in xs]


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
    total_genes = int(result[0][0])
    
    print("Total Number of Genes = " + str(total_genes))
    return total_genes


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

    # save dataframe to CSV
    dframe_GeneTrait.to_csv(f'GeneTraitTable_{taxID}.csv')

    print(f"File 'GeneTraitTable_{taxID}.csv' is saved.")


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

    print(" Number of genes in study is: " + str(len(total_DEXgenes)))
    return total_DEXgenes
