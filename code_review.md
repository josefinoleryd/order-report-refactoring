# Kodgranskning av order_report.py

## Utgångsläge 

Skriptet går att köra och skapar rapporter över bl.a. försäljning och returer.

## Sammanfattning 

Skriptet genererar korrekta rapporter, men saknar funktioner och modularitet vilket gör det svårt att enhetstesta. En omstrukturering kan förbättra kodens läsbarhet och underhållbarhet samtidigt som beräkningsresultaten förblir oförändrade.

## Granskningsfynd

### Fynd 1 - Hela programmet körs vid import

**Observation:** Hela arbetsflödet körs på modulnivå utan funktioner eller startpunkt.

**Konsekvens:** Import läser och skriver filer, vilket ger oväntade sidoeffekter och gör koden svår att återanvända och testa.

**Förslag:** Kapsla in körningen i en `main()`-funktion och skydda anropet med en main-guard (`if __name__ == "__main__":`).

**Prioritet**: Hög

### Fynd 2 - Flera ansvar är sammanblandade

**Observation:** Skriptet blandar filinläsning, datatvätt, affärslogik, aggregering och filskrivning i en enda linjär sekvens.

**Konsekvens:** Delarna kan inte testas eller återanvändas oberoende av varandra. Olika typer av förändringar behöver göras på samma ställe.

**Förslag:** Separera ren transformationslogik från filhantering och orkestrering i dedikerade moduler. 

**Prioritet**: Hög

### Fynd 3 - Valideringen ger ett generellt fel 

**Observation:** Valideringen kastar `Exception("Fel data")`om kolumner saknas. 

**Konsekvens:** Felet är svårt att felsöka och svårt att kontrollera specifikt i ett test. Det framgår inte vilka kolumner som saknas.

**Förslag:** Kasta `ValueError`och inkludera namnen på de saknade kolumnerna i felmeddelandet. 

**Prioritet**: Medel

### Fynd 4 - Övergripande try-except maskerar faktiska fel

**Observation:** Hela programmets flöde ligger inuti ett generellt `try-except Exception`-block på modulnivå.

**Konsekvens:** Verkliga fel fångas tyst och skrivs ut som en vanlig textsträng istället för att ge en traceback. Exempel: Råkar man göra ett stavfel (som `datta`istället för `data`), får man bara meddelandet `Något gick fel: name 'datta' is not defined'`utan om vilken rad som orsakade felet. Det försvårar felsökning och gör att skriptet felaktigt rapporterar en lyckad körning till operativsystemet trots att inga rapporter skapades.

**Förslag:** Ta bort det övergripande try-blocket på modulnivå och låt oväntade buggar krascha med en full traceback. Använd endast specifik felhantering där fel faktiskt förväntas uppstå och kan hanteras meningsfullt.

**Prioritet**: Hög

### Fynd 5 - Dold förutsättning och hårdkodade sökvägar

**Observation:** Sökvägen `OUTPUT_FOLDER = "output"`ligger hårdkodad och skriptet förutsätter att mappen redan finns på datorn.

**Konsekvens:** Om någon klonar projektet och mappen saknas kraschar skriptet direkt när filerna ska sparas. Mappen är en dold förutsättning för att koden ska fungera. 

**Förslag:** Låt exportfunktionen automatiskt skapa målmappen om den saknas innan filerna skrivs. 

**Prioritet**: Medel

### Fynd 6 - Statusmeddelanden använder print 

**Observation** `print()`används för att beskriva att skriptet startar, läser in rader och sparar filer.

**Konsekvens** Det går inte att styra loggnivåer, tidsstämplar eller format, och utskrifterna kan inte stängas av under automatiska tester. 

**Förslag** Använd en modul-logger från Pythons inbyggda `logging`-bibliotek istället för `print()`.

**Prioritet**: Medel

### Fynd 7 - Centrala regler saknar tydliga testgränser

**Observation** Beräkningar av `order_value`, `discounted_value` och `returned` är hårt bundna till hela skriptets filflöde. 

**Konsekvens** För att verifiera rabatt- eller returlogiken måste hela skriptet köras mot en fil på hårddisken. Testerna blir långsamma och svåra att isolera. 

**Förslag** Extrahera rena funktioner som tar emot en `DataFrame`och returnerar en ny `DataFrame`, så att de kan testas isolerat med testdata i minnet. 

**Prioritet**: Hög

### Fynd 8 - Namnen beskriver dataflödet dåligt och kod dupliceras

**Observation** Variablerna `result1`och `result2`säger lite om innehållet, och beräkningslogiken för aggregering och `return_rate`upprepas rakt av för båda tabellerna.

**Konsekvens** Dataflödet blir svårt att följa och kodduplicering ökar risken för buggar vid framtida förändringar.

**Förslag** Använd beskrivande namn som `sales_by_category`och `sales_by_region`, samt återanvänd en gemensam beräkningsfunktion. 

**Prioritet**: Låg

### Fynd 9 - Saknar dokumentation och typannoteringar

**Observation** Skriptet saknar docstrings, förklarande kommentarer kring affärsregler och typannoteringar. 

**Konsekvens** Det blir svårt att veta vilka datatyper och kolumner funktioner eller datastrukturer förväntar sig, vilket försvårar vidareutveckling och samarbete.

**Förslag** Dokumentera funktioner med docstrings och lägg till typannoteringar för argument och returvärden vid modulindelningen.

**Prioritet**: Låg

