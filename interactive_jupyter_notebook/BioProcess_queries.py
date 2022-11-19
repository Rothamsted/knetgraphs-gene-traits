"""
This script contains the pathway queries for gene--bioProc
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
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT *
FROM bkg:poaceae
WHERE {
    ?gene1 a bk:Gene;
        bka:TAXID '%s';
        bk:prefName ?geneName;
        dcterms:identifier ?geneAcc.

"""

pathways = [
    """?gene1 bk:participates_in ?bioProc. BIND ("GO_0-0" AS ?evidence)""",
    
    # """?gene1 bk:part_of ?coExpCluster.
    # ?coExpCluster a bk:CoExpCluster.
    # ?coExpCluster bk:enriched_for ?bioProc.
    # BIND ("CoExpCluster_0-0" AS ?evidence)""",

    """?gene1 bk:differentially_expressed ?dGES.
    ?dGES a bk:DGES.
    ?dGES bk:enriched_for ?bioProc.
    BIND ("DGES_0-0" AS ?evidence)""",

    """{ ?gene1 bk:homoeolog|^bk:homoeolog ?gene2. BIND ("GO_1-0" AS ?evidence) }
    UNION { ?gene1 (bk:regulates|bk:genetic|bk:physical|^bk:regulates|^bk:genetic|^bk:physical) ?gene2.
    BIND ("GO_0-1" AS ?evidence) }
    ?gene2 bk:participates_in ?bioProc.""",

    """?gene1 bk:enc ?protein1.
    ?protein1 (bk:h_s_s|bk:ortho|bk:xref|^bk:h_s_s|^bk:ortho|^bk:xref) ?protein2.
    ?protein2 bk:participates_in ?bioProc.
    BIND ("GO_1-0" AS ?evidence) """,

    """?gene1 bk:enc ?protein1.
    ?protein1 (bk:h_s_s|bk:ortho|bk:xref|^bk:h_s_s|^bk:ortho|^bk:xref) ?protein2.
    ?protein2 bk:has_domain ?protDomain.
    ?protDomain bk:participates_in ?bioProc.
    BIND ("GO_1-0" AS ?evidence) """,

    """?gene1 bk:enc ?protein1.
    ?protein1 bk:ortho|^bk:ortho ?protein2.
    ?protein2 ^bk:enc ?gene2.
        { ?gene2 bk:participates_in ?bioProc. BIND ("GO_1-0" AS ?evidence) }
    UNION { ?gene2 (bk:genetic|bk:physical|^bk:genetic|^bk:physical) ?gene3.
        ?gene3 bk:participates_in ?bioProc. BIND ("GO_1-1" AS ?evidence) }"""]

query_subset2 = """

    ?bioProc a bk:BioProc;
        bk:prefName ?preferredName;
        dcterms:identifier ?ontologyTerm.
} """

