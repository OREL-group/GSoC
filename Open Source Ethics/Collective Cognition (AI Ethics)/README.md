# A Collective Cognition Model for AI Ethics

## Terms, Definitions, and Acronyms

*OSDC: Open Source Development Community*\
The acronym *OSDC* is very useful for describing this model (as you might imagine) and relates to projects described as FOSS, or just Open Source, and the Communities surrounding those projects (as described by CHAOSS, for example).

## Co-Lab Notebooks

Included are Co-Lab Notebooks which detail the process of developing the computational model in Python, including code examples and "scratch" code to try things out. I go over each contribution and indicate its status and my hopes for its future! Find each notebook described below:

### Pass the Peas

This notebook is an attempt to try an "easy" problem first, before tackling the considerably more complex problem of modeling OSDCs. Starting with Collective Cognition as the overarching paradigm, it seemed that a family trying to pass a dish to each other around a table is an example of a sort of Collective Cognition.\
After making a simple Finite State Machine Computational Model of passing a dish around a table, the notebook begins to get more complex, but it is quickly apparent that even something as "simple" as a family around a table has the ability to be modeled as complexly as an OSDC.\
This notebook is not finished, and the implementation of aspects of embodiment, enaction, extension, and experience (where agents are looking, their theory of mind, etc) is a challenge for any future researchers looking for a "toy problem" of collective cognition to play with.

### Outline and Visualization

Here I lay out the basic ideas behind the model and how it will work (see Model Parameters Scratch Pad), starting from Kaufmann et al's "An Active Inference Model of Collective Intelligence" which incidentally comes with its own CoLab for other researchers to run and adapt (Simulation Run for an Active Inference Model of Collective Intelligence is my beginning at adapting it). Also here are some samples of code for visualizing the model using various libraries and techniques.\
This notebook is also not quite finished, in terms of the model presented and its connections to visualization functions.

### Model Parameters Scratch Pad

Using existing research as much as possible, and with the GitHub API in mind, this notebook explores the possible parameters for a model of OSDCs. See notebook for details and references.\
This notebook can't really be improved upon, but includes a lot of ideas that may be helpful for the future.

### Active Inference Agent OSDC

Adapted from the documentation for inferactively's PYMDP, this notebook tries to use the given multi-armed Bandit representation of an explore/exploit problem with underlying Active Inference equations to solve each agent in the OSDC's decision problems.\
This notebook could definitely be improved, it's debateable as to whether an explore/exploit approach is valid for this situation, but PYMDP lends itself to many approaches. Also the distributions are estimated and not updated, so the model as it exists right now isn't so exciting, but it's a start!

## NetLogo Files

Included are NetLogo files for running the simulation of the model. The files use the NetLogo Python extension, and require installation of numpy, matplotlib, and inferactively-pymdp.

### Simple OSDC

This is a simple NetLogo model of an OSDC, waiting to be filled with the guts of our conceptual choice.\
This is a good starter NetLogo Model.

### OSDC Model for Estimating Priors

Here is a model which uses matplotlib to visualize prior distributions (along with likelihoods and another useful probability distributions). This will require the user to have matplotlib installed.\
It may be easier to play with distributions in one of the CoLab notebooks, but it felt nice to see Python working reliably and constructively in NetLogo.

### Active Inference OSDC

This model is driven by the PYMDP library (see the Active Inference Agent OSDC notebook above) which uses the equations and methods of Active Inference. This will require the user to have PYMDP installed.\
Much like the CoLab notebook above entitled Active Inference Agent OSDC, this NetLogo model needs work, and indeed, that notebook and this model share Python code, the NetLogo incorporates it. So the notebook could be a good place to tweak things, then import it into NetLogo.

### Cooperation-driven OSDC

Made last after many Active Inference-related dead ends, this model is not too exciting, but it has many interesting qualities. It's based on equations from Glance and Huberman (1998), following on research from Marwell and Oliver (1993) which challenges Olson's "Free Rider" computational model (1965).\
These equations could be tweaked a bit, but especially the visualization of them, the way they are applied to the "Contribution Location" needs some adjustments. For instance, right now the boundaries and locations of the agents moving in the contribution space are adjusted based on the size of overall contributions in terms of repo size, which is not necessarily the best way to find patterns in cooperation.

## Bibliography

AlMarzouq M, Grover V, Thatcher J. Taxing the development structure of open source communities: An information processing view, Decision Support Systems, Volume 80, 2015; Pages 27-41, ISSN 0167-9236. https://doi.org/10.1016/j.dss.2015.09.004

Ashby M. Ethical Regulators and Super-Ethical Systems. Systems 2020, 8(4), 53; https://doi.org/10.3390/systems8040053 

CHAOSS Metrics https://chaoss.community/metrics/

Foulonneau, M et al. Analyzing the Open Source communities' lifecycle with communication data. ACM (2013) 978-1-4503-2004-7/10/10. https://dl.acm.org/doi/10.1145/2536146.2536183

Heins et al., (2022). pymdp: A Python library for active inference in discrete state spaces. Journal of Open Source Software, 7(73), 4098, https://doi.org/10.21105/joss.04098

Huberman, B, Glance, N. Beliefs and Cooperation. Xerox Palo Alto Research Center. (1994). https://arxiv.org/abs/adap-org/9405001

Kaufmann R, Gupta P, Taylor J. An Active Inference Model of Collective Intelligence. Entropy. 2021; 23(7):830. https://doi.org/10.3390/e23070830

McGregor, S, Baltieri, M, Buckley, C. A Minimal Active Inference Agent. University of Sussex, Brighton, UK. (2015). https://arxiv.org/abs/1503.04187v1

Parr, T, Pezzulo, G, Friston, K. Active Inference: The Free Energy Principle in Mind, Brain, and Behavior. MIT Press (2022). https://doi.org/10.7551/mitpress/12441.001.0001

Prietula, M, Carley, K, Gasser, L. Simulating Organizations: Computational Models of Institutions and Groups. American Association for Artificial Intelligence. (1998).

Reidl C, Kim Y, Gupta P, Woolley A. Quantifying collective intelligence in human groups. PNAS. 2021; 118(21). https://doi.org/10.1073/pnas.2005737118

Tamburri, D et al. Discovering community patterns in open-source: a systematic approach and its evaluation. Empirical Software Engineering (2019) 24:1369-1417. https://doi.org/10.1007/s10664-018-9659-9

Waade, P.T., Enevoldsen, K.C., Vermillet, AQ. et al. Introducing tomsup: Theory of mind simulations using Python. Behav Res (2022). https://doi.org/10.3758/s13428-022-01827-2

Young, J et al. Which contributions count? Analysis of attribution in open source. University of Vermont, Open Source programs Office, Google. (2021). https://arxiv.org/abs/2103.11007