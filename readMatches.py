"""
@brief: read csv export from dfb.net to get all games. developed with Python 3.5
@date: 02.03.2020
@author: Michael Jokesch
@email: michael.jokesch@oelsnitzer-fc.de
@mobil: +49 (0) 1522 7253326
"""

import os
import csv
import json
from datetime import datetime


def readCSV(fPath):
    if not os.path.exists(fPath):
        print('File "{0}" does not exist.'.format(fPath))
        return None
    readData = []
    with open(fPath, encoding='utf-16', newline='') as fp:
        reader = csv.DictReader(fp, delimiter='\t')
        for row in reader:
            readData.append(row)
    return readData


def writeJSON(inData, fPath):
    if not inData:
        print('"indata" is None. Cannot write None to a file')
        return None
    os.makedirs(os.path.dirname(fPath), exist_ok=True)

    # read required data
    outputData = []
    for game in inData:
        if 'oelsnitz' not in game.get('Heimmannschaft', '').lower():
            continue
        team = game.get('Mannschaftsart', 'Unknown').split('-')[0]
        date = str(game.get('Spieldatum')) + '-' + str(game.get('Uhrzeit'))
        outDate = datetime.strptime(date, '%d.%m.%Y-%H:%M').strftime('%y%m%d-%H%M')
        ref1 = game.get('Assistent 1')
        ref2 = game.get('Assistent 2')
        outputData.append({'team': team,
                           'date': outDate,
                           'referee1': ref1,
                           'referee2': ref2})

    # write read data to json file
    with open(fPath, 'w') as fp:
        json.dump(outputData, fp, indent=4)


if __name__ == '__main__':
    # set arguments
    fPathInput = os.path.join(os.getcwd(), 'input/2020-2021_B-Jugend-spielplan.csv')
    now = datetime.now().strftime("%d%m%Y-%H%M%S")
    fPathOutput = os.path.join(os.getcwd(), 'results', '{0}_dates.json'.format(now))

    # process
    dContent = readCSV(fPathInput)
    writeJSON(dContent, fPathOutput)

    print('FINISHED')
