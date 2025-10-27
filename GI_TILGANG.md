# Gi Tilgang til 14 Databaser

## Din Integration
**Navn:** Homo Lumen MCP Automation
**Workspace:** Osvald P. A. Johansen sin Notion

---

## Hvordan Gi Tilgang (For Hver Database)

### Trinn-for-Trinn:

1. **Klikk på database-linken** (fra listen under)
2. **Klikk "..." menyen** (øverst til høyre i databasen)
3. **Velg "Connections"** eller **"Tilkoblinger"**
4. **Finn "Homo Lumen MCP Automation"** i listen
5. **Klikk på den** for å gi tilgang
6. **Klikk "Bekreft"** eller **"Confirm"**
7. **Hak av** i listen under når ferdig

---

## Database Liste (Klikk for å åpne)

### Navngitte Databaser
- [ ] 1. [Spektral Dimensjoner](https://www.notion.so/Spektral-Dimensjoner-1d48fec9293180929092f2553a9f85aa)
- [ ] 2. [Phoenix-syklus](https://www.notion.so/Phoenix-syklus-1d48fec92931807b9e27c445b9840539)
- [ ] 3. [How we feel](https://www.notion.so/How-we-feel-1d48fec9293180b393c5c62a002280d0)
- [ ] 4. [Dagbok 2020 EchoLog](https://www.notion.so/Dagbok-2020-EchoLog-1db8fec9293180caa349fbe34ba1097e)

### Andre Databaser (se navn når du åpner dem)
- [ ] 5. [Database 5](https://www.notion.so/1dd8fec9293180298d8bd2c5d5330563) - Navn: _______________
- [ ] 6. [Database 6](https://www.notion.so/1dd8fec92931808ebc38ce8fc988b1a0) - Navn: _______________
- [ ] 7. [Database 7](https://www.notion.so/1dd8fec929318061be62facd8439da53) - Navn: _______________
- [ ] 8. [Database 8](https://www.notion.so/1e68fec9293180ba9264dd5dafbf53b6) - Navn: _______________
- [ ] 9. [Database 9](https://www.notion.so/1e68fec929318052afe2fe6ee282108e) - Navn: _______________
- [ ] 10. [Database 10](https://www.notion.so/1e68fec929318069bd61e2a8f22221f7) - Navn: _______________
- [ ] 11. [Database 11](https://www.notion.so/28e8fec9293180cbaa57d99549147b97) - Navn: _______________
- [ ] 12. [Database 12](https://www.notion.so/28e8fec929318056a2dcc2bb28fd166d) - Navn: _______________
- [ ] 13. [Database 13](https://www.notion.so/8b18dd1769ab48a6a70ec38b74e5140f) - Navn: _______________
- [ ] 14. [Database 14](https://www.notion.so/2988fec9293180509658e93447b3b259) - Navn: _______________

---

## Etter Du Er Ferdig

Når alle 14 databaser har tilgang, kjør:

```bash
python check_discovered_databases.py
```

Du skal da se:
- Navn på alle 14 databaser
- Properties/kolonner i hver database
- "Successfully retrieved 14/14 database schemas"

---

## Tips
- **Går raskere:** Åpne alle linkene i egne tabs først, gi så tilgang i hver tab
- **Kan ikke finne "Connections"?** Prøv å høyreklikke på database-tittelen
- **Får fortsatt 401 error?** Sjekk at du valgte riktig integration ("Homo Lumen MCP Automation")

**Estimert tid:** 10-15 minutter
