# Enrichment Analysis Notebooks 
Enrichment Analysis Use Cases. Tools to analyse plant biology knowledge graphs and find enriched traits or bioprocesses in differential gene expression data. The project uses data from Knetminer, ENSEMBL, EBI Gene Expression Atlas and others, exported as Knowledge graphs using Agrischemas/Bioschemas annotations.

# Database Files Notebook
This notebook is intended mainly for KnetMiner developers. The files generated are already provided in the interactive_jupyter_notebook folder on Github.

### Notebook Interface
There are two cellsin the notebook.

1. Run the first cell to choose the species and concepts.
![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/GeneConcept1.PNG?raw=true)

2. Run the second cell to get the download link for the database csv files.
![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/GeneConcept2.PNG?raw=true)

# Enrichment Analysis Notebook
This is the main notebook to perform the enrichment analysis.

# Running the notebooks using Binder
For running the jupyter notebook for Enrichment Analysis using KnetMiner SPARQL endpoint,<br>click on launch binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Rothamsted/knetgraphs-gene-traits/HEAD?labpath=interactive_jupyter_notebook%2FKnetMiner_SPARQL_EA.ipynb)

For running the jupyter notebook for gene-concept relations from the database,<br>click on launch binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Rothamsted/knetgraphs-gene-traits/HEAD?labpath=interactive_jupyter_notebook%2FGeneConcept_database_relations.ipynb)

View the [User Manuals](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/User%20Manuals.pdf) for instructions on how to load the NeoDash dashboard and how to run the Jupyter Notebooks on local computer.

# Running the notebooks on local computer

### Download the notebooks
Download the interactive notebooks and the required files from [here](https://github.com/Rothamsted/knetgraphs-gene-traits/raw/main/interactive_jupyter_notebook.zip). 


### Requirements:
- pandas v1.3.3 
- numpy v1.21.2
- matplotlib v3.4.3
- scipy v1.7.3
- ipympl v0.9.2
- sparqlwrapper v1.8.5
- ipywidgets v7.6.5
