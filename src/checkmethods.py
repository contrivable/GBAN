#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Convention:
# * check method has no input parameteer weights until it is called from
#   another check method or it doesn't call another method
# TODO:
# * check: do name named parameters, esp. debug=debug
# * check: it's "checkDigit", not "checkDigits"
# * check: check_XY uses debug "alert('check_XY::[..]"
# * check: check_XY uses "check_XY:: START:" and "check_XY:: RESULT:"
# * find real account numbers for each check method and check (unit test?)

# LAST 20131027

import sys
import re

def alert(msg):
    sys.stderr.write(msg+'\n')
def report(msg):
    sys.stdout.write(msg+'\n')

"""Modulus 10, Gewichtung 2, 1, 2, 1, 2, 1, 2, 1, 2
Die Stellen der Kontonummer sind von rechts nach links mit
den Ziffern 2, 1, 2, 1, 2 usw. zu multiplizieren. Die jeweiligen
Produkte werden addiert, nachdem jeweils aus den
zweistelligen Produkten die Quersumme gebildet wurde (z. B.
Produkt 16 = Quersumme 7). Nach der Addition bleiben
außer der Einerstelle alle anderen Stellen unberücksichtigt.
Die Einerstelle wird von dem Wert 10 subtrahiert. Das
Ergebnis ist die Prüfziffer (10. Stelle der Kontonummer).
Ergibt sich nach der Subtraktion der Rest 10, ist die
Prüfziffer 0.
Testkontonummern: 9290701, 539290858
1501824, 1501832"""
def check_00(accountno,weights=[2,1],debug=False):
    if debug: alert('check_00:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    if len(accountno)!=10:
        if debug: alert('check_00:: RESULT: False - accountno of length not 10')
        return False
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno)[-1])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    inter = [weighing(digits,weights,post=cross_sum,debug=debug)]
    inter.append(inter[-1] % 10)
    inter.append(10 - inter[-1])
    inter.append(inter[-1] % 10) # This gives 0 if inter[2]==10.
    if debug:
        alert('weight:\tx%10:\t10-x:\tx%10:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_00:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 10, Gewichtung 3, 7, 1, 3, 7, 1, 3, 7, 1
Die Stellen der Kontonummer sind von rechts nach links mit
den Ziffern 3, 7, 1, 3, 7, 1 usw. zu multiplizieren. Die
jeweiligen Produkte werden addiert. Nach der Addition
bleiben au(ss)er der Einerstelle alle anderen Stellen
unberücksichtigt. Die Einerstelle wird von dem Wert 10
subtrahiert. Das Ergebnis ist die Prüfziffer (10. Stelle der
Kontonummer). Ergibt sich nach der Subtraktion der Rest 10,
ist die Prüfziffer 0."""
def check_01(accountno,weights=[3,7,1],debug=False):
    if debug: alert('check_01:: START\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    if len(accountno)!=10:
        if debug: alert('check_01:: RESULT: False - accountno of length not 10')
        return False
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno)[-1])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    inter = [weighing(digits,weights,post=None,debug=debug)]
    inter.append(inter[-1] % 10)
    inter.append(10 - inter[-1])
    inter.append(inter[-1] % 10) # This gives 0 if inter[2]==10.
    if debug:
        alert('weight:\tx%10:\t10-x:\tx%10:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_01:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8, 9, 2
Die Stellen der Kontonummer sind von rechts nach links mit
den Ziffern 2, 3, 4, 5, 6, 7, 8, 9, 2 zu multiplizieren. Die
jeweiligen Produkte werden addiert. Die Summe ist durch 11
zu dividieren. Der verbleibende Rest wird vom Divisor (11)
subtrahiert. Das Ergebnis ist die Prüfziffer. Verbleibt nach der
Division durch 11 kein Rest, ist die Prüfziffer 0. Ergibt sich als
Rest 1, ist die Prüfziffer zweistellig und kann nicht verwendet
werden. Die Kontonummer ist dann nicht verwendbar."""
def check_02(accountno,weights=[2,3,4,5,6,7,8,9,2],debug=False):
    if debug: alert('check_02:: START\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno)[-1])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    inter = [weighing(digits,weights,post=None,debug=debug)]
    inter.append(inter[-1] % 11)
    if inter[-1]==1:
        if debug:
            alert('weight:\tx%11:\n'+'\t'.join([str(n) for n in inter]))
            alert('check_02:: RESULT: False - intermediate remainder = 1')
        return False
    inter.append(11 - inter[-1])
    inter.append(inter[-1] % 11) # This gives 0 if inter[2]==11.
    if debug:
        alert('weight:\tx%11:\t11-x:\tx%11:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_02:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 10, Gewichtung 2, 1, 2, 1, 2, 1, 2, 1, 2
Die Berechnung erfolgt wie bei Verfahren 01."""
def check_03(accountno,debug=False):
    if debug: alert('check_03:: START:\taccountno: '+str(accountno))
    result = check_01(accountno,weights=[2,1],debug=debug)
    if debug: alert('check_03:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 2, 3, 4
Die Berechnung erfolgt wie bei Verfahren 02."""
def check_04(accountno,debug=False):
    if debug: alert('check_04:: START:\taccountno: '+str(accountno))
    result = check_02(accountno,weights=[2,3,4,5,6,7],debug=debug)
    if debug: alert('check_04:: RESULT: '+str(result))
    return result

"""Modulus 10, Gewichtung 7, 3, 1, 7, 3, 1, 7, 3, 1
Die Berechnung erfolgt wie bei Verfahren 01."""
def check_05(accountno,debug=False):
    if debug: alert('check_05:: START:\taccountno: '+str(accountno))
    result = check_01(accountno,weights=[7,3,1],debug=debug)
    if debug: alert('check_05:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7 (modifiziert)
Die einzelnen Stellen der Kontonummer sind von rechts nach
links mit den Ziffern 2, 3, 4, 5, 6, 7, 2, 3 ff. zu multiplizieren.
Die jeweiligen Produkte werden addiert. Die Summe ist durch
11 zu dividieren. Der verbleibende Rest wird vom Divisor (11)
subtrahiert. Das Ergebnis ist die Prüfziffer. Ergibt sich als
Rest 1, findet von dem Rechenergebnis 10 nur die Einerstelle
(0) als Prüfziffer Verwendung. Verbleibt nach der Division
durch 11 kein Rest, dann ist auch die Prüfziffer 0. Die
Stelle 10 der Kontonummer ist die Prüfziffer.
Testkontonummern: 94012341, 5073321010"""
def check_06(accountno,weights=[2,3,4,5,6,7],debug=False):
    if debug: alert('check_06:: START:\taccountno: '+str(accountno)+'\tweights: '+str(weights))
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno)[-1])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    inter = [weighing(digits,weights,post=None,debug=debug)]
    inter.append(inter[-1] % 11)
    inter.append(11 - inter[-1])
    inter.append(inter[-1] % 11) # This gives 0 if inter[2]==11.
    inter.append(inter[-1] % 10) # This gives 0 if inter[2]==10.
    if debug:
        alert('weight:\tx%11:\t11-x:\tx%11:\tx%10:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_06:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8, 9, 10
Die Berechnung erfolgt wie bei Verfahren 02."""
def check_07(accountno,debug=False):
    if debug: alert('check_07:: START:\taccountno: '+str(accountno))
    result = check_02(accountno,weights=[2,3,4,5,6,7,8,9,10],debug=debug)
    if debug: alert('check_07:: RESULT: '+str(result))
    return result

"""Modulus 10, Gewichtung 2, 1, 2, 1, 2, 1, 2, 1, 2 (modifiziert)
Die Berechnung erfolgt wie bei Verfahren 00, jedoch erst ab
der Kontonummer 60 000."""
def check_08(accountno,debug=False):
    if debug: alert('check_08:: START:\taccountno: '+str(accountno))
    if long(accountno)>=60000:
        result = check_00(accountno,debug=debug)
    else:
        result = False
    if debug: alert('check_08:: RESULT: '+str(result))
    return result

"""Keine Prüfzifferberechnung"""
def check_09(accountno,debug=False):
    if debug: alert('check_09:: START:\taccountno: '+str(accountno)+
        '\ncheck_09:: RESULT: True')
    return True

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8, 9, 10 (modifiziert)
Die Berechnung erfolgt wie bei Verfahren 06.
Testkontonummern: 12345008, 87654008"""
def check_10(accountno,debug=False):
    if debug: alert('check_10:: START:\taccountno: '+str(accountno))
    result = check_06(accountno,weights=[2,3,4,5,6,7,8,9,10],debug=debug)
    if debug: alert('check_10:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8, 9, 10 (modifiziert)
Die Berechnung erfolgt wie bei Verfahren 06. Beim
Rechenergebnis 10 wird die Null jedoch durch eine 9 ersetzt."""
def check_11(accountno,weights=[2,3,4,5,6,7,8,9,10],debug=False):
    if debug: alert('check_11:: START:\naccountno: '+str(accountno)+'\tweights: '+str(weights))
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno)[-1])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    inter = [weighing(digits,weights,post=None,debug=debug)]
    inter.append(inter[-1] % 11)
    inter.append(11 - inter[-1])
    inter.append(inter[-1] % 11) # This gives 0 if inter[2]==11.
    inter.append(inter[-1] if inter[3]<10 else 9) # This gives 9 if inter[2]==10.
    if debug:
        alert('weight:\tx%11:\t11-x:\tx%11:\tx%10:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_11:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""12: frei"""

"""Modulus 10, Gewichtung 2, 1, 2, 1, 2, 1
Die Berechnung erfolgt wie bei Verfahren 00. Die für die
Berechnung relevante sechsstellige Grundnummer befindet
sich in den Stellen 2 bis 7, die Prüfziffer in Stelle 8 (von links
nach rechts gezählt). Die zweistellige Unterkontonummer
(Stellen 9 und 10) darf nicht in das Prüfzifferberechnungs-
verfahren einbezogen werden. Ist die Unterkontonummer
"00", kommt es vor, dass sie nicht angegeben ist. Ergibt die
erste Berechnung einen Prüfzifferfehler, wird empfohlen, die
Prüfzifferberechnung ein zweites Mal durchzuführen und
dabei die "gedachte" Unterkontonummer 00 an die Stellen 9
und 10 zu setzen und die vorhandene Kontonummer vorher
um zwei Stellen nach links zu verschieben."""
def check_13(accountno,weights=[2,1],debug=False):
    if debug: alert('check_13:: START:\naccountno:\t'+str(accountno)+'\tweights: '+str(weights))
    if len(accountno) not in [8,10]:
        if debug: alert('check_00:: RESULT: False - accountno of length not 8 and not 10')
        return False
    digits = accountno[1:7][::-1]
    checkDigit = int(str(accountno)[7])
    if len(accountno)==10:
        subaccount = accountno[8:10]
    else:
        subaccount = '00'
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit)+'\tsubaccount:\t'+subaccount)
    result = check_00('0'*3+accountno[1:8],debug=debug)
    if debug: alert('check_13:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7
Die Berechnung erfolgt wie bei Verfahren 02. Es ist jedoch zu
beachten, dass die zweistellige Kontoart nicht in das
Prüfzifferberechnungsverfahren mit einbezogen wird. Die
Kontoart belegt die Stellen 2 und 3, die zu berechnende
Grundnummer die Stellen 4 bis 9. Die Prüfziffer befindet sich
in Stelle 10. """
def check_14(accountno,debug=False):
    if debug: alert('check_14:: START:\naccountno:\t'+str(accountno))
    if len(accountno) not in [10]:
        if debug: alert('check_14:: RESULT: False - accountno of length not 10')
        return False
    accountType = accountno[1:3]
    digits = accountno[3:9][::-1]
    checkDigit = int(str(accountno)[9])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit)+'\taccount type:\t'+accountType)
    result = check_02('0'*3+accountno[3:10],weights=[2,3,4,5,6,7],debug=debug)
    if debug: alert('check_14:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5
Die Kontonummer ist 10-stellig. Die Berechnung erfolgt wie
bei Verfahren 06; es ist jedoch zu beachten, dass nur die
Stellen 6 bis 9 in das Prüfzifferberechnungsverfahren
einbezogen werden. Die Stelle 10 der Kontonummer ist die
Prüfziffer. """
def check_15(accountno,debug=False):
    if debug: alert('check_15:: START:\naccountno:\t'+str(accountno))
    if len(accountno) not in [10]:
        if debug: alert('check_15:: RESULT: False - accountno of length not 10')
        return False
    digits = accountno[5:9][::-1]
    checkDigit = int(str(accountno)[9])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    result = check_06('0'*5+accountno[5:10],weights=[2,3,4,5],debug=debug)
    if debug: alert('check_15:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 2, 3, 4
Die Berechnung erfolgt wie bei Verfahren 06. Sollte sich
jedoch nach der Division der Rest 1 ergeben, so ist die
Kontonummer unabhängig vom eigentlichen Berechnungs-
ergebnis richtig, wenn die Ziffern an 10. und 9. Stelle
identisch sind."""
def check_16(accountno,weights=[2,3,4,5,6,7],debug=False):      # same weights as 06
    if debug: alert('check_16:: START:\naccountno:\n'+str(accountno)+'\tweights: '+str(weights))
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno)[-1])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    inter = [weighing(digits,weights,post=None,debug=debug)]
    inter.append(inter[-1] % 11)
    if inter[-1]==1:
        if debug: alert('weight:\tx%11:\n'+'\t'.join([str(n) for n in inter]))
        result = accountno[8] == accountno[9]
        if debug: alert('check_16:: RESULT: '+str(result)+'\tintermediate remainder = 1, pos9: '+str(accountno[8])+'\tpos10: '+str(accountno[9]))
        return result
    inter.append(11 - inter[-1])
    inter.append(inter[-1] % 11) # This gives 0 if inter[2]==11.
    if debug: alert('weight:\tx%11:\t11-x:\tx%11:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_16:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 11, Gewichtung 1, 2, 1, 2, 1, 2
Die Kontonummer ist 10-stellig mit folgendem Aufbau;
KSSSSSSPUU
K = Kontoartziffer
S = Stammnummer
P = Prüfziffer
U = Unterkontonummer
Die für die Berechnung relevante 6-stellige Stammnummer
(Kundennummer) befindet sich in den Stellen 2 bis 7 der
Kontonummer, die Prüfziffer in der Stelle 8. Die einzelnen
Stellen der Stammnummer (S) sind von links nach rechts mit
den Ziffern 1, 2, 1, 2, 1, 2 zu multiplizieren. Die jeweiligen
Produkte sind zu addieren, nachdem aus eventuell
zweistelligen Produkten der 2., 4. und 6. Stelle der
Stammnummer die Quersumme gebildet wurde. Von der
Summe ist der Wert "1" zu subtrahieren. Das Ergebnis ist
dann durch 11 zu dividieren. Der verbleibende Rest wird von
10 subtrahiert. Das Ergebnis ist die Prüfziffer. Verbleibt nach
der Division durch 11 kein Rest, ist die Prüfziffer 0. 
Beispiel:
Stellennr.:  K S S S S S S P U U
Kontonummer: 0 4 4 6 7 8 6 0 4 0
Gewichtung:    1 2 1 2 1 2
               4+8+6+5+8+3 = 34
                     Q   Q
Q = Quersumme nur der jeweiligen Stellen lt. Beschreibung
34 - 1 = 33
33 : 11 = 3, Rest 0
0 = Prüfziffer
Testkontonummer: 0446786040"""
def check_17(accountno,weights=[1,2],debug=False):
    if debug: alert('check_17:: START:\naccountno:\t'+str(accountno)+'\tweights: '+str(weights))
    if len(accountno) not in [10]:
        if debug: alert('check_17:: RESULT: False - accountno of length not 10')
        return False
    accountType = accountno[0]
    digits = accountno[1:7]
    checkDigit = int(accountno[7])
    subaccount = accountno[8:10]
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit)+'\tsubaccount: '+str(subaccount)+'\taccount type: '+str(accountType))
    inter = [weighing(digits,weights,post=cross_sum,debug=debug)]
    inter.append(inter[-1] - 1 )
    inter.append(inter[-1] % 11)
    inter.append(10 - inter[-1])
    inter.append(inter[-1] % 10) # This gives 0 if inter[2]==0.
    if debug: alert('weight:\tx-1\tx%11:\t10-x:\tx%10:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_17:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 10, Gewichtung 3, 9, 7, 1, 3, 9, 7, 1, 3
Die Berechnung erfolgt wie bei Verfahren 01."""
def check_18(accountno,debug=False):
    if debug: alert('check_18:: START:\naccountno:\t'+str(accountno))
    result = check_01(accountno,weights=[3,9,7,1],debug=debug)
    if debug: alert('check_18:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8, 9, 1
Die Berechnung und mögliche Ergebnisse entsprechen dem
Verfahren 06.
Testkontonummern: 0240334000, 0200520016"""
def check_19(accountno,debug=False):
    if debug: alert('check_19:: START:\naccountno:\t'+str(accountno))
    result = check_06(accountno,weights=[2,3,4,5,6,7,8,9,1],debug=debug)
    if debug: alert('check_19:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8, 9, 3 (modifiziert)
Die Berechnung und mögliche Ergebnisse entsprechen dem
Verfahren 06."""
def check_20(accountno,debug=False):
    if debug: alert('check_20:: START:\taccountno: '+str(accountno))
    result = check_06(accountno,weights=[2,3,4,5,6,7,8,9,3],debug=debug)
    if debug: alert('check_20:: RESULT: '+str(result))
    return result

"""Modulus 10, Gewichtung 2, 1, 2, 1, 2, 1, 2, 1, 2 (modifiziert)
Die Berechnung erfolgt wie bei Verfahren 00. Nach der
Addition der Produkte werden neben der Einerstelle jedoch
alle Stellen berücksichtigt, indem solange Quersummen
gebildet werden, bis ein einstelliger Wert verbleibt. Die
Differenz zwischen diesem Wert und dem Wert 10 ist die
Prüfziffer."""
def check_21(accountno,weights=[2,1],debug=False):    # 
    if debug: alert('check_21:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    if len(accountno)!=10:
        if debug: alert('check_21:: RESULT: False - accountno of length not 10')
        return False
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno)[-1])
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    inter = [weighing(digits,weights,post=cross_sum,debug=debug)]
    inter.append(inter[-1])
    while inter[-1]>9:
        inter[-1] = cross_sum( inter[-1] )
    inter.append(10 - inter[-1])
    if debug:
        alert('weight:\tcross:\t10-x:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_21:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 10, Gewichtung 3, 1, 3, 1, 3, 1, 3, 1, 3
Die einzelnen Stellen der Kontonummer sind von rechts nach
links mit den Ziffern 3, 1, 3, 1 usw. zu multiplizieren. Von den
jeweiligen Produkten bleiben die Zehnerstellen
unberücksichtigt. Die verbleibenden Zahlen (Einerstellen)
werden addiert. Die Differenz bis zum nächsten Zehner ist
die Prüfziffer."""
def check_22(accountno,weights=[3,1],debug=False):    # 
    if debug: alert('check_22:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno[-1]))
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    inter = [weighing(digits,weights,post=None,debug=debug)]
    inter.append(inter[-1]%10)
    inter.append(10-inter[-1])
    if debug:
        alert('weight:\tx%10:\t10-x:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_22:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7
Das Berechnungsverfahren entspricht dem des
Kennzeichens 16, wird jedoch nur auf die ersten sechs
Ziffern der Kontonummer angewandt.
Die Prüfziffer befindet sich an der 7. Stelle der Kontonummer.
Die Stellen 8 bis 10 bleiben ungeprüft.
Stellennr.:   1 2 3 4 5 6 7 8 9 10
Kontonummer:  x x x x x x P x x x
Gewichtung:   7 6 5 4 3 2
Summe geteilt durch 11 = x, Rest
Rest = 0 Prüfziffer = 0
Rest = 1 Prüfziffer = 6. und 7. Stelle
der
Kontonummer müssen
identisch sein
Rest = 2 bis 10 Prüfziffer = 11 minus Rest
[geändert zum 2001-09-03]"""
def check_23(accountno,weights=[2,3,4,5,6,7],debug=False):    # same weights as 16 and 06
    if debug: alert('check_23:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    digits = accountno[:6][::-1]
    checkDigit = int(str(accountno[6]))
    workingno = accountno[7:]
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit)+'\tunused: '+str(workingno))
    result = check_16('0'*3+digits+str(checkDigit),weights=weights,debug=debug)
    if debug: alert('check_23:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 1, 2, 3, 1, 2, 3, 1, 2, 3
Die für die Berechnung relevanten Stellen der Kontonummer
befinden sich - von links nach rechts gelesen - in den Stellen
1 - 9; die Prüfziffer in Stelle 10. Die Kontonummer ist
rechtsbündig zu interpretieren und ggf. mit Nullen aufzufüllen.
Die einzelnen Ziffern der Kontonummer sind, beginnend mit
der ersten Ziffer ungleich 0, von links nach rechts bis
einschließlich Stelle 9 mit den o. g. Gewichtungsfaktoren zu
multiplizieren. Zum jeweiligen Produkt ist der zugehörige
Gewichtungsfaktor zu addieren (zum ersten Produkt +1, zum
zweiten +2, zum dritten +3, zum Vierten +1 usw.). Das
jeweilige Ergebnis ist durch 11 zu dividieren (5 : 11 = 0 Rest
5). Die sich aus der Division ergebenden Reste sind zu
summieren. Die letzte Ziffer dieser Summe ist die Prüfziffer.
Ausnahmen:
1) Eine ggf. in Stelle 1 vorhandene Ziffer 3, 4, 5 oder 6 wird
als 0 gewertet. Der o. g. Prüfalgorithmus greift erst ab der
ersten Stelle ungleich 0.
2) Eine ggf. in Stelle 1 vorhandene Ziffer 9 wird als 0
gewertet und führt dazu, dass auch die beiden
nachfolgenden Ziffern in den Stellen 2 und 3 der
Kontonummer als 0 gewertet werden müssen. Der o. g.
Prüfalgorithmus greift in diesem Fall also erst ab Stelle 4
der 10stelligen Kontonummer. Die Stelle 4 ist ungleich 0.
Beispiele:
Stellennr.: 1 2 3 4 5 6 7  8 9 10
Kontonr.:           1 3 8  3 0  1
Ktonr.      0 0 0 0 1 3 8  3 0
umgesetzt:
Gewichtung: ________1 2 3  1 2_
                    1 6 24 3 0
Gewich-     ________1 2 3  1 2_
tungsfaktor         2+8+27+4+2=21
                        11      1 = Prüfziffer
                        R5
Stellennr.: 1 2 3 4 5 6 7  8 9 10
Kontonr.:   1 3 0 6 1 1 8  6 0  5
Gewichtung:_1 2 3 1 2 3 1  2 3_
            1 6 0 6 2 3 8 12 0
Gewich-    _1 2 3 1 2 3 1  2 3_
tungsfaktor 2+8+3+7+4+6+9+14+3=45
                          11    5 = Prüfziffer
                          R3
Stellennr.: 1 2 3 4  5 6 7  8 9 10
Kontonr.:   3 3 0 7  1 1 8  6 0 8
Ktonr.      0 3 0 7  1 1 8  6 0
umgesetzt:
Gewichtung:___1 2 3  1 2 3  1 2_
              3 0 21 1 2 24 6 0
Gewich-    ___1 2 3  1 2 3  1 2_
tungsfaktor   4+2+24+2+4+27+7+2 = 28
                  11     11        8 = Prüfziffer
                  R2     R5
Stellennr.: 1 2 3 4  5 6 7  8 9 10
Kontonr.:   9 3 0 7  1 1 8  6 0  3
Ktonr.      0 0 0 7  1 1 8  6 0
umgesetzt:
Gewichtung:_______1  2 3 1  2 3_
                  7  2 3 8 12 0
Gewich-    _______1  2 3 1  2 3_
tungsfaktor       8 +4+6+9+14+3 = 33
                           11      3 = Prüfziffer
                           R3 """
def check_24(accountno,weights=[1,2,3],debug=False):    # 
    if debug: alert('check_24:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    accountno = '0'*(10-len(accountno))+accountno
    digits = accountno[:9]
    if digits[0] in ['3','4','5','6']:
        digits[0]='0'
    if digits[0]=='9':
        digits[0:3]='000'
    while digits[0]:
        digits = digits[1:]
    checkDigit = int(str(accountno[-1]))
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    if debug:
        report('hand:\tpos:\tdigit:\tweight:\tprod:')
    hand = 0
    for pos in range(len(str(digits))):
        digit = int( str(digits)[pos] )
        weight = int( weights[pos%len(weights)] )
        product = ((digit+1)*weight)%11
        alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product))
        hand += product
    inter = [hand]
    inter.append(inter[-1]%10)
    if debug:
        alert('weight:\tx%10:\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_24:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8, 9 ohne Quersumme
Die einzelnen Stellen der Kontonummer sind von rechts nach
links mit den Ziffern 2, 3, 4, 5, 6, 7, 8 und 9 zu multiplizieren.
Die jeweiligen Produkte werden addiert. Die Summe ist durch
11 zu dividieren. Der verbleibende Rest wird vom Divisor
subtrahiert. Das Ergebnis ist die Prüfziffer. Verbleibt nach der
Division durch 11 kein Rest, ist die Prüfziffer = 0. Ergibt sich als
Rest 1, so ist die Prüfziffer immer 0 und kann nur für die
Arbeitsziffern 8 und 9 verwendet werden. Die Kontonummer ist
für die Arbeitsziffern 0, 1, 2, 3, 4, 5, 6 und 7 dann nicht
verwendbar.
Die Arbeitsziffer (Geschäftsbereich oder Kontoart) befindet sich
in der 2. Stelle (von links) des 10-stelligen
Kontonummernfeldes.
Stellennr.: 1 2 3 4 5 6 7 8 9 A (A=10)
Kontonr.:   x x x x x x x x x P
Gewichtung:   9 8 7 6 5 4 3 2
Die Kontonummer ist 9-stellig, wobei die 1. Stelle die
Arbeitsziffer und die letzte Stelle die Prüfziffer ist.
Stellennr.: 1 2  3 4  5  6 7 8  9 A (A=10)
Kontonr.:     5  2 1  3  8 2 1  8 P
Gewichtung:___9  8 7  6  5 4 3  2_
             45+16+7+18+40+8+3+16 = 153
153 : 11 = 13, Rest 10
11 - 10 = 1, Prüfziffer = 1"""
def check_25(accountno,weights=[2,3,4,5,6,7,8,9],debug=False):    # 
    if debug: alert('check_25:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    workingno = accountno[1]
    digits = accountno[1:9][::-1]
    checkDigit = int(str(accountno[-1]))
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit)+'\tworking digit: '+workingno)
    inter = [weighing(digits,weights,post=None,debug=debug)]
    inter.append(inter[-1]%11)
    inter.append(11-inter[-1])
    inter.append(inter[-1]%11)  # remap remainder 0 to 0
    if debug:
        alert('weight:\tx%11:\t11-x:\tx%11\n'+'\t'.join([str(n) for n in inter]))
    if inter[-1]==10:   # remainder 1
        result = checkDigit==0 and workingno in ['8','9']
        if debug: alert('check_25:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1])+'\tworking digit: '+workingno)
    else:
        result = inter[-1]==checkDigit
        if debug: alert('check_25:: RESULT: '+str(result)+'\tcheck digit: '+str(checkDigit)+'\tcalculated: '+str(inter[-1]))
    return result

"""Modulus 11. Gewichtung 2, 3, 4, 5, 6, 7, 2
Die Kontonummer ist 10-stellig. Sind Stelle 1 und 2 mit Nullen
gefüllt ist die Kontonummer um 2 Stellen nach links zu
schieben und Stelle 9 und 10 mit Nullen zu füllen. Die
Berechnung erfolgt wie bei Verfahren 06 mit folgender
Modifizierung: für die Berechnung relevant sind die Stellen 1 -
7; die Prüfziffer steht in Stelle 8. Bei den Stellen 9 und 10
handelt es sich um eine Unterkontonummer, welche für die
Berechnung nicht berücksichtigt wird.
Testkontonummern: 0520309001, 1111118111, 0005501024"""
def check_26(accountno,weights=[2,3,4,5,6,7],debug=False):    # same weights as 06
    if debug: alert('check_26:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    if accountno[:2]=='00':
        accountno = accoutno[2:]+'00'
    digits = accountno[:7]
    checkDigit = int(str(accountno[7]))
    subaccount = accountno[8:]
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit)+'\tsubaccount: '+subaccount)
    result = check_06('00'+digits+str(checkDigit),weights=weights,debug=debug)
    if debug: alert('check_26:: RESULT: '+str(result))
    return result

"""Modulus 10, Gewichtung 2, 1, 2, 1, 2, 1, 2, 1, 2 (modifiziert)
Die Berechnung erfolgt wie bei Verfahren 00, jedoch nur für
die Kontonummern von 1 bis 999 999 999. Ab
Konto 1 000 000 000 kommt das Prüfziffernverfahren M10H
(iterierte Transformation) zum Einsatz.
Es folgt die Beschreibung der iterierten Transformation:
Die Position der einzelnen Ziffern von rechts nach links
innerhalb der Kontonummer gibt die Zeile 1 bis 4 der
Transformationstabelle noch an. Aus ihr sind die
übersetzungswerte zu summieren. Die Einerstelle wird von
10 subtrahiert. Die Differenz stellt die Prüfziffer dar.
Beispiel:
Kontonummer
284716948P (P = Prüfziffer)
143214321  (Transf.-Zeile)
Transformationstabelle:
Ziffer:  0123456789
Zeile 1: 0159374826
Zeile 2: 0176983254
Zeile 3: 0184629573
Zeile 4: 0123456789
Von rechts nach links:
Ziffer 8 wird 2 aus Transformationszeile 1
Ziffer 4 wird 9 aus Zeile 2
Ziffer 9 wird 3 aus Zeile 3
Ziffer 6 wird 6 aus Zeile 4
Ziffer 1 wird 1 aus Zeile 1
Ziffer 7 wird 2 aus Zeile 2
Ziffer 4 wird 6 aus Zeile 3
Ziffer 8 wird 8 aus Zeile 4
Ziffer 2 wird 5 aus Zeile 1
Summe 42
Die Einerstelle wird vom Wert 10 subtrahiert. Das Ergebnis
ist die Prüfziffer, in unserem Beispiel also 10 – 2 =
Prüfziffer 8, die Kontonummer lautet somit 2847169488."""
def check_27(accountno,weights=[2,1],debug=False):    # same weights as 00
    if debug: alert('check_27:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    if long(accountno) < 1000000000:    # lt 1 billion
        result = check_00(accountno,weights=weights,debug=debug)
        if debug:     alert('check_27:: RESULT: '+str(result))
        return result
    # M10H (?)
    indexes = [1,2,3,4]
    codes = {    1:[0,1,5,9,3,7,4,8,2,6],
                2:[0,1,7,6,9,8,3,2,5,4],
                3:[0,1,8,4,6,2,9,5,7,3],
                4:[0,1,2,3,4,5,6,7,8,9]}
    digits = accountno[:9][::-1]
    checkDigit = int(str(accountno[-1]))
    if debug: alert('account digits:\t'+str(digits)+'\tcheck digit: '+str(checkDigit))
    hand = 0
    if debug: alert('hand:\tpos:\tdigit:\tline:\tcode:')
    for i in range(len(str(accountno))-1):
        digit = int(digits[i])
        line = indexes[i%len(indexes)]
        code = codes[line][digit]
        if debug:     alert(str(hand)+'\t'+str(i)+'\t'+str(digit)+'\t'+str(line)+'\t'+str(code))
        hand += code
    inter = [hand]
    inter.append(inter[-1]%10)
    inter.append(10-inter[-1])
    inter.append(inter[-1]%10)  # undocumented assumed behaviour
    if debug:
        alert('weight:\tx%10:\t10-x:\tx%10\n'+'\t'.join([str(n) for n in inter]))
    result = inter[-1]==checkDigit
    if debug: alert('check_27:: RESULT: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8
Die Kontonummer ist 10-stellig. Die zweistellige
Unterkontonummer (Stellen 9 und 10) wird nicht in das
Berechnungsverfahren einbezogen. Die für die Berechnung
relevanten Stellen 1 bis 7 werden von rechts nach links mit
den Ziffern 2, 3, 4, 5, 6, 7, 8 multipliziert. Die 8. Stelle ist die
Prüfziffer. Die Berechnung und Ergebnisse entsprechen dem
Verfahren 06.
Stellennr.: 1 2 3 4 5 6 7 8 9 A (A=10)
Kontonr.:   x x x x x x x P x x
Gewichtung: 8 7 6 5 4 3 2
Wird als Rest eine 0 oder eine 1 ermittelt, so lautet die
Prüfziffer 0.
Testkontonummern: 19999000, 9130000201"""
def check_28(accountno,weights=[2,3,4,5,6,7,8],debug=False):    # 
    if debug: alert('check_28:: START:\naccountno:\t'+str(accountno)+'\tweights:\t'+str(weights))
    if len(accountno)!=10:
        if debug:     alert('check_28:: RESULT: False early out, unfit accountno')
        return False
    digits = accountno[:7][::-1]
    checkDigit = int(str(accountno[7]))
    result = check_06('00'+digits+str(checkDigit),weights=weights,debug=debug)
    if debug: alert('check_28:: RESULT: '+str(result))
    return result

"""Modulus 10, iterierte Transformation
Die einzelnen Ziffern der Kontonummer werden über eine
Tabelle in andere Werte transformiert. Jeder einzelnen Stelle
der Kontonummer ist hierzu eine der Zeilen 1 bis 4 der
Transformationstabelle fest zugeordnet. Die
Transformationswerte werden addiert. Die Einerstelle der
Summe wird von 10 subtrahiert. Das Ergebnis ist die
Prüfziffer. (Ist das Ergebnis = 10, ist die Prüfziffer = 0).
Beispiel:
Kontonummer: 3 1 4 5 8 6 3 0 2 P (P = Prüfziffer)
Die Kontonummer ist 10-stellig. Die 10. Stelle ist die
Prüfziffer.
Zugeordnete Zeile der
Transformationstabelle: 143214321
Transformationstabelle:
Ziffer:  0123456789
Zeile 1: 0159374826
Zeile 2: 0176983254
Zeile 3: 0184629573
Zeile 4: 0123456789
Transformation
von rechts nach
links: Ziffer 2 wird 5 (Tabelle: Zeile 1)
       "      0 wird 0 ("        "     2)
       "      3 wird 4 ("        "     3)
       "      6 wird 6 ("        "     4)
       "      8 wird 2 ("        "     1)
       "      5 wird 8 ("        "     2)
       "      4 wird 6 ("        "     3)
       "      1 wird 1 ("        "     4)
       "      3 wird 9 ("        "     1)
                    ___
Summe:              41     (Einerstelle = 1)
Subtraktion : (10 - 1) = 9 (= Prüfziffer)
Kontonummer mit Prüfziffer: 3 1 4 5 8 6 3 0 2 9"""
def check_29(accountno,debug=False):    # 
    if debug: alert('check_29:: starting:\taccountno: '+str(accountno))
    hand = 0
    indexes = [1,2,3,4]
    codes = {    1:[0,1,5,9,3,7,4,8,2,6],
                2:[0,1,7,6,9,8,3,2,5,4],
                3:[0,1,8,4,6,2,9,5,7,3],
                4:[0,1,2,3,4,5,6,7,8,9]}
    if debug: alert('check_29:: coding:\n'+'hand:\tpos:\tdigit:\tline:\tcode:')
    for i in range(len(str(accountno))-1):
        pos = -(i+2)
        digit = accountno[pos]
        line = indexes[i%len(indexes)]
        code = codes[line][digit]
        if debug:     alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(line)+'\t'+str(code))
        hand += code
    hand = hand%10
    if debug: alert('check_29:: mod 10: '+str(hand))
    result = hand==int(str(accountno)[-1])
    if debug: alert('check_29:: preresult: '+str(hand)+'\tlast account digit: '+str(accountno)[-1]+'\tresult: '+str(result))
    return result

"""Modulus 10, Gewichtung 2, 0, 0, 0, 0, 1, 2, 1, 2
Die letzte Stelle ist per Definition die Prüfziffer.
Die einzelnen Stellen der Kontonummer sind ab der ersten
Stelle von links nach rechts mit den Ziffern 2, 0, 0, 0, 0, 1, 2, 1,
2 zu multiplizieren. Die jeweiligen Produkte werden addiert
(ohne Quersummenbildung). Die weitere Berechnung erfolgt
wie bei Verfahren 00.
Stellennr.: 1 2 3 4 5 6 7 8 9 A (A=10)
Kontonr.:   x x x x x x x x x P
Gewichtung: 2 0 0 0 0 1 2 1 2"""
def check_30(accountno,weights=[2,0,0,0,0,1,2,1,2],debug=False):    # 
    if debug: alert('check_30:: starting:\taccountno: '+str(accountno)+'\tweights: '+str(weights))
    hand = 0
    if debug: alert('check_30:: weighing:\n'+
        'hand:\tpos:\tdigit:\tweight:\tproduct:')
    for i in range(len(str(accountno))-1):
        pos = i
        digit = int( str(accountno)[pos] )
        weight = int( weights[i%len(weights)] )
        product = digit*weight
        if debug:     alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product))
        hand += product
    if debug: alert('check_30:: weight: '+str(hand))
    hand = hand%10
    if debug: alert('check_30:: mod 10: '+str(hand))
    hand = 10-hand
    if debug: alert('check_30:: 10 diff: '+str(hand))
    hand = hand%10
    if debug: alert('check_30:: mod 10: '+str(hand))
    result = hand==int(str(accountno)[-1])
    if debug: alert('check_30:: result: '+str(result)+'\tlast account digit: '+str(accountno)[-1]+'\tpreresult: '+str(hand))
    return result

"""Modulus 11, Gewichtung 9, 8, 7, 6, 5, 4, 3, 2, 1
Die Kontonummer ist 10-stellig. Die Stellen 1 bis 9 der
Kontonummer sind von rechts nach links mit den Ziffern 9, 8, 7,
6, 5, 4, 3, 2, 1 zu multiplizieren. Die jeweiligen Produkte werden
addiert. Die Summe ist durch 11 zu dividieren. Der
verbleibende Rest ist die Prüfziffer. Verbleibt nach der Division
durch 11 kein Rest, ist die Prüfziffer 0. Ergibt sich ein Rest 10,
ist die Kontonummer falsch. Die Prüfziffer befindet sich in der
10. Stelle der Kontonummer.
Beispiel:                     P
Stellennr.: 1 2  3  4 5  6 7 8  9 10
Kontonr.:   0 2  6  3 1  6 0 1  6 5
Gewichtung: 1 2  3  4 5  6 7 8  9
            0+4+18+12+5+36+0+8+54 = 137
137 : 11 = 12 Rest 5
5 = Prüfziffer
Testkontonummern: 1000000524, 1000000583"""
def check_31(accountno,weights=[9,8,7,6,5,4,3,2,1],debug=False):    # 
    if debug: alert('check_31:: starting:\taccountno: '+str(accountno)+'\tweights: '+str(weights))
    if len(accountno)!=10:
        result = False
        if debug:     alert('check_31:: result: '+str(result)+' early out, unfit accountno')
        return result
    hand = 0
    if debug: alert('check_31:: weighing:\n'+
        'hand:\tpos:\tdigit:\tweight:\tproduct:')
    for i in range(len(str(accountno))-1):
        pos = -(i+2)
        digit = int( str(accountno)[pos] )
        weight = int( weights[i%len(weights)] )
        product = digit*weight
        if debug:     alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product))
        hand += product
    if debug: alert('check_31:: weight: '+str(hand))
    hand = hand%11
    if debug: alert('check_31:: mod 11: '+str(hand))
    if hand==10:
        result = False
        if debug:     alert('check_31:: result: '+str(result)+' earlyout, remainder 10')
    result = hand==int(str(accountno)[-1])
    if debug: alert('check_31:: result: '+str(result)+'\tlast account digit: '+str(accountno)[-1]+'\tpreresult: '+str(hand))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7
