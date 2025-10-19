/**
 * Emotion Word Data for HWF-inspired Mestring Flow
 *
 * 100 følelsesord (25 per kvadrant) basert på Marc Brackett's Mood Meter
 * Fra Manus' redesign proposal (19. oktober 2025)
 *
 * Basert på: Circumplex Model (Energy × Valence)
 */

export type EmotionWord = {
  id: string;
  word: string; // Norwegian word
  wordEnglish: string; // English word (from Mood Meter)
  definition: string; // Short definition in Norwegian
  quadrant: 1 | 2 | 3 | 4;
  color: string; // HEX color
  shape: "circle" | "diamond" | "rounded-square" | "hexagon" | "star-6" | "star-8";
};

/**
 * QUADRANT 1: Høy Energi, Ubehagelig (Rød/Korall)
 * Følelser: stress, sinne, angst, panikk, irritasjon, frustrasjon
 */
export const Q1_EMOTIONS: EmotionWord[] = [
  { id: "q1-01", word: "Rasende", wordEnglish: "Enraged", definition: "Ekstrem sinne, ute av kontroll", quadrant: 1, color: "#FF4136", shape: "star-8" },
  { id: "q1-02", word: "Panisk", wordEnglish: "Panicked", definition: "Overveldet av akutt frykt", quadrant: 1, color: "#FF5A4F", shape: "circle" },
  { id: "q1-03", word: "Stresset", wordEnglish: "Stressed", definition: "Presset av krav og forventninger", quadrant: 1, color: "#FF6F61", shape: "diamond" },
  { id: "q1-04", word: "Nervøs", wordEnglish: "Jittery", definition: "Urolig og rastløs i kropp og sinn", quadrant: 1, color: "#FF7A6D", shape: "rounded-square" },
  { id: "q1-05", word: "Sjokkert", wordEnglish: "Shocked", definition: "Overrasket av noe uventet og ubehagelig", quadrant: 1, color: "#FF8579", shape: "hexagon" },
  { id: "q1-06", word: "Livredd", wordEnglish: "Livid", definition: "Intens sinne, nesten ukontrollerbar", quadrant: 1, color: "#FF3B30", shape: "circle" },
  { id: "q1-07", word: "Rasende sint", wordEnglish: "Furious", definition: "Voldsom og ukontrollert sinne", quadrant: 1, color: "#FF4D42", shape: "diamond" },
  { id: "q1-08", word: "Frustrert", wordEnglish: "Frustrated", definition: "Hindret fra å nå mål, irritert", quadrant: 1, color: "#FF6156", shape: "rounded-square" },
  { id: "q1-09", word: "Anspent", wordEnglish: "Tense", definition: "Stram i kropp og sinn, på vakt", quadrant: 1, color: "#FF7568", shape: "circle" },
  { id: "q1-10", word: "Lamslått", wordEnglish: "Stunned", definition: "Overmannet og handlingslammet", quadrant: 1, color: "#FF897A", shape: "hexagon" },
  { id: "q1-11", word: "Kokende", wordEnglish: "Fuming", definition: "Intens sinne som koker under overflaten", quadrant: 1, color: "#FF2D22", shape: "star-6" },
  { id: "q1-12", word: "Redd", wordEnglish: "Frightened", definition: "Full av frykt og redsel", quadrant: 1, color: "#FF4136", shape: "circle" },
  { id: "q1-13", word: "Sint", wordEnglish: "Angry", definition: "Misfornøyd og irritert på noen eller noe", quadrant: 1, color: "#FF554A", shape: "diamond" },
  { id: "q1-14", word: "Nervøs", wordEnglish: "Nervous", definition: "Urolig og bekymret for noe som skal skje", quadrant: 1, color: "#FF695E", shape: "rounded-square" },
  { id: "q1-15", word: "Rastløs", wordEnglish: "Restless", definition: "Kan ikke finne ro, urolig energi", quadrant: 1, color: "#FF7D70", shape: "circle" },
  { id: "q1-16", word: "Engstelig", wordEnglish: "Anxious", definition: "Bekymret og nervøs, full av uro", quadrant: 1, color: "#FF1F14", shape: "circle" },
  { id: "q1-17", word: "Urolig", wordEnglish: "Apprehensive", definition: "Engstelig for noe som kan skje", quadrant: 1, color: "#FF3328", shape: "diamond" },
  { id: "q1-18", word: "Bekymret", wordEnglish: "Worried", definition: "Opptatt av problemer og mulige farer", quadrant: 1, color: "#FF473C", shape: "rounded-square" },
  { id: "q1-19", word: "Irritert", wordEnglish: "Irritated", definition: "Lett frustrert og lett på gråten", quadrant: 1, color: "#FF5B50", shape: "circle" },
  { id: "q1-20", word: "Ergerlig", wordEnglish: "Annoyed", definition: "Lett irritert og forstyrret", quadrant: 1, color: "#FF6F64", shape: "hexagon" },
  { id: "q1-21", word: "Vemmelig", wordEnglish: "Repulsed", definition: "Sterk avsmak og avsky", quadrant: 1, color: "#FF1106", shape: "circle" },
  { id: "q1-22", word: "Plaget", wordEnglish: "Troubled", definition: "Urolig og bekymret i sinnet", quadrant: 1, color: "#FF251A", shape: "diamond" },
  { id: "q1-23", word: "Urolig", wordEnglish: "Concerned", definition: "Bekymret for noe eller noen", quadrant: 1, color: "#FF392E", shape: "rounded-square" },
  { id: "q1-24", word: "Utilpass", wordEnglish: "Uneasy", definition: "Vag følelse av ubehag og uro", quadrant: 1, color: "#FF4D42", shape: "circle" },
  { id: "q1-25", word: "Irritert", wordEnglish: "Peeved", definition: "Lett irritert og misfornøyd", quadrant: 1, color: "#FF6156", shape: "hexagon" },
];

