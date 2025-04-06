[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)
# NINA API (14109)

## Beschreibung 

Baustein zum Abruf von Warnmeldungen über die <a href="https://nina.api.bund.dev/">NINA API</a> des Bundesamt für Bevölkerungsschutz</p>

Alle Ausgänge sind als Send-by-Change (sbc) ausgeführt.

<span style="color:red">Der Baustein zeigt standardmäßig **keine** DWD-Warnungen. Er filtert sie sogar aktiv heraus. DWD Warnungen
müssen über **Eingang 6** aktiviert oder über einen anderen Baustein bezogen und verarbeitet werden!</span><br>Z.B. diesen hier: [14101 DWD-Unwetter](https://github.com/En3rGy/14101_DWDUnwetter)

## Inputs

| No. | Name                       | Initialisation | Description                                                                                                                                                                                                                                                       |
|-----|----------------------------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Amtlicher Gebietsschlüssel |                | Amtlicher Gebietsschlüssel, kann z.B. <a href="https://www.orte-in-deutschland.de/">hier</a> bezogen werden. Die Letzten 7 Stellen müssen mit "0000000" ersetzt werden, da Daten nur auf Kreisebene bereitgestellt werden.                                        |
| 2   | POI N-Lat.                 | 0              | Nordweisender Latitude-Wert des POI als Dezimalgrad, z.B. 48.1234<br>Der POI (Point of Interest) beschreibt die genaue Koordinate für die Warnungen empfangen werden sollen. Der POI muss natürlich innerhalb des Gebiets des amtlichen Gebietsschlüssels liegen! |
| 3   | POI E-Lon.                 | 0              | Ostweisender Longitude-Wert des POI als Dezimalgrad, z.B. 11.1234<br>Der POI (Point of Interest) beschreibt die genaue Koordinate für die Warnungen empfangen werden sollen. Der POI muss natürlich innerhalb des Gebiets des amtlichen Gebietsschlüssels liegen! |
| 4   | Update-Rate (s)            | 307            | Intervall in Sekunden, in dem der BBK-Server nach neuen Warnungen abgefragt wird.                                                                                                                                                                                 |
| 5   | Ein/Aus                    | 1              | Bei 1 arbeitet der Bautein, bei 0 nicht                                                                                                                                                                                                                           |
| 6   | DWD-Meldungen nutzen (1/0) | 0              | Bei einer 1 werden die DWD-Warnungen verarbeitet, die über NINA bereitgestellt werden. Bei einer 0 werden diese gefiltert (sinnvoll, wenn hierfür ein eigener Baustein verwendet wird).                                                                           |

## Ausgänge

| No. | Name           | Initialisation | Description                                                                                                                                                                                                                                                                                                                                         |
|-----|----------------|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Alle Warnungen | ""             | Text mit allen aktuell vorliegenden Warnungen                                                                                                                                                                                                                                                                                                       |
| 2   | Meldung        | ""             | Kritischste Warnung                                                                                                                                                                                                                                                                                                                                 |
| 3   | Schweregrad    | 0              | Schweregrad der kritischsten Meldung                                                                                                                                                                                                                                                                                                                |
| 4   | Dringlichkeit  | ""             | Dringlichkeit der kritischsten Meldung                                                                                                                                                                                                                                                                                                              |
| 5   | Gewissheit     | 0              | Sicherheit / Gewissheit der kritischsten Meldung                                                                                                                                                                                                                                                                                                    |
| 6   | Beschreibung   | 0              | Beschreibung der kritischsten Meldung                                                                                                                                                                                                                                                                                                               |
| 7   | Anleitung      | 0              | Verhaltensanweisung zur kritischsten Meldung                                                                                                                                                                                                                                                                                                        |
| 8   | Symbol-Id      | 0              | Id des Symbols für die kritischste Meldung<br>Grundlage für die Id ist der EVent Code. das BBK bietet Symbole für folgende Event Codes BBK-EVC-?, wobei das ? eine 3-stellige Zahl ersetzt. Für den Event Code BBK-EVC-004 liefert der Baustein bspw. die Id 4.<br>1 = Std. Symbol, bzw. Event Code nicht von der Art BBK-EVC<br>0 = Keine Meldung. |
| 9   | Symbol-URL     | ""             | URL zum BBK Symbol des Events                                                                                                                                                                                                                                                                                                                       |
| 10  | Json           | 0              | Json-Meldung zu den empfangenen Warnungen                                                                                                                                                                                                                                                                                                           |

## Sonstiges

- Neuberechnung beim Start: Nein
- Baustein ist remanent: Nein
- Baustein Id: 14109
- Kategorie: Datenaustausch

### Change Log

Siehe Changelog zum jew. [Release](https://github.com/En3rGy/14109_NINA_API/releases) auf GitHub. 

### Open Issues / Know Bugs

- none

### Support

Please use [github issue feature](https://github.com/En3rGy/14109_NINA_API/issues) to report bugs or rise feature requests.
Questions can be addressed as new threads at the [knx-user-forum.de](https://knx-user-forum.de) also. There might be discussions and solutions already.

### Code

Der Python-Code des Bausteins befindet sich in der hslz Datei oder auf [github](https://github.com/En3rGy/14109_NINA_API).

### Devleopment Environment

- [Python 2.7.18](https://www.python.org/download/releases/2.7/)
    - Install python markdown module (for generating the documentation) `python -m pip install markdown`
- Python editor [PyCharm](https://www.jetbrains.com/pycharm/)
- [Gira Homeserver Interface Information](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip)

## Requirements

1. Der Baustein soll ein- und ausschaltbar sein.
2. Der Baustein soll in vorgegebenen Intervallen arbeiten.
3. Der Baustein soll für vorgegebene Gebiete bestehende Warnungen des BBK abrufen. 
4. Der Baustein soll bei empfangenen Warnungen, die Headlines aller Warnungen auf einem Ausgang ausgeben. 
5. Der Baustein soll bei empfangenen Warnungen, die bedeutendste Warnung bestimmen. 
6. Der Baustein soll bei empfangenen Warnungen, für die bedeutendste Warnung die Headline ausgeben. 
7. Der Baustein soll bei empfangenen Warnungen, für die bedeutendste Warnung die Description ausgeben. 
8. Der Baustein soll bei empfangenen Warnungen, für die bedeutendste Warnung die Instruction ausgeben.

## Software Design Description

### Definitions

x

### Solution Outline

Der Baustein ruft über die NINA-API alle relevanten Warnungen für das durch den Gebietsschlüssel definierte Gebiets ab.

Da dieses Gebiet recht groß seien kann, werden über einen POI (Point of Interest) alle Warnungen gefiltert, die nicht den POI enthalten. 

## Validation & Verification

x

## Licence

Copyright 2024 T. Paul

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
