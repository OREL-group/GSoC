globals [
  ;num_agents
  num_cooperating
  ;uncertainty
  ;reevaluate_rate
  churn_rate
  repo_size
  ;unit
  ;horizon
  dynamics_of_coop
  fraction_cooperating
  ;max_noise
]

breed [ members member ]

members-own [
  member_name
  qual
  quan
  engag
  contrib_size
  role
  other_agents
  utility
  benefit_rate
  personal_cost
  cooperating?
  local_num_cooperating
  horizon_length
  success_prob
  f_crit
]

to setup
  ca

  ;set unit 1 ; amount we count repo size by
  ;set horizon 2;
  let names [ "Abigail" "Adelard" "Astrid" "Alvin" "Arthur" "Annie" "Axel" "Adam" "Alf" "Alice" "Ansel" "Adelaide" "Arturo" "Amabalis" "Anais" "Angela" "Adolfo"
              "Beatrix" "Bernice" "Bob" "Barbie" "Baxter" "Bigby" "Brian" "Bullet" "Budgie" "Barbara" "Baron" "Byron" "Billy" "Beanie" "Bootsy" "Bobo" "Bono"
              "Cedric" "Christina" "Christian" "Christopher" "Christie" "Copernicus" "Calvin" "Calder" "Cecil" "Colin" "Cady" "Caitlin" "Caligula" "Charles" "Crissy" "Cinder"
              "Debra" "Delores" "Dudley" "Dilbert" "Dodge" "Dan" "Danielle" "David" "Duke" "Devina" "Denny" "Dingus" "Donathan" "Donny" "Dante" "Diogenes" "Dawn"
              "Edmund" "Edgar" "Eloise" "EttaLou" "Elvira" "Elsie" "Elmer" "Ettiene" "Erasmus" "Elohim" "Exeter" "Ever" "Eunice" "Eustice" "Eduardo" "Edwina" "Edith"
              "Francine" "Fallon" "Frank" "Feivel" "Fifi" "Francois" "Ferdinand" "Felicia" "Felix" "Fred" "Flannery" "Fido" "Faust" "Francisco" "Fanny" "Fenwick"
              "George" "Gertrude" "Georgie" "Gus" "Gary" "Gene" "Gramps" "Granny" "Gringo" "Geronimo" "Geraldo" "Glen" "Georgette" "Geoff" "Gunther" "Garland"
              "Howie" "Hannah" "Havarah" "Heinrick" "Henna" "Havana" "Heaven" "Holly" "Hope" "Heiman" "Heimy" "Howard" "Hulk" "Honey" "Hannibal" "Herod"
              "Icarus" "Ionia" "Isabelle" "Isis" "Israel" "Issy" "Ione" "Ingrid" "Ibex" "Ivy" "Imogen" "Inez" "Ignacio" "Isadora" "Irma" "Iggy" "India" "Inju"
              "Justine" "Joe" "Jack" "Jake" "Janet" "Jill" "Jonathan" "Jasper" "Janelle" "Janice" "Joaquin" "Jay" "Jerry" "Jessica" "Josephine" "Joa" "Joan" "Jolene"
              "Katya" "Kate" "Kathleen" "Karl" "Kathy" "Kortney" "Kronkite" "Kirby" "Kimberly" "Kim" "Kadisha" "Kristina" "Keith" "Kalamity" "Kenji" "Kendall"
              "Louise" "Louis" "Linda" "Loretta" "Lionel" "Lyle" "Lewis" "Lumpy" "Linette" "Lenny" "Lorene" "Lola" "Letecia" "Lisette" "Lucy" "Lucian" "Landry"
              "Montgomery" "Margerie" "Maggie" "Midge" "Myron" "Mark" "Mike" "Miles" "Minerva" "Mykael" "Michael" "Melissa" "Melanie" "Macy" "Moira" "Manny"
              "Nick" "Nicholas" "Nigel" "Nanine" "Nancy" "Ninette" "Naomi" "Ned" "Noona" "Nona" "Nina" "Nissa" "Nancy" "Neva" "Nieva" "Nora" "Newt" "Noam"
              "Octavius" "Oliver" "Ollie" "Olivia" "Ormand" "Oswald" "Orville" "Owen" "Oswaldo" "Olivander" "Orson" "Orex" "Onmund" "Offenglove" "Ozzy"
              "Peter" "Patricia" "Patrice" "Patrick" "Prince" "Pierce" "Patty" "Pygmalia" "Pigeon" "Paul" "Petey" "Pliny" "Penelope" "Ptomely" "Piper"
              "Quinn" "Quan"
              "Robert" "Raymond" "Reinhart" "Rachel" "Raquel" "Ringo" "Robbie" "Raleigh" "Riley" "Rory" "Roland" "Ryan" "Raphael" "Rapunzel" "Rupolph" "Rupbert" "Rufus" "Rusty"
              "Steve" "Steinway" "Sarah" "Sandra" "Sigourney" "Susie" "Sissy" "Sally" "Susan" "Silver" "Stella" "Stellathe" "Stewart" "Sylvia" "Sophie" "Sage" "Sophia" "Sonia"
              "Todd" "Timothy" "Talus" "Tallulah" "Ted" "Tyler" "Theodore" "Tom" "Thomas" "Tammy" "Tanya" "Titus" "Thor" "Tyra" "Tyree" "Thaddeus" "Thucydides" "Teal" "Tanner" "Tyson"
              "Ulysses" "Ulrich" "Undine" "Ulgar" "Uniqwa" "Ursula" "Ursaline" "Uzaki" "Usher"
              "Vanover" "Victor" "Valerie" "Valmor" "Val" "Veronica" "Vaughn" "Viviana" "Vivian" "Vivianca" "Vlad"
              "Wallace" "Walter" "William" "Wilemena" "Wilemette" "Wilhelm" "Wole" "Winona" "Winnie" "Wales" "Wyatt" "Wilt" "Wilson" "Waldo" "Wilbur" "Watson"
              "Xerxes" "Xander" "Xandra" "Xanadu" "Xiah" "Xavier" "Xerox"
              "Yaro" "Yahweh"
              "Zed" "Zena" "Zenon" "Zero" "Zeb"
  ]

  create-members num_agents [
    set member_name one-of names
    ; initialize values
    set utility random-normal 0.0 100.0
    set benefit_rate random-normal 0.0 100.0
    set personal_cost random-normal 0.0 100.0
    ifelse (one-of [0 1]) = 1 [set cooperating? TRUE] [set cooperating? FALSE]
    set horizon_length random-normal 0 100
    set success_prob random-normal 0.0 1.0

    ; find f_crit
    set f_crit ((num_agents * personal_cost - benefit_rate) / (horizon_length * reevaluate_rate * (benefit_rate - personal_cost)))

    ; estimate num_cooperating based on current values
    let cooperating_val 0
    if cooperating? [ set cooperating_val 1 ]
    set local_num_cooperating ((num_agents / benefit_rate) * (utility + (personal_cost * cooperating_val)))

    ifelse f_crit > local_num_cooperating
    [ set cooperating? TRUE ]
    [ set cooperating? FALSE ]

    set qual ((random 100) / 100)
    set quan ((random 100) / 100)
    set engag ((random 100) / 100)

    set contrib_size (quan * unit) ; using the quantitative value, find the size they contribute

    set role (one-of ["admin" "dev" "other"])

    setxy (qual * max-pxcor) (quan * max-pycor)

    set shape "person"
    ifelse role = "admin" [
      set color (list (engag * 255) 0 0)
    ]
    [
      ifelse role = "dev" [
        set color (list 0 (engag * 255) 0)
      ]
      [
        set color (list 0 0 (engag * 255))
      ]
    ]
  ]

  ask members [
    set repo_size (repo_size + contrib_size)
  ]

  reset-ticks