/**
 * QUADRANT 2: Høy Energi, Behagelig (Gul/Gull)
 * Følelser: glede, entusiasme, spenning, energi, inspirasjon
 */
export const Q2_EMOTIONS: EmotionWord[] = [
  { id: "q2-01", word: "Overrasket", wordEnglish: "Surprised", definition: "Positivt overrumplet av noe uventet", quadrant: 2, color: "#FFD700", shape: "star-8" },
  { id: "q2-02", word: "Opprømt", wordEnglish: "Upbeat", definition: "Positiv og energisk i humør", quadrant: 2, color: "#FFD91A", shape: "circle" },
  { id: "q2-03", word: "Festlig", wordEnglish: "Festive", definition: "Feststemt og glad", quadrant: 2, color: "#FFDB33", shape: "diamond" },
  { id: "q2-04", word: "Begeistret", wordEnglish: "Exhilarated", definition: "Intenst glad og energisk", quadrant: 2, color: "#FFDD4D", shape: "rounded-square" },
  { id: "q2-05", word: "Ekstatisk", wordEnglish: "Ecstatic", definition: "Overveldet av lykke", quadrant: 2, color: "#FFDF66", shape: "hexagon" },
  { id: "q2-06", word: "Hype", wordEnglish: "Hyper", definition: "Ekstremt energisk og aktiv", quadrant: 2, color: "#FFD500", shape: "circle" },
  { id: "q2-07", word: "Munter", wordEnglish: "Cheerful", definition: "Glad og oppløftende", quadrant: 2, color: "#FFD719", shape: "diamond" },
  { id: "q2-08", word: "Motivert", wordEnglish: "Motivated", definition: "Drevet og energisk mot mål", quadrant: 2, color: "#FFD932", shape: "rounded-square" },
  { id: "q2-09", word: "Inspirert", wordEnglish: "Inspired", definition: "Fylt med kreativ energi", quadrant: 2, color: "#FFDB4C", shape: "circle" },
  { id: "q2-10", word: "Henrykt", wordEnglish: "Elated", definition: "Intenst glad og opprømt", quadrant: 2, color: "#FFDD65", shape: "hexagon" },
  { id: "q2-11", word: "Energisk", wordEnglish: "Energized", definition: "Full av kraft og vitalitet", quadrant: 2, color: "#FFD300", shape: "star-6" },
  { id: "q2-12", word: "Livlig", wordEnglish: "Lively", definition: "Aktiv og full av liv", quadrant: 2, color: "#FFD518", shape: "circle" },
  { id: "q2-13", word: "Spent", wordEnglish: "Excited", definition: "Full av forventning og glede", quadrant: 2, color: "#FFD731", shape: "diamond" },
  { id: "q2-14", word: "Optimistisk", wordEnglish: "Optimistic", definition: "Positiv om fremtiden", quadrant: 2, color: "#FFD94B", shape: "rounded-square" },
  { id: "q2-15", word: "Entusiastisk", wordEnglish: "Enthusiastic", definition: "Ivrig og lidenskapelig engasjert", quadrant: 2, color: "#FFDB64", shape: "circle" },
  { id: "q2-16", word: "Fornøyd", wordEnglish: "Pleased", definition: "Tilfreds og glad", quadrant: 2, color: "#FFD100", shape: "circle" },
  { id: "q2-17", word: "Fokusert", wordEnglish: "Focused", definition: "Konsentrert og målrettet", quadrant: 2, color: "#FFD317", shape: "diamond" },
  { id: "q2-18", word: "Lykkelig", wordEnglish: "Happy", definition: "Glad og fornøyd", quadrant: 2, color: "#FFD530", shape: "rounded-square" },
  { id: "q2-19", word: "Stolt", wordEnglish: "Proud", definition: "Tilfreds med egen prestasjon", quadrant: 2, color: "#FFD74A", shape: "circle" },
  { id: "q2-20", word: "Begeistret", wordEnglish: "Thrilled", definition: "Intenst glad og spent", quadrant: 2, color: "#FFD963", shape: "hexagon" },
  { id: "q2-21", word: "Behagelig", wordEnglish: "Pleasant", definition: "Hyggelig og tiltalende", quadrant: 2, color: "#FFCF00", shape: "circle" },
  { id: "q2-22", word: "Gledesfull", wordEnglish: "Joyful", definition: "Fylt med glede", quadrant: 2, color: "#FFD116", shape: "diamond" },
  { id: "q2-23", word: "Håpefull", wordEnglish: "Hopeful", definition: "Full av håp og optimisme", quadrant: 2, color: "#FFD32F", shape: "rounded-square" },
  { id: "q2-24", word: "Leken", wordEnglish: "Playful", definition: "Lystbetont og morsom", quadrant: 2, color: "#FFD549", shape: "circle" },
  { id: "q2-25", word: "Lykkesalig", wordEnglish: "Blissful", definition: "Perfekt lykke og tilfredshet", quadrant: 2, color: "#FFD762", shape: "hexagon" },
];

