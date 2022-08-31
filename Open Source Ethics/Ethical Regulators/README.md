# Exploring Openness through Agent-Based Models of Personality 

"SOCRATES: Or again, in a ship, if a man having the power to do what he likes, has no intelligence or skill in navigation [aretes kybernetikes], do you see what will happen to him and to his fellow-sailors?" -Plato, Alcibiades I

As revolutions and innovations have been pushed forward in the field of cybernetics, spanning the foundations of other disciplines like cognitive science, computer science, and robotics, since the field’s inception by ​​Norbert Wiener, researchers have studied how similar principles are involved in the regulation of artificial control systems and organisms. When understanding how humans think and behave, provides a way for creating models of cybernetic theories of the human experience - including personality, emotions, and moods. For personality, in particular, we can construct a "complex" personality using NetLogo, as produced by ​​Duncan McGreggor.

Historically, cybernetics has been developed during about the same period as behaviorism. This resulted in cybernetics being strongly behavioristic. The first cyberneticians made it clear that they regarded humans as black boxes (Ashby) or muddy boxes (Beer) and that they were only interested in developing mathematical models that described how the output of a system changed given different inputs. That is describing the external behavior of the system rather than fantasize about the inner workings of the system. Cognitivism has sprung up from cybernetics, but has taken this functional interpretation of systems too literally and created one psychological construct after another. Constructs that tend to get a life of their own. No, it is better that we interpret CB5T as behavioristic with the clear note that CB5T describes external and internal behavior. Someone scoring high on agreeableness is likely to also engage other people socially in terms of external behavior. At the same time thatsame person can also have internal behaviors that he would describe as activating a goal of working together with other people. DeYoung makes clear that when it comes to external behavior that we interpret as goal driven, it could well be that the person involved has a conscious goal, an unconscious goal or no goal at all! We, as observers, interpret his behavior as goal orientated. But this doesn’t have to mean that there really is a goal. Cybernetics has been developed from the viewpoint of the observer. 

## Agent-Based Models of Personality 

In NetLogo, agent-based models of human behavior and interaction can be constructed. The socio-natural one, for example, is used in studying how different social behaviors contribute to the resiliency of interactions between culture and environment when there are differing social systems. Many of these models are used in simulating human behavior in virtual environments, and allow users to create equations and general descriptions for modelling forces such as attraction and repulsion between individuals for studying how those individuals interact. For this project, we use a NetLogo model for simulating how people with different personality types interact with each other. With four main personality types (I, II, III, IV) with two subtypes (a and b) for each, we use a model with a total of 8 different types of personalities, each interacting with each other in the table shown below: 

"Attraction and Repulsion between personality types"
|           |           | green  | turqouise | cyan    | blue    | yellow   | orange   | red     | pink    |
|-----------|-----------|--------|-----------|---------|---------|----------|----------|---------|---------|
|           |           | Ia (0) | Ib (1)    | IIa (2) | IIb (3) | IIIa (4) | IIIb (5) | IVa (6) | IVb (7) |
| green     | Ia (0)    | +      | +         | +       | +       | +        | +        | +       | +       |
| turquoise | Ib (1)    |        | +         | +       | +       | +        | +        | +       | -       |
| cyan      | IIa (2)   |        |           | +       | +       | +        | +        | -       | -       |
| blue      | IIb (3)   |        |           |         | +       | +        | -        | -       | -       |
| yellow    | IIIa (4)  |        |           |         |         | -        | -        | -       | -       |
| orange    | IIIb (5)  |        |           |         |         |          | -        | -       | -       |
| red       | IVa (6)   |        |           |         |         |          |          | -       | -       |
| pink      | IVb (7)   |        |           |         |         |          |          |         | -       |

For a given personality type (I, II, III, and IV) and subtype (a, b, c, d), do the two individuals attract (plus) to one another or repel (minus)? (Numbers in parentheses indicate the personality trait code used in NetLogo for coding purposes). The colors of each person on the NetLogo application are given, as well. As these 8 personalities, in some ways, represent how readily an individual will attract or repel another person, they can be used to measure a form of Openness, one of the personality traits as indicated by the Big Five Personality model (alongside Neuroticism, Extraversion, Agreeableness, and Conscientiousness). In Cybernetics, we refer to the Cybernetic Big Five Theory (CB5T) attempts to explain personality in cybernetic terms, conceptualizing personality traits as manifestations of variation in parameters of the neural mechanisms that evolved to facilitate cybernetic control. 

