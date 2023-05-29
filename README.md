Ce programme, réalisé début 2021, permet de de gérer un catalogue d'UE (Unité d'Enseignement) et d'inscrire des étudiants à ces mêmes UEs.

Le programme a été développé en Python principalement avec l'appel d'une fonction C permettant de valider la compatibilité entre 2 créneaux. L'objectif était de créer un catalogue vérifiant les erreurs de saisies de l'utilisateur : horaires invalides, créneaux se chevauchant, effectifs maximum, etc...
L'ensemble du programme est documenté avec le logiciel Doxygen.

Plusieurs UE et étudiants sont déjà crés dans les fichiers liseetus.json et listeUEs.json

Fonctionnalités :

- ajouter une UE au catalogue (code, nom, description, effectifs, créneaux (Type, jour, Heure de début, Heure de fin, Semaine))
- supprimer une UE
- modifier une UE
- valider le catalogue (puis passer à l'inscription des étudiants)

- inscrire un étudiant dans une UE
- modifier les choix d'UE
- visualiser les UE disponibles