Die Kontonummer ist 10-stellig. Die Stellen 4 bis 9 der
Kontonummer werden von rechts nach links mit den Ziffern 2,
3, 4, 5, 6, 7 multipliziert. Die Berechnung und Ergebnisse
entsprechen dem Verfahren 06. Die Stelle 10 der
Kontonummer ist per Definition die Prüfziffer.
Stellennr.: 1 2 3 4 5 6 7 8 9 A (A=10)
Kontonr.:   x x x x x x x x x P
Gewichtung:       7 6 5 4 3 2
Testkontonummern: 9141405, 1709107983, 0122116979,
0121114867, 9030101192, 9245500460"""
def check_32(accountno,weights=[2,3,4,5,6,7],debug=False):    # 
    if debug: alert('check_32:: starting:\taccountno: '+str(accountno)+'\tweights: '+str(weights))
    if len(accountno)!=10:
        result = False
        if debug:     alert('check_32:: result: '+str(result)+' early out, unfit accountno')
        return result
    accountno = accountno[3:]
    if debug: alert('check_32:: 4-10 digit:\taccountno: '+str(accountno))
    hand = 0
    if debug: alert('check_32:: weighing:\n'+'hand:\tpos:\tdigit:\tweight:\tproduct:')
    for i in range(len(str(accountno))-1):
        pos = -(i+2)
        digit = int( str(accountno)[pos] )
        weight = int( weights[i%len(weights)] )
        product = digit*weight
        if debug:     alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product))
        hand += product
    if debug: alert('check_32:: weight: '+str(hand))
    hand = hand%11
    if debug: alert('check_32:: mod 11: '+str(hand))
    hand = 11-hand
    if debug: alert('check_32:: 11 diff: '+str(hand))
    hand = hand%10
    if debug: alert('check_32:: mod 10: '+str(hand))
    result = hand==int(str(accountno)[-1])
    if debug: alert('check_32:: result: '+str(result)+'\tlast account digit: '+str(accountno)[-1]+'\tpreresult: '+str(hand))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6
Die Kontonummer ist 10-stellig. Die Stellen 5 bis 9 der
Kontonummer werden von rechts nach links mit den Ziffern 2,
3, 4, 5, 6 multipliziert. Die restliche Berechnung und
Ergebnisse entsprechen dem Verfahren 06. Die Stelle 10 der
Kontonummer ist per Definition die Prüfziffer.
Stellennr.: 1 2 3 4 5 6 7 8 9 A (A=10)
Kontonr.:   x x x x x x x x x P
Gewichtung:         6 5 4 3 2
Testkontonummern: 48658, 84956"""
def check_33(accountno,weights=[2,3,4,5,6],debug=False):    # 
    if debug: alert('check_33:: starting:\taccountno: '+str(accountno)+'\tweights: '+str(weights))
    if len(accountno)!=10:
        result = False
        if debug:     alert('check_33:: result: '+str(result)+' early out, unfit accountno')
        return result
    accountno = accountno[4:]
    if debug: alert('check_33:: 5-10 digit:\taccountno: '+str(accountno))
    hand = 0
    if debug: alert('check_33:: weighing:\n'+'hand:\tpos:\tdigit:\tweight:\tproduct:')
    for i in range(len(str(accountno))-1):
        pos = -(i+2)
        digit = int( str(accountno)[pos] )
        weight = int( weights[i%len(weights)] )
        product = digit*weight
        if debug:     alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product))
        hand += product
    if debug: alert('check_33:: weight: '+str(hand))
    hand = hand%11
    if debug: alert('check_33:: mod 11: '+str(hand))
    hand = 11-hand
    if debug: alert('check_33:: 11 diff: '+str(hand))
    hand = hand%10
    if debug: alert('check_33:: mod 10: '+str(hand))
    result = hand==int(str(accountno)[-1])
    if debug: alert('check_33:: result: '+str(result)+'\tlast account digit: '+str(accountno)[-1]+'\tpreresult: '+str(hand))
    return result

