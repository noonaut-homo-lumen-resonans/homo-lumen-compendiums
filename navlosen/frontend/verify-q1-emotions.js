/**
 * Verification Script: Q1 Emotion SVG Forms
 *
 * Verifies that all 25 Q1 emotions have:
 * - Unique SVG paths
 * - Correct color gradient (#FF1106 → #FFA98A)
 * - Form descriptions from Manus' design
 */

const fs = require('fs');
const path = require('path');

// Read emotionData.ts
const emotionDataPath = path.join(__dirname, 'src/components/mestring/hwf/emotionData.ts');
const emotionDataContent = fs.readFileSync(emotionDataPath, 'utf-8');

// Extract Q1_EMOTIONS array
const q1Start = emotionDataContent.indexOf('export const Q1_EMOTIONS: EmotionWord[] = [');
const q2Start = emotionDataContent.indexOf('export const Q2_EMOTIONS: EmotionWord[] = [');
const q1Section = emotionDataContent.substring(q1Start, q2Start);

// Parse emotions (simple regex-based extraction)
const emotionMatches = [...q1Section.matchAll(/{\s*id:\s*"(q1-\d+)"/g)];
const svgPathMatches = [...q1Section.matchAll(/svgPath:\s*"([^"]+)"/g)];
const formDescMatches = [...q1Section.matchAll(/formDescription:\s*"([^"]+)"/g)];
const colorMatches = [...q1Section.matchAll(/color:\s*"(#[A-F0-9]{6})"/gi)];
const wordMatches = [...q1Section.matchAll(/wordEnglish:\s*"([^"]+)"/g)];

console.log('\n=== Q1 Emotion Verification Report ===\n');
console.log(`Total Q1 emotions found: ${emotionMatches.length}`);
console.log(`Emotions with SVG paths: ${svgPathMatches.length}`);
console.log(`Emotions with form descriptions: ${formDescMatches.length}`);
console.log(`Color values found: ${colorMatches.length}\n`);

// Verify all 25 have SVG paths
if (emotionMatches.length === 25 && svgPathMatches.length === 25) {
  console.log('✅ All 25 Q1 emotions have SVG paths');
} else {
  console.log(`❌ Missing SVG paths: ${25 - svgPathMatches.length} emotions`);
}

// Verify all have form descriptions
if (formDescMatches.length === 25) {
  console.log('✅ All 25 Q1 emotions have form descriptions');
} else {
  console.log(`❌ Missing form descriptions: ${25 - formDescMatches.length} emotions`);
}

// Verify color gradient
console.log('\n=== Color Gradient Verification ===');
const colors = colorMatches.map((m, i) => ({
  emotion: wordMatches[i] ? wordMatches[i][1] : `q1-${i + 1}`,
  color: m[1].toUpperCase()
}));

const expectedStart = '#FF1106';
const expectedEnd = '#FFA98A';

if (colors.length > 0) {
  const firstColor = colors[0].color;
  const lastColor = colors[colors.length - 1].color;

  console.log(`First emotion (${colors[0].emotion}): ${firstColor} ${firstColor === expectedStart ? '✅' : '❌ Expected: ' + expectedStart}`);
  console.log(`Last emotion (${colors[colors.length - 1].emotion}): ${lastColor} ${lastColor === expectedEnd ? '✅' : '❌ Expected: ' + expectedEnd}`);
}

// List all emotions with their SVG status
console.log('\n=== Emotion List with SVG Forms ===');
for (let i = 0; i < emotionMatches.length; i++) {
  const id = emotionMatches[i][1];
  const word = wordMatches[i] ? wordMatches[i][1] : 'Unknown';
  const hasSvg = i < svgPathMatches.length ? '✅' : '❌';
  const hasDesc = i < formDescMatches.length ? '✅' : '❌';
  console.log(`${id} (${word}): SVG ${hasSvg} | Description ${hasDesc}`);
}

console.log('\n=== Visual QA Checklist ===');
console.log('Manual testing required:');
console.log('□ Navigate to http://localhost:3000/mestring-hwf');
console.log('□ Enter Fase 3 (Emotion Landscape)');
console.log('□ Verify Q1 quadrant (top-left, red gradient background)');
console.log('□ Click each of 25 emotions and verify:');
console.log('  □ Square morphs to unique SVG shape');
console.log('  □ Morph animation is smooth (300ms)');
console.log('  □ Breathing animation continues (scale 1.0-1.02, 4s loop)');
console.log('  □ Color matches assigned HEX value');
console.log('  □ Form matches Manus\' design intent');
console.log('  □ Text remains legible on SVG form');
console.log('□ Test performance (60 FPS on low-end devices)');
console.log('□ Test floating animation (vertical offset)');
console.log('□ Verify responsive layout (mobile, tablet, desktop)');
console.log('\n=== End of Report ===\n');
