import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:sensors_plus/sensors_plus.dart';

enum ConsciousnessLayer {
  reactive,    // HRV < 60
  strategic,   // HRV 60-80
  meta,        // HRV 80-100
  evolutionary // HRV > 100
}

class HRVMonitor extends ChangeNotifier {
  StreamSubscription<AccelerometerEvent>? _accelerometerSubscription;
  StreamSubscription<GyroscopeEvent>? _gyroscopeSubscription;
  
  double _currentHRV = 75.0;
  ConsciousnessLayer _currentLayer = ConsciousnessLayer.strategic;
  bool _isMonitoring = false;
  List<double> _hrvHistory = [];
  
  // Getters
  double get currentHRV => _currentHRV;
  ConsciousnessLayer get currentLayer => _currentLayer;
  bool get isMonitoring => _isMonitoring;
  List<double> get hrvHistory => List.unmodifiable(_hrvHistory);
  
  // Consciousness layer thresholds
  static const double REACTIVE_THRESHOLD = 60.0;
  static const double STRATEGIC_THRESHOLD = 80.0;
  static const double META_THRESHOLD = 100.0;
  
  void startMonitoring() {
    if (_isMonitoring) return;
    
    _isMonitoring = true;
    _hrvHistory.clear();
    
    // Monitor accelerometer for heart rate variability
    _accelerometerSubscription = accelerometerEvents.listen((event) {
      _processSensorData(event);
    });
    
    // Monitor gyroscope for additional biofelt data
    _gyroscopeSubscription = gyroscopeEvents.listen((event) {
      _processGyroscopeData(event);
    });
    
    notifyListeners();
  }
  
  void stopMonitoring() {
    _isMonitoring = false;
    _accelerometerSubscription?.cancel();
    _gyroscopeSubscription?.cancel();
    notifyListeners();
  }
  
  void _processSensorData(AccelerometerEvent event) {
    // Calculate HRV from accelerometer data
    // This is a simplified algorithm - in practice, you'd use more sophisticated methods
    
    final magnitude = _calculateMagnitude(event.x, event.y, event.z);
    final hrv = _calculateHRVFromMagnitude(magnitude);
    
    _updateHRV(hrv);
  }
  
  void _processGyroscopeData(GyroscopeEvent event) {
    // Additional biofelt data processing
    // Could be used for breathing patterns, movement analysis, etc.
  }
  
  double _calculateMagnitude(double x, double y, double z) {
    return (x * x + y * y + z * z).sqrt();
  }
  
  double _calculateHRVFromMagnitude(double magnitude) {
    // Simplified HRV calculation
    // In practice, this would involve:
    // 1. Peak detection in the signal
    // 2. RR interval calculation
    // 3. Frequency domain analysis
    
    // Placeholder algorithm
    final baseHRV = 75.0;
    final variation = (magnitude - 9.8) * 10; // 9.8 m/s² is gravity
    return (baseHRV + variation).clamp(40.0, 120.0);
  }
  
  void _updateHRV(double hrv) {
    _currentHRV = hrv;
    _hrvHistory.add(hrv);
    
    // Keep only last 100 measurements
    if (_hrvHistory.length > 100) {
      _hrvHistory.removeAt(0);
    }
    
    // Update consciousness layer
    _updateConsciousnessLayer();
    
    notifyListeners();
  }
  
  void _updateConsciousnessLayer() {
    ConsciousnessLayer newLayer;
    
    if (_currentHRV < REACTIVE_THRESHOLD) {
      newLayer = ConsciousnessLayer.reactive;
    } else if (_currentHRV < STRATEGIC_THRESHOLD) {
      newLayer = ConsciousnessLayer.strategic;
    } else if (_currentHRV < META_THRESHOLD) {
      newLayer = ConsciousnessLayer.meta;
    } else {
      newLayer = ConsciousnessLayer.evolutionary;
    }
    
    if (newLayer != _currentLayer) {
      _currentLayer = newLayer;
      _onConsciousnessLayerChanged();
    }
  }
  
  void _onConsciousnessLayerChanged() {
    // Notify other components about consciousness layer change
    // This could trigger different AI processing modes, UI updates, etc.
    print('Consciousness layer changed to: ${_currentLayer.name}');
  }
  
  // Biofelt validation methods
  bool isBiofeltValid() {
    // Check if HRV is within acceptable range for consciousness operations
    return _currentHRV >= 50.0 && _currentHRV <= 110.0;
  }
  
  double getBiofeltCoherence() {
    // Calculate coherence based on HRV stability
    if (_hrvHistory.length < 10) return 0.5;
    
    final mean = _hrvHistory.reduce((a, b) => a + b) / _hrvHistory.length;
    final variance = _hrvHistory.map((h) => (h - mean) * (h - mean))
        .reduce((a, b) => a + b) / _hrvHistory.length;
    
    // Higher coherence = lower variance
    return (1.0 / (1.0 + variance)).clamp(0.0, 1.0);
  }
  
  // Breathing pattern detection
  List<double> getBreathingPattern() {
    // Analyze HRV data for breathing patterns
    // This would implement 4-6-8 breathing technique detection
    return _hrvHistory.take(20).toList();
  }
  
  @override
  void dispose() {
    stopMonitoring();
    super.dispose();
  }
} 