"""Modulus 11, Gewichtung 2, 4, 8, 5, A, 9, 7 (A = 10)
Die Kontonummer ist 10-stellig. Es wird das
Berechnungsverfahren 28 mit modifizierter Gewichtung
angewendet. Die Gewichtung lautet 2, 4, 8, 5, A, 9, 7. Dabei
steht der Buchstabe A für den Wert 10.
Testkontonummern: 9913000700, 9914001000"""
def check_34(accountno,weights=[2,4,8,5,10,9,7],debug=False):
    if debug: alert('check_34:: starting:\taccountno: '+str(accountno))
    if len(accountno)!=10:
        result = False
        if debug:     alert('check_34:: result: '+str(result)+' early out, unfit accountno')
        return result
    result = check_28(accountno,weights=weights,debug=debug)
    if debug: alert('check_34:: result: '+str(result))
    return result

"""Modulus 11, Gewichtung 2, 3, 4, 5, 6, 7, 8, 9, 10
Die Kontonummer ist ggf. durch linksbündige Nullenauffüllung
10-stellig darzustellen. Die 10. Stelle der Kontonummer ist die
Prüfziffer. Die Stellen 1 bis 9 der Kontonummer werden von
rechts nach links mit den Ziffern 2, 3, 4, ff. multipliziert. Die
jeweiligen Produkte werden addiert. Die Summe der Produkte
ist durch 11 zu dividieren. Der verbleibende Rest ist die
Prüfziffer. Sollte jedoch der Rest 10 ergeben, so ist die
Kontonummer unabhängig vom eigentlichen Berechnungs-
ergebnis richtig, wenn die Ziffern an 10. und 9. Stelle identisch
sind.
Beispiel 1:                      P
Stellennr.:  1 2 3 4 5 6  7  8 9 10
Kontonr.:    0 0 0 0 1 0  8  4 4 3
Gewichtung: 10 9 8 7 6 5  4  3 2
             0+0+0+0+6+0+32+12+8 = 58
58 : 11 = 5 Rest 3
3 ist die Prüfziffer
Beispiel 2:                      P
Stellennr.:  1 2 3 4 5 6 7  8 9 10
Kontonr.:    0 0 0 0 1 0 1  5 9 9
Gewichtung: 10 9 8 7 6 5 4  3 2
             0+0+0+0+6+0+4+15+18 = 43:11 Rest 10
Testkontonummern: 0000108443, 0000107451, 0000102921,
0000102349, 0000101709, 0000101599"""
def check_35(accountno,weights=[2,3,4,5,6,7,8,9,10],debug=False):    # 
    if debug: alert('check_35:: starting:\taccountno: '+str(accountno)+'\tweights: '+str(weights))
    if len(accountno)!=10:
        accountno = '0'*(10-len(accountno))+accountno
        if debug:   alert('check_35:: fill-up, accountno: '+accountno)
    hand = 0
    if debug: alert('check_35:: weighing:\n'+'hand:\tpos:\tdigit:\tweight:\tproduct:')
    for i in range(len(str(accountno))-1):
        pos = -(i+2)
        digit = int( str(accountno)[pos] )
        weight = int( weights[i%len(weights)] )
        product = digit*weight
        if debug:   alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product))
        hand += product
    if debug: alert('check_35:: weight: '+str(hand))
    hand = hand%11
    if debug: alert('check_35:: mod 11: '+str(hand))
    if hand==10 and accountno[8]==accountno[9]:
        result = True
        if debug:     alert('check_35:: result: '+str(result)+'\tearly out')
        return result
    result = hand==int(str(accountno)[-1])
    if debug: alert('check_35:: result: '+str(result)+'\tlast account digit: '+str(accountno)[-1]+'\tpreresult: '+str(hand))
    return result

