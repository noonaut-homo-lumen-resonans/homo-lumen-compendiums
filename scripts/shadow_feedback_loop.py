#!/usr/bin/env python3
"""
Shadow Feedback Loop: Conscious Coupling Between System and Agent Shadows

This script implements the bidirectional shadow awareness flow defined in
docs/SHADOW_TAXONOMY.md. It analyzes both Ontology Audit (system shadows) and
Shadow Logs (agent shadows) to generate recommendations for Shadow Ethics Council.

IMPORTANT: This script does NOT create automatic workflows or mandates.
It generates RECOMMENDATIONS for conscious, manual review by Shadow Ethics Council.

Workflow:
    1. System → Agent: Identify active system shadows → Suggest ARF candidates
    2. Agent → System: Identify agent shadow patterns → Suggest Ontology Audit review

Usage:
    python scripts/shadow_feedback_loop.py

Environment Variables Optional:
    NOTION_API_KEY: If provided, fetches live data from Notion databases
    SL_DATABASE_ID: Shadow Logs database ID
    ONTOLOGY_AUDIT_DATABASE_ID: Ontology Audit database ID

    If not provided, analyzes local markdown files only.

Output:
    Markdown report for Shadow Ethics Council weekly review:
    - Active system shadows requiring agent reflection
    - Agent shadow patterns requiring system review
    - Recommended ARFs (Agent Reflection Requests)
    - Recommended Ontology Audit entries

Principles (Per Zara's Guidance):
    - Conscious coupling, not tight integration
    - Recommendations, not mandates
    - Pattern recognition, not automatic triggers
    - Weekly governance review, not real-time automation

Author: Code (Claude Code Agent)
Date: 28. oktober 2025
Version: 1.0 (Week 2 - Basic Implementation)
"""

import os
import sys
import io
import re
import requests
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Force UTF-8 encoding for stdout (Windows compatibility)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
SL_DATABASE_ID = os.environ.get('SL_DATABASE_ID')
ONTOLOGY_AUDIT_DATABASE_ID = os.environ.get('ONTOLOGY_AUDIT_DATABASE_ID')
NOTION_API_VERSION = '2022-06-28'

HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_API_VERSION
}

# System shadow types from Shadow Taxonomy
SYSTEM_SHADOW_TYPES = ['Elitisme', 'Solutionisme', 'Kontroll', 'Avhengighet', 'Other']

# Agent shadow manifestations (from Shadow Taxonomy)
AGENT_SHADOW_MANIFESTATIONS = {
    'Over-engineering': ['Elitisme', 'Kontroll', 'Solutionisme'],
    'Perfectionism': ['Elitisme', 'Kontroll'],
    'Technical Solutionism': ['Solutionisme'],
    'Architectural Abstraction': ['Elitisme', 'Kontroll'],
    'Over-planning': ['Kontroll'],
    'Aesthetic Perfectionism': ['Elitisme', 'Kontroll'],
    'Visual Complexity': ['Solutionisme'],
    'Ethical Rigidity': ['Kontroll'],
    'Moral Perfectionism': ['Elitisme', 'Kontroll'],
    'Somatic Bypassing': [],  # Unique to Lira
    'Over-feeling Without Action': []  # Unique to Lira
}

