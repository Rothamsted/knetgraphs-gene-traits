"""
This script contains the common queries used for the enrichmnet_analysis_functions.py
"""

query_count_genes = """
PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (count(*) as ?Count)
{
    ?gene a bk:Gene;
    bka:TAXID '%s'.
} """


query_study_list = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
    PREFIX bkr: <http://knetminer.org/data/rdf/resources/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
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

        ?study a bioschema:Study;
            schema:additionalProperty bkr:gxa_analysis_type_differential;
            dc:title ?studyTitle;
            schema:identifier ?studyAcc.
    } """


query_CountStudyGenes = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
    PREFIX bkr: <http://knetminer.org/data/rdf/resources/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX agri: <http://agrischemas.org/>
    PREFIX bioschema: <http://bioschemas.org/>
    PREFIX schema: <http://schema.org/>

    SELECT (count(*) as ?Count)
    WHERE {
        ?gene a bk:Gene;
            dcterms:identifier ?geneAcc.

        ?gene bioschema:expressedIn ?condition.

        ?expStatement a rdfs:Statement;
            rdf:subject ?gene;
            rdf:predicate bioschema:expressedIn;
            rdf:object ?condition;
            agri:evidence ?study.

        ?study a bioschema:Study;
            dc:title ?studyTitle;
            schema:identifier '%s'.
    } """


query_DEXgenes_in_study = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
    PREFIX bkr: <http://knetminer.org/data/rdf/resources/>
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

        ?study a bioschema:Study;
            dc:title ?studyTitle;
            schema:identifier '%s'.
    } """


query_StudyPvalues = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
    PREFIX bkr: <http://knetminer.org/data/rdf/resources/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX agri: <http://agrischemas.org/>
    PREFIX bioschema: <http://bioschemas.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?pvalue
    WHERE {
        ?gene a bk:Gene;
            dcterms:identifier ?geneAcc.

        ?gene bioschema:expressedIn ?condition.

        ?expStatement a rdfs:Statement;
            rdf:subject ?gene;
            rdf:predicate bioschema:expressedIn;
            rdf:object ?condition;
            agri:evidence ?study.
        
        ?expStatement agri:pvalue ?pvalue.

        ?study a bioschema:Study;
            schema:additionalProperty bkr:gxa_analysis_type_differential;
            dc:title ?studyTitle;
            schema:identifier '%s'.
    } """


query_FilterByPvalues = """
    PREFIX bk: <http://knetminer.org/data/rdf/terms/biokno/>
    PREFIX bka: <http://knetminer.org/data/rdf/terms/biokno/attributes/>
    PREFIX bkr: <http://knetminer.org/data/rdf/resources/>
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
        
        ?expStatement agri:pvalue ?pvalue.
        FILTER ( ?pvalue <= %s)

        ?study a bioschema:Study;
            schema:additionalProperty bkr:gxa_analysis_type_differential;
            dc:title ?studyTitle;
            schema:identifier '%s'.
    } """