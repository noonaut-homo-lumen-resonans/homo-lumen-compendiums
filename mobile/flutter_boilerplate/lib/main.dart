import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:provider/provider.dart';

import 'core/biofelt/hrv_monitor.dart';
import 'core/ai/local_ai_engine.dart';
import 'core/agents/local_agent_coalition.dart';
import 'core/ama/local_memory.dart';
import 'ui/screens/consciousness_dashboard.dart';
import 'services/firebase_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp();
  
  runApp(HomoLumenApp());
}

class HomoLumenApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => HRVMonitor()),
        ChangeNotifierProvider(create: (_) => LocalAIEngine()),
        ChangeNotifierProvider(create: (_) => LocalAgentCoalition()),
        ChangeNotifierProvider(create: (_) => LocalMemory()),
        ChangeNotifierProvider(create: (_) => FirebaseService()),
      ],
      child: MaterialApp(
        title: 'Homo Lumen',
        theme: ThemeData(
          primarySwatch: Colors.indigo,
          brightness: Brightness.dark,
          visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
        home: ConsciousnessDashboard(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
} 