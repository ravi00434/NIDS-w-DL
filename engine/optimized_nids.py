#!/usr/bin/env python3
"""
🚀 Optimized NIDS Engine - High Performance Network Intrusion Detection
Optimized for speed, memory efficiency, and ease of use
"""

import numpy as np
import tensorflow as tf
import joblib
import time
import threading
import queue
from collections import deque, defaultdict
from datetime import datetime
import logging

# Configure TensorFlow for optimal performance
tf.config.experimental.enable_memory_growth = True
tf.config.threading.set_inter_op_parallelism_threads(0)
tf.config.threading.set_intra_op_parallelism_threads(0)

class OptimizedNIDS:
    """High-performance NIDS with GPU optimization"""
    
    def __init__(self, batch_size=32, max_queue_size=1000):
        self.batch_size = batch_size
        self.max_queue_size = max_queue_size
        
        # Models and preprocessing
        self.model = None
        self.scaler = None
        self.feature_names = None
        
        # Processing queues
        self.input_queue = queue.Queue(maxsize=max_queue_size)
        self.result_queue = queue.Queue(maxsize=max_queue_size)
        
        # Statistics
        self.stats = {
            'flows_processed': 0,
            'attacks_detected': 0,
            'processing_time': deque(maxlen=100),
            'start_time': None
        }
        
        # Threading
        self.running = False
        self.batch_processor = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, 
                          format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def load_models(self, model_path='models/nids_deep_model.h5', 
                   scaler_path='nids_scaler.pkl', features_path='nids_features.pkl'):
        """Load pre-trained models with optimization"""
        try:
            # Load deep learning model
            self.model = tf.keras.models.load_model(model_path)
            
            # Optimize model for inference
            self.model.compile(optimizer='adam', loss='binary_crossentropy')
            
            # Load preprocessing components
            self.scaler = joblib.load(scaler_path)
            self.feature_names = joblib.load(features_path)
            
            # Warm up the model with dummy data
            dummy_input = np.random.randn(1, len(self.feature_names)).astype(np.float32)
            _ = self.model.predict(dummy_input, verbose=0)
            
            self.logger.info("✅ Models loaded and optimized")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load models: {e}")
            return False
    
    def extract_features(self, flow_data):
        """Optimized feature extraction"""
        features = np.zeros(len(self.feature_names), dtype=np.float32)
        
        for i, feature in enumerate(self.feature_names):
            if feature in flow_data:
                features[i] = float(flow_data[feature])
        
        return features
    
    def batch_predict(self, batch_data):
        """Optimized batch prediction"""
        if len(batch_data) == 0:
            return []
        
        # Convert to numpy array
        batch_array = np.array(batch_data, dtype=np.float32)
        
        # Scale features
        batch_scaled = self.scaler.transform(batch_array)
        
        # GPU prediction
        start_time = time.time()
        predictions = self.model.predict(batch_scaled, verbose=0)
        processing_time = time.time() - start_time
        
        # Store processing time for statistics
        self.stats['processing_time'].append(processing_time)
        
        # Convert predictions to results
        results = []
        for i, pred in enumerate(predictions):
            confidence = float(pred[0])
            is_attack = confidence > 0.5
            
            results.append({
                'is_attack': is_attack,
                'confidence': confidence if is_attack else 1 - confidence,
                'processing_time': processing_time / len(batch_data)
            })
        
        return results
    
    def batch_processor_thread(self):
        """Background thread for batch processing"""
        batch_data = []
        batch_metadata = []
        
        while self.running:
            try:
                # Collect batch
                while len(batch_data) < self.batch_size and self.running:
                    try:
                        item = self.input_queue.get(timeout=0.1)
                        flow_data, metadata = item
                        features = self.extract_features(flow_data)
                        batch_data.append(features)
                        batch_metadata.append(metadata)
                    except queue.Empty:
                        break
                
                # Process batch if we have data
                if batch_data:
                    results = self.batch_predict(batch_data)
                    
                    # Send results back
                    for result, metadata in zip(results, batch_metadata):
                        self.result_queue.put((result, metadata))
                        self.stats['flows_processed'] += 1
                        if result['is_attack']:
                            self.stats['attacks_detected'] += 1
                    
                    # Clear batch
                    batch_data.clear()
                    batch_metadata.clear()
                
            except Exception as e:
                self.logger.error(f"Batch processing error: {e}")
    
    def start_processing(self):
        """Start the optimized processing engine"""
        if self.model is None:
            self.logger.error("❌ Models not loaded. Call load_models() first.")
            return False
        
        self.running = True
        self.stats['start_time'] = datetime.now()
        
        # Start batch processor thread
        self.batch_processor = threading.Thread(target=self.batch_processor_thread)
        self.batch_processor.daemon = True
        self.batch_processor.start()
        
        self.logger.info("🚀 Optimized NIDS processing started")
        return True
    
    def stop_processing(self):
        """Stop the processing engine"""
        self.running = False
        if self.batch_processor:
            self.batch_processor.join(timeout=5)
        self.logger.info("🛑 NIDS processing stopped")
    
    def process_flow(self, flow_data, metadata=None):
        """Add flow to processing queue"""
        if not self.running:
            return None
        
        try:
            self.input_queue.put((flow_data, metadata), timeout=0.1)
            return True
        except queue.Full:
            self.logger.warning("⚠️ Processing queue full, dropping flow")
            return False
    
    def get_result(self, timeout=0.1):
        """Get processing result"""
        try:
            return self.result_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_performance_stats(self):
        """Get performance statistics"""
        runtime = (datetime.now() - self.stats['start_time']).total_seconds() if self.stats['start_time'] else 0
        
        avg_processing_time = np.mean(self.stats['processing_time']) if self.stats['processing_time'] else 0
        flows_per_second = self.stats['flows_processed'] / runtime if runtime > 0 else 0
        
        return {
            'flows_processed': self.stats['flows_processed'],
            'attacks_detected': self.stats['attacks_detected'],
            'runtime_seconds': runtime,
            'flows_per_second': flows_per_second,
            'avg_processing_time_ms': avg_processing_time * 1000,
            'queue_size': self.input_queue.qsize(),
            'detection_rate': (self.stats['attacks_detected'] / max(1, self.stats['flows_processed'])) * 100
        }

