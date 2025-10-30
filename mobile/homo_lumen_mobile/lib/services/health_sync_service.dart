/// Health Sync Service - Syncs biofelt data with Health Connect API
///
/// Sends real-time HRV and biofelt metrics from mobile device to backend.
/// Supports Google Health Connect (Android) and Apple HealthKit (iOS).
///
/// Philosophy: "The body knows before the mind understands"

import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

enum HealthDataSource {
  googleHealthConnect,
  appleHealthKit,
  samsungHealth,
  fitbit,
  garmin,
  manual,
  simulated
}

class HealthMetrics {
  final double hrvMs;
  final double? heartRateBpm;
  final double coherence;
  final double stressLevel;
  final String energyLevel;
  final String pustRytme;
  final DateTime timestamp;

  HealthMetrics({
    required this.hrvMs,
    this.heartRateBpm,
    required this.coherence,
    this.stressLevel = 0,
    this.energyLevel = 'balanced',
    this.pustRytme = '4-6-8',
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  Map<String, dynamic> toJson() => {
        'hrv_ms': hrvMs,
        if (heartRateBpm != null) 'heart_rate_bpm': heartRateBpm,
        'coherence': coherence,
        'stress_level': stressLevel,
        'energy_level': energyLevel,
        'pust_rytme': pustRytme,
        'timestamp': timestamp.toIso8601String(),
      };
}

class HealthSyncResponse {
  final bool success;
  final String message;
  final String resonanceLevel;
  final List<String> recommendations;

  HealthSyncResponse({
    required this.success,
    required this.message,
    required this.resonanceLevel,
    this.recommendations = const [],
  });

  factory HealthSyncResponse.fromJson(Map<String, dynamic> json) {
    return HealthSyncResponse(
      success: json['success'] ?? false,
      message: json['message'] ?? '',
      resonanceLevel: json['resonance_level'] ?? 'unknown',
      recommendations: (json['recommendations'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
    );
  }
}

class HealthSyncService extends ChangeNotifier {
  // Configuration
  final String apiBaseUrl;
  final String userId;
  final String deviceId;
  final HealthDataSource dataSource;

  // State
  bool _isSyncing = false;
  DateTime? _lastSyncTime;
  HealthSyncResponse? _lastResponse;
  String? _lastError;

  // Auto-sync settings
  bool _autoSyncEnabled = false;
  Timer? _autoSyncTimer;
  Duration _autoSyncInterval = const Duration(seconds: 30);

  HealthSyncService({
    this.apiBaseUrl = 'http://10.0.2.2:8004', // Android emulator localhost
    required this.userId,
    required this.deviceId,
    this.dataSource = HealthDataSource.simulated,
  });

  // Getters
  bool get isSyncing => _isSyncing;
  DateTime? get lastSyncTime => _lastSyncTime;
  HealthSyncResponse? get lastResponse => _lastResponse;
  String? get lastError => _lastError;
  bool get autoSyncEnabled => _autoSyncEnabled;

  /// Sync health metrics to Health Connect API
  Future<bool> syncHealthData(HealthMetrics metrics) async {
    if (_isSyncing) {
      debugPrint('⚠️ Sync already in progress, skipping...');
      return false;
    }

    _isSyncing = true;
    _lastError = null;
    notifyListeners();

    try {
      debugPrint('🔄 Syncing health data to $apiBaseUrl/api/health/sync');
      debugPrint('   HRV: ${metrics.hrvMs}ms, Coherence: ${metrics.coherence}');

      final url = Uri.parse('$apiBaseUrl/api/health/sync');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': userId,
          'device_id': deviceId,
          'source': _dataSourceToString(dataSource),
          'metrics': metrics.toJson(),
          'metadata': {
            'platform': defaultTargetPlatform.name,
            'app_version': '1.0.0',
          },
        }),
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          throw TimeoutException('Health sync request timed out');
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _lastResponse = HealthSyncResponse.fromJson(data);
        _lastSyncTime = DateTime.now();
        _lastError = null;

        debugPrint('✅ Health sync successful!');
        debugPrint('   Resonance: ${_lastResponse!.resonanceLevel}');
        if (_lastResponse!.recommendations.isNotEmpty) {
          debugPrint('   Recommendations: ${_lastResponse!.recommendations}');
        }

        notifyListeners();
        return true;
      } else {
        _lastError = 'HTTP ${response.statusCode}: ${response.body}';
        debugPrint('❌ Health sync failed: $_lastError');
        notifyListeners();
        return false;
      }
    } catch (e) {
      _lastError = e.toString();
      debugPrint('❌ Health sync error: $_lastError');
      notifyListeners();
      return false;
    } finally {
      _isSyncing = false;
      notifyListeners();
    }
  }

  /// Enable automatic syncing at regular intervals
  void enableAutoSync({Duration? interval}) {
    if (interval != null) {
      _autoSyncInterval = interval;
    }

    _autoSyncEnabled = true;
    _autoSyncTimer?.cancel();

    debugPrint('✅ Auto-sync enabled (interval: ${_autoSyncInterval.inSeconds}s)');

    // Don't start timer immediately - let the HRV monitor trigger the first sync
    notifyListeners();
  }

  /// Disable automatic syncing
  void disableAutoSync() {
    _autoSyncEnabled = false;
    _autoSyncTimer?.cancel();
    _autoSyncTimer = null;

    debugPrint('⏸️ Auto-sync disabled');
    notifyListeners();
  }

  /// Schedule next auto-sync (called by HRV monitor after measurement)
  void scheduleNextSync() {
    if (!_autoSyncEnabled) return;

    _autoSyncTimer?.cancel();
    _autoSyncTimer = Timer(_autoSyncInterval, () {
      debugPrint('⏰ Auto-sync timer triggered');
      // Timer is just a trigger - actual sync happens when HRV monitor provides new data
    });
  }

  /// Check if device can reach the API
  Future<bool> checkConnection() async {
    try {
      debugPrint('🔍 Checking Health Connect API connection...');

      final url = Uri.parse('$apiBaseUrl/api/health/status');
      final response = await http.get(url).timeout(
            const Duration(seconds: 5),
            onTimeout: () {
              throw TimeoutException('Connection check timed out');
            },
          );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        debugPrint('✅ Health Connect API is operational');
        debugPrint('   Service: ${data['service']}');
        debugPrint('   Version: ${data['version']}');
        return true;
      } else {
        debugPrint('❌ Health Connect API returned ${response.statusCode}');
        return false;
      }
    } catch (e) {
      debugPrint('❌ Health Connect API connection failed: $e');
      return false;
    }
  }

  /// Get connection status text for UI
  String getConnectionStatusText() {
    if (_lastSyncTime == null) {
      return 'Not synced yet';
    }

    final age = DateTime.now().difference(_lastSyncTime!);

    if (age.inSeconds < 60) {
      return 'Synced ${age.inSeconds}s ago';
    } else if (age.inMinutes < 60) {
      return 'Synced ${age.inMinutes}m ago';
    } else {
      return 'Synced ${age.inHours}h ago';
    }
  }

  String _dataSourceToString(HealthDataSource source) {
    switch (source) {
      case HealthDataSource.googleHealthConnect:
        return 'google_health_connect';
      case HealthDataSource.appleHealthKit:
        return 'apple_healthkit';
      case HealthDataSource.samsungHealth:
        return 'samsung_health';
      case HealthDataSource.fitbit:
        return 'fitbit';
      case HealthDataSource.garmin:
        return 'garmin';
      case HealthDataSource.manual:
        return 'manual';
      case HealthDataSource.simulated:
        return 'simulated';
    }
  }

  @override
  void dispose() {
    _autoSyncTimer?.cancel();
    super.dispose();
  }
}