"""Modulus 11, Gewichtung 2, 4, 8, 5
Die Kontonummer ist 10-stellig. Die Stellen 6 bis 9 der
Kontonummer werden von rechts nach links mit den Ziffern 2, 4,
8, 5 multipliziert. Die restliche Berechnung und Ergebnisse
entsprechen dem Verfahren 06. Die Stelle 10 der Kontonummer
ist per Definition die Prüfziffer.
Stellennr.: 1 2 3 4 5 6 7 8 9 A (A = 10)
Kontonr.:   x x x x x x x x x P
Gewichtung:           5 8 4 2
Testkontonummern: 113178, 146666"""
def check_36(accountno,weights=[2,4,8,5],debug=False):    # 
    if debug: alert('check_36:: starting:\taccountno: '+str(accountno)+'\tweights: '+str(weights))
    if len(accountno)!=10:
        result = False
        if debug:     alert('check_36:: result: '+str(result)+' early out, unfit accountno')
        return result
    accountno = accountno[5:]
    if debug: alert('check_36:: 6-10 digit:\taccountno: '+str(accountno))
    hand = 0
    if debug: alert('check_36:: weighing:\n'+'hand:\tpos:\tdigit:\tweight:\tproduct:')
    for i in range(len(str(accountno))-1):
        pos = -(i+2)
        digit = int( str(accountno)[pos] )
        weight = int( weights[i%len(weights)] )
        product = digit*weight
        if debug:     alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product))
        hand += product
    if debug: alert('check_36:: weight: '+str(hand))
    hand = hand%11
    if debug: alert('check_36:: mod 11: '+str(hand))
    hand = 11-hand
    if debug: alert('check_36:: 11 diff: '+str(hand))
    hand = hand%10
    if debug: alert('check_36:: mod 10: '+str(hand))
    result = hand==int(str(accountno)[-1])
    if debug: alert('check_36:: result: '+str(result)+'\tlast account digit: '+str(accountno)[-1]+'\tpreresult: '+str(hand))
    return result



