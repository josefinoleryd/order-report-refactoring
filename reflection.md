**1. Vilka var de viktigaste problemen i orginalkoden?** 

Hela programmet körs vid import, flera ansvar är sammanblandade, ett övergripande ```try-except``` maskerar faktiska fel och beräkningsfunktionerna är svåra att testa.

**2. Vilka förändringar tycker du förbättrade programmet mest?**

De förändringar som förbättrade programmet mest var:

- Uppdelningen i moduler med tydlig ansvarsfördelning: Inläsning, validering, beräkningar och filskrivning separerades i egna filer vilket gjorde koden överskådlig och lättare att underhålla
- Skyddad startpunkt utan sidoeffekter: Flytten av kodkörningen till ```__main__.py``` under en main-guard så att moduler kan importeras utan att hela pipelinen körs.
- Införandet av automatiserade enhetstester med pytest: Funktionerna gjordes testbara och fick tester både för normalfall och felaktig indata.
- Tydlig felhantering och logging istället för dolda fel: Det breda ```try-except```-blocket togs bort till förmån för explicit validering och centraliserad logging av avvikelser.

**3. Varför valde du den projektstruktur du använde?**

Jag valde en standardiserad src-layout av följande skäl:

- Tydlig separation av ansvar: Applikationskoden hålls helt skild från tester, datafiler och projektkonfiguration i roten.
- Förhindrar importfel: Genom att placera kod i src/ kan man inte råka importera lokala filer av misstag vid testning, utan tvingas köra mot det installerade paketet (via ```pip install -e```). Det säkerställer att paketerigen och importvägarna faktiskt fungerar i praktiken.
- Standardiserad och skalbar paketstruktur: Det följer modern Python-praxis (tillsammans med ```pyproject.toml```) vilket gör projektet enkelt att installera, underhålla och bygga vidare på.

**4. Var använde du OOP/dataclass och varför passade det där?**

Jag använde en ```@dataclass(frozen=True)``` för konfigurationen (```ReportConfig``` i ```config.py```)

Kort sagt använder man oftast en vanlig klass när man vill ha logik, metoder och ett internt läg som ändras, medan en dataclass passar när man bara vill paketera ren data utan krångel. Eftersom jag bara behövde samla sökvägarna på ett ställe gav dataclass mig det direkt på två rader utan onödig kod. Med ```frozen=True``` blev inställningarna dessutom låsta så att man inte råkar ändra dem under körningen och i testerna kunde jag enkelt skicka in temporöra mappar (```tmp_path```). 

I resten av projektet valde jag bort klasser helt. För databehandling i Pandas blir det bara onödigt krångligt om en klass ska hålla i datan och komma ihåg ett tillstånd. Där är det mycket smidigare och enklare att använda vanliga funktioner: man skickar in en ```DataFrame```, gör beräkningen och returnerar en ny utan att röra orginalet. 

**5. Vilka viktiga beteenden skyddar dina automatiska tester och vilken nytta ger testerna om programmet förändras i framtiden?**

Mina automatiska tester skyddar framför allt tre kritiska beteenden i programmet: 

- Att beräkningar och affärslogik förblir korrekta: De säkerställer att ordervärden, rabatter och aggregerade nyckeltal räknas ut på exakt samma sätt utan avvikelser. 
- Datatvätt och immutabilitet: De verifierar att saknade värden fylls i enligt reglerna, att kolumner formateras rätt och att funktionerna faktiskt returnerar en ny ```DataFrame``` utan att ändra på indata.
- Defensiv felhantering: De kontrollerar att programmet inte kraschar oväntat, utan kastar tydliga fel (t.ex. ```ValueError```) om obligatoriska kolumner saknas eller om datafilen är tom. 

Nyttan om programmet förändras i framtiden: Testerna fungerar som ett säkerhetsnät (regressionsskydd). Om en utvecklare i framtiden vill optimera koden, lägga till nya kolumner eller ändra hur rapporter sparas, räcker det med att köra ```pytest``` för att direkt se om någon gammal funktionalitet råkade gå sönder. Man slipper testa manuellt och kan göra ändringar med trygghet. 

**6. Vad var svåras?**

Det svåraste var att hitta rätt balans mellan att införa ordentlig validering och datatvätt utan att förändra beräkningsresultatet mot orginalet. När man ser konstigheter i datan (som saknade värden eller felaktig text i numeriska fält) är den spontana reflexen att rensa bort eller kasta fel, men här behövde jag säkerställa att rapporterna i ```output/``` blev helt identiska med facit. Lösningen blev att logga varningar i stället för att ändra datamängden. 

En annan utmaning var hela tänket kring felhanteringen. Det svåraste är sällan de fel som gör att programmet kraschar direkt utan de tysta felen där koden kör på utan problem men ger fel resultat i bakgrunden. Att bygga en robust felhantering som faktiskt fångar upp och synliggör dessa fel krävde en del eftertanke. Just därför kändes det också väldigt skönt att sätta upp testerna och få ett kvitto på att man faktiskt har tänkt rätt och både logiken och avvikelserna hanteras som det är tänkt. 

**7. Vad hade du velat förbättra ytterligare om du haft mer tid?**

Om jag hade haft mer tid hade jag velat vidareutveckla framför allt tre saker: 

- Automatiserad datavalidering med Pandera: Eftersom jag i den andra uppgiften har snöat in på Pandera hade det varit roligt att ta med det tänket hit också. Just nu görs kontroller och loggning med vanlig kod, men med ett deklarativt Pandera-schema hade datatyper, gränsvärden och regler blivit samlade på ett ställe och mycket smidigare att underhålla. 
- Ett riktigt CLI-gränssnitt med argument: Nu körs programmet via fasta sökvägar i konfigurationen, men med ```argparse``` eller ```click``` hade man kunnat låta användaren styra in- och utdatasökvägar direkt från terminalen via flaggor (t.ex. ```--input``` och ```--output```).
- Ännu fler edge cases i testerna: Jag hade velat bygga ut testsviten med fler gränsfall, t.ex. hur systemet reagerar på korrupta CSV-rader eller oväntade teckenkodningar.