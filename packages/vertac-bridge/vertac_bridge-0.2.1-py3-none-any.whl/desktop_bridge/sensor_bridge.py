"""
SensorHub Desktop Bridge v1.0
Lightweight application that:
1. Reads sensor data (CSV files or live streams)
2. Formats data into standard format
3. Sends to backend API via HTTP

Architecture: Desktop Bridge → Web API → Web Dashboard
"""

import csv
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import logging
import argparse
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class SensorBridge:
    """Bridges sensor data to backend API"""
    
    def __init__(self, backend_url: str = "http://localhost:8000", batch_size: int = 10):
        """
        Initialize the sensor bridge.
        
        Args:
            backend_url: Backend API URL (default: localhost:8000)
            batch_size: Number of samples to batch before sending (default: 10)
        """
        self.backend_url = backend_url
        self.batch_size = batch_size
        self.session = requests.Session()
        
        # Verify backend is running
        self._check_backend_health()
    
    def _check_backend_health(self):
        """Verify backend is accessible"""
        try:
            response = self.session.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ Connected to backend at {self.backend_url}")
            else:
                logger.warning(f"⚠️ Backend returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            logger.error(f"❌ Cannot connect to backend at {self.backend_url}")
            logger.error("   Make sure the backend is running: python -m uvicorn app.main:app --reload")
            raise
    
    def register_stream(self, stream_name: str, sensors: List[str]) -> str:
        """
        Register a new data stream with the backend.
        
        Args:
            stream_name: Name of the stream (e.g., 'machine_01')
            sensors: List of sensor names (e.g., ['motor_speed', 'vibration', 'temperature'])
        
        Returns:
            stream_id for future reference
        """
        # Convert sensor names to SensorConfig objects
        sensor_configs = [
            {
                "sensor_id": f"sensor_{i}",
                "name": sensor,
                "type": "numeric",
                "unit": "default"
            }
            for i, sensor in enumerate(sensors)
        ]
        
        payload = {
            "device_name": stream_name,
            "sensor_count": len(sensors),
            "sensors": sensor_configs
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/api/live/register",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            stream_id = data.get('stream_id')
            logger.info(f"✅ Registered stream '{stream_name}' → stream_id: {stream_id}")
            return stream_id
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to register stream: {e}")
            raise
    
    def send_samples(self, stream_id: str, samples: List[Dict[str, Any]]) -> bool:
        """
        Send sensor samples to backend.
        
        Args:
            stream_id: Stream ID from registration
            samples: List of sample dictionaries with format:
                    [
                        {
                            "timestamp": "2026-01-12T20:00:00.000000",
                            "motor_speed": 1500.5,
                            "vibration": 0.45,
                            "temperature": 25.3
                        },
                        ...
                    ]
        
        Returns:
            True if successful, False otherwise
        """
        if not samples:
            return True
        
        # Convert samples to backend format
        formatted_samples = []
        for sample in samples:
            timestamp = sample.get('timestamp')
            # Convert sensor readings to backend format
            for sensor_key, value in sample.items():
                if sensor_key == 'timestamp':
                    continue
                formatted_samples.append({
                    "timestamp": timestamp,
                    "sensor_id": f"sensor_{sensor_key}",
                    "sensor_name": sensor_key,
                    "value": float(value),
                    "unit": "default",
                    "quality": 1.0
                })
        
        payload = {
            "stream_id": stream_id,
            "samples": formatted_samples
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/api/live/batch",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"✅ Sent {len(formatted_samples)} sample points to backend")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send samples: {e}")
            return False
    
    def import_csv(self, csv_file: Path, stream_id: str) -> int:
        """
        Import sensor data from CSV file to backend.
        
        CSV format expected:
            timestamp,motor_speed,vibration,temperature
            2026-01-12T20:00:00.000000,1500.5,0.45,25.3
            ...
        
        Args:
            csv_file: Path to CSV file
            stream_id: Stream ID from registration
        
        Returns:
            Number of samples imported
        """
        if not csv_file.exists():
            logger.error(f"❌ CSV file not found: {csv_file}")
            return 0
        
        logger.info(f"📂 Reading CSV: {csv_file.name}")
        
        samples = []
        count = 0
        
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        # Convert to proper types
                        sample = {
                            "timestamp": row['timestamp'].strip(),
                            "motor_speed": float(row.get('motor_speed', 0)),
                            "vibration": float(row.get('vibration', 0)),
                            "temperature": float(row.get('temperature', 0))
                        }
                        samples.append(sample)
                        count += 1
                        
                        # Send in batches
                        if len(samples) >= self.batch_size:
                            self.send_samples(stream_id, samples)
                            samples = []
                    
                    except (ValueError, KeyError) as e:
                        logger.warning(f"⚠️ Skipping row: {e}")
                        continue
                
                # Send remaining samples
                if samples:
                    self.send_samples(stream_id, samples)
            
            logger.info(f"✅ Imported {count} samples from CSV")
            return count
        
        except Exception as e:
            logger.error(f"❌ Error reading CSV: {e}")
            return 0
    
    def monitor_directory(self, directory: Path, stream_id: str, processed_files: set = None):
        """
        Monitor a directory for new CSV files and continuously import new data as it's written.
        Enables live streaming by reading files as they grow.
        
        Args:
            directory: Directory to monitor for CSV files
            stream_id: Stream ID from registration
            processed_files: Set of already processed files (to avoid re-importing)
        """
        if processed_files is None:
            processed_files = set()
        
        # Track last read position for each file (for live streaming)
        file_positions = {}
        
        logger.info(f"📂 Monitoring directory: {directory}")
        logger.info("   🔴 LIVE MODE: Streaming data as it's generated")
        logger.info("   (Press Ctrl+C to stop)")
        
        try:
            while True:
                # Find CSV files
                csv_files = list(directory.glob("generated_data_*.csv"))
                
                for csv_file in csv_files:
                    file_name = csv_file.name
                    
                    # Skip if file doesn't exist or is empty
                    if not csv_file.exists() or csv_file.stat().st_size == 0:
                        continue
                    
                    # Initialize tracking for new files
                    if file_name not in file_positions:
                        file_positions[file_name] = 0
                        logger.info(f"🆕 Monitoring new file: {file_name}")
                    
                    # Read new data from file
                    try:
                        with open(csv_file, 'r') as f:
                            # Skip to last read position
                            f.seek(file_positions[file_name])
                            
                            # Read new lines
                            new_lines = f.readlines()
                            if new_lines:
                                # Update position
                                file_positions[file_name] = f.tell()
                                
                                # Parse and send new data
                                samples = []
                                # For incremental reading, we need to manually specify fieldnames
                                # since the header row is only at the beginning of the file
                                fieldnames = ['timestamp', 'motor_speed', 'vibration', 'temperature']
                                reader = csv.DictReader(new_lines, fieldnames=fieldnames)
                                
                                for row in reader:
                                    try:
                                        # Skip if this is the header row
                                        if row['timestamp'] == 'timestamp':
                                            continue
                                        
                                        sample = {
                                            "timestamp": row['timestamp'].strip(),
                                            "motor_speed": float(row.get('motor_speed', 0)),
                                            "vibration": float(row.get('vibration', 0)),
                                            "temperature": float(row.get('temperature', 0))
                                        }
                                        samples.append(sample)
                                        
                                        # Send in small batches for live updates
                                        if len(samples) >= 5:
                                            self.send_samples(stream_id, samples)
                                            samples = []
                                    
                                    except (ValueError, KeyError) as e:
                                        continue
                                
                                # Send remaining samples
                                if samples:
                                    self.send_samples(stream_id, samples)
                    
                    except Exception as e:
                        logger.warning(f"⚠️ Error reading {file_name}: {e}")
                        continue
                
                time.sleep(0.5)  # Check every 0.5 seconds for live updates
        
        except KeyboardInterrupt:
            logger.info("\n⏹️  Stopped monitoring")


def main():
    """Main entry point with argument parsing"""
    
    parser = argparse.ArgumentParser(
        description='VerTac Sensor Data Bridge - Upload sensor data to VerTac backend',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor current directory with default backend
  vertac-bridge

  # Monitor specific directory
  vertac-bridge --monitor-dir /path/to/data

  # Connect to specific backend
  vertac-bridge --backend-url http://api.example.com:8001

  # Custom stream name
  vertac-bridge --stream-name factory_line_02

Environment Variables:
  BACKEND_URL    Backend API endpoint (default: http://localhost:8000)
  STREAM_NAME    Stream identifier (default: machine_01)
  CSV_DIRECTORY  Directory to monitor (default: current directory)
        """
    )
    
    parser.add_argument(
        '--backend-url',
        help='Backend API endpoint URL',
        default=os.getenv('BACKEND_URL', 'http://localhost:8000')
    )
    
    parser.add_argument(
        '--monitor-dir',
        help='Directory to monitor for CSV files',
        default=os.getenv('CSV_DIRECTORY', os.getcwd())
    )
    
    parser.add_argument(
        '--stream-name',
        help='Stream identifier name',
        default=os.getenv('STREAM_NAME', 'machine_01')
    )
    
    parser.add_argument(
        '--batch-size',
        help='Number of samples to batch before sending',
        type=int,
        default=10
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='VerTac Sensor Data Bridge v1.0'
    )
    
    args = parser.parse_args()
    
    # Configuration from arguments
    BACKEND_URL = args.backend_url
    STREAM_NAME = args.stream_name
    SENSORS = ["motor_speed", "vibration", "temperature"]
    CSV_DIRECTORY = Path(args.monitor_dir)
    
    logger.info("🚀 SensorHub Desktop Bridge v1.0")
    logger.info("=" * 60)
    logger.info(f"📡 Backend: {BACKEND_URL}")
    logger.info(f"📂 Monitor: {CSV_DIRECTORY}")
    logger.info(f"🏷️  Stream: {STREAM_NAME}")
    logger.info("=" * 60)
    
    try:
        # Initialize bridge
        bridge = SensorBridge(backend_url=BACKEND_URL, batch_size=args.batch_size)
        
        # Register stream
        stream_id = bridge.register_stream(STREAM_NAME, SENSORS)
        
        # Start monitoring for CSV files
        bridge.monitor_directory(CSV_DIRECTORY, stream_id)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
