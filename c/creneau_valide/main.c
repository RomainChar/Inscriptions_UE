/**
 * @file main.c
 * @author Charrondiere Romain et Cousaert Flavien
 * @brief Fonction de vérifiant la compatibilité de deux créneaux
 * @version 1
 *
 * @copyright Copyright (c) 2021
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define bool unsigned int
#define true 1
#define false 0


/** @brief Vérification de la compatibilité de deux créneaux.
 *
 * @param[in] Jour1 Le numero du jour de la semaine du premier créneau.
 * @param[in] HeureD1 L'heure de début du premier créneau.
 * @param[in] HeureF1 L'heure de fin du premier créneau.
 * @param[in] Semaine1 La semaine du premier créneau.
 * @param[in] Jour2 Le numero du jour de la semaine du second créneau.
 * @param[in] HeureD2 L'heure de début du second créneau.
 * @param[in] HeureF2 L'heure de fin du second créneau.
 * @param[in] Semaine2 La semaine du second créneau.
 * @return Un bool vrai si les créneaux sont compatibles, faux sinon.
 */

bool CompatibiliteCreneaux(char Jour1, wchar_t* HeureD1, wchar_t* HeureF1, char Semaine1, char Jour2, wchar_t* HeureD2, wchar_t* HeureF2, char Semaine2) {
    char HeureD1str[5] =  {HeureD1[0], HeureD1[1], HeureD1[2], HeureD1[3], HeureD1[4] };
    char HeureF1str[5] =  {HeureF1[0], HeureF1[1], HeureF1[2], HeureF1[3], HeureF1[4] };
    char HeureD2str[5] =  {HeureD2[0], HeureD2[1], HeureD2[2], HeureD2[3], HeureD2[4] };
    char HeureF2str[5] =  {HeureF2[0], HeureF2[1], HeureF2[2], HeureF2[3], HeureF2[4] };
    if (Jour1 != Jour2) {
        return true;
    }
    else if ((Semaine1 == 'A' && Semaine2 == 'B') || (Semaine1 == 'B' && Semaine2 == 'A')) {
        return true;
    }
    else if ((strcmp(HeureF1str,HeureD2str) <= 0) || (strcmp(HeureF2str,HeureD1str) <= 0) ){
        return true;
    }
    else {
        return false;
    }
};

/** @brief Test de la fonction CompatibiliteCreneaux(char Jour1, char* HeureD1, char* HeureF1, char Semaine1, char Jour2, char* HeureD2, char* HeureF2, char Semaine2).
 */


