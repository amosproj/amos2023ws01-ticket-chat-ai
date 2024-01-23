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
    "service": "",
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
    "priority": "Mittel", 
    // Niedrig, Mittel, Hoch, Sehr Hoch,
    "requestType": "Incident"
    // Service Request, Incident
  }
}
```

## Making Use of ChatGPT

### 1. Starting the Conversation with a Short Description

Prompt:

```text
Bitte erstelle einen Datensatz für Support-Anfragen und Tickets auf Deutsch im angegebenen JSON-Format:

<paste in the format>

Unter "text" sollen der Betreff und der Inhalt einer E-Mail-Anfrage an den technischen Kundensupport als Zeilen in einem Array aufgeführt werden.
Zusätzlich soll unter "ticket" ein entsprechendes Support-Ticket mit den folgenden Attributen vorhanden sein:
- Das Attribut "title" enthält einen prägnanten Titel im Nominalstil für das Ticket.
- Das Attribut "service" spiegelt einen relevanten Service aus der Liste wider: Adobe, Atlassian, München, Reporting, Salesforce oder ein Ort (Fürth, Nürnberg, Berlin, Frankfurt, München).
- Das Attribut "category" klassifiziert das Problem prägnant.
- Das Attribut "keywords" ist ein Array mit 1 bis 4 relevanten Schlagworten, die mit dem Ticketinhalt zusammenhängen.
- Das Attribut "customerPriority" beschreibt die Auswirkungen des Problems und kann eines der folgenden sein: "Störung aber kann arbeiten", "Störung kann nicht arbeiten", "Störung mehrere können nicht arbeiten", "Störung Abteilung kann nicht arbeiten".
- Das Attribut "affectedPerson" repräsentiert den Namen der betroffenen Person im Format "Nachname, Vorname(n)".
- Das Attribut "description" enthält eine detaillierte Beschreibung des mit dem Ticket verbundenen Problems.
- Das Attribut "priority" klassifiziert die Relevanz des Tickets mit Werten wie "Niedrig", "Mittel", "Hoch", "Sehr Hoch"
- Das Attribut "requestType" klassifiziert den Tickettyp als "Incident" oder "Service Request". "Incident" steht für ein Problem oder eine ähnliche Herausforderung, mit der der Benutzer konfrontiert ist, während "Service Request" für ein Ticket steht, in dem der Benutzer einen Service bestellt.

Bitte liefere 5 Beispiele, die sich auf Folgendes konzentrieren:
1. Ein Problem im Zusammenhang mit Adobe
2. Ein Problem im Zusammenhang mit Atlassian
3. Eine standortbasierte Anfrage (Füge einen der Orte (Fürth, Nürnberg, Berlin, Frankfurt, München) hinzu)
4. Ein Problem im Bereich Reporting
5. Eine Anfrage im Zusammenhang mit Salesforce
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