class FastTrafficGenerator:
    """Optimized traffic generator for testing"""
    
    def __init__(self, attack_probability=0.1):
        self.attack_probability = attack_probability
        self.feature_templates = self._create_templates()
    
    def _create_templates(self):
        """Pre-create feature templates for speed"""
        normal_template = {
            'dur': 0.1, 'proto': 0, 'service': 1, 'state': 2, 'spkts': 50, 'dpkts': 45,
            'sbytes': 2000, 'dbytes': 1800, 'rate': 500, 'sttl': 64, 'dttl': 64,
            'sload': 400, 'dload': 350, 'sloss': 0, 'dloss': 0, 'sinpkt': 20, 'dinpkt': 18,
            'sjit': 2.0, 'djit': 1.8, 'swin': 32768, 'stcpb': 0, 'dtcpb': 0, 'dwin': 32768,
            'tcprtt': 10, 'synack': 5, 'ackdat': 3, 'smean': 800, 'dmean': 750,
            'trans_depth': 1, 'response_body_len': 1000, 'ct_srv_src': 2, 'ct_state_ttl': 1,
            'ct_dst_ltm': 2, 'ct_src_dport_ltm': 1, 'ct_dst_sport_ltm': 1, 'ct_dst_src_ltm': 2,
            'is_ftp_login': 0, 'ct_ftp_cmd': 0, 'ct_flw_http_mthd': 1, 'ct_src_ltm': 2,
            'ct_srv_dst': 2, 'is_sm_ips_ports': 0
        }
        
        attack_template = normal_template.copy()
        attack_template.update({
            'spkts': 5000, 'sbytes': 50000, 'rate': 10000, 'sload': 8000,
            'response_body_len': 100000, 'trans_depth': 10
        })
        
        return {'normal': normal_template, 'attack': attack_template}
    
    def generate_flow(self):
        """Generate optimized network flow"""
        is_attack = np.random.random() < self.attack_probability
        template = self.feature_templates['attack' if is_attack else 'normal']
        
        # Add some randomness
        flow = template.copy()
        for key in ['spkts', 'dpkts', 'sbytes', 'dbytes']:
            flow[key] = int(template[key] * (0.8 + 0.4 * np.random.random()))
        
        # Add metadata
        flow['src_ip'] = f"192.168.1.{np.random.randint(1, 255)}"
        flow['dst_ip'] = f"10.0.0.{np.random.randint(1, 255)}"
        flow['timestamp'] = datetime.now().isoformat()
        flow['actual_attack'] = is_attack  # Ground truth for testing
        
        return flow

def run_optimized_demo():
    """Run optimized NIDS demo"""
    print("🚀 Optimized NIDS Demo")
    print("="*50)
    
    # Initialize NIDS
    nids = OptimizedNIDS(batch_size=16)
    
    if not nids.load_models():
        print("❌ Failed to load models")
        return
    
    # Start processing
    if not nids.start_processing():
        print("❌ Failed to start processing")
        return
    
    # Initialize traffic generator
    generator = FastTrafficGenerator(attack_probability=0.2)
    
    print("🛡️ Starting high-performance monitoring...")
    print("📊 Processing flows in optimized batches...")
    
    try:
        start_time = time.time()
        flows_sent = 0
        
        # Generate and process flows
        while time.time() - start_time < 30:  # Run for 30 seconds
            flow = generator.generate_flow()
            
            if nids.process_flow(flow, {'flow_id': flows_sent}):
                flows_sent += 1
            
            # Check for results
            result = nids.get_result()
            if result:
                prediction, metadata = result
                if prediction['is_attack']:
                    print(f"🚨 ATTACK DETECTED - Confidence: {prediction['confidence']:.2%}")
            
            # Show stats every 5 seconds
            if flows_sent % 100 == 0:
                stats = nids.get_performance_stats()
                print(f"📈 Processed: {stats['flows_processed']}, "
                      f"Rate: {stats['flows_per_second']:.1f} flows/sec, "
                      f"Attacks: {stats['attacks_detected']}")
            
            time.sleep(0.01)  # Small delay to prevent overwhelming
        
        # Final statistics
        final_stats = nids.get_performance_stats()
        print("\n🎯 Final Performance Report:")
        print(f"Total Flows: {final_stats['flows_processed']}")
        print(f"Processing Rate: {final_stats['flows_per_second']:.1f} flows/sec")
        print(f"Attacks Detected: {final_stats['attacks_detected']}")
        print(f"Detection Rate: {final_stats['detection_rate']:.1f}%")
        print(f"Avg Processing Time: {final_stats['avg_processing_time_ms']:.2f}ms")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    
    finally:
        nids.stop_processing()
        print("✅ Optimized demo completed!")

if __name__ == "__main__":
    run_optimized_demo()