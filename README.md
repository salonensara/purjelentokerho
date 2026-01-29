# Purjelentokerho

## Sovelluksen toiminnot

- Sovelluksessa käyttäjät voivat varata purjelentokoneita. Purjelentokoneen tiedoissa lukee nimi, rekisteritunnus ja kisatunnus.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään purjelentokoneita ja muokkaamaan ja poistamaan niitä.
- Käyttäjä näkee sovellukseen lisätyt purjelentokoneet.
- Käyttäjä pystyy etsimään prujelentokoneita hakusanalla.
- Käyttäjäsivu näyttää, montako purjekonetta käyttäjä on lisännyt ja listan käyttäjän lisäämistä purjekoneista.
- Käyttäjä pystyy valitsemaan purjekoneelle yhden tai useamman luokittelun (esim. kerholuokka, vakioluokka, 15m, turbo, itselähtevä).
- Käyttäjä pystyy lisäämään varauksen purjekoneeseen. Ilmoituksessa näytetään, ketkä käyttäjät ovat konetta varanneet.
- Tässä pääasiallinen tietokohde on purjelentokone ja toissijainen purjelentokoneen varaus.

## Sovelluksen asennus

Asenna 'flask'-kirjasto:

...
$ pip install flask
...

Luo tietokannan taulut ja lisää alkutiedot:

...
$ sqlite3 database.db < schema.sql
...

Voit käynnistää sovelluksen näin:

...
$ flask run
...
