// Quick test to check what's in localStorage
// Run this in browser console after selecting emotion

console.log("=== Checking localStorage for emotion data ===");
console.log("navlosen-selected-emotion:", localStorage.getItem("navlosen-selected-emotion"));
console.log("navlosen-emotions:", localStorage.getItem("navlosen-emotions"));
console.log("navlosen-stress-level:", localStorage.getItem("navlosen-stress-level"));
console.log("navlosen-somatic-signals:", localStorage.getItem("navlosen-somatic-signals"));

// Parse and display selected emotion
const selectedEmotion = localStorage.getItem("navlosen-selected-emotion");
if (selectedEmotion) {
  try {
    const parsed = JSON.parse(selectedEmotion);
    console.log("Parsed selected emotion:", parsed);
    console.log("- word:", parsed.word);
    console.log("- color:", parsed.color);
    console.log("- svgPath:", parsed.svgPath ? "YES" : "NO");
    console.log("- definition:", parsed.definition);
  } catch (e) {
    console.error("Failed to parse:", e);
  }
} else {
  console.log("❌ No selected emotion in localStorage");
}
