<p align="center">
	  <img src="https://user-images.githubusercontent.com/92572013/266610534-0b13f675-40f1-4b16-b9cd-19f5ff21619e.png" />
</p>


# OREL - Open Source Sustainability Project

## Introduction
As demonstrated by many organisations, open-source communities can do great things. But this is only true if the contributor community is able to maintain public goods such as the software codebase and institutional knowledge over time and despite contributor turnover.


The goal of this project is to develop tools and techniques for managing and maintaining open-source projects.

  

The formal description of this project can be found [here](https://neurostars.org/t/gsoc-2023-project-idea-4-1-maintaining-an-open-source-sustainability-project-orthogonal-research-and-education-lab-350-h/24574).

  

This project aims to incorporate a combination of Agent-based modelling and Reinforcement learning approach to explore and analyse the sustainability of open-source communities.

  

<p align="center">
	<img  src="https://i.ibb.co/xD1tmcy/Screenshot-2023-08-04-at-8-56-32-PM.png"  alt="Screenshot-2023-08-04-at-8-56-32-PM"  border="0">
</p>

## Previous Work

This project was a part of Google Summer of Code 2022 as well, where it was developed on NetLogo - a multi-agent programmable modelling environment. (Click [here](https://github.com/OREL-group/GSoC/tree/main/Open%20Source%20Ethics/Collective%20Cognition%20%28Reinforcement%20Learning%29) to view the previous year's project).


<p align="center">
	<img  src="https://user-images.githubusercontent.com/92572013/266616768-d440273e-eb97-469a-b43c-f055a48eddd4.gif"  alt="Screenshot-2023-08-04-at-9-24-52-PM"  border="0">

</p>


There are several limitations in the Netlogo platform that hinder the long term viability of this project. The main ones are : -

<ul>
	<li>It uses its own language called nlogo, so it's not really expandable and developer friendly.</li>
	<li>The Q-learning plugin in Netlogo does not save the training data post every session, so the models do not improve over time</li>
	<li>Feeding the models data and parameters from various platforms like Github would be much more feasible in Python</li>
	<li>Python provides many more libraries to analyse and visuallise the data obtained from the simulations</li>
</ul>

## Google Summer of Code 2023

Hence, this summer I have attempted to recreate this project using Mesa - an agent-based simulation library which uses Python, as developing with Python opens a door to a lot of creativity and extensive libraries.


This project consists of a website, and deployed Mesa models embedded in the website  - in the form of playgrounds. They help in tweaking the parameters and give a picture on how the sustainability of an open-source community looks like in the long run.


The goal of the project is to develop RL models to cater the key challenges faced in open-source-sustainability, such as Contributor retention, promotion of Contributor ➡️ Admin etc.

## Tech Stack

1. Next js & Tailwind CSS

	The website for this project is developed using the Next.js framework and is deployed on Vercel.
	It uses Tailwind CSS for styling.

  

2. Github GraphQL API

	The app uses the Github Access token to fetch the user data (repositories, issues, organisations etc) from the Github `GraphQL API`.

  

3. Mesa for Agent-based Modelling

	Mesa - an Apache2 licensed agent-based modelling (or ABM) framework in Python has been used for developing ABMs for this project. Mesa has been prescribed as the framework to develop ABMs for this project, as development in Python opens the door to creativity and extensibility.

  

Feel free to clone this repository, raise any issue and make contribute towards this project. The setup instructions can be found in the SETUP.md file.
	

## Mentors : -

<ol>
	<li>Dr Bradly Alicea</li>
	<li>Jesse Parent</li>
	<li>Ankit Grover</li>
</ol>

## Slack Channel and other information

https://launchpass.com/orthogonal-research