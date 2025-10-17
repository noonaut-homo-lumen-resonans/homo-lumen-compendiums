#!/usr/bin/env ts-node
/**
 * Linear Issue Sync Script
 *
 * Creates Linear issues from Lira's 8 guidance categories
 * Tagged with Triadic Ethics ports (Port 1, 2, 3)
 *
 * Usage:
 *   npx ts-node scripts/linear-sync.ts
 */

import { LinearClient } from '@linear/sdk';
import dotenv from 'dotenv';

// Load .env file from project root
dotenv.config();

const LINEAR_API_KEY = process.env.LINEAR_API_KEY;

if (!LINEAR_API_KEY) {
  console.error('❌ Error: LINEAR_API_KEY environment variable is required');
  console.error('   Set it in .env file: LINEAR_API_KEY=your_api_key_here');
  process.exit(1);
}

const client = new LinearClient({
  apiKey: LINEAR_API_KEY,
});

/**
 * Lira's 8 Main Categories from her deep guidance
 */
const liraGuidance = [
  {
    title: '🌿 Polyvagal Design - Co-regulation & Tolerance Windows',
    description: `Implement deeper polyvagal anchoring:

**Tasks:**
- [ ] Add breathing circle visualization in dorsal mode (co-regulation)
- [ ] Implement tolerance windows in UI (user capacity check)
- [ ] Create somatic memory visualization (patterns over time)
- [ ] Add subtle breathing rhythm in background during dorsal mode

**Triadisk Ethics:** Port 1 (Suverenitet) + Port 2 (Koherens)
**Priority:** High
**Estimated:** 3-5 days`,
    labels: ['Port 1', 'Port 2', 'Polyvagal', 'High Priority'],
    priority: 1,
  },
  {
    title: '💬 NVC Language - Validation & Needs vs Suggestions',
    description: `Extend NVC microcopy throughout the app:

**Completed:**
✅ Stage 1-4 now have validation before questions
✅ "Suggestions, not requirements" language in Stage 4

**Next Tasks:**
- [ ] Add language feedback buttons (Port 2: user can adjust wording)
- [ ] Implement "observation → feeling → need → request" flow in Stage 3
- [ ] Create emotion word search/filter for 100 emotions
- [ ] Add contextual NVC prompts based on stress state

**Triadisk Ethics:** Port 1 (Suverenitet)
**Priority:** High
**Estimated:** 2-3 days`,
    labels: ['Port 1', 'NVC', 'High Priority', 'In Progress'],
    priority: 1,
  },
  {
    title: '🧘 RAIN Practice - Mini-Module Between Stages',
    description: `Integrate RAIN (Recognize, Allow, Investigate, Nurture) as optional reflection:

**Tasks:**
- [ ] Create RAIN mini-module component
- [ ] Add as optional step between Stage 2 and 3
- [ ] Include audio/text guides for each RAIN phase
- [ ] Self-reflection prompts after Stage 4
- [ ] "Investigate with curiosity" somatic exercise

**Triadisk Ethics:** Port 3 (Healing)
**Priority:** High
**Estimated:** 2-3 days`,
    labels: ['Port 3', 'RAIN', 'High Priority', 'Self-compassion'],
    priority: 1,
  },
  {
    title: '⚖️ Triadic Ethics - Granular User Control',
    description: `Enhance all three Triadic ports with deeper granularity:

**Port 1 (Kognitiv Suverenitet):**
✅ Skip buttons in all stages
- [ ] User can change order of stages
- [ ] Data control dashboard (view, export, delete)
- [ ] Choose which sensors to activate (HR, sleep, etc.)

**Port 2 (Ontologisk Koherens):**
- [ ] Explain recommendation logic transparently
- [ ] Add science context boxes (polyvagal, emotion granularity)
- [ ] Language feedback: "Does this wording feel right?"

**Port 3 (Regenerativ Healing):**
- [ ] Mastery Log (user saves own strategies)
- [ ] Graduation plan (reduce system use over time)
- [ ] Co-regulation with trusted person (share with mentor)

**Priority:** High
**Estimated:** 4-5 days`,
    labels: ['Port 1', 'Port 2', 'Port 3', 'High Priority', 'Ethics'],
    priority: 1,
  },
  {
    title: '🎯 Deep Personalization - Weather, Patterns, HRV',
    description: `Extend personalization beyond current stress state:

**Tasks:**
- [ ] Weather API integration (seasonal affective patterns)
- [ ] Historical pattern analysis (e.g., "exhausted" words recurring)
- [ ] HealthConnect MCP for HRV, pulse, sleep data
- [ ] Interactive learning (adjust slider to see recommendations change)
- [ ] Weekly check-in prompts for deeper issues (burnout detection)

**Triadisk Ethics:** Port 2 (Koherens)
**Priority:** Medium
**Estimated:** 5-7 days`,
    labels: ['Port 2', 'Personalization', 'Medium Priority', 'Data'],
    priority: 2,
  },
  {
    title: '🔒 Privacy & Data Control - Informed Choice',
    description: `Implement transparent data practices:

**Tasks:**
- [ ] Data control dashboard (view all stored data)
- [ ] Export to PDF for therapist/doctor
- [ ] One-click delete (local + server, confirmed within 24h)
- [ ] Sensor permission panel (choose HR, sleep, location)
- [ ] Encryption info banner ("All data is encrypted")
- [ ] Private session mode (memory-only, no storage)

**Triadisk Ethics:** Port 1 (Suverenitet)
**Priority:** Medium
**Estimated:** 3-4 days`,
    labels: ['Port 1', 'Privacy', 'Medium Priority', 'Security'],
    priority: 2,
  },
  {
    title: '📝 Mastery Log & Journaling - Port 3 Graduation',
    description: `Create tools for user to become independent:

**Tasks:**
- [ ] Mastery Log component (user saves their own strategies)
- [ ] Journaling with emotion tags
- [ ] Free text field after Stage 3 or 4
- [ ] Self-compassion guidelines (not perfection)
- [ ] Progress tracking (exercises completed, but optional)
- [ ] Graduation dashboard (show reduced system use over time)

**Triadisk Ethics:** Port 3 (Healing)
**Priority:** High
**Estimated:** 3-4 days`,
    labels: ['Port 3', 'Journaling', 'High Priority', 'Graduation'],
    priority: 1,
  },
  {
    title: '🔗 HealthConnect & External Integrations',
    description: `Prepare for external data sources:

**Tasks:**
- [ ] HealthConnect MCP server setup
- [ ] HRV, pulse, sleep data integration
- [ ] Multi-data calibration for stress state detection
- [ ] Clinical report PDF export (for therapist/doctor)
- [ ] Controlled sharing (snapshot to therapist via Gmail)
- [ ] Weather API for seasonal patterns

**Triadisk Ethics:** Port 2 (Koherens)
**Priority:** Low (future work)
**Estimated:** 7-10 days`,
    labels: ['Port 2', 'Integration', 'Low Priority', 'Future'],
    priority: 3,
  },
];

