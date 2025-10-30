import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:sensors_plus/sensors_plus.dart';
import '../../services/health_sync_service.dart';

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

  // Health Connect integration
  HealthSyncService? healthSyncService;
  DateTime? _lastSyncTime;
  Timer? _syncThrottleTimer;
  
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

    // Sync to Health Connect API (throttled to every 10 seconds)
    _syncHealthDataThrottled();

    notifyListeners();
  }

  /// Sync health data to backend (throttled)
  void _syncHealthDataThrottled() {
    // Only sync if Health Sync Service is configured
    if (healthSyncService == null || !healthSyncService!.autoSyncEnabled) {
      return;
    }

    // Throttle syncs to once every 10 seconds
    final now = DateTime.now();
    if (_lastSyncTime != null &&
        now.difference(_lastSyncTime!).inSeconds < 10) {
      return;
    }

    // Cancel existing throttle timer
    _syncThrottleTimer?.cancel();

    // Start new throttle timer (debounce rapid changes)
    _syncThrottleTimer = Timer(const Duration(milliseconds: 500), () async {
      final metrics = HealthMetrics(
        hrvMs: _currentHRV,
        heartRateBpm: 60 + (_currentHRV / 2), // Estimate from HRV
        coherence: _calculateCoherence(),
        stressLevel: _calculateStressLevel(),
        energyLevel: _getEnergyLevel(),
        pustRytme: '4-6-8',
      );

      final success = await healthSyncService!.syncHealthData(metrics);

      if (success) {
        _lastSyncTime = DateTime.now();
        debugPrint('✅ Health data synced: HRV=${_currentHRV.toStringAsFixed(1)}ms');
      }
    });
  }

  /// Calculate coherence from HRV history variance
  double _calculateCoherence() {
    if (_hrvHistory.length < 10) return 0.5;

    // Calculate variance of recent HRV measurements
    final recent = _hrvHistory.skip(_hrvHistory.length - 10).toList();
    final mean = recent.reduce((a, b) => a + b) / recent.length;
    final variance = recent
        .map((v) => (v - mean) * (v - mean))
        .reduce((a, b) => a + b) / recent.length;

    // Lower variance = higher coherence
    final coherence = 1.0 / (1.0 + variance / 100);
    return coherence.clamp(0.0, 1.0);
  }

  /// Calculate stress level from HRV
  double _calculateStressLevel() {
    if (_currentHRV > 80) return 1.0; // Very low stress
    if (_currentHRV > 65) return 3.0; // Low stress
    if (_currentHRV > 50) return 5.0; // Moderate stress
    if (_currentHRV > 40) return 7.0; // High stress
    return 9.0; // Very high stress
  }

  /// Get energy level string
  String _getEnergyLevel() {
    if (_currentHRV > 100) return 'transcendent';
    if (_currentHRV > 80) return 'optimal';
    if (_currentHRV > 65) return 'balanced';
    if (_currentHRV > 40) return 'low';
    return 'depleted';
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