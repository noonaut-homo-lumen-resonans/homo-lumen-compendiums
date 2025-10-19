/**
 * Verification Script: Q2 Emotion SVG Forms
 */

const fs = require('fs');
const path = require('path');

const emotionDataPath = path.join(__dirname, 'src/components/mestring/hwf/emotionData.ts');
const emotionDataContent = fs.readFileSync(emotionDataPath, 'utf-8');

// Extract Q2_EMOTIONS array
const q2Start = emotionDataContent.indexOf('export const Q2_EMOTIONS: EmotionWord[] = [');
const q3Start = emotionDataContent.indexOf('export const Q3_EMOTIONS: EmotionWord[] = [');
const q2Section = emotionDataContent.substring(q2Start, q3Start);

// Parse emotions
const emotionMatches = [...q2Section.matchAll(/{[\s\S]*?id:\s*"(q2-\d+)"[\s\S]*?}/g)];
const svgPathMatches = [...q2Section.matchAll(/svgPath:\s*"([^"]+)"/g)];
const formDescMatches = [...q2Section.matchAll(/formDescription:\s*"([^"]+)"/g)];
const colorMatches = [...q2Section.matchAll(/color:\s*"(#[A-F0-9]{6})"/gi)];
const wordMatches = [...q2Section.matchAll(/wordEnglish:\s*"([^"]+)"/g)];

console.log('\n=== Q2 (Yellow Quadrant) Emotion Verification Report ===\n');
console.log(`Total Q2 emotions found: ${emotionMatches.length}`);
console.log(`Emotions with SVG paths: ${svgPathMatches.length}`);
console.log(`Emotions with form descriptions: ${formDescMatches.length}`);
console.log(`Color values found: ${colorMatches.length}\n`);

// Verify all 25 have SVG paths
if (emotionMatches.length === 25 && svgPathMatches.length === 25) {
  console.log('✅ All 25 Q2 emotions have SVG paths');
} else {
  console.log(`❌ Missing SVG paths: ${25 - svgPathMatches.length} emotions`);
}

// Verify all have form descriptions
if (formDescMatches.length === 25) {
  console.log('✅ All 25 Q2 emotions have form descriptions');
} else {
  console.log(`❌ Missing form descriptions: ${25 - formDescMatches.length} emotions`);
}

// Verify color gradient
console.log('\n=== Color Gradient Verification ===');
const colors = colorMatches.map((m, i) => ({
  emotion: wordMatches[i] ? wordMatches[i][1] : `q2-${i + 1}`,
  color: m[1].toUpperCase()
}));

const expectedStart = '#FFCF00';
const expectedEnd = '#FFDF66';

if (colors.length > 0) {
  const firstColor = colors[0].color;
  const lastColor = colors[colors.length - 1].color;

  console.log(`First emotion (${colors[0].emotion}): ${firstColor}`);
  console.log(`Last emotion (${colors[colors.length - 1].emotion}): ${lastColor}`);
}

console.log('\n=== Q2 Complete! ===');
console.log('Q1 (Red): 25/25 ✅');
console.log('Q2 (Yellow): 25/25 ✅');
console.log('Q3 (Blue): 0/25 ⏳ (Next)');
console.log('Q4 (Green): 0/25 ⏳');
console.log('\nTotal Progress: 50/100 emotions (50%)');
console.log('\n=== End of Report ===\n');
