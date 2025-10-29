#!/bin/bash

# Homo Lumen Flutter Setup Script
# Sets up Flutter environment for on-device AI integration

set -e

echo "🚀 Setting up Flutter environment for Homo Lumen..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}❌ Flutter not found. Please install Flutter first:${NC}"
    echo "https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo -e "${GREEN}✅ Flutter found${NC}"

# Check Flutter version
FLUTTER_VERSION=$(flutter --version | grep -o 'Flutter [0-9.]*' | cut -d' ' -f2)
echo -e "${BLUE}📱 Flutter version: $FLUTTER_VERSION${NC}"

# Create Flutter project
PROJECT_NAME="homo_lumen_mobile"
if [ -d "$PROJECT_NAME" ]; then
    echo -e "${YELLOW}⚠️  Project directory already exists. Removing...${NC}"
    rm -rf "$PROJECT_NAME"
fi

echo -e "${BLUE}📁 Creating Flutter project: $PROJECT_NAME${NC}"
flutter create --org com.homolumen --project-name homo_lumen_mobile "$PROJECT_NAME"

cd "$PROJECT_NAME"

# Add dependencies to pubspec.yaml
echo -e "${BLUE}📦 Adding dependencies...${NC}"

# Create updated pubspec.yaml
cat > pubspec.yaml << 'EOF'
name: homo_lumen_mobile
description: Homo Lumen Consciousness-Supporting Network Mobile App
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.4.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # Firebase
  firebase_core: ^3.6.0
  firebase_firestore: ^5.4.0
  firebase_functions: ^5.3.0
  
  # AI & ML
  tensorflow_lite_flutter: ^0.10.4
  google_ai_edge: ^0.1.0
  
  # Sensors & Biofelt
  sensors_plus: ^4.0.2
  permission_handler: ^11.3.1
  
  # State Management
  provider: ^6.1.2
  
  # UI
  cupertino_icons: ^1.0.6
  fl_chart: ^0.68.0
  
  # Local Storage
  shared_preferences: ^2.2.3
  path_provider: ^2.1.3
  
  # Networking
  http: ^1.2.1
  connectivity_plus: ^5.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0

flutter:
  uses-material-design: true
  
  assets:
    - assets/models/
    - assets/config/
  
  fonts:
    - family: Roboto
      fonts:
        - asset: fonts/Roboto-Regular.ttf
        - asset: fonts/Roboto-Bold.ttf
          weight: 700
EOF

# Create directory structure
echo -e "${BLUE}📂 Creating directory structure...${NC}"
mkdir -p lib/core/{biofelt,ai,agents,ama}
mkdir -p lib/ui/{screens,widgets}
mkdir -p lib/services
mkdir -p assets/{models,config}
mkdir -p test

# Copy boilerplate files
echo -e "${BLUE}📋 Copying boilerplate files...${NC}"

# Copy main.dart
cp ../flutter_boilerplate/lib/main.dart lib/

# Copy core files
cp ../flutter_boilerplate/lib/core/biofelt/hrv_monitor.dart lib/core/biofelt/
cp ../flutter_boilerplate/lib/core/ai/local_ai_engine.dart lib/core/ai/
cp ../flutter_boilerplate/lib/ui/screens/consciousness_dashboard.dart lib/ui/screens/

# Create placeholder files for missing components
cat > lib/core/agents/local_agent_coalition.dart << 'EOF'
import 'package:flutter/foundation.dart';

class LocalAgentCoalition extends ChangeNotifier {
  // Placeholder for local agent coalition
  // Will be implemented with actual agent logic
}
EOF

cat > lib/core/ama/local_memory.dart << 'EOF'
import 'package:flutter/foundation.dart';

class LocalMemory extends ChangeNotifier {
  // Placeholder for local AMA memory
  // Will be implemented with actual memory logic
}
EOF

cat > lib/services/firebase_service.dart << 'EOF'
import 'package:flutter/foundation.dart';

class FirebaseService extends ChangeNotifier {
  // Placeholder for Firebase service
  // Will be implemented with actual Firebase logic
}
EOF

