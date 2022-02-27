# NINA API (14109)

## Beschreibung 

Baustein zum Abruf von Warnmeldungen über die <a href="https://nina.api.bund.dev/">NINA API</a> des Bundesamt für Bevölkerungsschutz</p>

## Inputs

| No. | Name | Initialisation | Description |
| --- | --- | --- | --- |
| 1 | Amtlicher Gebietsschlüssel | "" | Amtlicher Gebietsschlüssel, kann z.B. <a href="">hier</a> bezogen werden. Die Letzten 7 Stellen müssen mit "0000000" ersetzt werden, da Daten nur auf Kreisebene bereitgestellt werden. |


## Ausgänge

| No. | Name | Initialisation | Description |
| --- | --- | --- | --- |
| 1 | Headline | "" | Warnmeldung |
| 2 | Severity | 0 | Warnmeldung |
| 3 | Json | 0 | Empfangene Json Meldung mit allen Details. |

## Sonstiges

- Neuberechnung beim Start: Nein
- Baustein ist remanent: Nein
- Baustein Id: 14109
- Kategorie: Datenaustausch

### Change Log

- v0.1
    - Initiales Release

### Open Issues / Know Bugs

- none

### Support

Please use [github issue feature](https://github.com/En3rGy/14109_NINA_API/issues) to report bugs or rise feature requests.
Questions can be addressed as new threads at the [knx-user-forum.de](https://knx-user-forum.de) also. There might be discussions and solutions already.


### Code

Der Python-Code des Bausteins befindet sich in der hslz Datei oder auf [github](https://github.com/En3rGy/14102_FritzBox_TR-064).

### Devleopment Environment

- [Python 2.7.18](https://www.python.org/download/releases/2.7/)
    - Install python markdown module (for generating the documentation) `python -m pip install markdown`
- Python editor [PyCharm](https://www.jetbrains.com/pycharm/)
- [Gira Homeserver Interface Information](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip)


## Requirements

x

## Software Design Description

### Definitions

x

### Solution Outline

x

## Validation & Verification

x

## Licence

Copyright 2022 T. Paul

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