end

to go
  ask members [
    get-sensory-info
    take-action
    update-world
  ]

  set num_cooperating (count members with [cooperating? = TRUE])
  set dynamics_of_coop find-dynamics

  tick
end

to-report find-dynamics
  set fraction_cooperating (num_cooperating / num_agents)
  report (- reevaluate_rate) * (fraction_cooperating - (1 / 2) * (1 + error-func))
end

to-report error-func
  let mean_f_crit (mean [f_crit] of members)
  let mean_success_prob (mean [success_prob] of members)
  let mean_num_cooperating (mean [local_num_cooperating] of members)
  let f_coop (mean_success_prob * mean_num_cooperating + (1 - mean_success_prob) * (1 - mean_num_cooperating))
  let coop_function ((f_coop - mean_f_crit) / (uncertainty * (sqrt 2)))
  report coop_function
end

to get-sensory-info
  ; find the local horizon of the given agent
  let horizon_value (engag * horizon)
  ; look around at all the agents around that agent and their variables
  set other_agents (members in-radius horizon_value)

  ; find f_crit
  set f_crit (((num_agents * personal_cost) - benefit_rate) / (horizon_length * reevaluate_rate * (benefit_rate - personal_cost)))
  ;show f_crit

  ; set the cooperating value (kroenecker delta)
  let cooperating_val 0.0
  if cooperating? [ set cooperating_val 1.0 ]

  ; calculate local utility using last known local_num_cooperating
  set utility (benefit_rate * (local_num_cooperating / num_agents) - (personal_cost * cooperating_val))

  ; estimate local_num_cooperating based on current values
  set local_num_cooperating (((count other_agents) / benefit_rate) * (utility + (personal_cost * cooperating_val)))
  
  ;let local_fraction_cooperating (local_num_cooperating / num_agents)
  let local_fraction_cooperating (success_prob * local_num_cooperating + (1 - success_prob) * (1 - num_cooperating))
  
  show f_crit
  show local_fraction_cooperating
  ifelse f_crit = local_fraction_cooperating
  [ set cooperating? one-of [TRUE FALSE] ] 
  [  
    ifelse f_crit < local_fraction_cooperating
    [ set cooperating? TRUE ]
    [ set cooperating? FALSE ]
  ]