def check_B8(accountno,debug=False):
    if debug: alert('check_B8:: starting:\taccountno: '+str(accountno))
    if check_20(accountno,debug=debug):
        result = True
        if debug:     alert('check_B8:: check_20: '+str(result))
    elif check_29(accountno,debug=debug):
        result = True
        if debug:     alert('check_B8:: check_29: '+str(result))
    elif     (    (5100000000<=long(accountno) \
                and long(accountno)<=5999999999) \
            or     (9010000000<=long(accountno) \
                and long(accountno)<=9109999999)) \
            and check_09(accountno,debug=debug):
        result = True
        if debug:     alert('check_B8:: check_9: '+str(result))
    else:
        result = False
    if debug: alert('check_B8:: result: '+str(result))
    return result

def check_118(accountno,debug=False):
    if debug: alert('check_118:: starting:\taccountno: '+str(accountno))
    result = check_B8(accountno,debug=debug)
    if debug: alert('check_118:: result: '+str(result))
    return result

def sanity_check():
    for accountno in ['9290701', '539290858', '1501824', '1501832']:
        if not check_00(accountno):
            alert('check_00 failed: '+accountno+' false negative')
    if not check_06('94012341'):
        alert('check_06 failed: 94012341 false negative')
    if check_06('5073321010'):
        alert('check_06 failed: 5073321010 false positive')
    for accountno in ['12345008', '87654008']:
        if not check_10(accountno):
            alert('check_10 failed: '+accountno+' false negative')
    if not check_17('0446786040'):
        alert('check_17 failed: 0446786040 false negative')
    for accountno in ['0240334000','0200520016']:
        if not check_19(accountno):
            alert('check_19 failed: '+accountno+' false negative')
    if not check_20('4114637180'):
        alert('check_20 failed: 4114637180 false negative')
    for c in '012345678':
        if check_29('314586302'+c):
            alert('check_29 failed: 314586302'+c+' false positive')
    if not check_29('3145863029'):
        alert('check_29 failed: 3145863029 false negative')

