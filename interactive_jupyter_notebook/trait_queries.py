"""
This script contains the pathway queries for gene--trait
to be used in the enrichmnet_analysis_functions.py
"""

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

"""

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


query_subset2 = """

    ?trait a bk:Trait;
        bk:prefName ?preferredName;
        dcterms:identifier ?ontologyTerm.
} """

