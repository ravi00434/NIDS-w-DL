#!/usr/bin/env python3
"""
⚙️ NIDS Configuration - Easy settings management
Simple configuration for all NIDS components
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class NIDSConfig:
    """NIDS Configuration Settings"""
    
    # Performance Settings
    batch_size: int = 32
    max_queue_size: int = 1000
    processing_threads: int = 4
    gpu_memory_growth: bool = True
    
    # Detection Settings
    confidence_threshold: float = 0.7
    alert_cooldown_seconds: int = 60
    max_alerts_per_minute: int = 10
    
    # Traffic Generation (for demos)
    attack_probability: float = 0.1
    flows_per_second: int = 5
    simulation_duration: int = 30
    
    # Web Dashboard
    web_host: str = "0.0.0.0"
    web_port: int = 5000
    web_debug: bool = False
    auto_refresh_seconds: int = 2
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "nids.log"
    alert_log_file: str = "nids_alerts.log"
    max_log_size_mb: int = 100
    
    # Model Paths
    deep_model_path: str = "models/nids_deep_model.h5"
    rf_model_path: str = "models/nids_rf_model.pkl"
    scaler_path: str = "nids_scaler.pkl"
    features_path: str = "nids_features.pkl"
    
    # Network Settings (for real network monitoring)
    network_interface: str = "eth0"
    capture_filter: str = "tcp or udp"
    promiscuous_mode: bool = False
    
    def save(self, config_path: str = "nids_config.json"):
        """Save configuration to file"""
        with open(config_path, 'w') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load(cls, config_path: str = "nids_config.json"):
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            return cls(**data)
        except FileNotFoundError:
            # Return default config if file doesn't exist
            config = cls()
            config.save(config_path)  # Save default config
            return config
    
    def get_performance_preset(self, preset: str):
        """Apply performance presets"""
        presets = {
            "low": {
                "batch_size": 8,
                "max_queue_size": 100,
                "processing_threads": 2,
                "flows_per_second": 2
            },
            "medium": {
                "batch_size": 16,
                "max_queue_size": 500,
                "processing_threads": 4,
                "flows_per_second": 5
            },
            "high": {
                "batch_size": 64,
                "max_queue_size": 2000,
                "processing_threads": 8,
                "flows_per_second": 20
            },
            "extreme": {
                "batch_size": 128,
                "max_queue_size": 5000,
                "processing_threads": 16,
                "flows_per_second": 50
            }
        }
        
        if preset in presets:
            for key, value in presets[preset].items():
                setattr(self, key, value)
    
    def optimize_for_gpu(self, gpu_memory_mb: int):
        """Optimize settings based on GPU memory"""
        if gpu_memory_mb >= 8000:  # 8GB+
            self.get_performance_preset("extreme")
        elif gpu_memory_mb >= 4000:  # 4GB+
            self.get_performance_preset("high")
        elif gpu_memory_mb >= 2000:  # 2GB+
            self.get_performance_preset("medium")
        else:  # <2GB
            self.get_performance_preset("low")
    
    def print_summary(self):
        """Print configuration summary"""
        print("⚙️ NIDS Configuration Summary")
        print("=" * 40)
        print(f"🚀 Performance: Batch size {self.batch_size}, {self.processing_threads} threads")
        print(f"🎯 Detection: {self.confidence_threshold:.0%} confidence threshold")
        print(f"🌐 Web Dashboard: {self.web_host}:{self.web_port}")
        print(f"📊 Traffic Simulation: {self.flows_per_second} flows/sec, {self.attack_probability:.0%} attacks")
        print(f"📝 Logging: {self.log_level} level to {self.log_file}")
        print("=" * 40)

# Global configuration instance
config = NIDSConfig.load()

def configure_nids():
    """Interactive configuration setup"""
    print("⚙️ NIDS Configuration Setup")
    print("=" * 40)
    
    # Load existing config
    config = NIDSConfig.load()
    
    print("Current configuration:")
    config.print_summary()
    
    print("\n🎛️ Configuration Options:")
    print("1. 🚀 Performance Presets")
    print("2. 🎯 Detection Settings") 
    print("3. 🌐 Web Dashboard Settings")
    print("4. 📊 Traffic Simulation")
    print("5. 💾 Save & Exit")
    print("6. ❌ Exit without saving")
    
    while True:
        try:
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                print("\n🚀 Performance Presets:")
                print("1. Low (2GB RAM, basic CPU)")
                print("2. Medium (4GB RAM, decent CPU)")
                print("3. High (8GB RAM, good GPU)")
                print("4. Extreme (16GB+ RAM, powerful GPU)")
                
                preset_choice = input("Select preset (1-4): ").strip()
                presets = {"1": "low", "2": "medium", "3": "high", "4": "extreme"}
                
                if preset_choice in presets:
                    config.get_performance_preset(presets[preset_choice])
                    print(f"✅ Applied {presets[preset_choice]} performance preset")
            
            elif choice == "2":
                print("\n🎯 Detection Settings:")
                threshold = input(f"Confidence threshold (current: {config.confidence_threshold:.0%}): ").strip()
                if threshold:
                    config.confidence_threshold = float(threshold) / 100
                
                cooldown = input(f"Alert cooldown seconds (current: {config.alert_cooldown_seconds}): ").strip()
                if cooldown:
                    config.alert_cooldown_seconds = int(cooldown)
            
            elif choice == "3":
                print("\n🌐 Web Dashboard Settings:")
                port = input(f"Port (current: {config.web_port}): ").strip()
                if port:
                    config.web_port = int(port)
                
                refresh = input(f"Auto-refresh seconds (current: {config.auto_refresh_seconds}): ").strip()
                if refresh:
                    config.auto_refresh_seconds = int(refresh)
            
            elif choice == "4":
                print("\n📊 Traffic Simulation:")
                attack_prob = input(f"Attack probability % (current: {config.attack_probability:.0%}): ").strip()
                if attack_prob:
                    config.attack_probability = float(attack_prob) / 100
                
                flows_rate = input(f"Flows per second (current: {config.flows_per_second}): ").strip()
                if flows_rate:
                    config.flows_per_second = int(flows_rate)
            
            elif choice == "5":
                config.save()
                print("✅ Configuration saved!")
                break
            
            elif choice == "6":
                print("❌ Exiting without saving")
                break
            
            else:
                print("❌ Invalid choice")
                
        except (ValueError, KeyboardInterrupt):
            print("❌ Invalid input or cancelled")
            break
    
    return config

if __name__ == "__main__":
    configure_nids()