##  Auxiliary methods  ##
def cross_sum(num,debug=False):
#    if debug: report('AUX:cross_sum:: starting, num: '+str(num))
    result = sum([ int(digit) for digit in str(num) ])
#    if debug: report('AUX:cross_sum:: result: '+str(result))
    return result

def weighing(digits,weights,post=None,debug=False):
    """Weighs the given digits with given weights repeating the sequence of weights if necessary, applying post to intermediate products."""
    if debug:
        report('AUX:weighing:: START\ndigits:\t'+digits+'\tweights:\t'+str(weights)+'\tpost:\t'+('none' if post==None else post.func_name))
        report('hand:\tpos:\tdigit:\tweight:\tprod:'+('' if post==None else '\t'+post.func_name+':'))
    hand = 0
    for pos in range(len(str(digits))):
        digit = int( str(digits)[pos] )
        weight = int( weights[pos%len(weights)] )
        product = digit*weight
        if post!=None:
            postRes = post(product,debug=debug)
            if debug: alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product)+'\t'+str(postRes))
            hand += postRes
        else:
            if debug: alert(str(hand)+'\t'+str(pos)+'\t'+str(digit)+'\t'+str(weight)+'\t'+str(product))
            hand += product
    if debug: report('AUX:weighing:: RESULT: '+str(hand))
    return hand
     
