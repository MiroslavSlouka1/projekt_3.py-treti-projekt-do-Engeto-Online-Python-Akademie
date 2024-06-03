# Engeto-pa-3-projekt
Třetí projekt na Python Akademii od Engeta
## Popis projektu
Tento projekt slouží k získání výsledků z parlamentních voleb v roce 2017.
Odkaz k prohlédnutí najdete [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)
## Instalace knihoven
Knihovny použité v tomto projektu jsou uloženy v souboru **requirements.txt**, který je přiložen v repozitáři.
Pro instalaci knihoven doporučuji použít nové virtuální prostředí s nainstalovaným manažerem.
Instalaci provedete následovně:

``` pip install -r requirements.txt ```         případně

``` pip3 install -r requirements.txt ```

## Spuštění programu
Program Elections_Scraper.py se spouští v příkazovém řádku se dvěma parametry.

První parametr obsahuje URL webové stránky z odkazu výše.

Druhý parametr definuje název souboru s příponou ".csv",kam se uloží výsledky

Vzor příkazu:

```python Elections_Scraper.py <URL webove stranky> <soubor_s_vysledky.csv>```

## Ukázka programu

Výsledky hlasování pro okres Benešov

Spuštění programu:

``` python Elections_Scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101' 'vysledky_benesov.csv' ```

Průběh stahování:

``` Stahuji data z vybraneho URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101 ```

během stahování se zobrazuji "*"

```
********************
**
```

po stažení dat se uloží do souboru a program se ukončí

```
Ukladam data do souboru:  vysledky_benesov.csv
Ukoncuji program Election_Scraper
```

Ukázka výstupu:
```
code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko
529303,Benešov,13104,8485,8437,1052,10,2,624,3,802,597,109,35,112,6,11,948,3,6,414,2577,3,21,314,5,58,17,16,682,10
532568,Bernartice,191,148,148,4,0,0,17,0,6,7,1,4,0,0,0,7,0,0,3,39,0,0,37,0,3,0,0,20,0
530743,Bílkovice,170,121,118,7,0,0,15,0,8,18,0,2,0,0,0,3,0,0,2,47,1,0,6,0,0,0,0,9,0
```

