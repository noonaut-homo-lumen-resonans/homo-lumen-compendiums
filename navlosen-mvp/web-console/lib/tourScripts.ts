/**
 * Guided Tour Scripts for Mobile Simulator
 *
 * Pre-defined tours with NVC language and Triadic Ethics compliance:
 * - Port 1: Every step can be skipped
 * - Port 2: NVC language, 8th grade reading level, transparent science
 * - Port 3: Empowerment messaging, celebrates user capacity
 *
 * @version 1.0
 * @date 2025-10-22
 * @author Code (Agent #9) - Motor Cortex
 */

export interface TourStep {
  id: string;
  title: string;
  description: string;
  targetPage: string; // Which page to navigate to
  targetElement?: string; // CSS selector or description
  position: 'top' | 'bottom' | 'left' | 'right';
}

export interface Tour {
  id: string;
  name: string;
  description: string;
  duration: string; // Estimated duration
  steps: TourStep[];
}

/**
 * Tour 1: New User Onboarding
 *
 * Introduces NAV-Losen's key features with empowering language.
 * 5 steps covering Dashboard, Mestring, Chatbot, Dokumenter, Rettigheter.
 */
export const newUserOnboardingTour: Tour = {
  id: 'new-user-onboarding',
  name: 'Welcome to NAV-Losen',
  description: 'A friendly introduction to help you explore NAV-Losen at your own pace',
  duration: '2-3 minutes',
  steps: [
    {
      id: 'welcome',
      title: 'Welcome! You're in the right place 🌟',
      description: 'NAV-Losen is here to support you on your journey with NAV. You're in control - explore at your own pace, skip what you don't need, and come back anytime.',
      targetPage: '/',
      position: 'bottom',
    },
    {
      id: 'mestring',
      title: 'Check in with yourself 🧠',
      description: 'The Mestring page helps you understand how you're feeling right now. It's based on science (Polyvagal Theory) but explained in plain language. You choose what to share - nothing is tracked without your permission.',
      targetPage: '/mestring',
      targetElement: 'Emotion Wheel',
      position: 'right',
    },
    {
      id: 'chatbot',
      title: 'Ask questions anytime 💚',
      description: 'Lira is here to answer your NAV questions in a way that makes sense to you. She won't judge - just help. You can ask about rights, deadlines, or anything else on your mind.',
      targetPage: '/chatbot',
      targetElement: 'Chat Input',
      position: 'top',
    },
    {
      id: 'dokumenter',
      title: 'Organize your documents 📄',
      description: 'Keep all your NAV documents in one place. You own this data - it's stored on your device, not our servers. Delete it anytime if you want.',
      targetPage: '/dokumenter',
      position: 'bottom',
    },
    {
      id: 'rettigheter',
      title: 'Know your rights ⚖️',
      description: 'NAV-Losen shows you what you're entitled to, with real court cases as examples. Knowledge is power - the more you understand, the stronger you become.',
      targetPage: '/rettigheter',
      position: 'right',
    },
  ],
};

/**
 * Tour 2: QDA v2.0 Demo
 *
 * Showcases the neurobiological question-answering engine.
 * 4 steps highlighting Lira's empathetic intelligence.
 */
export const qdaDemoTour: Tour = {
  id: 'qda-demo',
  name: 'Meet Lira - Your AI Guide',
  description: 'See how Lira combines AI intelligence with human empathy',
  duration: '2 minutes',
  steps: [
    {
      id: 'qda-intro',
      title: 'How Lira works 🧠',
      description: 'Lira uses 6 layers of intelligence, just like your brain. She starts with safety (Is this urgent?), then emotion (How are you feeling?), then knowledge (What do you need to know?). You'll see all 6 layers - nothing is hidden.',
      targetPage: '/chatbot',
      position: 'bottom',
    },
    {
      id: 'qda-example',
      title: 'Try asking a question 💬',
      description: 'Ask Lira anything about NAV - rights, deadlines, appeals, etc. She'll respond in Norwegian (Bokmål or Nynorsk - your choice) and explain her reasoning.',
      targetPage: '/chatbot',
      targetElement: 'Chat Input',
      position: 'top',
    },
    {
      id: 'qda-wisdom',
      title: 'Wisdom extraction 📚',
      description: 'Lira doesn't just answer - she helps you build your own understanding. You can save insights to your "Mastery Log" (if you want) so you become more independent over time.',
      targetPage: '/chatbot',
      targetElement: 'Wisdom Panel',
      position: 'right',
    },
    {
      id: 'qda-empowerment',
      title: 'You're the expert on your life 💪',
      description: 'Lira's goal is to help you need her less over time. The more you learn, the more confident you become. That's success - not dependency.',
      targetPage: '/chatbot',
      position: 'bottom',
    },
  ],
};

/**
 * Tour 3: Polyvagal Journey
 *
 * Guides users through the nervous system regulation tools.
 * 6 steps covering Dashboard, HRV, Emotions, Grounding, Music, Reflection.
 */
export const polyvagalJourneyTour: Tour = {
  id: 'polyvagal-journey',
  name: 'Regulate Your Nervous System',
  description: 'Learn science-backed techniques to feel calmer and more in control',
  duration: '3-4 minutes',
  steps: [
    {
      id: 'polyvagal-intro',
      title: 'Understanding your nervous system 🌊',
      description: 'Your body has built-in stress responses (fight, flight, freeze). NAV-Losen helps you notice these patterns and shift into a calmer state. This is based on Polyvagal Theory (Dr. Stephen Porges).',
      targetPage: '/min-reise',
      position: 'bottom',
    },
    {
      id: 'hrv-widget',
      title: 'Check your stress level 💓',
      description: 'Heart Rate Variability (HRV) shows how your nervous system is doing. Higher = calmer. Lower = stressed. You can track this over time if you want (optional).',
      targetPage: '/min-reise',
      targetElement: 'HRV Widget',
      position: 'right',
    },
    {
      id: 'emotion-check',
      title: 'Name what you're feeling 🎨',
      description: 'Research shows that naming emotions (called "affect labeling") actually reduces their intensity. The Mestring page helps you do this with 100 Norwegian emotion words.',
      targetPage: '/mestring',
      targetElement: 'Emotion Wheel',
      position: 'bottom',
    },
    {
      id: 'grounding-exercise',
      title: 'Ground yourself (5-4-3-2-1) 🧘',
      description: 'This simple exercise brings you back to the present moment. Notice 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste. It calms your nervous system in 2-3 minutes.',
      targetPage: '/ovelser/grounding-54321',
      position: 'top',
    },
    {
      id: 'healing-music',
      title: 'Listen to healing frequencies 🎵',
      description: 'Certain sound frequencies (like 528 Hz) are known to promote relaxation. Science is still exploring why, but many people find it helpful. Try it if you're curious.',
      targetPage: '/musikk',
      targetElement: 'Frequency Player',
      position: 'right',
    },
    {
      id: 'reflection',
      title: 'Celebrate your practice 🌱',
      description: 'You just learned 4 science-backed techniques to regulate stress. That's real skill-building. Use what works for you, skip what doesn't. You're the expert on your own experience.',
      targetPage: '/min-reise',
      position: 'bottom',
    },
  ],
};

/**
 * All available tours
 */
export const allTours: Tour[] = [
  newUserOnboardingTour,
  qdaDemoTour,
  polyvagalJourneyTour,
];

/**
 * Get tour by ID
 */
export function getTourById(id: string): Tour | undefined {
  return allTours.find((tour) => tour.id === id);
}
