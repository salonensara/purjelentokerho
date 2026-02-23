# Purjelentokerho

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan käyttäjätunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan purjelentokoneita.
- Käyttäjä pystyy valitsemaan purjekoneelle yhden tai useamman luokittelun (luokka ja moottori).
- Käyttäjä näkee sovellukseen lisätyt purjelentokoneet.
- Käyttäjä pystyy hakemaan purjelentokoneita konetyypin tai rekisteritunnuksen perusteella.
- Käyttäjäsivu näyttää, montako purjelentokonetta käyttäjä on lisännyt ja listan käyttäjän lisäämistä purjelentokoneista.
- Käyttäjä pystyy valitsemaan purjelentokoneelle yhden tai useamman luokittelun (luokka ja moottori).
- Käyttäjä pystyy anomaan purjelentokoneen käyttöönsä. Ilmoituksessa näytetään, ketkä käyttäjät ovat konetta anoneet.
- Tässä pääasiallinen tietokohde on purjelentokone ja toissijainen koneanomus.

## Sovelluksen asennus

Asenna 'flask'-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
