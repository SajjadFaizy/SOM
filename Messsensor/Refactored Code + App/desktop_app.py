import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QComboBox, 
                            QFileDialog, QMessageBox)
from PyQt5.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
import csv
import os
from src.data_processing.mqtt_subscriber import TemperatureSubscriber

class TemperatureMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperature Monitor")
        self.setMinimumSize(800, 600)
        
        # Initialize data handling
        self.subscriber = TemperatureSubscriber()
        self.subscriber.start()
        self.temp_data = []
        self.full_temp_history = []
        
        # Setup UI
        self.setup_ui()
        
        # Setup timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update every second

    def setup_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add controls
        controls_layout = QHBoxLayout()
        
        # Theme selector
        theme_label = QLabel("Theme:")
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Light", "Dark"])
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        
        # Stats labels
        self.min_temp_label = QLabel("Min: --°C")
        self.max_temp_label = QLabel("Max: --°C")
        self.avg_temp_label = QLabel("Avg: --°C")
        
        # Add widgets to controls layout
        controls_layout.addWidget(theme_label)
        controls_layout.addWidget(self.theme_selector)
        controls_layout.addStretch()
        controls_layout.addWidget(self.min_temp_label)
        controls_layout.addWidget(self.avg_temp_label)
        controls_layout.addWidget(self.max_temp_label)
        
        # Setup matplotlib figure
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.setup_plot()
        
        # Add top controls and plot to main layout
        layout.addLayout(controls_layout)
        layout.addWidget(self.canvas)
        
        # Add export controls in 3:1 arrangement
        export_layout = QHBoxLayout()
        
        # Left side (3 parts)
        export_options_layout = QHBoxLayout()
        
        # Data export dropdown
        data_export_layout = QVBoxLayout()
        data_export_label = QLabel("Export Data")
        self.data_format_selector = QComboBox()
        self.data_format_selector.addItems(["-", "entire session", "last 60 seconds"])
        data_export_layout.addWidget(data_export_label)
        data_export_layout.addWidget(self.data_format_selector)
        
        # Graph export dropdown
        graph_export_layout = QVBoxLayout()
        graph_export_label = QLabel("Export Graph")
        self.graph_format_selector = QComboBox()
        self.graph_format_selector.addItems(["-", "entire session", "last 60 seconds"])
        graph_export_layout.addWidget(graph_export_label)
        graph_export_layout.addWidget(self.graph_format_selector)
        
        # Add both dropdown sections to options layout
        export_options_layout.addLayout(data_export_layout)
        export_options_layout.addLayout(graph_export_layout)
        
        # Add options (3 parts) to main export layout
        export_layout.addLayout(export_options_layout, stretch=3)
        
        # Add export button (1 part)
        self.export_button = QPushButton("Export")
        self.export_button.setFixedWidth(100)
        self.export_button.clicked.connect(self.handle_export)
        export_layout.addWidget(self.export_button, stretch=1, alignment=Qt.AlignCenter)
        
        # Add export section to main layout
        layout.addLayout(export_layout)
        
        # Add some padding at the bottom
        layout.addSpacing(20)

    def setup_plot(self):
        self.ax.set_title("Real-time Temperature", pad=10)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.line, = self.ax.plot([], [], 'b-', linewidth=2)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_ylim(15, 35)
        self.figure.tight_layout()

    def update_plot(self):
        # Get latest data
        data = self.subscriber.get_temperature_data()
        if data:
            # Only store the latest reading if it has a new timestamp
            latest_data = data[-1]  # Get most recent reading
            if not self.full_temp_history or \
            self.full_temp_history[-1]['timestamp'] != datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.full_temp_history.append({
                    'timestamp': timestamp,
                    'temperature': latest_data['temp'],
                    'read_index': len(self.full_temp_history),
                    'connection_result_code': self.subscriber.last_connection_code
                })
            
            # Update display data
            temperatures = [item['temp'] for item in data]
            self.temp_data = temperatures[-60:]  # Keep last 60 readings
            
            # Update plot
            x_data = list(range(len(self.temp_data)))
            self.line.set_data(x_data, self.temp_data)
            self.ax.set_xlim(0, 60)
            
            # Update stats
            self.update_stats()
            
            # Redraw canvas
            self.canvas.draw()


    def update_stats(self):
        if self.temp_data:
            self.min_temp_label.setText(f"Min: {min(self.temp_data):.1f}°C")
            self.max_temp_label.setText(f"Max: {max(self.temp_data):.1f}°C")
            self.avg_temp_label.setText(f"Avg: {sum(self.temp_data)/len(self.temp_data):.1f}°C")

    def change_theme(self, theme):
        if theme == "Dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #2b2b2b; }
                QLabel { color: #ffffff; }
                QComboBox { 
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #555555;
                }
            """)
            self.figure.set_facecolor('#2b2b2b')
            self.ax.set_facecolor('#2b2b2b')
            self.ax.tick_params(colors='white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color('white')
            self.ax.grid(color='#404040')
        else:
            self.setStyleSheet("")
            self.figure.set_facecolor('white')
            self.ax.set_facecolor('white')
            self.ax.tick_params(colors='black')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.title.set_color('black')
            self.ax.grid(color='#cccccc')
        self.canvas.draw()

    def handle_export(self):
        data_option = self.data_format_selector.currentText()
        graph_option = self.graph_format_selector.currentText()
        
        if data_option == "-" and graph_option == "-":
            QMessageBox.warning(self, "Export Error", "Please select at least one export option.")
            return
            
        # Create export directory dialog
        export_dir = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if not export_dir:
            return
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Handle data export
            if data_option != "-":
                self.export_temperature_data(export_dir, data_option, timestamp)
                
            # Handle graph export
            if graph_option != "-":
                self.export_temperature_graph(export_dir, graph_option, timestamp)
                
            QMessageBox.information(self, "Export Success", "Export completed successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Error during export: {str(e)}")

    def export_temperature_data(self, export_dir, option, timestamp):
        filename = os.path.join(export_dir, f"temperature_data_{timestamp}.csv")
        
        # Select data based on option
        if option == "last 60 seconds":
            data_to_export = self.full_temp_history[-60:]
        else:  # entire session
            data_to_export = self.full_temp_history
            
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(["timestamp", "temp_reading_in_C", "read_index", "connection_result_code"])
            # Write data
            for entry in data_to_export:
                writer.writerow([
                    entry['timestamp'],
                    entry['temperature'],
                    entry['read_index'],
                    entry['connection_result_code']
                ])

    def export_temperature_graph(self, export_dir, option, timestamp):
        filename = os.path.join(export_dir, f"temperature_graph_{timestamp}.png")
        
        # Create a new figure for export
        export_fig = Figure(figsize=(10, 6))
        ax = export_fig.add_subplot(111)
        
        # Select data based on option
        if option == "last 60 seconds":
            data_to_plot = self.full_temp_history[-60:]
        else:  # entire session
            data_to_plot = self.full_temp_history
            
        # Plot data
        temperatures = [entry['temperature'] for entry in data_to_plot]
        timestamps = [entry['timestamp'] for entry in data_to_plot]
        
        # Plot with proper formatting
        ax.plot(range(len(temperatures)), temperatures, 'b-', linewidth=2)
        ax.set_title("Temperature History")
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature (°C)")
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Set x-axis ticks and labels
        if len(timestamps) > 10:
            tick_spacing = len(timestamps) // 10
            ax.set_xticks(range(0, len(timestamps), tick_spacing))
            ax.set_xticklabels([timestamps[i] for i in range(0, len(timestamps), tick_spacing)], rotation=45)
        else:
            ax.set_xticks(range(len(timestamps)))
            ax.set_xticklabels(timestamps, rotation=45)
        
        export_fig.tight_layout()
        export_fig.savefig(filename, dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TemperatureMonitor()
    window.show()
    sys.exit(app.exec_())