With CB5T, one can describe how the differences between different individuals can be assigned as or categorized using personality traits or types of adaptations in response to how individuals perceive their environments. Using probabilistic dersciptions of patterns of behavior that can be observed between individuals and their environemnts (as well as interactions between individuals themselves), the personality traits themselves can be edefind as these patterns of behavior that emerge when the environments and individuals appraoch stable states. They can then be studied for constructs of behavior, motivaiton, emotioon, cognition, and be seen as responses to classes of stimuli. Taken as representative of an individuals’ personality, the relevant stimuli can then be observed as response variables that the individual experiences when its own personality is defined a certain way. Like the dimensions of variation between people, traits are reflected through questionnaire methods, and the trait-like dispositions show stability within the individual. This gives us a conneciton between the stability of a NetLogo environment in which individuals have reached a point at which their positions have become steady and stable and how the personality traits have, accordingly, brought them to that state. 

As such, the human cybernetic system compares its current state to a state it predicts. Neuroticisim, another CB5T trait, can be observed as well. Violating expectations, the world perceived increases psychological entropy, and, without an action reaching its goal, the individual can perceive it as potentially threatening. ACcording to CB5T, Neuroticism is a function of the parameters used in determining whether an increase in psychological entropy triggers a defensive response. Thus, those who score high on the Neuroticism trait experience greater effective dysregulation of their negative emotions when they themselves perceive they’re not in the state they’d like to be in.

We can use the attraction and repulsion between different personalities of agents as a means of representing how high one would score on the Opennness trait for the Big Five Personality model. This measures the degree to which one is open-minded. Someone who scores high on the openness trait would be a person who is imaginative, curious, and who enjoys trying new things. With 8 different personality types that interact with one another according to the table above, we can create a NetLogo environment that simulates how those individuals would move towards or away from one another and observe the emergent phenomena and properties of such a system. We can also characterize Big Five traits using metatraits of Stability (a shared variance of Conscientiousness, Agreeableness, and inverse Neuroticism) as well as Plasticity (a shared variance of Extraversion and Openness/Intellect). As they have analogues in cybernetic control systems, we can view stability as the optimization for resisting disruption of ongoing goal pursuit - a useful capacity for a cybernetic system. 

Control hierarchies for complex cybernetic systems can weigh goals for different types of brain activity across contexts and under different conditions that can be used for performing control operations that may involve executive functions or higher-level thinking and reasoning. For different objectives, the brain needs ways of appropriately reasoning through the best methods of doing so and achieving them. 

For the NetLogo system, we can observe how different variations in the setup produce different responses after 1000 ticks of the system. We begin by varying the parameters to select (agent-count=32, interaction-radius=7, force-multiplier=3.50, personality-stdd=3.99, personality-norm=.51, rand-seed=22). This sets the norm of the personality distribution (personality-norm) close to the 0th personality with a standard deviation (personality-stdd) of about 4 for a total of 32 agents. The interaction radius defines the range in which an agent may be in for the force (attraction vs. repulsion) to take place. The force multiplier dictates the effect of the force’s action, and rand-seed simply indicates the random state at which the agents distribute during setup. This process is repeated while changing the personality-norm parameter to test a normal distribution around each of the 8 personalities (to 1, 2, 3, 4, 5, 6, and 7). 

As they say, three’s a crowd. Or, in this case, crowds form as people come and go in the NetLogo environments. 

