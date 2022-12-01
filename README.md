# Enrichment Analysis Notebooks

Enrichment Analysis Use Cases. Tools to analyse plant biology knowledge graphs and find enriched traits or bioprocesses in differential gene expression data. The project uses data from Knetminer, ENSEMBL, EBI Gene Expression Atlas and others, exported as Knowledge graphs using Agrischemas/Bioschemas annotations.
<br>
<br>

# Database Files Notebook

This notebook is intended mainly for KnetMiner developers. The files generated are already provided in the **interactive_jupyter_notebook folder** on Github.

### There are two cells in the notebook:

1. Run the first cell to choose the species and concepts.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/GeneConcept1.PNG?raw=true)

2. Run the second cell to get the download link for the database csv files.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/GeneConcept2.PNG?raw=true)
    <br>
    <br>

# Enrichment Analysis Notebook

This is the main notebook to perform the enrichment analysis.

### The first two cells are mainly for the analysis:

1. Run the first cell to choose the species, concept and study/list.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/EnrichmentAnalysis1.PNG?raw=true)

2. Run the second cell to perform the analysis:

    - If you chose "study", you will get a list of studies to choose from for the species.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/EnrichmentAnalysis2.PNG?raw=true)

    - Then you will be asked whteher you want to use all genes in the study or filter the genes according to p-value.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/EnrichmentAnalysis3.PNG?raw=true)

    - If you chose to filter, you will get an interactive line graph represtation for the p-values and the corresponding number of genes.<br>
    You can also filter using the slider.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/EnrichmentAnalysis4.PNG?raw=true)

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/EnrichmentAnalysis5.PNG?raw=true)

    - Whether you chose list or study, the final result is two tables, which can be downloaded as csv files:<br>
        - The first table shows the chosen genes and related ontology, with the evidence and the link to the network knowledge graphs on KnetMiner.<br>
        - The second table shows the p-values for the ontology terms.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/EnrichmentAnalysis6.PNG?raw=true)
    <br>
    <br>

### Other cells:

1. Run the cells in the "View whole tables section" if you want to print the complete tables in the notebooks.

2. To filter the first table (gene-concept), run the cells in the sections:
    - choosing the ontology term to display the related genes
    - or choosing a gene to display the related ontology terms
    <br>

# Running the notebooks using Binder

**Please Note:** The binders take sometime to be built and might fail a couple of times before launching successfully.

For running the jupyter notebook for Enrichment Analysis using KnetMiner SPARQL endpoint,<br>click on launch binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Rothamsted/knetgraphs-gene-traits/HEAD?labpath=interactive_jupyter_notebook%2FKnetMiner_SPARQL_EA.ipynb)

For running the jupyter notebook for gene-concept relations from the database,<br>click on launch binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Rothamsted/knetgraphs-gene-traits/HEAD?labpath=interactive_jupyter_notebook%2FGeneConcept_database_relations.ipynb)
<br>

# Running the notebooks on local computer

### Download the notebooks

[Download the zipped folder](https://github.com/Rothamsted/knetgraphs-gene-traits/raw/main/interactive_jupyter_notebook.zip) for the interactive notebooks and the required files and unzip it. 
<br>

### Install conda and dependncies

1. [Install Miniconda](https://docs.conda.io/en/latest/miniconda.html)

2. Open the miniconda prompt and write the following commands:<br>
    (note: change "path/to/interactive_jupyter_notebook" to actual path)

    ```
    conda create -n my-conda-env python=3.9.12      # creates new virtual env
    conda activate my-conda-env                     # activate environment in terminal
    cd "path/to/interactive_jupyter_notebook"       # change directory to interactive_jupyter_notebook folder
    pip install -r requirements.txt                 # install requirements
    jupyter notebook                                # start server + kernel inside my-conda-env
    ```


# Requirements
- python v3.9.12
- pandas v1.3.3 
- numpy v1.21.2
- matplotlib v3.4.3
- scipy v1.7.3
- ipympl v0.9.2
- sparqlwrapper v1.8.5
- ipywidgets v7.6.5
