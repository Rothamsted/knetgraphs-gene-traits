# NeoDash User Manual

## Loading the Dashboard in Web Browser

1.	Download the [dashboard.json](https://raw.githubusercontent.com/Rothamsted/knetgraphs-gene-traits/e6f111a33fad7a3967a2bb777342ef68c274f11b/NeoDash_dashboard/dashboard.json) file using right mouse click -> Save as… -> save the file.

2.	Open [NeoDash](http://neodash.graphapp.io/) in a web browser.

3.	Click on "NEW DASHBOARD".

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture1.png?raw=true)
                                   
4.	Fill the following details as follows:
    - Protocol: Choose "bolt" from the drop-down menu
    - Hostname: knetminer-neo4j.cyverseuk.org
    - Port: 7687 <br>
    And click "CONNECT"

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture2.png?raw=true)
                        
5.	Click the three dashes on the top left side ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture3.png?raw=true) and click on "Load" from the menu.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture4.png?raw=true)
                                            
6.	Click "SELECT FROM FILE", choose the "dashboard.json" file and click "open".

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture5.png?raw=true)

7.	Then click on "LOAD DASHBOARD" to load the "KnetMiner Dashboard".

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture6.png?raw=true)

8.	To view the cypher query for each report, click on the three dots ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture7.png?raw=true) at the top right of each report box.
<br>


## Loading the Dashboard in Neo4j Desktop

1.	Download [Neo4j](https://neo4j.com/download/).

2.	Fill the form with your name and email and choose a country. *(If you don’t have a company name, you can just add dot ".")* <br>
    Then click "Download Desktop".

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture8.png?raw=true)
 
3.	This will open a new page with the activation key. click "Copy to clipboard".

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture9.png?raw=true)
 
4.	After installing Neo4j desktop, paste the activation key into "Software Key" and click "Activate".

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture10.png?raw=true)

5.	Install NeoDash from the following [link](neo4j-desktop://graphapps/install?url=https://registry.npmjs.org/neodash).<br>
    *(Note: other Neo4j tools are available in the [gallery](https://install.graphapp.io/).)*

6.	This will show a pop-up, click on "Open Neo4j Desktop".

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture11.png?raw=true)

7.	Neo4j will open and ask for confirmation.

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture12.png?raw=true)
 
8.	Click on "Graphs App" button on the left. Then, hover over "NeoDash" and click "Open".

    ![image](https://github.com/Rothamsted/knetgraphs-gene-traits/blob/main/images_for_HTML/Picture13.png?raw=true)
                                                  
9.	This will open a new window for NeoDash. Follow the same steps as [previous section](#loading-the-dashboard-in-web-browser) to load the dashboard.