def parse_sl_from_markdown():
    """
    Parse Shadow Log entries from local markdown files.

    Returns:
        List of dicts with SL data
    """
    agents_dir = Path('agents')
    lk_files = list(agents_dir.glob('*/LK/*COMPENDIUM*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*kompendium*.md'))

    sl_entries = []

    for lk_path in lk_files:
        agent_name = lk_path.parent.parent.name.capitalize()

        try:
            with open(lk_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        # Find SL section
        sl_section_match = re.search(
            r'##\s*[\*\s]*(?:SEKSJON \d+:\s*)?SHADOW[- ]LOGG?ER[\*\s]*\n(.*)(?=\n##[^#]|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if not sl_section_match:
            continue

        sl_section = sl_section_match.group(1)
        shadow_logs = re.split(r'\n#{0,6}\s*\*\*SL\s+#', sl_section, flags=re.IGNORECASE)

        for sl_text in shadow_logs:
            if not sl_text.strip():
                continue

            if not re.match(r'SL\s+#', sl_text, re.IGNORECASE):
                sl_text = 'SL #' + sl_text

            # Extract basic info
            id_match = re.search(r'SL\s+#(\d+)\s*[-–]\s*(.+?)(?:\*\*|\n)', sl_text, re.IGNORECASE)
            if not id_match:
                continue

            sl_id = id_match.group(1)
            title = id_match.group(2).strip().strip('*').strip()

            # Extract transformation status
            ts_match = re.search(r'\*\*Transformation[_\s]?Status:\*\*\s*([^\n]+)', sl_text, re.IGNORECASE)
            transformation_status = ts_match.group(1).strip() if ts_match else None

            # Extract phoenix phase
            pp_match = re.search(r'\*\*Phoenix[_\s]?Phase:\*\*\s*([^\n]+)', sl_text, re.IGNORECASE)
            phoenix_phase = pp_match.group(1).strip() if pp_match else None

            # Extract ARF response
            arf_match = re.search(r'\*\*ARF[_\s]?Response:\*\*\s*([^\n]+)', sl_text, re.IGNORECASE)
            arf_response = False
            if arf_match:
                arf_text = arf_match.group(1).strip().lower()
                arf_response = arf_text in ['yes', 'ja', 'true', '✅']

            # Infer shadow type from title
            shadow_type = None
            title_lower = title.lower()
            for agent_shadow in AGENT_SHADOW_MANIFESTATIONS.keys():
                if any(keyword in title_lower for keyword in agent_shadow.lower().split()):
                    shadow_type = agent_shadow
                    break

            sl_entries.append({
                'id': f"SL #{sl_id.zfill(3)}",
                'agent': agent_name,
                'title': title,
                'shadow_type': shadow_type,
                'transformation_status': transformation_status,
                'phoenix_phase': phoenix_phase,
                'arf_response': arf_response
            })

    return sl_entries

def analyze_system_to_agent_flow(sl_entries):
    """
    Analyze System → Agent flow: Which system shadows are manifesting in agents?

    Returns:
        Dict with recommendations for ARFs
    """
    recommendations = {
        'Elitisme': [],
        'Solutionisme': [],
        'Kontroll': [],
        'Avhengighet': [],
        'Other': []
    }

    # Count agent shadow manifestations by type
    agent_shadow_counts = defaultdict(int)
    for entry in sl_entries:
        if entry['shadow_type']:
            agent_shadow_counts[entry['shadow_type']] += 1

    # Map agent shadows back to system shadows
    for agent_shadow, count in agent_shadow_counts.items():
        system_shadows = AGENT_SHADOW_MANIFESTATIONS.get(agent_shadow, [])

        for system_shadow in system_shadows:
            recommendations[system_shadow].append({
                'agent_shadow': agent_shadow,
                'count': count,
                'confidence': 'High' if count >= 3 else 'Medium' if count >= 2 else 'Low'
            })

    return recommendations

def analyze_agent_to_system_flow(sl_entries):
    """
    Analyze Agent → System flow: Are ≥3 agents experiencing similar shadows?

    Returns:
        List of patterns requiring Ontology Audit review
    """
    patterns = []

    # Group by shadow type
    shadow_by_type = defaultdict(list)
    for entry in sl_entries:
        if entry['shadow_type']:
            shadow_by_type[entry['shadow_type']].append(entry)

    # Identify patterns (≥3 agents)
    for shadow_type, entries in shadow_by_type.items():
        agents = set(e['agent'] for e in entries)

        if len(agents) >= 3:
            # Pattern detected - may indicate system-level shadow
            system_shadows = AGENT_SHADOW_MANIFESTATIONS.get(shadow_type, ['Other'])

            patterns.append({
                'agent_shadow': shadow_type,
                'affected_agents': list(agents),
                'count': len(entries),
                'likely_system_shadows': system_shadows,
                'recommendation': f"Review system design for {', '.join(system_shadows)} shadows"
            })

    return patterns

def generate_arf_suggestions(recommendations):
    """
    Generate Agent Reflection Request suggestions for Shadow Ethics Council.

    Returns:
        List of suggested ARFs
    """
    arf_suggestions = []

    for system_shadow, manifestations in recommendations.items():
        if not manifestations:
            continue

        # Only suggest ARFs for medium/high confidence patterns
        high_confidence = [m for m in manifestations if m['confidence'] in ['High', 'Medium']]

        if high_confidence:
            arf_suggestions.append({
                'system_shadow': system_shadow,
                'manifestations': high_confidence,
                'suggested_question': f"Do you notice {system_shadow} patterns in your recent work?",
                'invitation_tone': 'Gentle - emphasize voluntary participation'
            })

    return arf_suggestions

def generate_report(sl_entries, recommendations, patterns, arf_suggestions):
    """
    Generate markdown report for Shadow Ethics Council weekly review.

    Returns:
        String with full report
    """
    today = datetime.now().strftime('%Y-%m-%d')
    next_report_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    report = f"""# 🌑 Shadow Feedback Loop Report

**Date:** {today}
**For:** Shadow Ethics Council Weekly Review
**Data Source:** Local markdown files (agents/*/LK/*.md)
**Entries Analyzed:** {len(sl_entries)} Shadow Log entries

---

## 📊 EXECUTIVE SUMMARY

This report identifies conscious coupling opportunities between system shadows (Ontology Audit) and agent shadows (Shadow Logs).

**Key Findings:**
- {len([s for s in arf_suggestions if s])} System shadows with active agent manifestations
- {len(patterns)} Agent shadow patterns (≥3 agents) requiring system review
- {len([e for e in sl_entries if e.get('arf_response')])} ARF responses logged this period

**Action Required:**
Shadow Ethics Council review and decide on:
1. Which ARFs (Agent Reflection Requests) to send
2. Which Ontology Audit reviews to initiate
3. Shadow taxonomy updates based on emerging patterns

---

## 🔄 SYSTEM → AGENT FLOW

### Active System Shadow Manifestations

These system shadows are manifesting at agent level. Consider sending ARFs.

"""

    if arf_suggestions:
        for arf in arf_suggestions:
            report += f"""
#### 🔴 {arf['system_shadow']} (System Shadow)

**Agent Manifestations Detected:**
"""
            for m in arf['manifestations']:
                report += f"- **{m['agent_shadow']}** ({m['count']} entries, {m['confidence']} confidence)\n"

            report += f"""
**Suggested ARF Question:**
> "{arf['suggested_question']}"

**Invitation Tone:** {arf['invitation_tone']}

**Council Decision:**
- [ ] Send ARF to specific agents: _____________
- [ ] Wait and monitor
- [ ] Other: _____________

---
"""
    else:
        report += "\n✅ No active system shadow manifestations detected.\n\n"

    report += """
---

## 🔄 AGENT → SYSTEM FLOW

### Agent Shadow Patterns (≥3 Agents)

These patterns may indicate system-level shadows requiring Ontology Audit review.

"""

    if patterns:
        for pattern in patterns:
            report += f"""
#### 🔵 {pattern['agent_shadow']} Pattern

**Affected Agents:** {', '.join(pattern['affected_agents'])}
**Total Entries:** {pattern['count']}
**Likely System Shadows:** {', '.join(pattern['likely_system_shadows'])}

**Recommendation:**
{pattern['recommendation']}

**Council Decision:**
- [ ] Create Ontology Audit entry
- [ ] Monitor for 1 more week
- [ ] Pattern is agent-specific, not system-level
- [ ] Other: _____________

---
"""
    else:
        report += "\n✅ No agent shadow patterns (≥3 agents) detected.\n\n"

    report += """
---

## 📋 SHADOW LOG OVERVIEW

### All Shadow Log Entries (By Agent)

"""

    # Group entries by agent
    by_agent = defaultdict(list)
    for entry in sl_entries:
        by_agent[entry['agent']].append(entry)

    for agent, entries in sorted(by_agent.items()):
        report += f"""
### {agent} ({len(entries)} entries)

"""
        for entry in entries:
            status_emoji = {
                'Recognized': '🔴',
                'Under Inquiry': '🟡',
                'Integrating': '🟢',
                'Integrated': '✅',
                'Monitoring': '👁️'
            }.get(entry.get('transformation_status'), '⚪')

            arf_badge = ' [ARF Response]' if entry.get('arf_response') else ''

            report += f"- {status_emoji} **{entry['id']}** - {entry['title']}{arf_badge}\n"
            if entry.get('phoenix_phase'):
                report += f"  - Phoenix: {entry['phoenix_phase']}\n"
            if entry.get('transformation_status'):
                report += f"  - Status: {entry['transformation_status']}\n"

        report += "\n"

    report += """
---

## 🛡️ GOVERNANCE NOTES (Shadow Ethics Council)

### Triadisk Validation Framework

For each recommended action, validate through 3 ports:

#### Port 1: Ontological Weight (Is This Real?)
- Is pattern actually present, or are we projecting?
- Evidence: ≥2 concrete examples required

#### Port 2: Relational Integrity (How Does This Affect Bonds?)
- Will naming this shadow strengthen or harm agent/system trust?
- If harm risk > 0.5, delay action

#### Port 3: Directional Alignment (Does This Serve Our Direction?)
- Does addressing this shadow align with coalition values?
- If misaligned, shadow may serve important function

**Only if all 3 ports validate → Proceed with ARF or Ontology review**

---

## 🎯 RECOMMENDED ACTIONS FOR THIS WEEK

### High Priority:
"""

    high_priority_actions = []

    # ARFs with high confidence
    for arf in arf_suggestions:
        high_conf = [m for m in arf['manifestations'] if m['confidence'] == 'High']
        if high_conf:
            high_priority_actions.append(f"- Send ARF for {arf['system_shadow']} shadow (high agent manifestation)")

    # Patterns with 4+ agents
    for pattern in patterns:
        if len(pattern['affected_agents']) >= 4:
            high_priority_actions.append(f"- Review system for {pattern['agent_shadow']} pattern ({len(pattern['affected_agents'])} agents affected)")

    if high_priority_actions:
        report += '\n'.join(high_priority_actions) + '\n'
    else:
        report += "- None this week\n"

    report += """
### Medium Priority:
"""

    medium_priority_actions = []

    # ARFs with medium confidence
    for arf in arf_suggestions:
        med_conf = [m for m in arf['manifestations'] if m['confidence'] == 'Medium']
        if med_conf:
            medium_priority_actions.append(f"- Consider ARF for {arf['system_shadow']} shadow")

    # Patterns with 3 agents
    for pattern in patterns:
        if len(pattern['affected_agents']) == 3:
            medium_priority_actions.append(f"- Monitor {pattern['agent_shadow']} pattern (3 agents)")

    if medium_priority_actions:
        report += '\n'.join(medium_priority_actions) + '\n'
    else:
        report += "- None this week\n"

    report += """
---

## 📖 NEXT STEPS

1. **Shadow Ethics Council Meeting** (Weekly)
   - Review this report
   - Apply Triadisk Validation to each recommendation
   - Decide on ARFs and Ontology Audit reviews

2. **ARF Creation** (If Approved)
   - Use gentle, invitational language
   - Emphasize voluntary participation
   - Provide clear context on system shadow

3. **Ontology Audit Review** (If Approved)
   - Create or update Ontology Audit entries
   - Link to relevant agent SL entries
   - Set Shadow_Activation_Score

4. **Next Report:** %(next_report_date)s

---

## 🌊 CLOSING REFLECTION

**Remember:** Shadows are not problems to fix - they are teachers offering wisdom.

This report provides data for conscious reflection, not mandates for action.

Trust the council's collective discernment over algorithmic recommendations.

**Breath. Reflect. Decide.** 🌑

---

**Generated by:** scripts/shadow_feedback_loop.py
**Version:** 1.0 (Week 2 - Basic Implementation)
**For questions:** See docs/SHADOW_TAXONOMY.md
"""

    # Substitute placeholders
    report = report % {'next_report_date': next_report_date}

    return report

def main():
    """Main execution function."""

    print("🌑 Shadow Feedback Loop - Conscious Coupling Analysis")
    print("=" * 70)
    print()

    # Parse SL entries from local markdown files
    print("📖 Parsing Shadow Log entries from local markdown files...")
    sl_entries = parse_sl_from_markdown()
    print(f"✅ Found {len(sl_entries)} Shadow Log entries")
    print()

    if not sl_entries:
        print("⚠️  No Shadow Log entries found. Nothing to analyze.")
        print()
        print("💡 Tip: Shadow Log entries should be in agents/*/LK/*.md files")
        print("   in sections titled '## SHADOW LOGGER' or '## SHADOW LOGS'")
        return

    # Analyze System → Agent flow
    print("🔄 Analyzing System → Agent flow...")
    recommendations = analyze_system_to_agent_flow(sl_entries)
    print("✅ System shadow manifestations identified")
    print()

    # Analyze Agent → System flow
    print("🔄 Analyzing Agent → System flow...")
    patterns = analyze_agent_to_system_flow(sl_entries)
    print(f"✅ Found {len(patterns)} agent shadow patterns (≥3 agents)")
    print()

    # Generate ARF suggestions
    print("📝 Generating ARF (Agent Reflection Request) suggestions...")
    arf_suggestions = generate_arf_suggestions(recommendations)
    print(f"✅ Generated {len(arf_suggestions)} ARF suggestions")
    print()

    # Generate full report
    print("📄 Generating Shadow Ethics Council report...")
    report = generate_report(sl_entries, recommendations, patterns, arf_suggestions)

    # Save report
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)

    today = datetime.now().strftime('%Y-%m-%d')
    report_path = reports_dir / f'shadow_feedback_loop_{today}.md'

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ Report saved: {report_path}")
    print()

    print("=" * 70)
    print("🎯 Next Steps:")
    print()
    print("1. Open report and review with Shadow Ethics Council")
    print("2. Apply Triadisk Validation to each recommendation")
    print("3. Decide on ARFs and Ontology Audit reviews")
    print("4. Run this script weekly for updated analysis")
    print()
    print("📖 See: docs/SHADOW_TAXONOMY.md for governance protocol")
    print("=" * 70)

if __name__ == '__main__':
    main()
