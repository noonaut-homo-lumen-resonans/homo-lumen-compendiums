# Quick Reference - Homo Lumen / NAV-Losen

**Last Updated:** 16. oktober 2025

---

## 🚀 Common Commands

### Development Server
```bash
cd navlosen/frontend
npm run dev
# Opens at http://localhost:3000
```

### Build for Production
```bash
npm run build
npm run start  # Preview production build
```

### Run Tests
```bash
npm test              # Run all tests
npm test -- --watch   # Watch mode
npm test -- --coverage  # Coverage report
```

### Linting & Formatting
```bash
npm run lint          # ESLint
npm run format        # Prettier
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/mestring-emotion-wheel

# Commit changes
git add .
git commit -m "feat: Add emotion wheel component"

# Push to GitHub
git push origin feature/mestring-emotion-wheel

# Create PR
gh pr create --title "feat: Add Mestring emotion wheel" --body "Implements emotion wheel..."

# Merge after Thalus approval
gh pr merge --squash
```

---

## 📁 Important File Paths

### Documentation
```
navlosen/docs/DESIGN_SYSTEM.md                    # Design specs (READ THIS!)
navlosen/docs/FILE_ORGANIZATION_GUIDE.md          # File organization
navlosen/docs/AI_STUDIO_PROTOTYPE_INTEGRATION_PLAN.md  # Integration plan
docs/HOMOLUMENCONSTITUTIONV1.1.md                 # Constitution
docs/HOMO_LUMEN_FILOSOFI_V1.0.md                  # Philosophy
```

### Source Code
```
navlosen/ai-studio-source/                        # AI Studio backup (reference)
navlosen/frontend/                                # Your work goes here!
agents/src/                                       # Agent code (Lira, Orion, etc.)
firebase/                                         # Firebase config
```

### Screenshots
```
navlosen/prototype/screenshots/01_Dashboard.png
navlosen/prototype/screenshots/04_Mestring.png    # Crown Jewel!
navlosen/prototype/screenshots/06_Chatbot_Lira.png
```

### GitHub
```
.github/PULL_REQUEST_TEMPLATE.md                  # Triadisk checklist
.github/workflows/thalus-gate.yml                 # Automated validation
```

### Claude Code
```
.claude/instructions.md                           # Full system prompt
.claude/memory.md                                 # Key facts & decisions
.claude/quick-reference.md                        # This file!
```

---

## 🏛️ Triadisk Ethics Quick Check

### Port 1: Suverenitet (Sovereignty)
- ✅ User has control? (opt-in, opt-out, customization)
- ✅ Clear disclaimers? (AI limitations, privacy)
- ✅ Informed consent? (explicit, not implicit)

### Port 2: Koherens (Coherence)
- ✅ Science-grounded? (Polyvagal Theory, evidence-based)
- ✅ Consistent design? (follows DESIGN_SYSTEM.md)
- ✅ Predictable? (no surprises, clear feedback)

### Port 3: Healing (Capacity Building)
- ✅ Teaches? (user learns, not just does)
- ✅ Reduces dependence? (empowerment over time)
- ✅ Supports regulation? (stress reduction, somatic awareness)

### Scoring
```
Score 0.0-0.3: ✅ PROCEED (minor concern, awareness needed)
Score 0.3-0.6: ⚠️ PAUSE (moderate concern, revise)
Score 0.6-1.0: ❌ BLOCK (major concern, redesign)
```

---

## 🎨 Design System Quick Reference

### Colors
```css
/* Primary */
--color-primary: #0067C5;        /* NAV Blue */
--color-secondary: #06BED7;      /* Teal */

/* Semantic */
--color-success: #4CAF50;        /* Green */
--color-warning: #FFC107;        /* Yellow */
--color-error: #F44336;          /* Red */
--color-info: #2196F3;           /* Blue */

/* Polyvagal Stress States */
--color-calm: #4CAF50;           /* Ventral Vagal (1-3) */
--color-alert: #FFC107;          /* Sympathetic (4-7) */
--color-freeze: #F44336;         /* Dorsal Vagal (8-10) */

/* Neutrals */
--color-gray-50: #FAFAFA;
--color-gray-100: #F5F5F5;
--color-gray-200: #EEEEEE;
--color-gray-300: #E0E0E0;
--color-gray-400: #BDBDBD;
--color-gray-500: #9E9E9E;
--color-gray-600: #757575;
--color-gray-700: #616161;
--color-gray-800: #424242;
--color-gray-900: #212121;
```

