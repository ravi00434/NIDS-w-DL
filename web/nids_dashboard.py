#!/usr/bin/env python3
"""
Web Dashboard for Network Intrusion Detection System
Provides a real-time web interface for monitoring network security
"""

import json
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import queue
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from engine.optimized_nids import OptimizedNIDS, FastTrafficGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nids_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global NIDS instance
nids_system = None
traffic_generator = None
dashboard_data = {
    'alerts': [],
    'stats': {},
    'recent_flows': []
}

class DashboardManager:
    """Manages dashboard data and real-time updates"""
    
    def __init__(self):
        self.running = False
        
    def update_dashboard(self):
        """Update dashboard data periodically"""
        
        while self.running:
            if nids_system and traffic_generator:
                # Generate and process traffic
                for _ in range(5):  # Process 5 flows per update
                    flow = traffic_generator.generate_flow()
                    nids_system.process_flow(flow)
                    
                    # Check for results
                    result = nids_system.get_result()
                    if result:
                        prediction, metadata = result
                        if prediction['is_attack']:
                            # Create alert
                            alert = {
                                'id': len(dashboard_data['alerts']) + 1,
                                'timestamp': datetime.now().isoformat(),
                                'severity': 'CRITICAL' if prediction['confidence'] > 0.9 else 'HIGH',
                                'confidence': prediction['confidence'],
                                'src_ip': flow.get('src_ip', 'unknown'),
                                'dst_ip': flow.get('dst_ip', 'unknown'),
                                'description': f"Attack detected with {prediction['confidence']:.1%} confidence"
                            }
                            dashboard_data['alerts'].append(alert)
                            socketio.emit('new_alert', alert)
                
                # Get performance stats
                stats = nids_system.get_performance_stats()
                dashboard_data['stats'] = stats
                socketio.emit('stats_update', stats)
            
            time.sleep(2)  # Update every 2 seconds
    
    def start(self):
        """Start dashboard updates"""
        self.running = True
        update_thread = threading.Thread(target=self.update_dashboard)
        update_thread.daemon = True
        update_thread.start()
    
    def stop(self):
        """Stop dashboard updates"""
        self.running = False

