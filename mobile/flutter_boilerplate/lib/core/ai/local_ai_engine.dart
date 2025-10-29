import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:tensorflow_lite_flutter/tensorflow_lite_flutter.dart';

import '../biofelt/hrv_monitor.dart';

class LocalAIEngine extends ChangeNotifier {
  Interpreter? _interpreter;
  bool _isInitialized = false;
  String _modelPath = '';
  
  // Getters
  bool get isInitialized => _isInitialized;
  String get modelPath => _modelPath;
  
  Future<void> initialize({String modelPath = 'assets/models/gemma_3b.tflite'}) async {
    try {
      _modelPath = modelPath;
      
      // Load TensorFlow Lite model
      _interpreter = await Interpreter.fromAsset(modelPath);
      
      // Allocate tensors
      _interpreter!.allocateTensors();
      
      _isInitialized = true;
      notifyListeners();
      
      print('✅ Local AI Engine initialized with model: $modelPath');
    } catch (e) {
      print('❌ Failed to initialize Local AI Engine: $e');
      _isInitialized = false;
    }
  }
  
  Future<String> processConsciousnessQuery(
    String query, 
    double hrv,
    ConsciousnessLayer layer
  ) async {
    if (!_isInitialized || _interpreter == null) {
      return 'AI Engine not initialized';
    }
    
    try {
      // Prepare input data
      final inputData = _prepareInputData(query, hrv, layer);
      
      // Prepare output tensor
      final outputShape = _interpreter!.getOutputTensor(0).shape;
      final outputData = List.filled(outputShape.reduce((a, b) => a * b), 0.0);
      
      // Run inference
      _interpreter!.run(inputData, outputData);
      
      // Process output
      final response = _processOutput(outputData, query);
      
      return response;
    } catch (e) {
      print('❌ AI processing error: $e');
      return 'Error processing query: $e';
    }
  }
  
  List<List<double>> _prepareInputData(String query, double hrv, ConsciousnessLayer layer) {
    // Convert text to numerical representation
    final textEncoding = _encodeText(query);
    
    // Normalize HRV (0-1 range)
    final normalizedHRV = (hrv - 40.0) / 80.0; // Assuming HRV range 40-120
    
    // Encode consciousness layer
    final layerEncoding = _encodeConsciousnessLayer(layer);
    
    // Combine all inputs
    final combinedInput = [
      ...textEncoding,
      normalizedHRV,
      ...layerEncoding,
    ];
    
    // Pad or truncate to expected input size (512 for this example)
    final paddedInput = _padToSize(combinedInput, 512);
    
    return [paddedInput];
  }
  
  List<double> _encodeText(String text) {
    // Simple character-based encoding
    // In practice, you'd use a proper tokenizer
    final bytes = utf8.encode(text);
    return bytes.map((b) => b / 255.0).toList();
  }
  
  List<double> _encodeConsciousnessLayer(ConsciousnessLayer layer) {
    // One-hot encoding for consciousness layers
    final encoding = List.filled(4, 0.0);
    encoding[layer.index] = 1.0;
    return encoding;
  }
  
  List<double> _padToSize(List<double> input, int size) {
    if (input.length >= size) {
      return input.take(size).toList();
    } else {
      return [...input, ...List.filled(size - input.length, 0.0)];
    }
  }
  
  String _processOutput(List<double> outputData, String originalQuery) {
    // Convert output back to text
    // This is a simplified version - in practice, you'd use proper decoding
    
    final maxIndex = outputData.indexOf(outputData.reduce((a, b) => a > b ? a : b));
    
    // Generate response based on output
    final responses = {
      0: 'Reactive response: Processing at basic level.',
      1: 'Strategic response: Analyzing patterns and planning.',
      2: 'Meta response: Philosophical and ontological insights.',
      3: 'Evolutionary response: Creative and transformative insights.',
    };
    
    return responses[maxIndex] ?? 'Processing complete.';
  }
  
  // Biofelt-aware processing
  Future<String> processWithBiofeltValidation(
    String query,
    double hrv,
    double coherence
  ) async {
    // Check biofelt validity before processing
    if (coherence < 0.6) {
      return 'Biofelt coherence too low (${(coherence * 100).toStringAsFixed(1)}%). Please practice breathing techniques.';
    }
    
    final layer = _getConsciousnessLayer(hrv);
    return await processConsciousnessQuery(query, hrv, layer);
  }
  
  ConsciousnessLayer _getConsciousnessLayer(double hrv) {
    if (hrv < 60) return ConsciousnessLayer.reactive;
    if (hrv < 80) return ConsciousnessLayer.strategic;
    if (hrv < 100) return ConsciousnessLayer.meta;
    return ConsciousnessLayer.evolutionary;
  }
  
  // Model management
  Future<void> loadModel(String modelPath) async {
    await initialize(modelPath: modelPath);
  }
  
  Future<void> unloadModel() async {
    _interpreter?.close();
    _interpreter = null;
    _isInitialized = false;
    notifyListeners();
  }
  
  // Performance monitoring
  Map<String, dynamic> getPerformanceMetrics() {
    if (_interpreter == null) return {};
    
    return {
      'model_loaded': _isInitialized,
      'model_path': _modelPath,
      'input_tensors': _interpreter!.getInputTensors().length,
      'output_tensors': _interpreter!.getOutputTensors().length,
      'memory_usage': 'N/A', // Would need platform-specific implementation
    };
  }
  
  @override
  void dispose() {
    unloadModel();
    super.dispose();
  }
} 