/**
 * QUADRANT 3: Lav Energi, Ubehagelig (Blå)
 * Følelser: tristhet, ensomhet, utmattelse, sorg, håpløshet
 */
export const Q3_EMOTIONS: EmotionWord[] = [
  { id: "q3-01", word: "Kvalm", wordEnglish: "Disgusted", definition: "Sterkt misfornøyd og avskydd", quadrant: 3, color: "#4A90E2", shape: "star-8" },
  { id: "q3-02", word: "Nedstemt", wordEnglish: "Glum", definition: "Mørk og trist i humøret", quadrant: 3, color: "#5298E5", shape: "circle" },
  { id: "q3-03", word: "Skuffet", wordEnglish: "Disappointed", definition: "Lei seg over uoppfylte forventninger", quadrant: 3, color: "#5AA0E8", shape: "diamond" },
  { id: "q3-04", word: "Nede", wordEnglish: "Down", definition: "Trist og deprimert", quadrant: 3, color: "#62A8EB", shape: "rounded-square" },
  { id: "q3-05", word: "Apatisk", wordEnglish: "Apathetic", definition: "Likegyldig og uten interesse", quadrant: 3, color: "#6AB0EE", shape: "hexagon" },
  { id: "q3-06", word: "Pessimistisk", wordEnglish: "Pessimistic", definition: "Negativ om fremtiden", quadrant: 3, color: "#4288DF", shape: "circle" },
  { id: "q3-07", word: "Trist", wordEnglish: "Morose", definition: "Dyp trist og mørk", quadrant: 3, color: "#4A90E2", shape: "diamond" },
  { id: "q3-08", word: "Motløs", wordEnglish: "Discouraged", definition: "Mistet mot og håp", quadrant: 3, color: "#5298E5", shape: "rounded-square" },
  { id: "q3-09", word: "Lei seg", wordEnglish: "Sad", definition: "Ulykkelig og trist", quadrant: 3, color: "#5AA0E8", shape: "circle" },
  { id: "q3-10", word: "Kjeder seg", wordEnglish: "Bored", definition: "Uinteressert og rastløs", quadrant: 3, color: "#62A8EB", shape: "hexagon" },
  { id: "q3-11", word: "Fremmedgjort", wordEnglish: "Alienated", definition: "Isolert og frakoblet andre", quadrant: 3, color: "#3A80DC", shape: "star-6" },
  { id: "q3-12", word: "Elendig", wordEnglish: "Miserable", definition: "Dypt ulykkelig", quadrant: 3, color: "#4288DF", shape: "circle" },
  { id: "q3-13", word: "Ensom", wordEnglish: "Lonely", definition: "Isolert og savner tilknytning", quadrant: 3, color: "#4A90E2", shape: "diamond" },
  { id: "q3-14", word: "Motløs", wordEnglish: "Disheartened", definition: "Mistet håp og entusiasme", quadrant: 3, color: "#5298E5", shape: "rounded-square" },
  { id: "q3-15", word: "Sliten", wordEnglish: "Tired", definition: "Fysisk eller mentalt utmattet", quadrant: 3, color: "#5AA0E8", shape: "circle" },
  { id: "q3-16", word: "Fortvilet", wordEnglish: "Despondent", definition: "Uten håp eller mot", quadrant: 3, color: "#3278D9", shape: "circle" },
  { id: "q3-17", word: "Deprimert", wordEnglish: "Depressed", definition: "Vedvarende trist og energiløs", quadrant: 3, color: "#3A80DC", shape: "diamond" },
  { id: "q3-18", word: "Sur", wordEnglish: "Sullen", definition: "Trist og irritabel", quadrant: 3, color: "#4288DF", shape: "rounded-square" },
  { id: "q3-19", word: "Utmattet", wordEnglish: "Exhausted", definition: "Fullstendig tappet for energi", quadrant: 3, color: "#4A90E2", shape: "circle" },
  { id: "q3-20", word: "Utslitt", wordEnglish: "Fatigued", definition: "Langvarig tretthet", quadrant: 3, color: "#5298E5", shape: "hexagon" },
  { id: "q3-21", word: "Fortvilet", wordEnglish: "Despairing", definition: "Full av fortvilelse", quadrant: 3, color: "#2A70D6", shape: "circle" },
  { id: "q3-22", word: "Håpløs", wordEnglish: "Hopeless", definition: "Uten håp om bedring", quadrant: 3, color: "#3278D9", shape: "diamond" },
  { id: "q3-23", word: "Øde", wordEnglish: "Desolate", definition: "Ensom og forlatt", quadrant: 3, color: "#3A80DC", shape: "rounded-square" },
  { id: "q3-24", word: "Brukt opp", wordEnglish: "Spent", definition: "Fullstendig utbrukt", quadrant: 3, color: "#4288DF", shape: "circle" },
  { id: "q3-25", word: "Tømt", wordEnglish: "Drained", definition: "Uten energi eller ressurser", quadrant: 3, color: "#4A90E2", shape: "hexagon" },
];

