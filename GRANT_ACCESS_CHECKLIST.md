# Database Access Checklist

Quick checklist for granting API access to the 14 discovered databases.

## Step 1: Find Your Integration
- [ ] Go to https://www.notion.so/my-integrations
- [ ] Find integration with key `4dcd1dce-c52d-43df-9505-ed0b3061f9f2`
- [ ] Note integration name: ___________________

## Step 2: Grant Access to Each Database

### Named Databases
- [ ] [Spektral Dimensjoner](https://www.notion.so/Spektral-Dimensjoner-1d48fec9293180929092f2553a9f85aa) → "..." → Connections → [Your Integration]
- [ ] [Phoenix-syklus](https://www.notion.so/Phoenix-syklus-1d48fec92931807b9e27c445b9840539) → "..." → Connections → [Your Integration]
- [ ] [How we feel](https://www.notion.so/How-we-feel-1d48fec9293180b393c5c62a002280d0) → "..." → Connections → [Your Integration]
- [ ] [Dagbok 2020 EchoLog](https://www.notion.so/Dagbok-2020-EchoLog-1db8fec9293180caa349fbe34ba1097e) → "..." → Connections → [Your Integration]

### Numbered Databases (Note Names When You Open Them)
- [ ] [Database 5](https://www.notion.so/1dd8fec9293180298d8bd2c5d5330563) - Name: ___________________
- [ ] [Database 6](https://www.notion.so/1dd8fec92931808ebc38ce8fc988b1a0) - Name: ___________________
- [ ] [Database 7](https://www.notion.so/1dd8fec929318061be62facd8439da53) - Name: ___________________
- [ ] [Database 8](https://www.notion.so/1e68fec9293180ba9264dd5dafbf53b6) - Name: ___________________
- [ ] [Database 9](https://www.notion.so/1e68fec929318052afe2fe6ee282108e) - Name: ___________________
- [ ] [Database 10](https://www.notion.so/1e68fec929318069bd61e2a8f22221f7) - Name: ___________________
- [ ] [Database 11](https://www.notion.so/28e8fec9293180cbaa57d99549147b97) - Name: ___________________
- [ ] [Database 12](https://www.notion.so/28e8fec929318056a2dcc2bb28fd166d) - Name: ___________________
- [ ] [Database 13](https://www.notion.so/8b18dd1769ab48a6a70ec38b74e5140f) - Name: ___________________
- [ ] [Database 14](https://www.notion.so/2988fec9293180509658e93447b3b259) - Name: ___________________

## Step 3: Verify Access
- [ ] Run: `python check_discovered_databases.py`
- [ ] Check output shows "Successfully retrieved 14/14 database schemas"
- [ ] Review file: `discovered_database_schemas.json`

## Step 4: Report Back
Once all checkboxes are complete, let Code know so we can:
- Analyze database schemas
- Recommend integration priorities
- Create parser scripts for selected databases

---

**Estimated Time:** 10-15 minutes
**See Full Guide:** [docs/GRANT_DATABASE_ACCESS.md](docs/GRANT_DATABASE_ACCESS.md)
