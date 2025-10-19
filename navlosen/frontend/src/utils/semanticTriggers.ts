/**
 * Semantic Micro-Challenges System
 *
 * Generates adaptive, semantically-grounded micro-challenges based on:
 * - User's Kairos Window (personality + physiology + emotion)
 * - Recent engagement patterns (low activity detection)
 * - Current polyvagal state
 * - User preferences (opt-in/opt-out)
 *
 * Philosophy:
 * - Challenges are "semantic triggers" - small nudges that respect user's capacity
 * - Adapt complexity and intensity to user's readiness
 * - Track completion but only show stats if user wants to see them
 *
 * Triadisk Score: 0.18 (PROCEED)
 * - Suverenitet: User chooses to enable/disable, controls visibility
 * - Koherens: Challenges grounded in user's actual state
 * - Healing: Builds capacity incrementally, never overwhelming
 */

import { KairosWindow } from './kairosMapping';
import { affectBus, AffectSignal } from './affectBus';

// ============================================================================
// TYPES
// ============================================================================

export type MicroChallengeCategory =
  | 'somatic'      // Body-based (breathing, grounding)
  | 'cognitive'    // Mind-based (reflection, reframing)
  | 'social'       // Connection-based (reach out, share)
  | 'behavioral'   // Action-based (walk, tidy space)
  | 'creative';    // Expression-based (draw, write)

export type MicroChallengeDifficulty = 'easy' | 'medium' | 'hard';

export interface MicroChallenge {
  id: string;
  category: MicroChallengeCategory;
  difficulty: MicroChallengeDifficulty;
  title: string;
  description: string;
  estimatedMinutes: number;
  reasoning: string; // Why this challenge was suggested (for transparency)
  polyvagalMatch: 'ventral' | 'sympathetic' | 'dorsal';
}

export interface ChallengeCompletion {
  challengeId: string;
  completedAt: number; // timestamp
  feltHelpful: boolean | null; // User feedback (optional)
}

export interface ChallengePreferences {
  enabled: boolean;
  showStats: boolean;
  preferredCategories: MicroChallengeCategory[];
  maxDifficulty: MicroChallengeDifficulty;
}

// ============================================================================
// STORAGE KEYS
// ============================================================================

const STORAGE_KEY_PREFERENCES = 'navlosen-challenge-preferences';
const STORAGE_KEY_COMPLETIONS = 'navlosen-challenge-completions';
const STORAGE_KEY_CURRENT_CHALLENGE = 'navlosen-current-challenge';

// ============================================================================
// CHALLENGE DATABASE
// ============================================================================