def isValidCheckMethod(checkMethod):
    return checkMethod!='12' and re.match('^[0-2][0-9]$|^3[0-4]$|^B8$|^118$',checkMethod)!=None # Currently available
#    return checkMethod!='12' and re.match('^([0-9]|[A-D]|1[0-4])[0-9]$|^E0$',checkMethod)!=None

def executeCheck(checkMethod,accountno,debug=False):
    if isValidCheckMethod(checkMethod):
        return str(globals()['check_'+method](accountno,debug=debug))
    else:
        return 'Invalid check method'

def main():
    if len(sys.argv)>2:
        method = sys.argv[1].upper()
        if not isValidCheckMethod(method):
            alert('ERROR: Unknown check method')
            sys.exit(1)
        if sys.argv[2].lower()=='debug':
            debug = True
            numbers = sys.argv[3:]
        else:
            debug = False
            numbers = sys.argv[2:]
        report('Method:\t'+method+'\t[debug:'+('on' if debug else 'off')+']')
        report('Numbers:\t'+str(numbers))
        for accountno in numbers:
            report('No.: '+accountno+'\tresult: '+str(executeCheck(method,accountno,debug=debug)))
    else:
        alert('Usage: ./checkmethods.py <check-method> [debug] <account-number>+')

if __name__=='__main__':
    main()