end

to take-action
  let chosen_action 3

  if cooperating?
  [  set chosen_action one-of [0 1 2]  ]

  ;show chosen_action
  ; 0 => qual+ 1 => quan+ 2 => engag+ 3 => all-

  let change_val ((contrib_size * (random-normal 1.0 max_noise)) / repo_size)
  if role = "admin" [
    set change_val (change_val * 2)
  ]
  if role = "dev" [
    set change_val (change_val * 1.5)
  ]
  if chosen_action = 0 [ set qual (qual + change_val) ]
  if chosen_action = 1 [ set quan (quan + change_val) ]
  if chosen_action = 2 [ set engag (engag + change_val) ]
  if chosen_action = 3 [
    set qual (qual - change_val)
    set quan (quan - change_val)
    set engag (engag - change_val)
  ]

  set contrib_size (contrib_size + (quan * unit)) ; using the quantitative value, find the size they contribute
end

to update-world
  set repo_size (repo_size + contrib_size)
  
  if (qual * max-pxcor) > max-pxcor [ set qual 1.0 ]
  if (quan * max-pycor) > max-pycor [ set quan 1.0 ]
  if (engag * 255) > 255 [ set engag 1.0 ]
  if (qual * max-pxcor) < min-pxcor [ set qual 0.0 ]
  if (quan * max-pycor) < min-pycor [ set quan 0.0 ]
  if (engag * 255) < 0 [ set engag 0.0 ]

  setxy (qual * max-pxcor) (quan * max-pycor)

  set shape "person"
  ifelse role = "admin" [ set color (list (engag * 255) 0 0) ]
    [ ifelse role = "dev" [ set color (list 0 (engag * 255) 0) ]
    [ set color (list 0 0 (engag * 255)) ] ]

end