const CHALLENGE_POOL: MicroChallenge[] = [
  // === SOMATIC CHALLENGES ===
  {
    id: 'somatic-breath-468',
    category: 'somatic',
    difficulty: 'easy',
    title: '3 minutter med 4-6-8 pust',
    description: 'Pust inn på 4, hold på 6, pust ut på 8. Dette aktiverer parasympatiske nervesystemet.',
    estimatedMinutes: 3,
    reasoning: 'Pusteteknikker er dokumentert effektive for å regulere stress og angst.',
    polyvagalMatch: 'sympathetic',
  },
  {
    id: 'somatic-grounding-54321',
    category: 'somatic',
    difficulty: 'easy',
    title: '5-4-3-2-1 jordingsøvelse',
    description: 'Finn 5 ting du ser, 4 du føler, 3 du hører, 2 du lukter, 1 du smaker.',
    estimatedMinutes: 5,
    reasoning: 'Sansegrounding hjelper ved dissosiasjon og dysregulering.',
    polyvagalMatch: 'dorsal',
  },
  {
    id: 'somatic-body-scan',
    category: 'somatic',
    difficulty: 'medium',
    title: 'Kort kroppsscanning',
    description: 'Gå langsomt gjennom kroppen fra topp til tå. Legg merke til spenninger uten å dømme.',
    estimatedMinutes: 7,
    reasoning: 'Øker interoceptiv bevissthet - evnen til å kjenne egne kroppslige signaler.',
    polyvagalMatch: 'ventral',
  },
  {
    id: 'somatic-hand-heart',
    category: 'somatic',
    difficulty: 'easy',
    title: 'Hånd på hjertet',
    description: 'Legg en hånd på hjertet i 2 minutter. Kjenn varmen. Pust rolig.',
    estimatedMinutes: 2,
    reasoning: 'Fysisk berøring av hjerteområdet kan aktivere vagusnerven og skape trygghet.',
    polyvagalMatch: 'dorsal',
  },

  // === COGNITIVE CHALLENGES ===
  {
    id: 'cognitive-3-gratitudes',
    category: 'cognitive',
    difficulty: 'easy',
    title: 'Skriv ned 3 ting du er takknemlig for',
    description: 'Store eller små ting - alt teller. Hvorfor er du takknemlig for akkurat dette?',
    estimatedMinutes: 5,
    reasoning: 'Takknemlighet flytter oppmerksomhet fra trussel til ressurs, styrker ventral tonus.',
    polyvagalMatch: 'ventral',
  },
  {
    id: 'cognitive-worry-time',
    category: 'cognitive',
    difficulty: 'medium',
    title: 'Planlagt bekymringstid (10 min)',
    description: 'Sett av 10 minutter til å bekymre deg intenst. Når tiden er ute, gå videre.',
    estimatedMinutes: 10,
    reasoning: 'Strukturert bekymring kan redusere grubletrang resten av dagen.',
    polyvagalMatch: 'sympathetic',
  },
  {
    id: 'cognitive-reframe-thought',
    category: 'cognitive',
    difficulty: 'medium',
    title: 'Omformuler en negativ tanke',
    description: 'Ta en tøff tanke du hadde i dag. Kan du finne en alternativ tolkning?',
    estimatedMinutes: 8,
    reasoning: 'Kognitiv omstrukturering er kjerneverktøy i KBT for angst og depresjon.',
    polyvagalMatch: 'sympathetic',
  },
  {
    id: 'cognitive-future-self',
    category: 'cognitive',
    difficulty: 'hard',
    title: 'Skriv et brev til fremtids-deg',
    description: 'Hva vil du fortelle deg selv om 6 måneder? Hva håper du å ha lært?',
    estimatedMinutes: 15,
    reasoning: 'Narrativ identitetsarbeid styrker mestringsopplevelse og autonomi.',
    polyvagalMatch: 'ventral',
  },

  // === SOCIAL CHALLENGES ===
  {
    id: 'social-reach-out',
    category: 'social',
    difficulty: 'medium',
    title: 'Send en melding til noen du liker',
    description: 'Bare "hei, tenkte på deg". Ingen forventning om svar med en gang.',
    estimatedMinutes: 3,
    reasoning: 'Sosial forbindelse er den sterkeste buffereffekten mot stress.',
    polyvagalMatch: 'ventral',
  },
  {
    id: 'social-share-feeling',
    category: 'social',
    difficulty: 'hard',
    title: 'Del hvordan du egentlig har det',
    description: 'Med én person du stoler på. Ikke pynt på det.',
    estimatedMinutes: 10,
    reasoning: 'Autentisk deling av sårbarhet styrker tilknytning og reduserer ensomhet.',
    polyvagalMatch: 'dorsal',
  },
  {
    id: 'social-active-listening',
    category: 'social',
    difficulty: 'medium',
    title: 'Øv på aktiv lytting',
    description: 'I neste samtale: lytt uten å planlegge hva du skal si. Reflekter tilbake.',
    estimatedMinutes: 15,
    reasoning: 'Co-regulering gjennom empatisk tilstedeværelse styrker ventral vagal tonus.',
    polyvagalMatch: 'ventral',
  },

  // === BEHAVIORAL CHALLENGES ===
  {
    id: 'behavioral-walk-nature',
    category: 'behavioral',
    difficulty: 'easy',
    title: '10 minutters gåtur ute',
    description: 'Ingen mobil. Bare deg og naturen (eller byen).',
    estimatedMinutes: 10,
    reasoning: 'Fysisk aktivitet + naturkontakt har robust evidens for å redusere stress.',
    polyvagalMatch: 'sympathetic',
  },
  {
    id: 'behavioral-tidy-space',
    category: 'behavioral',
    difficulty: 'easy',
    title: 'Rydd ett lite område',
    description: 'Skrivebordet, en skuff, eller bare nattbordet. Én liten ting.',
    estimatedMinutes: 10,
    reasoning: 'Ytre orden kan skape indre ro. Mestringsopplevelse gjennom konkret handling.',
    polyvagalMatch: 'dorsal',
  },
  {
    id: 'behavioral-phone-free-hour',
    category: 'behavioral',
    difficulty: 'medium',
    title: 'Én time uten mobil',
    description: 'Slå av varsler. Legg telefonen i en annen rom. Hva skjer?',
    estimatedMinutes: 60,
    reasoning: 'Digital detox reduserer kognitivt stress og øker tilstedeværelse.',
    polyvagalMatch: 'sympathetic',
  },
  {
    id: 'behavioral-bedtime-routine',
    category: 'behavioral',
    difficulty: 'medium',
    title: 'Lag en kveldsrutine',
    description: '3 aktiviteter du alltid gjør før du legger deg. Skriv dem ned.',
    estimatedMinutes: 15,
    reasoning: 'Rutiner skaper forutsigbarhet, noe som er trygt for nervesystemet.',
    polyvagalMatch: 'dorsal',
  },

  // === CREATIVE CHALLENGES ===
  {
    id: 'creative-doodle',
    category: 'creative',
    difficulty: 'easy',
    title: 'Tegn noe abstrakt',
    description: 'Ingen regler. Bare penn og papir. Hva kommer ut?',
    estimatedMinutes: 10,
    reasoning: 'Kreativ utfoldelse aktiverer ventral vagal tonus og reduserer perfeksjonisme.',
    polyvagalMatch: 'ventral',
  },
  {
    id: 'creative-freewrite',
    category: 'creative',
    difficulty: 'medium',
    title: '5 minutters fri skriving',
    description: 'Skriv uten å stoppe. Ingen korrektur. Hva enn som dukker opp.',
    estimatedMinutes: 5,
    reasoning: 'Ekspressiv skriving har dokumentert effekt på mental helse og stressreduksjon.',
    polyvagalMatch: 'sympathetic',
  },
  {
    id: 'creative-playlist',
    category: 'creative',
    difficulty: 'easy',
    title: 'Lag en "følelse-spilleliste"',
    description: 'Velg 5 sanger som matcher hvordan du har det nå. Eller hvordan du vil ha det.',
    estimatedMinutes: 10,
    reasoning: 'Musikk påvirker autonome nervesystemet direkte via auditiv vagal stimulering.',
    polyvagalMatch: 'ventral',
  },
  {
    id: 'creative-photo-walk',
    category: 'creative',
    difficulty: 'medium',
    title: 'Ta 10 bilder av "skjønnhet"',
    description: 'Gå en tur og fotografer 10 ting du synes er vakre. Små detaljer teller.',
    estimatedMinutes: 20,
    reasoning: 'Estetisk oppmerksomhet bygger bro mellom kognisjon og affekt.',
    polyvagalMatch: 'ventral',
  },
];

