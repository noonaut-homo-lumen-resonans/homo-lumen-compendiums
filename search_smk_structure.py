#!/usr/bin/env python3
"""Search for LP and EM structure in SMK files"""
import sys
import io
from pathlib import Path
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('=' * 70)
print('SØKER ETTER LP (LEARNING POINTS) OG EM I SMK-FILER')
print('=' * 70 + '\n')

smk_dir = Path('SMK')
lp_pattern = re.compile(r'##.*LP.*|##.*LEARNING.*POINT|##.*LÆRINGS|## 📚', re.IGNORECASE)
em_pattern = re.compile(r'##.*EMERGENT|##.*MØNSTER', re.IGNORECASE)

found_count = 0
for smk_file in smk_dir.glob('*.md'):
    try:
        content = smk_file.read_text(encoding='utf-8')
        has_lp = lp_pattern.search(content)
        has_em = em_pattern.search(content)

        if has_lp or has_em:
            print(f'📄 {smk_file.name}')
            if has_lp:
                # Find the section
                match = lp_pattern.search(content)
                section_start = match.start()
                section_preview = content[section_start:section_start+200]
                print(f'   ✅ Har Learning Points seksjon')
                print(f'      Preview: {section_preview[:100]}...')
            if has_em:
                match = em_pattern.search(content)
                section_start = match.start()
                section_preview = content[section_start:section_start+200]
                print(f'   ✅ Har Emergent Pattern seksjon')
                print(f'      Preview: {section_preview[:100]}...')
            print()
            found_count += 1
    except Exception as e:
        pass

print('=' * 70)
print(f'TOTALT: {found_count} SMK-filer med LP eller EM seksjoner')
print('=' * 70)
