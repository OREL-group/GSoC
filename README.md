## Google Summer of Code Projects 2022

<P>
    <IMG align="center" height = "150" width = "150" SRC="https://github.com/OREL-group/GSoC/blob/main/Media/GSoC.png">
</P>
    
Featuring projects in the following groups: Ethics, Society, and Technology, DevoWorm, and Rokwire Community.     
    
* [Introduction to OREL](https://github.com/OREL-group/Onboarding/blob/main/Intro-to-OREL.md).

* [How to OREL]() (coming soon).
    
* [Onboarding guide](https://github.com/devoworm/Proposals-Public-Lectures/blob/master/Onboarding%20Guide/onboarding-guide.md) for 2022 (DevoWorm). 
  
* Prior GSoC projects have lead to: [DevoLearn](https://github.com/DevoLearn/devolearn), [Developmental Braitenberg Vehicles](https://github.com/OREL-group/dBV), [Contextual Geometric Structures](https://github.com/Orthogonal-Research-Lab/CGS)

### Ethics, Technology, and Society
    
<P>
    <IMG align="center" height = "150" width = "150" SRC="https://github.com/OREL-group/GSoC/blob/main/Media/OREL.png">
</P>

#### A Collective Cognition Model for AI Ethics

The need for automated evaluation of real-time data is important in a number of sociotechnical contexts. Our group is looking to develop an auditing system and simulation of collective cognition that will improve open-source community sustainability. This interdisciplinary approach to AI ethics will involve both the development of a homeostatic system that encourages cooperative and altruistic interactions, and using simulated data generated through an agent-based model of open-source behaviors and interactions.

In taking a cybernetic approach, the candidate will build an analytical model that incorporates features such as general feedback loops (recurrent relationships) and causal loops (reciprocal causality). This might be in the form of a traditional boxes and arrows (input-output) model, or something more exotic such as Reinforcement Learning. Applicants might take inspiration from Mick Ashby’s ethical regulator (https://en.wikipedia.org/wiki/Ethical_regulator).

The broader goal is to build a model of cultural evolution that will encourage desired behaviors. The first part of this project will involve building a computational system to model the resources, activities, and interrelationships of an open-source community. The second part of the project will involve simulating this community using an agent-based model, which will provide the candidate with output data necessary to train and benchmark the cybernetic model.

__What can I do before GSoC?__
You can join the Orthogonal Lab Slack and Github, as well as attend our Saturday Morning NeuroSim meetings. You will work with our Ethics, Society, and Technology group, and interactions with your colleagues is key. You will also want to become familiar with a scientific programming approach (such as Python or Julia) to construct your cybernetic model, as well as the NetLogo platform for building agent-based models.

__Requirements__
Expertise or the ability to learn Python, Julia, or Kotlin (for the cybernetic model) and Scala and Java (for the agent-based model). The ability to extract model representations from complex systems is helpful. Knowledge of open-source development practices and an interest in interdisciplinary research are a must.

__Planned Effort__
350 hours. Mentors: Bradly Alicea (bradly.alicea@outlook.com), Jesse Parent (jtparent2018@gmail.com)

### DevoWorm
    
<P>
    <IMG align="center" height = "115" width = "150" SRC="https://github.com/OREL-group/GSoC/blob/main/Media/DW.png">
</P>

#### GNNs as Developmental Networks
Biological development features many different types of networks: neural connectomes, gene regulatory networks, interactome networks, and anatomical networks. Using cell tracking and high-resolution microscopy, we can reconstruct the origins of these networks in the early embryo. Building on our group's past work in deep learning and pre-trained models, we look to apply graph neural networks (GNNs) to developmental biological analysis.

We seek to create graph embeddings that resemble actual biological networks found throughout development. Potential activities include growing graph embeddings using biological rules, differentiation of nodes in the network, and GNNs that generate different types of movement output based on movement seen in microscopy movies. The goal is to create a library of GNNs that can simulate developmental processes by analyzing time-series microscopy data.

DevoWorm is an interdisciplinary group engaged in both computational and biological data analysis. We have weekly meetings on Jit.si, and are a part of the OpenWorm Foundation. You may also have the chance to work with our DevoLearn (open-source pre-trained deep learning) software, in addition to adding your contributions to the DevoWorm AI library.

__What can I do before GSoC?__
You can ask one of the mentors to direct you to the data source and you can start working on it. Please feel free to join the OpenWorm Slack or attend our meetings to raise questions/discussions regarding your approach to the problem.

DevoWorm website: link

DevoLearn (preprint): link

DevoWorm AI: link

__Skills/requirements__
PyTorch/Tensorflow (PyTorch will be preferred because all our other models are on that framework already) Wrangling with video data Building a simple GUI on top of the model to run it on local systems (on Linux/windows/macOS). Basic knowledge of biology and complex networks theory would be helpful.

__Planned Effort__
175 hours. Mentors: Bradly Alicea (balicea@illinois.edu), TBA

#### Digital Microsphere
This project will build upon the specialized microscopy techniques to develop a shell composed of projected microscopy images, arranged to represent the full external surface of a sphere. This will allow us to create an atlas of the embryo’s outer surface, which in some species (e.g. Axolotl) enables us to have a novel perspective on neural development. You will build a computational tool that allows us to visualize 4D data derived from the surface of an Axolotl embryo.

__What can I do before GSoC?__
Build basic prototypes for this project and discuss about them with the mentors, then read these papers:

Gordon, R. (2009). Google Embryo for Building Quantitative Understanding of an Embryo As It Builds Itself. II. Progress Toward an Embryo Surface Microscope. Biological Theory, 4, 396–412.

Crawford-Young, S., Dittapongpitch, S., Gordon, R., and Harrington, K. (2018). Acquisition and reconstruction of 4D surfaces of axolotl embryos with the flipping stage robotic microscope. Biosystems, 173, 214-220.

__Skills/requirements__
Handling higher dimensional microscopy data (preferably also creating an API to load them as tensors for computation on the GPU). Building an intuitive GUI (or a web interface). Feature extraction (canny edges/thresholding/denoising).

__Planned Effort__
175 hours. Mentors: Bradly Alicea (balicea@openworm.org), Susan Crawford-Young (susan.crawfordyoung@gmail.com).

### Rokwire Community
    
<P>
    <IMG align="center" height = "100" width = "200" SRC="https://github.com/OREL-group/GSoC/blob/main/Media/RokComm.png">
</P>

#### Interactive Applications for the Open-source Contributors Community

Support the Rokwire Community of mobile developers by creating sample applications as tutorials for new open-source contributors. [Rokwire](https://rokwire.org/) is an open-source platform for developing mobile applications that enable smart communities. Existing applications include the Illinois App (campus app for the University of Illinois Urbana-Champaign) and Safer (a public health and COVID management app).

We are interested in creating programming templates in the form of interactive programming. This will consist of breaking down the steps to creating things in Rokwire and demonstrating this to potential open-source contributors. These programming templates will be distributable in the form of video tutorials and digital notebooks. These templates will allow open-source contributors with limited understanding of the architecture to create their own capabilities and talents for inclusion as functionality in a community mobile app.

One prerequisite to this project is to develop a working understanding of the Rokwire architecture. A starting point for this is the [Building Blocks API](https://github.com/rokwire/rokwire-building-blocks-api) and various [Community Wiki](https://github.com/rokwire/rokwire-community/wiki/API-Ecosystem-Diagram) entries. In Rokwire, capabilities and talents are build atop the Rokwire building blocks, which enable users to have a customized, privacy-assured experience. Your efforts will also help to facilitate adoption of the Rokwire platform, serve to establish a set of community standards, and participate in educational opportunities related to open-source. 

__Skills/requirements__
This project requires familiarity with some or all of the following languages: Python, Golang, Dart, and Flutter.

__Planned Effort__
350 hours. Mentors: Bradly Alicea (balicea@illinois.edu), Sandeep Puthanveetil Satheesan (sandeeps@illinois.edu)

#### Extended Reality (XR) for Open-source Community-building
Help the Rokwire Community to develop an extended reality (XR) infrastructure. The focus will be building upon the Mozilla platforms A-Frame (web framework), Mozilla Hubs (virtual rooms), and Spoke (3-D social scenes). Your efforts will culminate in two outcomes. The first outcomes involves developing a pipeline of virtual experiences for education and collaboration in the Rokwire Community. Secondarily, we would like to develop Augmented Reality resources to be integrated into mobile apps. Contribute to our broader vision of smart communities in XR! 

__Skills/Requirements__
Familiarity with Unity or Blender is a must. Experience with C++, Python, or Java are desirable.

__Planned Effort__
175 hours. Mentors: Bradly Alicea (balicea@illinois.edu).
    
### Towhee
    
#### Towhee Open Source Machine Learning Pipelines
Towhee is a flexible, application-oriented framework for running machine learning (ML) pipelines. It is a Python project that aims to make greatly simple anything2vec, allowing 
everyone - from beginner developers to large organizations - to deploy complex pipelines with just a few lines of code. It has become a common practice among the industry to drive data applications with neural network models. Applications involving embedding can be seen in all walks of life, such as product recommender system, copyright protection, data management, software security, new drug discovery, finance, insurance, etc. Despite the fact that the concept of "embed everything" has prevailed in academia and industry in recent years, how to embed unstructured data reasonably and efficiently based on business needs is still an urgent problem that has not yet been resolved. The idea of the Towhee project is to sweep out those obstacles and make MLops significantly easier. Support Towhee community by creating pipelines for STEM. Interdisciplinary pipelines which reach diversified audience. 
    
__Some of Towhee's key features include__    
* easy ML for everyone: Run a machine learning pipeline with less than five lines of code.

* rich operators and pipelines: Collaborate and share pipelines with the open source community.

* automatic versioning: Our versioning mechanism for pipelines and operators ensures that you never run into dependency hell. Support for fine-tuning models: Feed your dataset into our Trainer and get a new model in just a few easy steps.
    
* deploy to cloud (to be implemented): Ready-made pipelines can be deployed to the cloud with minimal effort.

__What can I do before GSoC?__    
Find us on [GitHub](http://www.github.com/towhee-io), join our [Slack Channel](http://slack.towhee.io), follow us on [Twitter](https://www.twitter.com/towheeio), visit our [Towhee hub](https://towhee.io). Join our Office Hours every Thursday from 4-5pm PST.

You can also build a basic prototype for this project. Please feel free to join the Towhee Slack or attend our Office Hour to raise questions/discussions 
regarding your approach to the problem.
    
__Skills/requirements__   
Pytorch and good understanding of python programming language along with interest in interdisciplinary research.

__Planned Effort__    
350 hours Mentors: Krishna Katyal [(krishnakatyal5121@gmail.com)](mailto:krishnakatyal5121@gmail.com), Frank Liu [(frank.zijie@gmail.com)](mailto:frank.zijie@gmail.com).