// ============================================================================
// PREFERENCE MANAGEMENT
// ============================================================================

export function getDefaultPreferences(): ChallengePreferences {
  return {
    enabled: false, // Opt-in by default
    showStats: false,
    preferredCategories: ['somatic', 'cognitive', 'behavioral', 'social', 'creative'],
    maxDifficulty: 'hard',
  };
}

export function loadPreferences(): ChallengePreferences {
  if (typeof window === 'undefined') return getDefaultPreferences();

  try {
    const stored = localStorage.getItem(STORAGE_KEY_PREFERENCES);
    if (!stored) return getDefaultPreferences();

    const parsed = JSON.parse(stored);
    return { ...getDefaultPreferences(), ...parsed };
  } catch (e) {
    console.error('Failed to load challenge preferences', e);
    return getDefaultPreferences();
  }
}

export function savePreferences(prefs: ChallengePreferences): void {
  if (typeof window === 'undefined') return;

  try {
    localStorage.setItem(STORAGE_KEY_PREFERENCES, JSON.stringify(prefs));
  } catch (e) {
    console.error('Failed to save challenge preferences', e);
  }
}

// ============================================================================
// COMPLETION TRACKING
// ============================================================================

export function loadCompletions(): ChallengeCompletion[] {
  if (typeof window === 'undefined') return [];

  try {
    const stored = localStorage.getItem(STORAGE_KEY_COMPLETIONS);
    if (!stored) return [];

    return JSON.parse(stored);
  } catch (e) {
    console.error('Failed to load challenge completions', e);
    return [];
  }
}

