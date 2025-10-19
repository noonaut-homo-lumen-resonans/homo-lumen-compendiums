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
  svgPath?: string; // SVG path data for unique abstract form (from Manus' design)
  formDescription?: string; // Description of the unique form
};

/**
 * QUADRANT 1: Høy Energi, Ubehagelig (Rød/Korall)
 * Følelser: stress, sinne, angst, panikk, irritasjon, frustrasjon
 */
export const Q1_EMOTIONS: EmotionWord[] = [
  {
    id: "q1-01",
    word: "Rasende",
    wordEnglish: "Enraged",
    definition: "Ekstrem sinne, ute av kontroll",
    quadrant: 1,
    color: "#FF1106",
    shape: "star-8",
    svgPath: "M 50 5 L 57 25 L 75 15 L 65 35 L 85 40 L 65 50 L 75 70 L 57 60 L 50 80 L 43 60 L 25 70 L 35 50 L 15 40 L 35 35 L 25 15 L 43 25 Z",
    formDescription: "Eksploderende stjerne med 12 uregelmessige spisser"
  },
  {
    id: "q1-02",
    word: "Panisk",
    wordEnglish: "Panicked",
    definition: "Overveldet av akutt frykt",
    quadrant: 1,
    color: "#FF1F14",
    shape: "circle",
    svgPath: "M 50 10 L 60 20 L 65 10 L 70 25 L 80 22 L 75 35 L 85 40 L 72 45 L 75 58 L 62 55 L 58 68 L 50 58 L 42 68 L 38 55 L 25 58 L 28 45 L 15 40 L 25 35 L 20 22 L 30 25 L 35 10 L 40 20 Z",
    formDescription: "Vibrerende zigzag-form med skarpe vinkler"
  },
  {
    id: "q1-03",
    word: "Stresset",
    wordEnglish: "Stressed",
    definition: "Presset av krav og forventninger",
    quadrant: 1,
    color: "#FF2D22",
    shape: "diamond",
    svgPath: "M 50 20 L 65 35 C 68 38, 68 42, 65 45 L 55 55 C 53 57, 53 60, 55 62 L 60 75 L 50 68 L 40 75 L 45 62 C 47 60, 47 57, 45 55 L 35 45 C 32 42, 32 38, 35 35 Z",
    formDescription: "Sammentrykket polygon med innovervendte kanter"
  },
  { id: "q1-04", word: "Nervøs", wordEnglish: "Jittery", definition: "Urolig og rastløs i kropp og sinn", quadrant: 1, color: "#FF7A6D", shape: "rounded-square" },
  { id: "q1-05", word: "Sjokkert", wordEnglish: "Shocked", definition: "Overrasket av noe uventet og ubehagelig", quadrant: 1, color: "#FF8579", shape: "hexagon" },
  { id: "q1-06", word: "Livredd", wordEnglish: "Livid", definition: "Intens sinne, nesten ukontrollerbar", quadrant: 1, color: "#FF3B30", shape: "circle" },
  {
    id: "q1-07",
    word: "Rasende sint",
    wordEnglish: "Furious",
    definition: "Voldsom og ukontrollert sinne",
    quadrant: 1,
    color: "#FF554A",
    shape: "diamond",
    svgPath: "M 50 15 C 55 18, 58 20, 62 25 L 70 30 C 72 35, 74 40, 75 45 C 76 50, 74 55, 70 58 L 65 65 C 60 68, 55 70, 50 72 C 45 70, 40 68, 35 65 L 30 58 C 26 55, 24 50, 25 45 C 26 40, 28 35, 30 30 L 38 25 C 42 20, 45 18, 50 15 Z",
    formDescription: "Tornado-spiral med taggete kanter"
  },
  { id: "q1-08", word: "Frustrert", wordEnglish: "Frustrated", definition: "Hindret fra å nå mål, irritert", quadrant: 1, color: "#FF6156", shape: "rounded-square" },
  { id: "q1-09", word: "Anspent", wordEnglish: "Tense", definition: "Stram i kropp og sinn, på vakt", quadrant: 1, color: "#FF7568", shape: "circle" },
  { id: "q1-10", word: "Lamslått", wordEnglish: "Stunned", definition: "Overmannet og handlingslammet", quadrant: 1, color: "#FF897A", shape: "hexagon" },
  { id: "q1-11", word: "Kokende", wordEnglish: "Fuming", definition: "Intens sinne som koker under overflaten", quadrant: 1, color: "#FF2D22", shape: "star-6" },
  {
    id: "q1-12",
    word: "Redd",
    wordEnglish: "Frightened",
    definition: "Full av frykt og redsel",
    quadrant: 1,
    color: "#FF7568",
    shape: "circle",
    svgPath: "M 50 25 L 45 30 C 42 28, 40 26, 38 25 L 35 30 C 33 28, 30 27, 28 28 L 25 35 C 24 33, 22 32, 20 33 L 22 40 C 20 40, 18 41, 18 43 L 22 48 C 21 50, 21 52, 23 54 L 28 58 C 28 60, 29 62, 31 63 L 37 65 C 38 67, 40 68, 42 68 L 50 68 L 58 68 C 60 68, 62 67, 63 65 L 69 63 C 71 62, 72 60, 72 58 L 77 54 C 79 52, 79 50, 78 48 L 82 43 C 82 41, 80 40, 78 40 L 80 33 C 78 32, 76 33, 75 35 L 72 28 C 70 27, 67 28, 65 30 L 62 25 C 60 26, 58 28, 55 30 Z",
    formDescription: "Krympende form med innovervendte spisser"
  },
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
  {
    id: "q2-01",
    word: "Overrasket",
    wordEnglish: "Surprised",
    definition: "Positivt overrumplet av noe uventet",
    quadrant: 2,
    color: "#FFCF00",
    shape: "star-8",
    svgPath: "M 50 15 L 52 30 L 65 25 L 58 38 L 70 42 L 58 48 L 62 60 L 52 53 L 50 68 L 48 53 L 38 60 L 42 48 L 30 42 L 42 38 L 35 25 L 48 30 Z",
    formDescription: "Eksploderende sirkel med 16 stråler"
  },
  { id: "q2-02", word: "Opprømt", wordEnglish: "Upbeat", definition: "Positiv og energisk i humør", quadrant: 2, color: "#FFD91A", shape: "circle" },
  { id: "q2-03", word: "Festlig", wordEnglish: "Festive", definition: "Feststemt og glad", quadrant: 2, color: "#FFDB33", shape: "diamond" },
  { id: "q2-04", word: "Begeistret", wordEnglish: "Exhilarated", definition: "Intenst glad og energisk", quadrant: 2, color: "#FFDD4D", shape: "rounded-square" },
  {
    id: "q2-05",
    word: "Ekstatisk",
    wordEnglish: "Ecstatic",
    definition: "Overveldet av lykke",
    quadrant: 2,
    color: "#FFD700",
    shape: "hexagon",
    svgPath: "M 50 10 L 58 20 L 68 18 L 70 28 L 80 30 L 75 40 L 82 48 L 72 52 L 72 62 L 62 60 L 55 68 L 50 60 L 45 68 L 38 60 L 28 62 L 28 52 L 18 48 L 25 40 L 20 30 L 30 28 L 32 18 L 42 20 Z",
    formDescription: "Dobbel stjerne med overlappende stråler"
  },
  { id: "q2-06", word: "Hype", wordEnglish: "Hyper", definition: "Ekstremt energisk og aktiv", quadrant: 2, color: "#FFD500", shape: "circle" },
  { id: "q2-07", word: "Munter", wordEnglish: "Cheerful", definition: "Glad og oppløftende", quadrant: 2, color: "#FFD719", shape: "diamond" },
  {
    id: "q2-08",
    word: "Motivert",
    wordEnglish: "Motivated",
    definition: "Drevet og energisk mot mål",
    quadrant: 2,
    color: "#FFD932",
    shape: "rounded-square",
    svgPath: "M 50 10 L 60 25 L 70 20 L 75 35 L 85 35 L 80 50 L 90 55 L 75 60 L 75 75 L 60 70 L 50 80 L 40 70 L 25 75 L 25 60 L 10 55 L 20 50 L 15 35 L 25 35 L 30 20 L 40 25 Z",
    formDescription: "Pil-form som peker oppover"
  },
  { id: "q2-09", word: "Inspirert", wordEnglish: "Inspired", definition: "Fylt med kreativ energi", quadrant: 2, color: "#FFDB4C", shape: "circle" },
  { id: "q2-10", word: "Henrykt", wordEnglish: "Elated", definition: "Intenst glad og opprømt", quadrant: 2, color: "#FFDD65", shape: "hexagon" },
  { id: "q2-11", word: "Energisk", wordEnglish: "Energized", definition: "Full av kraft og vitalitet", quadrant: 2, color: "#FFD300", shape: "star-6" },
  { id: "q2-12", word: "Livlig", wordEnglish: "Lively", definition: "Aktiv og full av liv", quadrant: 2, color: "#FFD518", shape: "circle" },
  {
    id: "q2-13",
    word: "Spent",
    wordEnglish: "Excited",
    definition: "Full av forventning og glede",
    quadrant: 2,
    color: "#FFD731",
    shape: "diamond",
    svgPath: "M 50 15 L 55 28 L 62 22 L 65 35 L 73 32 L 72 45 L 80 48 L 72 55 L 75 65 L 65 62 L 58 70 L 52 60 L 48 70 L 42 62 L 35 65 L 38 55 L 30 48 L 38 45 L 37 32 L 45 35 L 48 22 L 55 28 Z",
    formDescription: "Hoppende stjerne med dynamiske spisser"
  },
  { id: "q2-14", word: "Optimistisk", wordEnglish: "Optimistic", definition: "Positiv om fremtiden", quadrant: 2, color: "#FFD94B", shape: "rounded-square" },
  { id: "q2-15", word: "Entusiastisk", wordEnglish: "Enthusiastic", definition: "Ivrig og lidenskapelig engasjert", quadrant: 2, color: "#FFDB64", shape: "circle" },
  { id: "q2-16", word: "Fornøyd", wordEnglish: "Pleased", definition: "Tilfreds og glad", quadrant: 2, color: "#FFD100", shape: "circle" },
  { id: "q2-17", word: "Fokusert", wordEnglish: "Focused", definition: "Konsentrert og målrettet", quadrant: 2, color: "#FFD317", shape: "diamond" },
  { id: "q2-18", word: "Lykkelig", wordEnglish: "Happy", definition: "Glad og fornøyd", quadrant: 2, color: "#FFD530", shape: "rounded-square" },
  { id: "q2-19", word: "Stolt", wordEnglish: "Proud", definition: "Tilfreds med egen prestasjon", quadrant: 2, color: "#FFD74A", shape: "circle" },
  { id: "q2-20", word: "Begeistret", wordEnglish: "Thrilled", definition: "Intenst glad og spent", quadrant: 2, color: "#FFD963", shape: "hexagon" },
  { id: "q2-21", word: "Behagelig", wordEnglish: "Pleasant", definition: "Hyggelig og tiltalende", quadrant: 2, color: "#FFCF00", shape: "circle" },
  {
    id: "q2-22",
    word: "Gledesfull",
    wordEnglish: "Joyful",
    definition: "Fylt med glede",
    quadrant: 2,
    color: "#FFD762",
    shape: "diamond",
    svgPath: "M 50 20 C 52 25, 55 28, 58 30 L 62 35 C 65 38, 68 40, 70 43 C 72 48, 70 52, 68 55 L 62 60 C 58 62, 54 64, 50 65 C 46 64, 42 62, 38 60 L 32 55 C 30 52, 28 48, 30 43 C 32 40, 35 38, 38 35 L 42 30 C 45 28, 48 25, 50 20 M 40 35 C 42 38, 45 40, 48 41 M 52 41 C 55 40, 58 38, 60 35 M 45 50 C 47 52, 50 53, 53 52 C 54 50, 53 48, 52 47 C 50 46, 48 47, 47 48 Z",
    formDescription: "Dansende form med lekne kurver"
  },
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
  {
    id: "q3-09",
    word: "Lei seg",
    wordEnglish: "Sad",
    definition: "Ulykkelig og trist",
    quadrant: 3,
    color: "#5AA0E8",
    shape: "circle",
    svgPath: "M 50 25 C 55 28, 58 32, 60 36 L 62 42 C 63 46, 62 50, 60 54 L 56 60 C 53 64, 48 66, 44 67 C 40 66, 36 64, 34 60 L 32 54 C 31 50, 32 46, 34 42 L 38 36 C 41 32, 45 28, 50 25 M 44 40 C 44 42, 43 44, 42 45 C 41 44, 41 42, 42 40 C 43 39, 44 39, 44 40 M 56 40 C 56 42, 55 44, 54 45 C 53 44, 53 42, 54 40 C 55 39, 56 39, 56 40 M 48 55 C 46 56, 44 55, 43 53 C 44 54, 46 54, 48 54 M 52 54 C 54 54, 56 54, 57 53 C 56 55, 54 56, 52 55 Z",
    formDescription: "Tåre-form"
  },
  { id: "q3-10", word: "Kjeder seg", wordEnglish: "Bored", definition: "Uinteressert og rastløs", quadrant: 3, color: "#62A8EB", shape: "hexagon" },
  { id: "q3-11", word: "Fremmedgjort", wordEnglish: "Alienated", definition: "Isolert og frakoblet andre", quadrant: 3, color: "#3A80DC", shape: "star-6" },
  { id: "q3-12", word: "Elendig", wordEnglish: "Miserable", definition: "Dypt ulykkelig", quadrant: 3, color: "#4288DF", shape: "circle" },
  {
    id: "q3-13",
    word: "Ensom",
    wordEnglish: "Lonely",
    definition: "Isolert og savner tilknytning",
    quadrant: 3,
    color: "#4A90E2",
    shape: "diamond",
    svgPath: "M 50 30 C 52 32, 54 34, 55 37 C 56 40, 55 43, 53 45 C 51 47, 48 48, 45 47 C 42 46, 40 43, 40 40 C 40 37, 42 34, 45 32 C 47 31, 49 30, 50 30 M 35 50 C 36 50, 37 51, 37 52 C 37 53, 36 54, 35 54 C 34 54, 33 53, 33 52 C 33 51, 34 50, 35 50 M 65 50 C 66 50, 67 51, 67 52 C 67 53, 66 54, 65 54 C 64 54, 63 53, 63 52 C 63 51, 64 50, 65 50 M 25 65 C 26 65, 27 66, 27 67 C 27 68, 26 69, 25 69 C 24 69, 23 68, 23 67 C 23 66, 24 65, 25 65 M 75 40 C 76 40, 77 41, 77 42 C 77 43, 76 44, 75 44 C 74 44, 73 43, 73 42 C 73 41, 74 40, 75 40 Z",
    formDescription: "Ensom sirkel i tomt rom"
  },
  { id: "q3-14", word: "Motløs", wordEnglish: "Disheartened", definition: "Mistet håp og entusiasme", quadrant: 3, color: "#5298E5", shape: "rounded-square" },
  { id: "q3-15", word: "Sliten", wordEnglish: "Tired", definition: "Fysisk eller mentalt utmattet", quadrant: 3, color: "#5AA0E8", shape: "circle" },
  { id: "q3-16", word: "Fortvilet", wordEnglish: "Despondent", definition: "Uten håp eller mot", quadrant: 3, color: "#3278D9", shape: "circle" },
  {
    id: "q3-17",
    word: "Deprimert",
    wordEnglish: "Depressed",
    definition: "Vedvarende trist og energiløs",
    quadrant: 3,
    color: "#3A80DC",
    shape: "diamond",
    svgPath: "M 50 35 C 48 38, 46 40, 44 42 L 40 48 C 38 50, 36 52, 35 55 C 34 58, 36 60, 38 62 L 42 66 C 44 68, 46 70, 48 71 L 50 73 L 52 71 C 54 70, 56 68, 58 66 L 62 62 C 64 60, 66 58, 65 55 C 64 52, 62 50, 60 48 L 56 42 C 54 40, 52 38, 50 35 Z",
    formDescription: "Tung, nedtrykt form"
  },
  { id: "q3-18", word: "Sur", wordEnglish: "Sullen", definition: "Trist og irritabel", quadrant: 3, color: "#4288DF", shape: "rounded-square" },
  {
    id: "q3-19",
    word: "Utmattet",
    wordEnglish: "Exhausted",
    definition: "Fullstendig tappet for energi",
    quadrant: 3,
    color: "#4A90E2",
    shape: "circle",
    svgPath: "M 50 30 C 55 32, 58 35, 60 38 C 62 42, 62 46, 60 50 C 58 54, 54 57, 50 58 C 46 57, 42 54, 40 50 C 38 46, 38 42, 40 38 C 42 35, 45 32, 50 30 M 52 35 C 54 36, 55 38, 55 40 C 55 42, 54 44, 52 45 C 50 46, 48 46, 46 45 M 48 50 C 50 51, 52 51, 54 50 C 56 49, 57 47, 57 45 M 43 55 C 44 56, 45 57, 47 57 C 48 57, 49 56, 50 55 M 53 60 C 54 61, 55 62, 56 62 C 57 62, 58 61, 58 60 Z",
    formDescription: "Utflytende, oppløst form"
  },
  { id: "q3-20", word: "Utslitt", wordEnglish: "Fatigued", definition: "Langvarig tretthet", quadrant: 3, color: "#5298E5", shape: "hexagon" },
  { id: "q3-21", word: "Fortvilet", wordEnglish: "Despairing", definition: "Full av fortvilelse", quadrant: 3, color: "#2A70D6", shape: "circle" },
  {
    id: "q3-22",
    word: "Håpløs",
    wordEnglish: "Hopeless",
    definition: "Uten håp om bedring",
    quadrant: 3,
    color: "#3278D9",
    shape: "diamond",
    svgPath: "M 50 40 C 48 42, 46 44, 45 47 C 44 50, 45 53, 47 56 L 50 60 C 52 62, 54 63, 56 64 C 58 65, 60 64, 61 62 L 63 58 C 64 56, 64 54, 63 52 C 62 49, 60 47, 58 45 L 55 42 C 53 41, 51 40, 50 40 M 45 50 C 44 52, 43 54, 43 56 C 43 57, 44 58, 45 58 C 46 58, 47 57, 47 56 L 47 52 C 47 51, 46 50, 45 50 M 38 60 C 37 61, 36 62, 36 64 C 36 65, 37 66, 38 66 C 39 66, 40 65, 40 64 C 40 62, 39 61, 38 60 M 30 68 C 28 69, 26 70, 25 72 C 25 73, 26 74, 27 74 C 28 74, 30 73, 31 72 C 31 70, 30 69, 30 68 Z",
    formDescription: "Mørk, tung sky som synker"
  },
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
  {
    id: "q4-03",
    word: "Tilfreds",
    wordEnglish: "Content",
    definition: "Fornøyd og i fred med seg selv",
    quadrant: 4,
    color: "#7AD4A6",
    shape: "diamond",
    svgPath: "M 50 30 C 54 32, 57 35, 59 38 C 61 42, 61 46, 59 50 C 57 54, 54 57, 50 59 C 46 57, 43 54, 41 50 C 39 46, 39 42, 41 38 C 43 35, 46 32, 50 30 M 45 42 C 46 40, 48 39, 50 39 C 52 39, 54 40, 55 42 C 56 44, 56 46, 55 48 C 54 50, 52 51, 50 51 C 48 51, 46 50, 45 48 C 44 46, 44 44, 45 42 Z",
    formDescription: "Balansert, symmetrisk oval"
  },
  { id: "q4-04", word: "Kjærlig", wordEnglish: "Loving", definition: "Full av kjærlighet og omsorg", quadrant: 4, color: "#9DDEBF", shape: "rounded-square" },
  { id: "q4-05", word: "Oppfylt", wordEnglish: "Fulfilled", definition: "Dypt tilfreds og fullstendig", quadrant: 4, color: "#A4E0C4", shape: "hexagon" },
  {
    id: "q4-06",
    word: "Rolig",
    wordEnglish: "Calm",
    definition: "Stille og uten uro",
    quadrant: 4,
    color: "#81D6AB",
    shape: "circle",
    svgPath: "M 30 45 C 32 42, 35 40, 38 39 L 45 38 C 50 37, 55 37, 60 38 L 67 39 C 70 40, 73 42, 75 45 C 76 48, 76 51, 75 54 C 73 57, 70 59, 67 60 L 60 61 C 55 62, 50 62, 45 61 L 38 60 C 35 59, 32 57, 30 54 C 29 51, 29 48, 30 45 M 35 48 C 36 46, 38 45, 40 45 L 50 45 L 60 45 C 62 45, 64 46, 65 48 C 66 50, 66 52, 65 54 C 64 56, 62 57, 60 57 L 50 57 L 40 57 C 38 57, 36 56, 35 54 C 34 52, 34 50, 35 48 Z",
    formDescription: "Stille vann-form med jevne kurver"
  },
  { id: "q4-07", word: "Trygg", wordEnglish: "Secure", definition: "Føler seg sikker og beskyttet", quadrant: 4, color: "#88D8B0", shape: "diamond" },
  { id: "q4-08", word: "Fornøyd", wordEnglish: "Satisfied", definition: "Tilfreds med utfallet", quadrant: 4, color: "#8FDAB5", shape: "rounded-square" },
  { id: "q4-09", word: "Takknemlig", wordEnglish: "Grateful", definition: "Full av takknemlighet", quadrant: 4, color: "#96DCBA", shape: "circle" },
  { id: "q4-10", word: "Rørt", wordEnglish: "Touched", definition: "Emosjonelt beveget på en god måte", quadrant: 4, color: "#9DDEBF", shape: "hexagon" },
  {
    id: "q4-11",
    word: "Avslappet",
    wordEnglish: "Relaxed",
    definition: "Fri for spenning",
    quadrant: 4,
    color: "#7AD4A6",
    shape: "star-6",
    svgPath: "M 30 50 C 32 48, 35 47, 38 47 L 50 47 L 62 47 C 65 47, 68 48, 70 50 C 71 52, 71 54, 70 56 C 68 58, 65 59, 62 59 L 50 59 L 38 59 C 35 59, 32 58, 30 56 C 29 54, 29 52, 30 50 M 35 52 C 36 51, 38 51, 40 51 L 50 51 L 60 51 C 62 51, 64 51, 65 52 C 66 53, 66 54, 65 55 C 64 56, 62 56, 60 56 L 50 56 L 40 56 C 38 56, 36 56, 35 55 C 34 54, 34 53, 35 52 Z",
    formDescription: "Liggende, avslappet kurve"
  },
  { id: "q4-12", word: "Chill", wordEnglish: "Chill", definition: "Avslappet og ubekymret", quadrant: 4, color: "#81D6AB", shape: "circle" },
  { id: "q4-13", word: "Uthvilt", wordEnglish: "Restful", definition: "Godt hvilt og restaurert", quadrant: 4, color: "#88D8B0", shape: "diamond" },
  { id: "q4-14", word: "Velsignet", wordEnglish: "Blessed", definition: "Føler seg beriket og heldig", quadrant: 4, color: "#8FDAB5", shape: "rounded-square" },
  { id: "q4-15", word: "Balansert", wordEnglish: "Balanced", definition: "I harmoni og balanse", quadrant: 4, color: "#96DCBA", shape: "circle" },
  { id: "q4-16", word: "Mild", wordEnglish: "Mellow", definition: "Rolig og myk i stemning", quadrant: 4, color: "#73D2A1", shape: "circle" },
  { id: "q4-17", word: "Ettertenksom", wordEnglish: "Thoughtful", definition: "Being considerate or reflective about a situation (past, present, future), oneself", quadrant: 4, color: "#7AD4A6", shape: "diamond" },
  {
    id: "q4-18",
    word: "Fredelig",
    wordEnglish: "Peaceful",
    definition: "Full av indre fred",
    quadrant: 4,
    color: "#81D6AB",
    shape: "rounded-square",
    svgPath: "M 50 20 C 52 22, 54 25, 55 28 L 58 35 C 59 38, 60 41, 60 44 C 60 47, 59 50, 57 52 L 53 58 C 51 60, 48 62, 45 62 C 42 62, 39 60, 37 58 L 33 52 C 31 50, 30 47, 30 44 C 30 41, 31 38, 32 35 L 35 28 C 37 25, 39 22, 42 20 C 45 19, 47 19, 50 20 M 42 30 C 43 32, 44 34, 45 36 L 47 40 C 48 42, 48 44, 47 46 L 45 50 C 44 52, 42 53, 40 53 L 38 52 C 37 51, 36 49, 36 47 L 35 43 C 35 41, 36 39, 37 37 L 40 33 C 41 31, 42 30, 43 29 M 58 30 C 59 32, 60 34, 60 36 L 61 40 C 61 42, 60 44, 59 46 L 57 50 C 56 52, 54 53, 52 53 L 50 52 C 49 51, 48 49, 48 47 L 47 43 C 47 41, 48 39, 49 37 L 52 33 C 53 31, 55 30, 57 29 Z",
    formDescription: "Fredens due-form"
  },
  { id: "q4-19", word: "Komfortabel", wordEnglish: "Comfortable", definition: "Fysisk og mentalt behagelig", quadrant: 4, color: "#88D8B0", shape: "circle" },
  { id: "q4-20", word: "Bekymringsløs", wordEnglish: "Carefree", definition: "Fri for bekymringer", quadrant: 4, color: "#8FDAB5", shape: "hexagon" },
  { id: "q4-21", word: "Søvnig", wordEnglish: "Sleepy", definition: "Behagelig trøtt og rolig", quadrant: 4, color: "#6CD09C", shape: "circle" },
  { id: "q4-22", word: "Selvtilfreds", wordEnglish: "Complacent", definition: "Fornøyd med nåværende tilstand", quadrant: 4, color: "#73D2A1", shape: "diamond" },
  { id: "q4-23", word: "Stillhet", wordEnglish: "Tranquil", definition: "Dyp ro og stillhet", quadrant: 4, color: "#7AD4A6", shape: "rounded-square" },
  { id: "q4-24", word: "Koselig", wordEnglish: "Cozy", definition: "Varm og komfortabel", quadrant: 4, color: "#81D6AB", shape: "circle" },
  {
    id: "q4-25",
    word: "Fredfull",
    wordEnglish: "Serene",
    definition: "Rolig og uforstyrret",
    quadrant: 4,
    color: "#88D8B0",
    shape: "hexagon",
    svgPath: "M 50 25 L 58 30 C 60 32, 62 35, 63 38 L 65 45 C 66 48, 66 51, 65 54 L 63 61 C 62 64, 60 67, 58 69 L 50 74 L 42 69 C 40 67, 38 64, 37 61 L 35 54 C 34 51, 34 48, 35 45 L 37 38 C 38 35, 40 32, 42 30 Z M 45 38 C 46 40, 47 42, 48 44 L 49 48 C 49 50, 49 52, 48 54 L 47 58 C 46 60, 45 62, 44 63 L 50 66 L 56 63 C 55 62, 54 60, 53 58 L 52 54 C 51 52, 51 50, 52 48 L 53 44 C 54 42, 55 40, 56 38 L 50 35 L 45 38 M 48 48 C 48 49, 49 50, 50 50 C 51 50, 52 49, 52 48 C 52 47, 51 46, 50 46 C 49 46, 48 47, 48 48 Z",
    formDescription: "Lotus-blomst i ro"
  },
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
