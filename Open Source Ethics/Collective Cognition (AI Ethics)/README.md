# A Collective Cognition Model for AI Ethics

## Terms, Definitions, and Acronyms

*OSDC: Open Source Development Community*\
The acronym *OSDC* is very useful for describing this model (as you might imagine) and relates to projects described as FOSS, or just Open Source, and the Communities surrounding those projects (as describted by CHAOSS).

## Co-Lab Notebooks

Included are Co-Lab Notebooks which detail the process of developing the computational model, including code examples and "scratch" code to try things out. I go over each contribution and indicate its status and my hopes for its future! Find each notebook described below:

### Pass the Peas

This notebook is an attempt to try an "easy" problem first, before tackling the considerably more complex problem of modeling OSDCs. Starting with Collective Cognition as the overarching paradigm, it seemed that a family trying to pass a dish to each other around a table is an example of a sort of Collective Cognition.\
After making a simple Finite State Machine Computational Model of passing a dish around a table, the notebook begins to get more complex, but it is quickly apparent that even something as "simple" as a family around a table has the ability to be modeled as complexly as an OSDC.\
This notebook is not finished, and the implementation of aspects of embodiment, enaction, extension, and experience (where agents are looking, their theory of mind, etc) is a challenge for any future researchers looking for a "toy problem" of collective cognition to play with.

### Outline and Visualization

Here I lay out the basic ideas behind the model and how it will work (see Model Parameters Scratch Pad), starting from Kaufmann et al's "An Active Inference Model of Collective Intelligence" which incidentally comes with its own CoLab for other researchers to run and adapt (Simulation Run for an Active Inference Model of Collective Intelligence is my beginning at adapting it).\
Also here are some samples of code for visualizing the model using various libraries and techniques.

### Model Parameters Scratch Pad

Using existing research as much as possible, and with the GitHub API in mind, this notebook explores the possible parameters for a model of OSDCs.

### Active Inference Agent OSDC

Adapted from the documentation for inferactively's PYMDP, this notebook tries to use the given multi-armed Bandit representation of an explore/exploit problem with underlying Active Inference equations to solve each agent in the OSDC's decision problems.

## NetLogo Files

Included are NetLogo files for running the simulation of the model. The files use the NetLogo Python extension, and require installation of numpy, matplotlib, and inferactively-pymdp.

### Simple OSDC

This is a simple NetLogo model of an OSDC, waiting to be filled with the guts of our conceptual choice.

### OSDC Model for Estimating Priors

Here is a model which uses matplotlib to visualize prior distributions (along with likelihoods and another useful probability distributions). This will require the user to have matplotlib installed.

### Active Inference OSDC

This model is driven by the pymdp library (see the Active Inference Agent OSDC notebook above) which uses the equations and methods of Active Inference. This will require the user to have pymdp installed.

### Cooperation-driven OSDC

Made last after many Active Inference-related dead ends, this model is not too exciting, but it has many interesting qualities.

## Bibliography

Kaufmann R, Gupta P, Taylor J. An Active Inference Model of Collective Intelligence. Entropy. 2021; 23(7):830. https://doi.org/10.3390/e23070830

Reidl C, Kim Y, Gupta P, Woolley A. Quantifying collective intelligence in human groups. PNAS. 2021; 118(21). https://doi.org/10.1073/pnas.2005737118

AlMarzouq M, Grover V, Thatcher J. Taxing the development structure of open source communities: An information processing view, Decision Support Systems, Volume 80, 2015; Pages 27-41, ISSN 0167-9236. https://doi.org/10.1016/j.dss.2015.09.004

Waade, P.T., Enevoldsen, K.C., Vermillet, AQ. et al. Introducing tomsup: Theory of mind simulations using Python. Behav Res (2022). https://doi.org/10.3758/s13428-022-01827-2

Ashby M. Ethical Regulators and Super-Ethical Systems. Systems 2020, 8(4), 53; https://doi.org/10.3390/systems8040053 

CHAOSS Metrics https://chaoss.community/metrics/