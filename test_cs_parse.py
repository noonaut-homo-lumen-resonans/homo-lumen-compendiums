import re
import sys
import io

# Force UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read the file
with open('agents/claude-code/LK/CODE_LIVING_COMPENDIUM_V1.4.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find CS section
# Try non-greedy first
cs_section_match_ng = re.search(
    r'##\s*[\*\s]*(?:SEKSJON \d+:\s*)?CASE[- ]STUD(?:IES|IER)[\*\s]*\n(.*?)(?=\n##[^#]|\Z)',
    content,
    re.DOTALL | re.IGNORECASE
)

# Try greedy
cs_section_match_g = re.search(
    r'##\s*[\*\s]*(?:SEKSJON \d+:\s*)?CASE[- ]STUD(?:IES|IER)[\*\s]*\n(.*)(?=\n##[^#]|\Z)',
    content,
    re.DOTALL | re.IGNORECASE
)

print("Non-greedy length:", len(cs_section_match_ng.group(1)) if cs_section_match_ng else "NONE")
print("Greedy length:", len(cs_section_match_g.group(1)) if cs_section_match_g else "NONE")

cs_section_match = cs_section_match_g  # Use greedy

if cs_section_match:
    cs_section = cs_section_match.group(1)
    print(f"✅ Found CS section ({len(cs_section)} chars)")
    print(f"\nFirst 500 chars:\n{cs_section[:500]}")

    # Split into individual case studies
    case_studies = re.split(r'\n#{0,6}\s*\*\*CS\s+#', cs_section, flags=re.IGNORECASE)

    print(f"\n✅ Split into {len(case_studies)} parts")
    for i, cs in enumerate(case_studies):
        print(f"\nPart {i} ({len(cs)} chars):")
        print(cs[:100].replace('\n', '\\n'))
else:
    print("❌ No CS section found")
