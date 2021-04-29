# SFP-DataBewerking

## Introduction

PlantScan3D is software with a GUI, as TI students we hate this kind of software. In order to make the software TI
approved we are going te remove the GUI to make the software easier to work with. Make sure to read the full read-me the
pay-off is huge.

## Requirements

In order for this software to be used a lot of pain needs to be sit trough. We spent a couple of days stripping the GUI
from PlantScan3D. A new approach made it possible for our own code to work. The following requirements are needed:

1. Pycharm(students can get professional for free)[https://www.jetbrains.com/pycharm/]
2. Anaconda[https://www.anaconda.com/products/individual#Downloads]
3. A lot of patience.

The openalea requirements are installed at a later time.

1. openalea[https://github.com/openalea]
2. openalea.mtg[https://github.com/openalea/mtg]
3. openalea.plantgl[https://github.com/openalea/plantgl]
4. openalea.plantscan3d[https://github.com/openalea/plantscan3d]

Pip packages.
1. `pip install pyvis`
2. `pip install termcolor`

## Installation
### Hard installation
1. Download and install pycharm and anaconda
2. Open a new project
3. Select Conda as the new interpreter
4. Select python version 3.7(higher might work, we didn't try tho)
5. Create the project
6. go to: File>
    settings>
   project:{name}>
   Python interpreter>
   +>
   manage repositories>
   +>
   https://conda.anaconda.org/fredboudon
   OK>
   manage repositories>
   +>
   conda-forge>
   OK>
7. Click on the following packages and install(would recommend installing 1 package,
   then wait for it to install, repeat this until every package is installed):
    1. openalea.plantscan3d
    2. openalea.mtg
    3. openalea.plantgl
8. click apply then click OK.
9. After everything is installed a git-clone can be done inside the project in order to clone the most recent software.
10. Any questions or help needed with the installing process please contact me: Luca van Elsas(email: 582178@student.inholland.nl)

### Easy installation
1. Download and install pycharm and anaconda.
2. Open a new project.
3. Select Conda as the new interpreter.
4. Select python version 3.7(higher might work, we didn't try tho).
5. Create the project.
6. Download the following environment from sharepoint(link: https://inholland.sharepoint.com/:u:/r/teams/MinorTIenLR20202021/Gedeelde%20documenten/2021-2021/projectgroepen%20minor%20software%20engineering/groep%202%20data%20bewerking/week%2017%20tm%2020/Conda/PearTreeDataProcessing.zip?csf=1&web=1&e=rwOoNa).
7. Go to the folder where the conda interpreter is located.
8. copy the files from the download into the environment folder.
9. Clone the git and you should be all set.

## Cat picture

After a hard day a programmer needs to find something that helps them to relax. The only possible solution is this
picture. A well fed cat trying to run a marathon. Enjoy! C:

![alt text](https://www.consumentenbond.nl/binaries/content/gallery/cbhippowebsite/tests/themapaginas/voeding-gezondheid/afbeeldingen-oud/dikke-kat.jpg/dikke-kat.jpg/cbhippowebsite%3Aplscs)
