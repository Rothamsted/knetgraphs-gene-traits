"""
This script reads the cypher-queries.txt to extract
the cypher pathways for the selected ontology.
"""

# import the os library
import os

def get_cypher_queries(input_file, ontology):
    """This function gets they cypher queries for the selected ontology"""
    
    # Create an empty list to add the query lines to it
    queries_list=[]
    
    # open the input file for reading
    with open(input_file, "r") as fr:        
        
        # read each line in the input file
        for line in fr:
            if ontology in line:
                # Add this line to the queries list
                queries_list.append(line)
    
    # Join the lines in the list and print them to screen
    queries = "".join(queries_list)
    print(queries)



### Example:

input_file = "./cypher_queries.txt"
ontology = "BioProc"
get_cypher_queries(input_file, ontology)


qu_string = """
MATCH path = (gene_1:Gene) - [participates_in_9_4_d:participates_in] -> (bioProc_4:BioProc) WHERE gene_1.iri IN $startGeneIris RETURN path
MATCH path = (gene_1:Gene) - [part_of_1_23_d:part_of] -> (coExpCluster_23:CoExpCluster) - [rel:enriched_for] -> (bioProc_4:BioProc) WHERE toFloat(rel.p_adjust)<1E-10 AND gene_1.iri IN $startGeneIris RETURN path
MATCH path = (gene_1:Gene) - [de_9_22_d:differentially_expressed] -> (dGES_22:DGES) - [enriched_for_23_4_d:enriched_for] -> (bioProc_4:BioProc) WHERE gene_1.iri IN $startGeneIris RETURN path
MATCH path = (gene_1:Gene) - [rel_1_9:homoeolog|regulates|genetic|physical] - (gene_9:Gene) - [participates_in_9_4_d:participates_in] -> (bioProc_4:BioProc) WHERE gene_1.iri IN $startGeneIris RETURN path
MATCH path = (gene_1:Gene) - [enc_1_10_d:enc] -> (protein_10:Protein) - [rel_10_10:h_s_s|ortho|xref*0..1] - (protein_10b:Protein) - [participates_in_10_4_d:participates_in] -> (bioProc_4:BioProc) WHERE gene_1.iri IN $startGeneIris RETURN path
MATCH path = (gene_1:Gene) - [enc_1_10_d:enc] -> (protein_10:Protein) - [rel_10_10:h_s_s|ortho|xref*0..1] - (protein_10b:Protein) - [has_domain_10_11_d:has_domain] -> (protDomain_11:ProtDomain) - [participates_in_11_4_d:participates_in] -> (bioProc_4:BioProc) WHERE gene_1.iri IN $startGeneIris RETURN path
MATCH path = (gene_1:Gene) - [enc_1_10_d:enc] -> (protein_10:Protein) - [rel_10_10:ortho] - (protein_10b:Protein) <- [enc_10_9_d:enc] - (gene_9:Gene) - [participates_in_9_4_d:participates_in] -> (bioProc_4:BioProc) WHERE gene_1.iri IN $startGeneIris RETURN path
MATCH path = (gene_1:Gene) - [enc_1_10_d:enc] -> (protein_10:Protein) - [rel_10_10:ortho] - (protein_10b:Protein) <- [enc_10_9_d:enc] - (gene_9:Gene) - [rel_9_9_2:genetic|physical] - (gene_9b:Gene) - [participates_in_9_4_d:participates_in] -> (bioProc_4:BioProc) WHERE gene_1.iri IN $startGeneIris RETURN path
"""

rep = ["WHERE gene_1.iri ", "WHERE toFloat(rel.p_adjust)<1E-10 AND gene_1.iri ", "IN $startGeneIris ",
"gene_1", "gene_9b", "gene_9", "bioProc_4", "coExpCluster_23", "protDomain_11", "de_9_22_d", "dGES_22",
"enriched_for_23_4_d", "has_domain_10_11_d", "part_of_1_23_d",
"enc_1_10_d", "enc_10_9_d", "participates_in_9_4_d", "participates_in_11_4_d", "participates_in_10_4_d",
"rel_1_9", "rel_9_9_2", "rel_10_10", "rel", "protein_10b", "protein_10"]


for w in rep:
    qu_string = qu_string.replace(w, "")
print(qu_string)


"""
MATCH path = (:Gene) - [:participates_in] -> (:BioProc) RETURN path
MATCH path = (:Gene) - [:part_of] -> (:CoExpCluster) - [:enriched_for] -> (:BioProc) RETURN path
MATCH path = (:Gene) - [:differentially_expressed] -> (:DGES) - [:enriched_for] -> (:BioProc) RETURN path
MATCH path = (:Gene) - [:homoeolog|regulates|genetic|physical] - (:Gene) - [:participates_in] -> (:BioProc) RETURN path
MATCH path = (:Gene) - [:enc] -> (:Protein) - [:h_s_s|ortho|xref*0..1] - (:Protein) - [:participates_in] -> (:BioProc) RETURN path
MATCH path = (:Gene) - [:enc] -> (:Protein) - [:h_s_s|ortho|xref*0..1] - (:Protein) - [:has_domain] -> (:ProtDomain) - [:participates_in] -> (:BioProc) RETURN path  
MATCH path = (:Gene) - [:enc] -> (:Protein) - [:ortho] - (:Protein) <- [:enc] - (:Gene) - [:participates_in] -> (:BioProc) RETURN path
MATCH path = (:Gene) - [:enc] -> (:Protein) - [:ortho] - (:Protein) <- [:enc] - (:Gene) - [:genetic|physical] - (:Gene) - [:participates_in] -> (:BioProc) RETURN path
"""