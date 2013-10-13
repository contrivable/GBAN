#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# LAST 20131013

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import checkmethods	# Validierung von Prüfmethodenangaben
import json
import re

def alert(msg):
    sys.stderr.write(msg+'\n')
def report(msg):
    sys.stdout.write(msg+'\n')

class TodoError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def lineToFields(line,lineno):
    global banks
    line = line.strip()
    if line == '': return
    if len(line) not in [168,174]:
        alert('ERROR: Unexpected length of line: '+str(len(line))+' >'+line[:8]+'<')
        raise TodoError('Unexpected length of line #'+lineno+': '+str(len(line))+' >'+line[:8]+'<')
    bank = {'Bankleitzahl':disectBLZ(line[:8])}
    bank['bankleitzahlführender Zahlungsdienstleister'] = line[8]
    bank['Bezeichnung'] = line[9:67]
    bank['Postleitzahl'] = line[67:72]
    bank['Ort'] = line[72:107]
    bank['Kurzbezeichnung'] = line[107:134]
    bank['Institutsnummer für PAN'] = line[134:139]
    bank['BIC'] = line[139:150]
    bank['Prüfzifferberechnungsmethode'] = line[150:152]
    bank['Nummer'] = line[152:158]
    bank['Änderungskennzeichen'] = line[158]
    bank['beabsichtigte Bankleitzahllöschung'] = line[159]
    bank['Nachfolge-Bankleitzahl'] = line[160:168]
    if len(line)==174:
        bank['IBAN-Regel'] = line[168:174]
    # sanity
    if re.match('^[1-8][0-9]{7}$',bank['Bankleitzahl']['BLZ'])==None:
        alert('ERROR: Malformed BLZ: '+bank['Bankleitzahl']['BLZ'])
        sys.exit(23)
    if bank['bankleitzahlführender Zahlungsdienstleister'] not in ['1','2']:
        alert('ERROR: Unknown lead indicator: '+bank['bankleitzahlführender Zahlungsdienstleister'])
    else:
        bank['bankleitzahlführender Zahlungsdienstleister (Text)'] =\
            {'1':'ja','2':'nein'}\
        [bank['bankleitzahlführender Zahlungsdienstleister']]
    if not checkmethods.isValidCheckMethod(bank['Prüfzifferberechnungsmethode']):
        alert('ERROR: Unknown check method: '+bank['Prüfzifferberechnungsmethode'])
        raise TodoError('Unknown check method: '+bank['Prüfzifferberechnungsmethode'])
    if bank['Änderungskennzeichen'] not in ['A','D','U','M']:
        alert('ERROR: Unknown status: '+bank['Änderungskennzeichen'])
    else:
        bank['Änderungskennzeichen (Text)'] = \
            {'A':'Addition/neuer Datensatz',
            'D':'Deletion/gelöschter Datensatz',
            'U':'Unchanged/unveränderter Datensatz',
            'M':'Modified/veränderter Datensatz'}\
            [bank['Änderungskennzeichen']]
    if bank['beabsichtigte Bankleitzahllöschung'] not in ['0','1']:
        alert('ERROR: Unknown deletion indicator: '+bank['beabsichtigte Bankleitzahllöschung'])
    else:
        bank['beabsichtigte Bankleitzahllöschung (Text)'] = \
            {'0':'keine Angabe',
            '1':'BLZ '+bank['Bankleitzahl']['BLZ']+' zur Löschung vorgesehen'}\
        [bank['beabsichtigte Bankleitzahllöschung']]
    if bank['Nummer'] in banks:
        alert('ERROR: Multiple records with same ID')
    banks[bank['Nummer']] = bank
    #print(json.dumps(bank,sort_keys=True,ensure_ascii=False))
    
def disectBLZ(blz):
    if len(blz)!=8:
        alert('ERROR: Unexpected length of BLZ: '+str(len(blz))+' >'+blz+'<')
        return
    info = {'BLZ':blz}
    info['clearingAreaNumber'] = blz[0]
    info['localNumber'] = blz[0:3]
    info['instituteGroupNumber'] = blz [3]
    info['intituteInternalNumber'] = blz [4:]
    clearingAreas = {
        '1':'Berlin, Brandenburg, Mecklenburg-Vorpommern',
        '2':'Bremen, Hamburg, Niedersachsen, Schleswig-Holstein',
        '3':'Rheinland (Regierungsbezirke Düsseldorf, Köln)',
        '4':'Westfalen',
        '5':'Hessen, Rheinland-Pfalz, Saarland',
        '6':'Baden-Württemberg',
        '7':'Bayern',
        '8':'Sachsen, Sachsen-Anhalt, Thüringen'}
    info['clearingAreaText'] = clearingAreas[info['clearingAreaNumber']] if info['clearingAreaNumber'] in clearingAreas.keys() else 'undefined'
    instituteGroups = {
        '0':'Deutsche Bundesbank',
        '1':'Zahlungsdienstleister, soweit nicht in einer anderen Gruppe erfasst',
        '2':'Zahlungsdienstleister, soweit nicht in einer anderen Gruppe erfasst',
        '3':'Zahlungsdienstleister, soweit nicht in einer anderen Gruppe erfasst',
        '4':'Commerzbank',
        '5':'Girozentralen und Sparkassen',
        '6':'Genossenschaftliche Zentralbanken, Kreditgenossenschaften sowie ehemalige Genossenschaften',
        '7':'Deutsche Bank',
        '8':'Commerzbank vormals Dresdner Bank',
        '9':'Genossenschaftliche Zentralbanken, Kreditgenossenschaften sowie ehemalige Genossenschaften'}
    info['instituteGroupText'] = instituteGroups[info['instituteGroupNumber']] if info['instituteGroupNumber'] in instituteGroups.keys() else 'undefined'
    if blz[3:6]=='100':
        info['additionalInfo'] = 'Hint: BLZ belongs to Deutsche Postbank AG'
    if info['clearingAreaNumber'] in ['2','3','4','5','6','7'] and blz[4]=='9':
        info['additionalInfo'] = 'Hint: BLZ for institute without BLZ giro account at Bundesbank'
    return info

def main():
    # HELP
    if len(sys.argv)==1:
        alert('USAGE: '+sys.argv[0]+' [bank number]*')
        alert('Continuing with display of all data.')
    # READ all
    global banks
    banks = {}
    lineno = 0
    for line in open('../resources/BLZ_20130909.txt','r'):
        lineno += 1
        lineToFields(line,str(lineno))
    alert('Records found: '+str(len(banks.keys())))
    # OUTPUT what?
    if len(sys.argv)>1:
        notFound = []
        for searchTerm in sorted(list(set(sys.argv[1:]))):
            hits = [ k for k in banks.keys() if banks[k]['Bankleitzahl']['BLZ']==searchTerm ]
            hits.sort()
            if len(hits)>0:
                for key in hits:
                    report(json.dumps(banks[key],sort_keys=True,ensure_ascii=False,indent=2))
            else:
                notFound.append(searchTerm)
        if len(notFound)>0:
            report('The following bank numbers were not listed:\n'+
                json.dumps(notFound,sort_keys=True,ensure_ascii=False))
    else:
        report(json.dumps(banks,sort_keys=True,ensure_ascii=False,indent=4))

if __name__=='__main__':
    main()
