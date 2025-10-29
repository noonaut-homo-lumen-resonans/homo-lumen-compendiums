import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/biofelt/hrv_monitor.dart';
import '../../core/ai/local_ai_engine.dart';
import '../../core/agents/local_agent_coalition.dart';
import '../../widgets/consciousness_indicator.dart';
import '../../widgets/hrv_chart.dart';
import '../../widgets/agent_status.dart';

class ConsciousnessDashboard extends StatefulWidget {
  @override
  _ConsciousnessDashboardState createState() => _ConsciousnessDashboardState();
}

class _ConsciousnessDashboardState extends State<ConsciousnessDashboard> {
  final TextEditingController _queryController = TextEditingController();
  String _aiResponse = '';
  bool _isProcessing = false;

  @override
  void initState() {
    super.initState();
    // Start HRV monitoring when dashboard loads
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<HRVMonitor>().startMonitoring();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Homo Lumen - Consciousness Dashboard'),
        backgroundColor: Colors.indigo[900],
        elevation: 0,
      ),
      body: Consumer<HRVMonitor>(
        builder: (context, hrvMonitor, child) {
          return Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.indigo[900]!,
                  Colors.indigo[800]!,
                  Colors.indigo[700]!,
                ],
              ),
            ),
            child: SafeArea(
              child: SingleChildScrollView(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Consciousness Status Card
                    Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Padding(
                        padding: EdgeInsets.all(20.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Consciousness Status',
                              style: TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                color: Colors.indigo[900],
                              ),
                            ),
                            SizedBox(height: 16),
                            ConsciousnessIndicator(
                              hrv: hrvMonitor.currentHRV,
                              layer: hrvMonitor.currentLayer,
                              coherence: hrvMonitor.getBiofeltCoherence(),
                            ),
                          ],
                        ),
                      ),
                    ),
                    
                    SizedBox(height: 20),
                    
                    // HRV Chart
                    Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Padding(
                        padding: EdgeInsets.all(20.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Biofelt Monitoring',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Colors.indigo[900],
                              ),
                            ),
                            SizedBox(height: 16),
                            HRVChart(hrvHistory: hrvMonitor.hrvHistory),
                            SizedBox(height: 16),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  'HRV: ${hrvMonitor.currentHRV.toStringAsFixed(1)}',
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                                Text(
                                  'Coherence: ${(hrvMonitor.getBiofeltCoherence() * 100).toStringAsFixed(1)}%',
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                    
                    SizedBox(height: 20),
                    
                    // AI Query Section
                    Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Padding(
                        padding: EdgeInsets.all(20.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Consciousness AI',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Colors.indigo[900],
                              ),
                            ),
                            SizedBox(height: 16),
                            TextField(
                              controller: _queryController,
                              decoration: InputDecoration(
                                hintText: 'Ask about consciousness evolution...',
                                border: OutlineInputBorder(
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                filled: true,
                                fillColor: Colors.grey[100],
                              ),
                              maxLines: 3,
                            ),
                            SizedBox(height: 16),
                            Row(
                              children: [
                                Expanded(
                                  child: ElevatedButton(
                                    onPressed: _isProcessing ? null : _processQuery,
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: Colors.indigo[600],
                                      padding: EdgeInsets.symmetric(vertical: 16),
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                    ),
                                    child: _isProcessing
                                        ? CircularProgressIndicator(color: Colors.white)
                                        : Text(
                                            'Process with AI',
                                            style: TextStyle(
                                              fontSize: 16,
                                              fontWeight: FontWeight.bold,
                                            ),
                                          ),
                                  ),
                                ),
                              ],
                            ),
                            if (_aiResponse.isNotEmpty) ...[
                              SizedBox(height: 16),
                              Container(
                                padding: EdgeInsets.all(16),
                                decoration: BoxDecoration(
                                  color: Colors.grey[100],
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'AI Response:',
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: Colors.indigo[900],
                                      ),
                                    ),
                                    SizedBox(height: 8),
                                    Text(_aiResponse),
                                  ],
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                    ),
                    
                    SizedBox(height: 20),
                    
                    // Agent Status
                    Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Padding(
                        padding: EdgeInsets.all(20.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Agent Coalition Status',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Colors.indigo[900],
                              ),
                            ),
                            SizedBox(height: 16),
                            AgentStatus(),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Future<void> _processQuery() async {
    if (_queryController.text.trim().isEmpty) return;

    setState(() {
      _isProcessing = true;
    });

    try {
      final hrvMonitor = context.read<HRVMonitor>();
      final aiEngine = context.read<LocalAIEngine>();
      final agentCoalition = context.read<LocalAgentCoalition>();

      // Check biofelt validity
      if (!hrvMonitor.isBiofeltValid()) {
        setState(() {
          _aiResponse = 'Biofelt validation failed. Please practice breathing techniques to improve HRV coherence.';
          _isProcessing = false;
        });
        return;
      }

      // Process with AI
      final response = await aiEngine.processWithBiofeltValidation(
        _queryController.text,
        hrvMonitor.currentHRV,
        hrvMonitor.getBiofeltCoherence(),
      );

      setState(() {
        _aiResponse = response;
        _isProcessing = false;
      });
    } catch (e) {
      setState(() {
        _aiResponse = 'Error processing query: $e';
        _isProcessing = false;
      });
    }
  }

  @override
  void dispose() {
    _queryController.dispose();
    super.dispose();
  }
} 