export function saveCompletion(completion: ChallengeCompletion): void {
  if (typeof window === 'undefined') return;

  try {
    const completions = loadCompletions();
    completions.push(completion);

    // Keep only last 100 completions to avoid bloat
    const trimmed = completions.slice(-100);

    localStorage.setItem(STORAGE_KEY_COMPLETIONS, JSON.stringify(trimmed));
  } catch (e) {
    console.error('Failed to save challenge completion', e);
  }
}

export function getChallengeStats() {
  const completions = loadCompletions();
  const last7Days = Date.now() - (7 * 24 * 60 * 60 * 1000);
  const last30Days = Date.now() - (30 * 24 * 60 * 60 * 1000);

  const completedLast7Days = completions.filter(c => c.completedAt > last7Days).length;
  const completedLast30Days = completions.filter(c => c.completedAt > last30Days).length;
  const totalCompleted = completions.length;

  const helpfulCount = completions.filter(c => c.feltHelpful === true).length;
  const helpfulPercentage = completions.length > 0
    ? Math.round((helpfulCount / completions.length) * 100)
    : 0;

  return {
    completedLast7Days,
    completedLast30Days,
    totalCompleted,
    helpfulPercentage,
  };
}

// ============================================================================
// LOW ENGAGEMENT DETECTION
// ============================================================================

/**
 * Detects if user has low engagement (hasn't checked in recently)
 * Returns true if:
 * - No affect signals in last 24 hours, OR
 * - No emotions logged in last 48 hours
 */
export function detectLowEngagement(): boolean {
  const latestAffect = affectBus.getLatest();
  const now = Date.now();
  const last24Hours = now - (24 * 60 * 60 * 1000);
  const last48Hours = now - (48 * 60 * 60 * 1000);

  // Check affect signals
  if (!latestAffect || latestAffect.timestamp < last24Hours) {
    return true;
  }

  // Check emotion logging
  if (typeof window !== 'undefined') {
    try {
      const emotionsStr = localStorage.getItem('navlosen-emotions');
      if (!emotionsStr) return true;

      const emotions = JSON.parse(emotionsStr);
      if (!Array.isArray(emotions) || emotions.length === 0) return true;

      // Check if most recent emotion is older than 48 hours
      // (Assuming emotions have timestamps - if not, we can't tell)
      const recentEmotions = emotions.filter((e: any) => {
        return e.timestamp && e.timestamp > last48Hours;
      });

      if (recentEmotions.length === 0) return true;
    } catch (e) {
      console.error('Failed to check emotion history', e);
    }
  }

  return false;
}

// ============================================================================
// CHALLENGE GENERATION
// ============================================================================

/**
 * Generates an adaptive micro-challenge based on user's current state
 */
