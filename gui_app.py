import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QPushButton, QComboBox, QLineEdit, QTextEdit, QTabWidget, QGroupBox,
    QTreeWidget, QTreeWidgetItem, QSplitter, QStatusBar, QToolBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction
import pyqtgraph as pg
import numpy as np
import random
import time

class ObservaStreamDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ObservaStream Designer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Dark theme setup
        pg.setConfigOption('background', '#2d2d2d')
        pg.setConfigOption('foreground', 'w')
        
        self.create_menu()
        self.create_toolbar()
        self.create_main_layout()
        self.create_status_bar()
        
        # Simulate real-time data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000)
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        new_action = QAction("New Project", self)
        open_action = QAction("Open Project", self)
        save_action = QAction("Save Project", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        dark_mode_action = QAction("Dark Mode", self, checkable=True)
        dark_mode_action.setChecked(True)
        
        view_menu.addAction(dark_mode_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Add toolbar actions
        start_action = QAction(QIcon(), "Start Stream", self)
        stop_action = QAction(QIcon(), "Stop Stream", self)
        add_dashboard_action = QAction(QIcon(), "Add Dashboard", self)
        
        toolbar.addAction(start_action)
        toolbar.addAction(stop_action)
        toolbar.addSeparator()
        toolbar.addAction(add_dashboard_action)
    
    def create_main_layout(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Left panel - Stream configuration
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(300)
        
        # Stream sources group
        sources_group = QGroupBox("Stream Sources")
        sources_layout = QVBoxLayout()
        
        source_combo = QComboBox()
        source_combo.addItems(["Kafka", "RabbitMQ", "IoT Hub", "WebSocket", "Custom API"])
        
        connection_form = QWidget()
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Connection URL:"))
        form_layout.addWidget(QLineEdit())
        form_layout.addWidget(QLabel("Authentication:"))
        form_layout.addWidget(QLineEdit())
        connection_form.setLayout(form_layout)
        
        test_button = QPushButton("Test Connection")
        
        sources_layout.addWidget(source_combo)
        sources_layout.addWidget(connection_form)
        sources_layout.addWidget(test_button)
        sources_group.setLayout(sources_layout)
        
        # Stream filters group
        filters_group = QGroupBox("Stream Filters")
        filters_layout = QVBoxLayout()
        
        filter_editor = QTextEdit()
        filter_editor.setPlaceholderText("Enter filter expressions...")
        
        filters_layout.addWidget(filter_editor)
        filters_group.setLayout(filters_layout)
        
        left_layout.addWidget(sources_group)
        left_layout.addWidget(filters_group)
        left_layout.addStretch()
        
        # Right panel - Dashboard
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Tab widget for multiple dashboards
        dashboard_tabs = QTabWidget()
        dashboard_tabs.setTabsClosable(True)
        
        # Create initial dashboard
        self.create_dashboard_tab(dashboard_tabs)
        
        right_layout.addWidget(dashboard_tabs)
        
        # Splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        main_layout.addWidget(splitter)
    
    def create_dashboard_tab(self, tab_widget):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Tab name with counter
        tab_count = tab_widget.count() + 1
        tab_name = f"Dashboard {tab_count}"
        tab_widget.addTab(tab, tab_name)
        
        # Create plot widgets
        plot_widget1 = pg.PlotWidget(title="Event Rate (events/sec)")
        plot_widget2 = pg.PlotWidget(title="Anomaly Detection")
        
        # Initialize plot data
        self.plot_data1 = [0] * 60
        self.plot_data2 = [0] * 60
        self.plot_curve1 = plot_widget1.plot(self.plot_data1, pen='g')
        self.plot_curve2 = plot_widget2.plot(self.plot_data2, pen='r')
        
        # Event log
        event_log = QTextEdit()
        event_log.setReadOnly(True)
        event_log.setMaximumHeight(150)
        
        # Add widgets to layout
        layout.addWidget(plot_widget1)
        layout.addWidget(plot_widget2)
        layout.addWidget(QLabel("Event Log:"))
        layout.addWidget(event_log)
    
    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Status indicators
        connection_status = QLabel("Disconnected")
        stream_status = QLabel("Idle")
        event_count = QLabel("Events: 0")
        
        status_bar.addWidget(connection_status)
        status_bar.addWidget(stream_status)
        status_bar.addPermanentWidget(event_count)
    
    def update_plots(self):
        # Simulate new data points
        new_value1 = random.randint(10, 100)
        new_value2 = random.gauss(0, 1)
        
        # Update plot data
        self.plot_data1 = self.plot_data1[1:] + [new_value1]
        self.plot_data2 = self.plot_data2[1:] + [new_value2]
        
        # Update plot curves
        self.plot_curve1.setData(self.plot_data1)
        self.plot_curve2.setData(self.plot_data2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set dark theme
    app.setStyle("Fusion")
    
    window = ObservaStreamDesigner()
    window.show()
    
    sys.exit(app.exec())