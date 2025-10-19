/**
 * Complete Verification: All 100 HWF Emotions
 */

const fs = require('fs');
const path = require('path');

const emotionDataPath = path.join(__dirname, 'src/components/mestring/hwf/emotionData.ts');
const emotionDataContent = fs.readFileSync(emotionDataPath, 'utf-8');

console.log('\n=== HWF EMOTION WHEEL - COMPLETE VERIFICATION ===\n');

// Extract all quadrants
const quadrants = [
  { name: 'Q1 (Red)', start: 'export const Q1_EMOTIONS', end: 'export const Q2_EMOTIONS', color: '#FF1106 → #FFA98A' },
  { name: 'Q2 (Yellow)', start: 'export const Q2_EMOTIONS', end: 'export const Q3_EMOTIONS', color: '#FFCF00 → #FFDF66' },
  { name: 'Q3 (Blue)', start: 'export const Q3_EMOTIONS', end: 'export const Q4_EMOTIONS', color: '#2A70D6 → #62A8EB' },
  { name: 'Q4 (Green)', start: 'export const Q4_EMOTIONS', end: '// End of Q4', color: '#6CD09C → #9DDEBF' }
];

let totalEmotions = 0;
let totalWithSVG = 0;
let totalWithFormDesc = 0;

quadrants.forEach((quad, idx) => {
  const quadNum = idx + 1;
  const startIdx = emotionDataContent.indexOf(quad.start);
  const endIdx = quad.end ? emotionDataContent.indexOf(quad.end, startIdx) : emotionDataContent.length;
  const section = emotionDataContent.substring(startIdx, endIdx);

  const emotions = [...section.matchAll(/id:\s*"(q\d+-\d+)"/g)].length;
  const svgPaths = [...section.matchAll(/svgPath:\s*"/g)].length;
  const formDescs = [...section.matchAll(/formDescription:\s*"/g)].length;

  totalEmotions += emotions;
  totalWithSVG += svgPaths;
  totalWithFormDesc += formDescs;

  const status = (emotions === svgPaths && emotions === formDescs) ? '✅' : '❌';
  console.log(`${status} ${quad.name}:`);
  console.log(`   Emotions: ${emotions}/25`);
  console.log(`   SVG Paths: ${svgPaths}/25`);
  console.log(`   Form Descriptions: ${formDescs}/25`);
  console.log(`   Color Gradient: ${quad.color}`);
  console.log('');
});

console.log('=== TOTAL SUMMARY ===\n');
console.log(`Total Emotions: ${totalEmotions}/100`);
console.log(`With SVG Paths: ${totalWithSVG}/100`);
console.log(`With Form Descriptions: ${totalWithFormDesc}/100\n`);

if (totalEmotions === 100 && totalWithSVG === 100 && totalWithFormDesc === 100) {
  console.log('🎉 SUCCESS! All 100 emotions are complete with SVG forms!\n');
  console.log('✅ Q1 (Red): 25/25 - Høy Energi, Ubehagelig');
  console.log('✅ Q2 (Yellow): 25/25 - Høy Energi, Behagelig');
  console.log('✅ Q3 (Blue): 25/25 - Lav Energi, Ubehagelig');
  console.log('✅ Q4 (Green): 25/25 - Lav Energi, Behagelig\n');
  console.log('Living Compendium V1.7.13 → V1.7.14');
  console.log('HWF Emotion Wheel: 100% Complete\n');
} else {
  console.log('❌ Some emotions are missing SVG paths or form descriptions\n');
}

console.log('=== End of Verification ===\n');
