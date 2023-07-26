:-dynamic(score_list/1).
:-dynamic(multiplier/1).
:-dynamic(tot_score/1).
:-dynamic(mult_score/1).
:-dynamic(final_score/1). 

runquestions :- questions, prognosis.

questions:-
    %modify_element(Index, NewElement), 
    initial_prompt, 
    question1,
    question2,
    question3,
    question4,
    question5,
    question6,
    question7,
    question8,
    question9,
    question10,
    question11,
    question12,
    question13,
    question14,
    question15.

prognosis:-
    score,
    question16,
    question17,
    question18,
    multiplier_score,
    multiply_scores,
    diagnosis.  

score_list([a,b,c,d,e,f,g,h,i,j,k,l,m,n,o]).

% Recursive rule to modify items in a list:
modify_element(Index, NewValue) :-
    score_list(List),
    nth0(Index, List, _, Rest),
    nth0(Index, NewList, NewValue, Rest),
    retractall(score_list(_)),
    asserta(score_list(NewList)),
    !.

% Write command to screen: 
initial_prompt :- write('Reply to all questions with a y. or n. (yes or no)'), nl, nl. 
     

% Environment question - weight of 5, or 1 for no contact: 
question1:-
    write('Have you been in contact with an infected person during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(0,5);
            modify_element(0,1)).

% Fever question - weight of 1: 
question2:-
    write('Have you been suffering with a fever during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(1,1);
            modify_element(1,0)).

% Dry Cough question - weight of 1: 
question3:-
    write('Have you had a persistant dry cough during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(2,1);
            modify_element(2,0)).

% Tired question - weight of 1: 
question4:-
    write('Have you been feeling more tired than usual during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(3,1);
            modify_element(3,0)).

% Aches and pains question - weight of 1:  
question5:-
    write('Have you been suffering with aches and pains during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(4,1);
            modify_element(4,0)).

% Sore throat question - weight of 1: 
question6:-
    write('Have you been suffering with a sore throat during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(5,1);
            modify_element(5,0)).

% Diarrhoea question - weight of 1: 
question7:-
    write('Have you been suffering with diarrhoea during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(6,1);
            modify_element(6,0)).

% Conjunctivitis question - weight of 1: 
question8:-
    write('Have you been suffering with conjunctivitis during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(7,1);
            modify_element(7,0)).

% Headache question - weight of 1: 
question9:-
    write('Have you been suffering with a persistant headache during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(8,1);
            modify_element(8,0)).

% Smell/taste question - weight of 1: 
question10:-
    write('Have you been suffering with a partial/total loss of taste and/or smell during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(9,1);
            modify_element(9,0)).

% Running nose question - weight of 1: 
question11:-
    write('Have you been suffering with a persistant running nose during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(10,1);
            modify_element(10,0)).
    
% Breathing question - weight of 20: 
question12:-
    write('Have you had a difficulty in breathing or shortness of breathe during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(11,12);
            modify_element(11,0)).

% Chest pain question - weight of 20: 
question13:-
    write('Have you been suffering with chest pain or chest pressure during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(12,12);
            modify_element(12,0)).

% Chest pain question - weight of 20: 
question14:-
    write('Have you suffered from a loss of speech during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(13,12);
            modify_element(13,0)).

% Headache question - weight of 20: 
question15:-
    write('Have you suffering from a loss of movement during the past 5 days?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            modify_element(14,12);
            modify_element(14,0)).

% Recursive rule to sum all the elements in the score list:
sum_list([], 0).
sum_list([Head|Tail],Sum) :-
    sum_list(Tail,TailSum),  
    Sum is Head + TailSum.   

%Calculate the total score using the sum_list rule:
score:-
    score_list(List), 
    sum_list(List,Total_score),
    write(Total_score),
    retractall(tot_score(_)),assertz(tot_score(Total_score)),
    nl. 


% Male or Female question - multiplier of 11: 
question16:-
    write('Would you classify yourself as male?'),
        nl,
        read(Reply),
        (Reply = y
             ->
            retractall(multiplier(_)), assertz(multiplier(11));
            retractall(multiplier(_)), assertz(multiplier(10))).

% Age question - multiplier of 19: 
question17:-
    write('Are you 70 years old or older?'),
        nl,
        read(Reply),
        (Reply = y
             ->
             assertz(multiplier(49));
             assertz(multiplier(10))).

% Health conditions question - multiplier of 20: 
question18:-
    write('Do you have pre-existent health conditions (e.g. hypertension, diabetes, cardiovascular disease, chronic respiratory disease and cancer) ?'),
        nl,
        read(Reply),
        (Reply = y
             ->
             assertz(multiplier(50));
             assertz(multiplier(10))).

% Use rule sum_list to add the multipliers together:
sum_multipliers(Multipliers_Sum) :-
    findall(N, multiplier(N), Multipliers),
    sum_list(Multipliers, Multipliers_Sum).
% Calculate the multipler sum - should give a score between 30 and 110:
multiplier_score:- 
    sum_multipliers(Multipliers_Sum),
    write(Multipliers_Sum),
    retractall(mult_score(_)),
    assertz(mult_score(Multipliers_Sum)),
    nl. 

% A rule that multiplies the question score and the Multiplier:
factor(X, Y, Product):-
    Product is X * Y,
    write(Product).

% Calculate the final score as the product of tot_score and mult_score:
multiply_scores :-
    findall(M, tot_score(M), X),
    findall(N, mult_score(N), Y),
    factor(X, Y, Product),
    retractall(final_score(_)),
    assertz(final_score(Product)),
    nl.

% The final score should be between 30 and  - use this to give advice to the patient:
diagnosis:-
    findall(M, final_score(M), Final),
    Final >= 750 -> write('You are in a high risk category with symptoms, you should seek immediate medical help');
    findall(M, final_score(M), Final),
    Final >= 414, Final < 749 -> write('You have some serious symptoms and should contact your medic (online or phone) for support');
    findall(M, final_score(M), Final),
    Final >= 300, Final < 414 -> write('You have a lot of symptoms and should isolate at home for the next 14 days');
    findall(M, final_score(M), Final),
    Final >= 180, Final < 300-> write('You have a number of symptoms and should isolate at home for the next 14 days');
    findall(M, final_score(M), Final),
    Final >= 0, Final < 180 -> write('You seem to be fine!').
    


