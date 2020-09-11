'''
@brief: assign assistant referees to games. developed with Python 3.5
@date: 27.02.2020
@author: Michael Jokesch
@email: michael.jokesch@oelsnitzer-fc.de
@mobil: +49 (0) 1522 7253326
'''

import os
import json
import random
from datetime import datetime

maxRefereeAppearance = 2


def synchronizeData(referees, dates, maxAppearance):
    # sync dates to referees
    for date in dates:
        if date.get('referee1'):
            if not updateRefereeData(referees, date.get('referee1'), date, maxAppearance):
                date['referee1'] = ''
        if date.get('referee2'):
            if not updateRefereeData(referees, date.get('referee2'), date, maxAppearance):
                date['referee2'] = ''

    return dates, referees


def updateRefereeData(referees, refName, date, maxAppearance):
    for ref in referees:
        if refName == ref[0]:
            if len(ref[1]) >= maxAppearance:
                print('Max. appearance {0} is reached for {1}'.format(maxAppearance, refName))
                return False
            ref[1].append([date['date'], date['team']])
            break
    return referees


def readInputFiles(fPathDates, fPathPersonal):
    with open(fPathDates, 'r') as fp:
        dates = json.load(fp)
        datesSorted = sorted(dates, key=lambda x: x.get('date'))
    with open(fPathPersonal, 'r') as fp:
        personal = json.load(fp)
    return datesSorted, personal


def getAvailableReferees(referees, maxAppearance):
    availableRefs = []
    for refName, refDates in referees:
        if 'False' == refDates:
            continue
        if len(refDates) < maxAppearance:
            availableRefs.append(refName)
    return availableRefs


def diceReferees(dates, referees):
    currentAppearanceCount = 1
    for date in dates:
        for refPair in [('referee1', 'referee2'), ('referee2', 'referee1')]:
            if not date.get(refPair[0]):
                # get available referees for equal distribution
                availableRefs = []
                while not availableRefs:
                    availableRefs = getAvailableReferees(referees, currentAppearanceCount)
                    if not availableRefs:
                        currentAppearanceCount += 1
                # get random referee
                randomRefName = random.choice(availableRefs)
                # check if ref already set for this date
                if randomRefName != date.get(refPair[1]):
                    date[refPair[0]] = randomRefName
                    updateRefereeData(referees, randomRefName, date, maxRefereeAppearance)
    return dates, referees


def writeResults(dates, referees, resultPath):
    now = datetime.now().strftime("%d%m%Y-%H%M%S")
    with open(os.path.join(resultPath, '{0}_dates.json'.format(now)), 'w') as fp:
        json.dump(dates, fp, indent=4)
    with open(os.path.join(resultPath, '{0}_referees.json'.format(now)), 'w') as fp:
        json.dump(referees, fp, indent=4)

    with open(os.path.join(resultPath, '{0}_result.csv'.format(now)), 'w') as fp:
        header = 'Datum;Mannschaft;Schiedsrichter-1;Schiedsrichter-2\n'
        fp.write(header)
        for date in dates:
            oDate = datetime.strptime(date['date'], '%y%m%d-%H%M')
            strDate = oDate.strftime('%d.%m.%Y %H:%M')
            line = '{0};{1};{2};{3}\n'.format(strDate, date['team'], date['referee1'], date['referee2'])
            fp.write(line)

    with open(os.path.join(resultPath, '{0}_resultReferees.csv'.format(now)), 'w') as fp:
        header = 'Name;Daten\n'
        fp.write(header)
        for ref in referees:
            line = '{0}'.format(ref[0])
            for date in ref[1]:
                line += ';{0}'.format(date)
            line += '\n'
            fp.write(line)


def mainGamble(jPathDates, jPathReferees):
    dates, referees = readInputFiles(jPathDates, jPathReferees)
    if not dates:
        print('ERROR: No dates available. Break')
    elif not referees:
        print('ERROR: No referees available. Break.')
    else:
        dates, referees = synchronizeData(referees, dates, maxRefereeAppearance)
        dates, referees = diceReferees(dates, referees)

    return dates, referees


if __name__ == '__main__':
    fPathDates = '/home/mjokesch/Dokumente/OFC/refereeTool/results/10092020-205524_dates.json' #)'dates_Saison19-20.json')
    fPathPersonal = os.path.join(os.getcwd(), 'personal.json')
    resultPath = os.path.join(os.getcwd(), 'results')

    dates, referees = mainGamble(fPathDates, fPathPersonal)
    if dates and referees:
        writeResults(dates, referees, resultPath)

    print('FINISHED')