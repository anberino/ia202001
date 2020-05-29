takeout(A,[A|B],B).
takeout(A,[B|C],[B|D]) :-
          takeout(A,C,D).

%método auxiliar baseado em um tutorial de prolog
remove(X, [X|Y], Y).
remove(X, [Y|Z], [Y|W]) :-
    remove(X, Z, W).

limpar([], []).

limpar([], _) :-
    false.

limpar(_, []) :-
    false.

limpar([A|At], B) :-
    remove(A, [A|At], NovoA),
    remove(A, B, NovoB),
    limpar(NovoA, NovoB).