/**
 * QUADRANT 4: Lav Energi, Behagelig (Grønn/Mint)
 * Følelser: ro, avslappethet, ettertanke, fred, tilfredsstillelse
 */
export const Q4_EMOTIONS: EmotionWord[] = [
  { id: "q4-01", word: "Avslappet", wordEnglish: "At Ease", definition: "Fri for spenning og bekymring", quadrant: 4, color: "#88D8B0", shape: "star-8" },
  { id: "q4-02", word: "Uanstrengt", wordEnglish: "Easygoing", definition: "Rolig og ubekymret", quadrant: 4, color: "#8FDAB5", shape: "circle" },
  { id: "q4-03", word: "Tilfreds", wordEnglish: "Content", definition: "Fornøyd og i fred med seg selv", quadrant: 4, color: "#96DCBA", shape: "diamond" },
  { id: "q4-04", word: "Kjærlig", wordEnglish: "Loving", definition: "Full av kjærlighet og omsorg", quadrant: 4, color: "#9DDEBF", shape: "rounded-square" },
  { id: "q4-05", word: "Oppfylt", wordEnglish: "Fulfilled", definition: "Dypt tilfreds og fullstendig", quadrant: 4, color: "#A4E0C4", shape: "hexagon" },
  { id: "q4-06", word: "Rolig", wordEnglish: "Calm", definition: "Stille og uten uro", quadrant: 4, color: "#81D6AB", shape: "circle" },
  { id: "q4-07", word: "Trygg", wordEnglish: "Secure", definition: "Føler seg sikker og beskyttet", quadrant: 4, color: "#88D8B0", shape: "diamond" },
  { id: "q4-08", word: "Fornøyd", wordEnglish: "Satisfied", definition: "Tilfreds med utfallet", quadrant: 4, color: "#8FDAB5", shape: "rounded-square" },
  { id: "q4-09", word: "Takknemlig", wordEnglish: "Grateful", definition: "Full av takknemlighet", quadrant: 4, color: "#96DCBA", shape: "circle" },
  { id: "q4-10", word: "Rørt", wordEnglish: "Touched", definition: "Emosjonelt beveget på en god måte", quadrant: 4, color: "#9DDEBF", shape: "hexagon" },
  { id: "q4-11", word: "Avslappet", wordEnglish: "Relaxed", definition: "Fri for spenning", quadrant: 4, color: "#7AD4A6", shape: "star-6" },
  { id: "q4-12", word: "Chill", wordEnglish: "Chill", definition: "Avslappet og ubekymret", quadrant: 4, color: "#81D6AB", shape: "circle" },
  { id: "q4-13", word: "Uthvilt", wordEnglish: "Restful", definition: "Godt hvilt og restaurert", quadrant: 4, color: "#88D8B0", shape: "diamond" },
  { id: "q4-14", word: "Velsignet", wordEnglish: "Blessed", definition: "Føler seg beriket og heldig", quadrant: 4, color: "#8FDAB5", shape: "rounded-square" },
  { id: "q4-15", word: "Balansert", wordEnglish: "Balanced", definition: "I harmoni og balanse", quadrant: 4, color: "#96DCBA", shape: "circle" },
  { id: "q4-16", word: "Mild", wordEnglish: "Mellow", definition: "Rolig og myk i stemning", quadrant: 4, color: "#73D2A1", shape: "circle" },
  { id: "q4-17", word: "Ettertenksom", wordEnglish: "Thoughtful", definition: "Being considerate or reflective about a situation (past, present, future), oneself", quadrant: 4, color: "#7AD4A6", shape: "diamond" },
  { id: "q4-18", word: "Fredelig", wordEnglish: "Peaceful", definition: "Full av indre fred", quadrant: 4, color: "#81D6AB", shape: "rounded-square" },
  { id: "q4-19", word: "Komfortabel", wordEnglish: "Comfortable", definition: "Fysisk og mentalt behagelig", quadrant: 4, color: "#88D8B0", shape: "circle" },
  { id: "q4-20", word: "Bekymringsløs", wordEnglish: "Carefree", definition: "Fri for bekymringer", quadrant: 4, color: "#8FDAB5", shape: "hexagon" },
  { id: "q4-21", word: "Søvnig", wordEnglish: "Sleepy", definition: "Behagelig trøtt og rolig", quadrant: 4, color: "#6CD09C", shape: "circle" },
  { id: "q4-22", word: "Selvtilfreds", wordEnglish: "Complacent", definition: "Fornøyd med nåværende tilstand", quadrant: 4, color: "#73D2A1", shape: "diamond" },
  { id: "q4-23", word: "Stillhet", wordEnglish: "Tranquil", definition: "Dyp ro og stillhet", quadrant: 4, color: "#7AD4A6", shape: "rounded-square" },
  { id: "q4-24", word: "Koselig", wordEnglish: "Cozy", definition: "Varm og komfortabel", quadrant: 4, color: "#81D6AB", shape: "circle" },
  { id: "q4-25", word: "Fredfull", wordEnglish: "Serene", definition: "Rolig og uforstyrret", quadrant: 4, color: "#88D8B0", shape: "hexagon" },
];

// Combine all emotions
export const ALL_EMOTIONS = [
  ...Q1_EMOTIONS,
  ...Q2_EMOTIONS,
  ...Q3_EMOTIONS,
  ...Q4_EMOTIONS,
];

// Get emotions by quadrant
export function getEmotionsByQuadrant(quadrant: 1 | 2 | 3 | 4): EmotionWord[] {
  return ALL_EMOTIONS.filter((e) => e.quadrant === quadrant);
}

// Get emotion by ID
export function getEmotionById(id: string): EmotionWord | undefined {
  return ALL_EMOTIONS.find((e) => e.id === id);
}