async function createLinearIssues() {
  try {
    console.log('🔗 Connecting to Linear...');

    // Get viewer (current user)
    const viewer = await client.viewer;
    console.log(`✅ Connected as: ${viewer.name} (${viewer.email})`);

    // Get all teams
    const teams = await client.teams();

    if (!teams.nodes.length) {
      console.error('❌ No teams found. Please create a team in Linear first.');
      return;
    }

    const team = teams.nodes[0];
    console.log(`📋 Using team: ${team.name} (${team.key})`);

    // Create parent epic for Lira's guidance
    console.log('\n🌿 Creating parent epic: "Lira\'s Deep Guidance - NAV-Losen Enhancement"...');

    const epicPayload = await client.createIssue({
      teamId: team.id,
      title: '🌿 Lira\'s Deep Guidance - NAV-Losen Enhancement',
      description: `This epic contains all 8 main categories from Lira's (Agent #3) comprehensive UX guidance for NAV-Losen prototype.

**Focus Areas:**
1. Polyvagal Design (co-regulation, tolerance windows)
2. NVC Language (validation, needs vs suggestions)
3. RAIN Practice (mini-module between stages)
4. Triadic Ethics (Port 1, 2, 3 granularity)
5. Deep Personalization (weather, patterns, HRV)
6. Privacy & Data Control
7. Mastery Log & Journaling
8. HealthConnect Integration

**Philosophy:**
"Møter dette brukerens nåværende kapasitet? Underviser det, regulerer det, og gjør det systemet overflødig på sikt?"

**Date:** ${new Date().toISOString().split('T')[0]}
**Agent:** Agent #9 (Claude Code)
**Reference:** Session notes in .claude/session-notes/`,
      priority: 1,
    });

    const epic = await epicPayload.issue;
    if (!epic) {
      console.error('❌ Failed to create epic');
      return;
    }

    console.log(`✅ Epic created: ${epic.identifier} - ${epic.title}`);

    // Create issues for each category
    console.log('\n📝 Creating issues from Lira\'s 8 categories...\n');

    for (const category of liraGuidance) {
      const issuePayload = await client.createIssue({
        teamId: team.id,
        title: category.title,
        description: category.description,
        priority: category.priority,
        parentId: epic.id,
      });

      const issue = await issuePayload.issue;
      if (issue) {
        console.log(`✅ Created: ${issue.identifier} - ${category.title}`);
      }
    }

    console.log('\n🎉 All issues created successfully!');
    console.log(`\n🔗 View in Linear: https://linear.app/team/${team.key}/project/lira-guidance`);

  } catch (error) {
    console.error('❌ Error:', error);
    throw error;
  }
}

// Run the script
createLinearIssues()
  .then(() => {
    console.log('\n✅ Linear sync complete!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\n❌ Linear sync failed:', error.message);
    process.exit(1);
  });
