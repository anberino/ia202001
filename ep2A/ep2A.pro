%%%%% Insira aqui os seus predicados.
%%%%% Use quantos predicados auxiliares julgar necess�rio

%Gabriel Sarti Massukado - NUSP 10284177

%funcao de verdade - lista_para_conjunto
lista_para_conjunto(L, Conjunto) :-
    ver_membro(L, [], Reverso),
    reverse(Reverso, Conjunto).

%funcoes auxiliares
ver_membro([], Conjunto, Conjunto).

ver_membro([L|Lt], Cs, Conjunto) :-
    member(L, Cs),
    ver_membro(Lt, Cs, Conjunto).

ver_membro([L|Lt], Cs, Conjunto) :-
    not(member(L, Cs)),
    ver_membro(Lt, [L|Cs], Conjunto).

%funcao de verdade - mesmo_conjunto
mesmo_conjunto(Conjunto1, Conjunto2) :-
    permutar(Conjunto1, Conjunto2).

%funcoes auxiliares
remover(X, [X|Y], Y).
remover(X, [Y|Z], [Y|W]) :-
    remover(X, Z, W).

permutar([], []).

permutar(A, [B|Bt]) :-
    remover(B, A, Tmp),
    permutar(Tmp, Bt).

%funcao de verdade - uniao de conjuntos
uniao_conjunto(A, B, Uni) :-
    append(A, B, Tmp),
    lista_para_conjunto(Tmp, Uni).

%funcao de verdade - interseccao de conjuntos
inter_conjunto(A, B, Int) :-
    varrer(A, B, [], Rev),
    reverse(Rev, Int).

%funcoes auxiliares
varrer([], _, Tmp, Tmp).

varrer([A|At], B, Tmp, Int) :-
    member(A, B),
    varrer(At, B, [A|Tmp], Int).

varrer([A|At], B, Tmp, Int) :-
    not(member(A, B)),
    varrer(At, B, Tmp, Int).

%funcao de verdade - diferenca de conjunto
diferenca_conjunto(A, B, Dif) :-
    diferenciar(A, B, [], Rev),
    reverse(Rev, Dif).

%funcoes auxiliares
diferenciar([], _, Tmp, Tmp).

diferenciar([A|At], B, Tmp, Dif) :-
    not(member(A, B)),
    diferenciar(At, B, [A|Tmp], Dif).

diferenciar([A|At], B, Tmp, Dif) :-
    member(A, B),
    diferenciar(At, B, Tmp, Dif).

%%%%%%%% Fim dos predicados adicionados
%%%%%%%% Os testes come�am aqui.
%%%%%%%% Para executar os testes, use a consulta:   ?- run_tests.

%%%%%%%% Mais informacoes sobre testes podem ser encontradas em:
%%%%%%%%    https://www.swi-prolog.org/pldoc/package/plunit.html

:- begin_tests(conjuntos).
test(lista_para_conjunto, all(Xs=[[1,a,3,4]]) ) :-
    lista_para_conjunto([1,a,3,3,a,1,4], Xs).
test(lista_para_conjunto2,fail) :-
    lista_para_conjunto([1,a,3,3,a,1,4], [a,1,3,4]).

test(mesmo_conjunto, set(Xs=[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    mesmo_conjunto([1,a,3], Xs).
test(uniao_conjunto2,fail) :-
    mesmo_conjunto([1,a,3,4], [1,3,4]).

test(uniao_conjunto, set(Ys==[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    uniao_conjunto([1,a], [a,3], Xs),
    mesmo_conjunto(Xs,Ys).
test(uniao_conjunto2,fail) :-
    uniao_conjunto([1,a,3,4], [1,2,3,4], [1,1,a,2,3,3,4,4]).

test(inter_conjunto, all(Xs==[[1,3,4]])) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], Xs).
test(inter_conjunto2,fail) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], [1,1,3,3,4,4]).

test(diferenca_conjunto, all(Xs==[[2]])) :-
    diferenca_conjunto([1,2,3], [3,a,1], Xs).
test(diferenca_conjunto2,fail) :-
    diferenca_conjunto([1,3,4], [1,2,3,4], [_|_]).

:- end_tests(conjuntos).