dashboard_manager = DashboardManager()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get current system statistics"""
    if nids_system:
        return jsonify(nids_system.get_performance_stats())
    return jsonify({'error': 'NIDS not running'})

@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    return jsonify(dashboard_data['alerts'][-50:])  # Last 50 alerts

@app.route('/api/start', methods=['POST'])
def start_nids():
    """Start the optimized NIDS system"""
    global nids_system, traffic_generator
    
    try:
        if not nids_system:
            nids_system = OptimizedNIDS(batch_size=16)
            if not nids_system.load_models():
                return jsonify({'status': 'error', 'message': 'Failed to load models'})
        
        attack_prob = request.json.get('attack_probability', 0.1)
        
        # Start processing engine
        if nids_system.start_processing():
            # Start traffic generator
            traffic_generator = FastTrafficGenerator(attack_probability=attack_prob)
            dashboard_manager.start()
            return jsonify({'status': 'started', 'message': 'Optimized NIDS started'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to start processing'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/stop', methods=['POST'])
def stop_nids():
    """Stop the NIDS system"""
    global nids_system, traffic_generator
    
    try:
        if nids_system:
            nids_system.stop_processing()
        
        traffic_generator = None
        dashboard_manager.stop()
        
        return jsonify({'status': 'stopped', 'message': 'NIDS monitoring stopped'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connected', {'message': 'Connected to NIDS Dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    # Create templates directory and HTML template
    import os
    
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create the HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NIDS Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .controls {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .alerts-section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .alert-item {
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid;
        }
        .alert-critical { border-left-color: #e74c3c; background-color: #fdf2f2; }
        .alert-high { border-left-color: #f39c12; background-color: #fef9e7; }
        .alert-medium { border-left-color: #f1c40f; background-color: #fffbf0; }
        .alert-low { border-left-color: #3498db; background-color: #f0f8ff; }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        .btn-start { background-color: #27ae60; color: white; }
        .btn-stop { background-color: #e74c3c; color: white; }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .status-running { background-color: #27ae60; }
        .status-stopped { background-color: #e74c3c; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Network Intrusion Detection System Dashboard</h1>
        <div>
            <span class="status-indicator" id="statusIndicator"></span>
            <span id="statusText">Stopped</span>
        </div>
    </div>

    <div class="controls">
        <h3>System Controls</h3>
        <button class="btn btn-start" onclick="startNIDS()">Start Monitoring</button>
        <button class="btn btn-stop" onclick="stopNIDS()">Stop Monitoring</button>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value" id="flowsProcessed">0</div>
            <div class="stat-label">Flows Processed</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="attacksDetected">0</div>
            <div class="stat-label">Attacks Detected</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="alertsGenerated">0</div>
            <div class="stat-label">Alerts Generated</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="processingRate">0.0</div>
            <div class="stat-label">Flows/Second</div>
        </div>
    </div>

    <div class="alerts-section">
        <h3>Recent Security Alerts</h3>
        <div id="alertsList">
            <p>No alerts yet...</p>
        </div>
    </div>

    <script>
        const socket = io();
        let isRunning = false;



        // Socket event handlers
        socket.on('connect', function() {
            console.log('Connected to NIDS Dashboard');
        });

        socket.on('stats_update', function(stats) {
            updateStats(stats);
        });

        socket.on('new_alert', function(alert) {
            addAlert(alert);
        });

        function updateStats(stats) {
            document.getElementById('flowsProcessed').textContent = stats.flows_processed || 0;
            document.getElementById('attacksDetected').textContent = stats.attacks_detected || 0;
            document.getElementById('alertsGenerated').textContent = stats.alerts_generated || 0;
            document.getElementById('processingRate').textContent = 
                (stats.flows_per_second || 0).toFixed(2);
        }

        function addAlert(alert) {
            const alertsList = document.getElementById('alertsList');
            
            // Remove "No alerts" message
            if (alertsList.innerHTML.includes('No alerts yet')) {
                alertsList.innerHTML = '';
            }

            const alertDiv = document.createElement('div');
            alertDiv.className = `alert-item alert-${alert.severity.toLowerCase()}`;
            alertDiv.innerHTML = `
                <strong>[${alert.severity}]</strong> Alert #${alert.id} - 
                Confidence: ${Math.round(alert.confidence * 100)}%<br>
                <small>
                    ${alert.timestamp} | 
                    ${alert.src_ip}:${alert.src_port} → ${alert.dst_ip}:${alert.dst_port}
                </small><br>
                <em>${alert.description}</em>
            `;
            
            alertsList.insertBefore(alertDiv, alertsList.firstChild);
            
            // Keep only last 10 alerts
            while (alertsList.children.length > 10) {
                alertsList.removeChild(alertsList.lastChild);
            }
        }

        function updateStatus(running) {
            isRunning = running;
            const indicator = document.getElementById('statusIndicator');
            const text = document.getElementById('statusText');
            
            if (running) {
                indicator.className = 'status-indicator status-running';
                text.textContent = 'Running';
            } else {
                indicator.className = 'status-indicator status-stopped';
                text.textContent = 'Stopped';
            }
        }

        function startNIDS() {
            fetch('/api/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    attack_probability: 0.1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'started') {
                    updateStatus(true);
                    console.log('NIDS started successfully');
                } else {
                    console.error('Failed to start NIDS:', data.message);
                }
            })
            .catch(error => {
                console.error('Error starting NIDS:', error);
            });
        }

        function stopNIDS() {
            fetch('/api/stop', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'stopped') {
                    updateStatus(false);
                    console.log('NIDS stopped successfully');
                } else {
                    console.error('Failed to stop NIDS:', data.message);
                }
            })
            .catch(error => {
                console.error('Error stopping NIDS:', error);
            });
        }

        // Load initial data
        fetch('/api/stats')
            .then(response => response.json())
            .then(stats => {
                if (!stats.error) {
                    updateStats(stats);
                    updateStatus(stats.flows_processed > 0);
                }
            });

        fetch('/api/alerts')
            .then(response => response.json())
            .then(alerts => {
                alerts.forEach(alert => addAlert(alert));
            });
    </script>
</body>
</html>'''
    
    with open('web/templates/dashboard.html', 'w') as f:
        f.write(html_template)
    
    print("🌐 Starting NIDS Web Dashboard...")
    print("📊 Dashboard available at: http://localhost:5000")
    print("🛡️ Use the web interface to start/stop monitoring")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)