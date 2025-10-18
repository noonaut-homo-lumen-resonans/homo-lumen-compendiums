# main.py - FASTMCP MED NOTION-INTEGRASJON
from fastmcp import FastMCP
from datetime import datetime
import json
import os
from notion_integration_fixed import SentinellNotionUpdater

# Environment variables
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
SENTINELL_PAGE_ID = os.getenv("SENTINELL_PAGE_ID", "")

# Opprett MCP server
mcp = FastMCP(name="SentinellMCPAutomation")

# Global storage + Notion updater
insights_store = []
sentinell_updates = []

# Notion updater setup
notion_updater = None
if NOTION_TOKEN and SENTINELL_PAGE_ID:
    notion_updater = SentinellNotionUpdater(NOTION_TOKEN, SENTINELL_PAGE_ID)
    print("🔗 Notion integration aktivert!")
else:
    print("⚠️ Notion credentials ikke satt - kun lokal lagring")

# 🚀 MCP TOOLS MED NOTION-INTEGRASJON
@mcp.tool()
def receive_agent_insight(agent_name: str, insight: str, biofelt_validated: bool = False) -> str:
    """Mottar og lagrer innsikter + oppdaterer Sentinell automatisk!"""
    timestamp = datetime.now().isoformat()
    
    insight_data = {
        "timestamp": timestamp,
        "agent_name": agent_name,
        "insight": insight,
        "biofelt_validated": biofelt_validated
    }
    
    # Lagre lokalt
    insights_store.append(insight_data)
    
    # Lagre til fil
    with open("agent_insights.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(insight_data, ensure_ascii=False) + "\n")
    
    # 🚀 AUTOMATISK NOTION-OPPDATERING!
    if notion_updater and len(insights_store) % 3 == 0:  # Hver 3. insight
        notion_updater.update_sentinell_with_insights(insights_store[-5:])  # Siste 5
        print("🌟 Sentinell automatisk oppdatert via Notion API!")
    
    print(f"🌟 Mottatt fra {agent_name}: {insight[:100]}...")
    return f"✅ Innsikt fra {agent_name} lagret OG sendt til Sentinell automatisk!"

@mcp.tool()
def update_sentinell_section(section: str, content: str, source_agent: str) -> str:
    """Oppdaterer spesifikk seksjon i Sentinell-dokumentet"""
    timestamp = datetime.now().isoformat()
    
    update_data = {
        "timestamp": timestamp,
        "section": section,
        "content": content,
        "source_agent": source_agent
    }
    
    sentinell_updates.append(update_data)
    
    # Lagre oppdatering til fil
    with open("sentinell_updates.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(update_data, ensure_ascii=False) + "\n")
    
    print(f"📝 Sentinell '{section}' oppdatert av {source_agent}")
    return f"✅ Sentinell seksjon '{section}' oppdatert av {source_agent}"

@mcp.tool()
def get_insights_summary() -> dict:
    """Henter sammendrag av alle agent-innsikter som er lagret"""
    total_insights = len(insights_store)
    latest_insights = insights_store[-5:] if insights_store else []
    
    # Statistikk per agent
    agent_stats = {}
    for insight in insights_store:
        agent = insight["agent_name"]
        agent_stats[agent] = agent_stats.get(agent, 0) + 1
    
    return {
        "total_insights": total_insights,
        "latest_insights": latest_insights,
        "agent_statistics": agent_stats,
        "last_updated": datetime.now().isoformat()
    }

@mcp.tool()
def generate_sentinell_report() -> str:
    """Genererer automatisk rapport for Sentinell basert på alle lagrede innsikter"""
    if not insights_store:
        return "Ingen innsikter funnet for rapport-generering."
    
    # Grupper innsikter per agent
    agent_groups = {}
    for insight in insights_store:
        agent = insight["agent_name"]
        if agent not in agent_groups:
            agent_groups[agent] = []
        agent_groups[agent].append(insight)
    
    # Generer rapport
    report = f"# 🌟 Sentinell Auto-Rapport - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    report += f"**Total innsikter:** {len(insights_store)}\n\n"
    
    for agent, agent_insights in agent_groups.items():
        report += f"## {agent} ({len(agent_insights)} innsikter)\n\n"
        for insight in agent_insights[-3:]:  # Siste 3 per agent
            report += f"- **{insight['timestamp'][:19]}:** {insight['insight'][:200]}...\n"
        report += "\n"
    
    return report

if __name__ == "__main__":
    print("🌟 Starter Sentinell MCP Automation Server...")
    print("🔗 Agenter kan nå koble til via MCP-protokoll!")
    mcp.run()