cat > lib/ui/widgets/consciousness_indicator.dart << 'EOF'
import 'package:flutter/material.dart';
import '../../core/biofelt/hrv_monitor.dart';

class ConsciousnessIndicator extends StatelessWidget {
  final double hrv;
  final ConsciousnessLayer layer;
  final double coherence;

  const ConsciousnessIndicator({
    Key? key,
    required this.hrv,
    required this.layer,
    required this.coherence,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text('Layer: ${layer.name}'),
            Text('HRV: ${hrv.toStringAsFixed(1)}'),
            Text('Coherence: ${(coherence * 100).toStringAsFixed(1)}%'),
          ],
        ),
      ),
    );
  }
}
EOF

cat > lib/ui/widgets/hrv_chart.dart << 'EOF'
import 'package:flutter/material.dart';

class HRVChart extends StatelessWidget {
  final List<double> hrvHistory;

  const HRVChart({Key? key, required this.hrvHistory}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      child: Center(
        child: Text('HRV Chart - ${hrvHistory.length} data points'),
      ),
    );
  }
}
EOF

cat > lib/ui/widgets/agent_status.dart << 'EOF'
import 'package:flutter/material.dart';

class AgentStatus extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Lira: Active'),
        Text('Thalus: Active'),
        Text('Orion: Active'),
        Text('Nyra: Active'),
        Text('Manus: Active'),
        Text('Zara: Active'),
        Text('Abacus: Active'),
      ],
    );
  }
}
EOF

# Create test file
cat > test/widget_test.dart << 'EOF'
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:homo_lumen_mobile/main.dart';

void main() {
  testWidgets('Homo Lumen app smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(HomoLumenApp());
    expect(find.text('Homo Lumen'), findsOneWidget);
  });
}
EOF

# Get dependencies
echo -e "${BLUE}📦 Getting dependencies...${NC}"
flutter pub get

# Check for issues
echo -e "${BLUE}🔍 Checking for issues...${NC}"
flutter analyze

# Create README
cat > README.md << 'EOF'
# Homo Lumen Mobile App

## On-Device AI for Consciousness Evolution

This Flutter app provides the mobile interface for Homo Lumen's consciousness-supporting network, featuring:

- **Biofelt Monitoring**: HRV and breathing pattern detection
- **Local AI Processing**: On-device Gemma 3B/Gemini Nano
- **Agent Coalition**: Local agent coordination
- **AMA Memory**: Offline-first consciousness memory
- **Consciousness Evolution**: Real-time consciousness layer tracking

## Setup

1. Install Flutter dependencies:
   ```bash
   flutter pub get
   ```

2. Run the app:
   ```bash
   flutter run
   ```

3. For production build:
   ```bash
   flutter build apk --release
   ```

## Architecture

- **Core**: Biofelt monitoring, AI processing, agent coordination
- **UI**: Consciousness dashboard, HRV charts, agent status
- **Services**: Firebase integration, local storage
- **Assets**: AI models, configuration files

## Consciousness Layers

- **Reactive**: HRV < 60 (basic operations)
- **Strategic**: HRV 60-80 (planning and coordination)
- **Meta**: HRV 80-100 (philosophical insights)
- **Evolutionary**: HRV > 100 (creative innovation)

## Development

This app is part of the Homo Lumen ecosystem, providing the ultimate layer of cognitive sovereignty through on-device AI processing.
EOF

echo -e "${GREEN}✅ Flutter environment setup complete!${NC}"
echo -e "${BLUE}📱 Project created in: $PROJECT_NAME${NC}"
echo -e "${YELLOW}🚀 Next steps:${NC}"
echo "1. cd $PROJECT_NAME"
echo "2. flutter run"
echo "3. Add AI models to assets/models/"
echo "4. Configure Firebase in lib/services/firebase_service.dart"

# Optional: Open in VS Code
if command -v code &> /dev/null; then
    echo -e "${BLUE}📝 Opening in VS Code...${NC}"
    code .
fi 