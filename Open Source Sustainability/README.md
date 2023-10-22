<p align="center">
	  <img src="https://user-images.githubusercontent.com/92572013/266610534-0b13f675-40f1-4b16-b9cd-19f5ff21619e.png" />
</p>


# OREL - Open Source Sustainability Project



## Introduction
As demonstrated by many organisations, open-source communities can do great things. But this is only true if the contributor community is able to maintain public goods such as the software codebase and institutional knowledge over time despite contributor turnover.


The goal of this project is to develop tools and techniques for managing and maintaining open-source projects.

  

The formal description of this project can be found [here](https://neurostars.org/t/gsoc-2023-project-idea-4-1-maintaining-an-open-source-sustainability-project-orthogonal-research-and-education-lab-350-h/24574).

  

This project aims to incorporate a combination of Agent-based modelling and Reinforcement learning approach to explore and analyse the sustainability of open-source communities.

  

<p align="center">
	<img src="https://i.ibb.co/xD1tmcy/Screenshot-2023-08-04-at-8-56-32-PM.png"  alt="Screenshot-2023-08-04-at-8-56-32-PM"  border="0">
</p>

## Previous Work

This project was a part of Google Summer of Code 2022 as well, where it was developed on NetLogo - a multi-agent programmable modelling environment. (Click [here](https://github.com/OREL-group/GSoC/tree/main/Open%20Source%20Ethics/Collective%20Cognition%20%28Reinforcement%20Learning%29) to view the previous year's project).


<p align="center">
	<img  src="https://user-images.githubusercontent.com/92572013/266616768-d440273e-eb97-469a-b43c-f055a48eddd4.gif"  alt="Screenshot-2023-08-04-at-9-24-52-PM"  border="0">

</p>


There are several limitations in the Netlogo platform that hinder the long term viability of this project. Few of them are as follows : -

<ul>
	<li>It uses its own language called nlogo, so it's not really expandable and developer friendly.</li>
	<li>The Q-learning plugin in Netlogo does not save the training data post every session, so the models do not improve over time</li>
	<li>Feeding the models data and parameters from various platforms like Github would be much more feasible in Python</li>
	<li>Python provides many more libraries to analyse and visuallise the data obtained from the simulations</li>
</ul>

## GSoC 2023

Hence, this summer I have attempted to move this project to Mesa - an Agent-based simulation library which uses Python, as developing with Python opens a door to a lot of creativity and extensive libraries.


This project consists of a website, where there are Mesa models embedded - in the form of playgrounds. They help in tweaking the parameters and give a picture on how the sustainability of an open-source community looks like in the long run.


The goal of the project is to develop RL models to cater the key challenges faced in open-source-sustainability, such as Contributor retention, promotion of Contributor ️→ Admin etc.

## Tech Stack

1. Website

	The website for this project is developed using the Next.js framework

  

2. Auth provider

	For simplicity sake, this project uses the Github GraphQL API to fetch data and insights of a given project of a particular user. This data can then be plugged-in to the models to explore and analyse the sustainability of a project.

  

3. Agent-based Models

	Mesa - an Apache2 licensed agent-based modelling (or ABM) framework in Python has been used for developing ABMs for this project. Mesa has been prescribed as the framework to develop ABMs for this project, as development in Python opens the door to creativity and extensibility.

  

	Feel free to clone this repository, raise any issue and make contribute towards this project. The project can be found at Orthogonal Lab's official GIthub over here.
	

## Mentors : -

<ol>
	<li>Dr Bradly Alicea</li>
	<li>Jesse Parent</li>
	<li>Ankit Grover</li>
</ol>