### Spacing
```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 12px;
--space-lg: 16px;
--space-xl: 24px;
--space-2xl: 32px;
--space-3xl: 48px;
--space-4xl: 64px;
```

### Typography
```css
/* Font Sizes */
--font-xs: 12px;
--font-sm: 14px;
--font-base: 16px;
--font-lg: 18px;
--font-xl: 20px;
--font-2xl: 24px;
--font-3xl: 28px;
--font-4xl: 32px;

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Breakpoints
```css
/* Mobile */
@media (max-width: 767px) { }

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) { }

/* Desktop */
@media (min-width: 1024px) { }
```

---

## 🧩 Common Component Patterns

### Button
```tsx
import { Button } from '@/components/ui/Button'

<Button variant="primary" size="medium" onClick={handleClick}>
  Click Me
</Button>

// Variants: primary, secondary, text
// Sizes: small, medium, large
```

### Card
```tsx
import { Card } from '@/components/ui/Card'

<Card variant="info" title="Information">
  <p>Content here</p>
</Card>

// Variants: standard, info, warning, success, error
```

### Input
```tsx
import { Input } from '@/components/ui/Input'

<Input
  type="text"
  label="Your Name"
  placeholder="Enter your name"
  value={name}
  onChange={(e) => setName(e.target.value)}
  error={errors.name}
/>
```

### Modal
```tsx
import { Modal } from '@/components/ui/Modal'

<Modal
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  title="Confirm Action"
>
  <p>Are you sure?</p>
  <Button onClick={handleConfirm}>Yes</Button>
</Modal>
```

---

## 🌊 Polyvagal Patterns

### Stress Level Detection
```tsx
const getStressState = (level: number): 'calm' | 'alert' | 'freeze' => {
  if (level <= 3) return 'calm'      // Ventral Vagal
  if (level <= 7) return 'alert'     // Sympathetic
  return 'freeze'                    // Dorsal Vagal
}

const stressColors = {
  calm: 'bg-green-100 text-green-800',
  alert: 'bg-yellow-100 text-yellow-800',
  freeze: 'bg-red-100 text-red-800',
}
```

### Stress-Adaptive UI
```tsx
const MestringPage = () => {
  const [stressLevel, setStressLevel] = useState(5)
  const stressState = getStressState(stressLevel)
  
  return (
    <div className={stressColors[stressState]}>
      {stressState === 'freeze' && (
        <GroundingExercise />  // Show grounding first
      )}
      {stressState === 'alert' && (
        <SimplifiedUI />       // Simplified language
      )}
      {stressState === 'calm' && (
        <FullFeatures />       // All features available
      )}
    </div>
  )
}
```

### Emotion Wheel (8 Emotions)
```tsx
const emotions = [
  { name: 'Rolig', valence: 'positive', energy: 'low', color: '#4CAF50' },
  { name: 'Fokusert', valence: 'positive', energy: 'low', color: '#2196F3' },
  { name: 'Håpefull', valence: 'positive', energy: 'medium', color: '#8BC34A' },
  { name: 'Bekymret', valence: 'negative', energy: 'medium', color: '#FFC107' },
  { name: 'Stresset', valence: 'negative', energy: 'high', color: '#FF9800' },
  { name: 'Nummen', valence: 'negative', energy: 'low', color: '#9E9E9E' },
  { name: 'Forvirret', valence: 'negative', energy: 'medium', color: '#FF5722' },
  { name: 'Nysgjerrig', valence: 'positive', energy: 'high', color: '#00BCD4' },
]
```

---

## 🧪 Testing Patterns

### Component Test
```tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click Me</Button>)
    expect(screen.getByText('Click Me')).toBeInTheDocument()
  })
  
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click Me</Button>)
    fireEvent.click(screen.getByText('Click Me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### Accessibility Test
```tsx
import { axe } from 'jest-axe'

it('has no accessibility violations', async () => {
  const { container } = render(<Button>Click Me</Button>)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### Stress-State Test
```tsx
describe('MestringPage stress states', () => {
  it('shows grounding exercise when stress is high (freeze)', () => {
    render(<MestringPage initialStressLevel={9} />)
    expect(screen.getByText(/grounding/i)).toBeInTheDocument()
  })
  
  it('shows simplified UI when stress is medium (alert)', () => {
    render(<MestringPage initialStressLevel={5} />)
    expect(screen.getByText(/simplified/i)).toBeInTheDocument()
  })
  
  it('shows full features when stress is low (calm)', () => {
    render(<MestringPage initialStressLevel={2} />)
    expect(screen.getByText(/full features/i)).toBeInTheDocument()
  })
})
```

---

## 🔗 API Integration Patterns

### Lira Chatbot (Gemini API)
```tsx
import { sendMessageToLira } from '@/services/chatService'

const ChatbotPage = () => {
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState('')
  
  const handleSend = async () => {
    const liraResponse = await sendMessageToLira(message, {
      stressLevel: userStressLevel,
      userId: currentUser.id,
      sessionId: currentSession.id,
    })
    setResponse(liraResponse)
  }
  
  return (
    <div>
      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={handleSend}>Send</button>
      <div>{response}</div>
    </div>
  )
}
```

### Manus Hub (Agent Routing)
```tsx
// This will be implemented by Manus
// You don't need to build this, just call the API

const routeToManusHub = async (query: string, context: UserContext) => {
  const response = await fetch('/api/manus/route', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, context })
  })
  return response.json()
}
```

---

## 📊 Triadisk Scoring Examples

### Example 1: Emotion Wheel (Low Risk)
```
Port 1 (Suverenitet): 0.05
- User chooses emotion (not forced)
- Can skip if uncomfortable
- Clear purpose explained