Workflow/process:
Download the “Modeling Crowds with Personality, Emotions and Moods” repository (https://github.com/oubiwann/abm-personality-and-emotions). 
Open NetLogo.
Select the `.nlogo` model (File → Open) for the Complex personality.
Adjust parameters accordingly for the model.
Click “Go” and observe the population dynamics w.r.t. initial conditions. 
Law of Requisite Variety

“Objects are always imagined as being present in the field of vision as would have to be there in order to produce the same impression on the nervous mechanism.”–Hermann Ludwig Ferdinand von Helmholtz (1910)

“Each movement we make by which we alter the appearance of objects should be thought of as an experiment designed to test whether we have understood correctly the invariant relations of the phenomena before us, that is, their existence in definite spatial relations.”–Hermann Ludwig Ferdinand von Helmholtz (1878) 

With the introduction of the Law of Requisite Variety (LRV) by Ross Ashby, another pioneer in cybernetics, which one might describe as “only variety can absorb variety.” It can also be described as, when the variety or complexity of the environment exceeds the capacity of a system (natural or artificial) the environment will dominate and ultimately destroy that system. This law, now well-known as the First Law of Cybernetics, can also be described as: In order to deal properly with the diversity of problems the world throws at you, you need to have a repertoire of responses which are (at least) as nuanced as the problems you face. 

Here, variety is the number of possible states available for a system. This is equivalent to statistical entropy. For example, a coin can be shown to have a variety of two – Heads and Tails. Thus, if a user wants a way to randomly choose one of two outcomes, the coin can be used. The user can toss the coin to randomly choose one of two options. However, if the user has 6 choices, they cannot use the coin to randomly choose one of six outcomes efficiently. In this case, a six-sided die can be used. A six-sided die has a variety of six. This is a simple explanation of variety absorbing variety. 

With this background, we can note the extended form of the Law of Requisite Variety as:

H(E) ≥ H(D) – H(A) + H(A|D) – B

The H portions of the term represents the statistical entropy for the term. For example, H(E) is the statistical entropy for the essential variables. The larger the value for H, the more the uncertainty around the variable. The goal for the controller is to keep the H(E) as low as possible since a larger value for the entropy for the essential variables indicate a larger range of values for the essential variables. If the essential variables are not kept to a small range of values, the viability of the organism is compromised. We can now look at the other terms of the equation and see how the value for H(E) can be maintained at a lower value.

As these processes would become more thoroughly elaborated upon, von Förster’s geometry came to encompass the patterns of biological life, mathematics, computers, and social systems, not as static structures but as complex and recursive processes of emergence. Here, the foundation is given to propose a project in which these processes come together in creating a homeostatic system that encourages and explores the necessary and sufficient conditions of Mick Ashby’s ethical regulator. 

According to Mick Ashby's ethical regulator theorem, the following nine requisites are necessary and sufficient for a cybernetic regulator to be both effective and ethical:

Purpose expressed as unambiguously prioritized goals.
Truth about the past and present.
Variety of possible actions.
Predictability of the future effects of actions.
Intelligence to choose the best actions.
Influence on the regulated system.
Ethics expressed as unambiguously prioritized rules.
Integrity of all subsystems.
Transparency of ethical behavior.

Of these nine requisites, only the first six are necessary for a regulator to be effective. If a system does not need to be ethical, the three requisites of ethics, integrity, and transparency are optional. 

Sources: 

Safron, Adam, and Colin G. DeYoung. "Integrating Cybernetic Big Five Theory with the Free Energy Principle: A new strategy for modeling personalities as complex systems." Measuring and modeling persons and situations. Academic Press, 2021. 617-649.


*************************************************************************************************************

#### Misc Issues

During Google Summer of Code 2022, a few issues came up with attempting to put together a model of the Law of Requisite Variety in NetLogo and test out its capabilities and functioning capacities for the duration of the summer. 

Attempts to get PyNetLogo running in the Colab environment
Difficulties with packaging issues and installation requirements
Issues sorting out which packages are dependent on each other
These issues would take weeks to pileup such that, at some point, other key features of the project began becoming delayed. 
For example, while a few visualizations were able to be observed, there were produced bugs and issues arising in the ways for them to be properly viewed via PyNetLogo, Colab, and similar platforms. 
Jupyter notebook provided another alterantive. However, with this came other package dependnency/install issues. It wouldn’t load properly on my Mac in many of the different conda environments I had tried.
I also used RNetLogo as well as an interface with Python to see if that’d work well. It still presented its own issues with packages and dependencies. 
Attempt to recreate Law of Requisite Variety (LRV) using PyNetLogo
Attempts to use different systems in demonstrating variety 
Recreating LRV require a more thorough, solid stable understanding and working model before attempting to begin with a theoretical notion of LRV from the ground-up. It varies from model to model and context to context. 