export function generateMicroChallenge(
  polyvagalState: 'ventral' | 'sympathetic' | 'dorsal',
  kairosWindow: KairosWindow | null
): MicroChallenge | null {
  const prefs = loadPreferences();

  // If user has disabled challenges, return null
  if (!prefs.enabled) {
    return null;
  }

  // Filter challenges by polyvagal match and user preferences
  let candidates = CHALLENGE_POOL.filter(challenge => {
    // Must match polyvagal state
    if (challenge.polyvagalMatch !== polyvagalState) return false;

    // Must be in preferred categories
    if (!prefs.preferredCategories.includes(challenge.category)) return false;

    // Must not exceed max difficulty
    const difficultyOrder: MicroChallengeDifficulty[] = ['easy', 'medium', 'hard'];
    const challengeDiffIdx = difficultyOrder.indexOf(challenge.difficulty);
    const maxDiffIdx = difficultyOrder.indexOf(prefs.maxDifficulty);
    if (challengeDiffIdx > maxDiffIdx) return false;

    return true;
  });

  // If Kairos Window available, further filter by complexity match
  if (kairosWindow) {
    const { complexity } = kairosWindow;

    if (complexity === 'low') {
      // Prefer easy challenges
      const easyCandidates = candidates.filter(c => c.difficulty === 'easy');
      if (easyCandidates.length > 0) {
        candidates = easyCandidates;
      }
    } else if (complexity === 'high') {
      // Allow all, but prefer hard
      const hardCandidates = candidates.filter(c => c.difficulty === 'hard');
      if (hardCandidates.length > 0) {
        candidates = [...hardCandidates, ...candidates.filter(c => c.difficulty !== 'hard')];
      }
    }
    // Medium complexity: no preference
  }

  if (candidates.length === 0) {
    return null;
  }

  // Check if user already has a current challenge (don't spam)
  const currentChallenge = getCurrentChallenge();
  if (currentChallenge) {
    const challengeAge = Date.now() - currentChallenge.generatedAt;
    const oneDayMs = 24 * 60 * 60 * 1000;

    // If current challenge is less than 1 day old, return it
    if (challengeAge < oneDayMs) {
      return currentChallenge.challenge;
    }
  }

  // Avoid recently completed challenges
  const completions = loadCompletions();
  const recentCompletions = completions
    .filter(c => c.completedAt > Date.now() - (7 * 24 * 60 * 60 * 1000))
    .map(c => c.challengeId);

  const freshCandidates = candidates.filter(
    c => !recentCompletions.includes(c.id)
  );

  const finalCandidates = freshCandidates.length > 0 ? freshCandidates : candidates;

  // Randomly select one
  const selected = finalCandidates[Math.floor(Math.random() * finalCandidates.length)];

  // Store as current challenge
  setCurrentChallenge(selected);

  return selected;
}

/**
 * Gets the current active challenge (if any)
 */
export function getCurrentChallenge(): { challenge: MicroChallenge; generatedAt: number } | null {
  if (typeof window === 'undefined') return null;

  try {
    const stored = localStorage.getItem(STORAGE_KEY_CURRENT_CHALLENGE);
    if (!stored) return null;

    return JSON.parse(stored);
  } catch (e) {
    console.error('Failed to load current challenge', e);
    return null;
  }
}

/**
 * Sets the current active challenge
 */
export function setCurrentChallenge(challenge: MicroChallenge): void {
  if (typeof window === 'undefined') return;

  try {
    const data = {
      challenge,
      generatedAt: Date.now(),
    };
    localStorage.setItem(STORAGE_KEY_CURRENT_CHALLENGE, JSON.stringify(data));
  } catch (e) {
    console.error('Failed to save current challenge', e);
  }
}

/**
 * Clears the current challenge (after completion or dismissal)
 */
export function clearCurrentChallenge(): void {
  if (typeof window === 'undefined') return;

  try {
    localStorage.removeItem(STORAGE_KEY_CURRENT_CHALLENGE);
  } catch (e) {
    console.error('Failed to clear current challenge', e);
  }
}