Port 2 (Koherens): 0.1
- Based on emotion research (Russell's circumplex)
- Consistent with Polyvagal Theory
- Predictable interaction

Port 3 (Healing): 0.0
- Builds emotional awareness (capacity)
- Teaches emotion labeling
- No dependence created

Total Weight: 0.05 ✅ PROCEED
```

### Example 2: Automatic Stress Detection (Higher Risk)
```
Port 1 (Suverenitet): 0.4
- User not asked for consent (automatic)
- May feel invasive
- Unclear how data is used

Port 2 (Koherens): 0.2
- HRV detection is science-based
- But accuracy concerns (false positives)

Port 3 (Healing): 0.1
- Could build capacity if done right
- But risk of over-reliance on tech

Total Weight: 0.23 ⚠️ PAUSE
- Recommendation: Add explicit opt-in, show how it works
```

---

## 🎯 Priority Checklist

### Before Starting Any Component

- [ ] Read relevant section in DESIGN_SYSTEM.md
- [ ] Review screenshot (if available)
- [ ] Check AI Studio source code (reference)
- [ ] Evaluate Triadisk Ethics (all 3 ports)
- [ ] Plan accessibility (keyboard nav, screen reader)
- [ ] Consider stress states (calm/alert/freeze)

### Before Creating PR

- [ ] Component works (manual testing)
- [ ] Tests pass (unit + accessibility)
- [ ] Triadisk checklist filled out
- [ ] Code follows style guide
- [ ] No console errors/warnings
- [ ] Accessible (keyboard + screen reader)
- [ ] Responsive (mobile/tablet/desktop)

### After PR Created

- [ ] Thalus Gate workflow triggered
- [ ] Wait for Thalus review
- [ ] Address feedback (if any)
- [ ] Get TH-OK label
- [ ] Merge!

---

## 💡 Pro Tips

### 1. Use `@` Mentions in Chat
```
"Review @navlosen/docs/DESIGN_SYSTEM.md and implement Button component"
```
Claude Code will automatically read the file.

### 2. Reference Screenshots
```
"Implement the emotion wheel from @navlosen/prototype/screenshots/04_Mestring.png"
```

### 3. Check Triadisk Early
```
"Before I implement this feature, let's evaluate it through Triadisk Ethics.
Port 1 (Suverenitet): [your analysis]
Port 2 (Koherens): [your analysis]
Port 3 (Healing): [your analysis]"
```

### 4. Test in All Stress States
```tsx
// Always test components in all 3 stress states
<MestringPage initialStressLevel={2} />  // Calm
<MestringPage initialStressLevel={5} />  // Alert
<MestringPage initialStressLevel={9} />  // Freeze
```

### 5. Use Design Tokens (Not Hardcoded Values)
```tsx
// ❌ Bad
<div className="p-4 text-blue-600">

// ✅ Good
<div className="p-lg text-primary">
```

---

## 🌿 Remember

**You are building healing technology, not just an app.**

Every component should:
- ✅ Empower users (Suverenitet)
- ✅ Be grounded in science (Koherens)
- ✅ Build capacity (Healing)

**Med ontologisk integritet & felt-bevissthet!** ◉🌊✨

