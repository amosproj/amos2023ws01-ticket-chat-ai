# Creation of Test Data

## JSON Data Format

```json
{
    "text": [
      "Betreff: Dringend: Netzwerk-Problem",
      "Hallo Support Team,",
      "ich habe Probleme mit der Netzwerk-Verbindung",
      "Wir haben ein paar neue Rechner in einem Rack im Technik Raum eingerichtet.",
      "Bei einem möchten wir, dass ein Kollege aus Ungarn Zugang dazu hat.",
      "Der Kollege ist Mustermann, Max max.mustermann@talktix.com in Erlangen. ",
      "Ich habe schon Admin Rechte fuer ihn auf dem Rechner eingerichtet.",
      "Er meldet, dass er kein Remote Desktop auf dem Rechner aufmachen kann.",
      "Ich kann arbeiten, aber der Kollege aus Ungarn braucht es dringend.",
      "Mit freundlichen Grüßen,",
      "Michael Müller"
    ],
    "ticket": {
      "title": "Störung -> Netzwerk",
      "location": "",
      "category": "Störung -> Netzwerk",
      "keywords": [
        "Remote Desktop",
        "Netzwerk"
      ],
      // 1 - 4 
      "customerPriority": "Störung aber kann arbeiten",
      // Störung aber kann arbeiten, Störung kann nicht arbeiten, Störung mehrere können nicht arbeiten, Störung Abteilung kann nicht arbeiten
      "affectedPerson": "Mustermann, Max",
      "description": "Wir haben ein paar neue Rechner in einem Rack im Technik Raum eingerichtet. Bei einem möchten wir, dass ein Kollege aus Ungarn Zugang dazu hat. Er meldet, dass er kein Remote Desktop auf dem Rechner öffnen kann.",
      "priority": "Mittel"
      // Niedrig, Mittel, Hoch, Sehr Hoch,
    }
  }
```

## Making Use of ChatGPT

### 1. Starting the Conversation with a Short Description

Prompt:

```text
Bitte erstelle mir einen Datensatz für Support-Anfragen und -Tickets in deutscher Sprache nach dem folgenden JSON Format:

<paste in the format>

Dabei soll unter "text" der Betreff und der Inhalt einer Email-Anfrage an einen Kunden-Support für technische Belange als Zeilen in einem Array aufgelistet sein.
Außerdem soll unter "ticket" ein zur Email passendes Support-Ticket mit den folgenden Attributen vorhanden sein.
Das Attribut "title" beinhaltet den Titel des Tickets, welcher möglichst kurz und im Nominalstil verfasst sein soll.
Das Attribut "location" spezifiziert die betroffene Stelle beim Kunden.
Das Attribut "category" klassifiziert das Problem möglichst knapp.
Das Attribut "keywords" ist ein Array mit 1 bis 4 verschiedenen Schlagworten, die den Inhalt des Tickets betreffen.
Das Attribut "customerPriority" beschreibt die Auswirkung des Problems auf den Kunden und kann die Werte "Störung aber kann arbeiten", "Störung kann nicht arbeiten", "Störung mehrere können nicht arbeiten" und "Störung Abteilung kann nicht arbeiten" annehmen.
Das Attribut "affectedPerson" ist der Name der betroffenen Person, d.h. oftmals der Verfasser der Email, im Format "Nachname, Vorname(n)".
Das Attribut "description" beinhaltet eine detaillierte Beschreibung des Problems, auf das sich das Ticket bezieht.
Das Attribut "priority" klassifiziert die Relevanz des Tickets mit den Werten "Niedrig", "Mittel", "Hoch" und "Sehr Hoch".

Bitte gib mir 5 Beispiele mit Fokus auf <insert a varying focus for the 5 examples>.
```

Copy the results to your own JSON file under `./test_data_<your name>/data.json` with the following structure:

```json
[
  // paste example 1
  {},
  // example 2
  {},
  // example 3
  {},
  // etc.
  {}
]
```

### 2. Getting more Examples

Prompt:

```text
Bitte gib mir 5 weitere Beispiele mit Fokus auf <insert a varying focus for the 5 examples>.
```

Example:

```text
Bitte gib mir 5 weitere Beispiele mit Fokus auf Probleme mit computergesteuerten Industrieanlagen.
```
