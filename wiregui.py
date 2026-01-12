#!/usr/bin/env python3
import sys
import os
import subprocess
import webbrowser
import time
from datetime import timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QListWidget, QLabel, 
                             QTextEdit, QTabWidget, QMessageBox, QInputDialog,
                             QFileDialog, QListWidgetItem, QDialog, QLineEdit,
                             QFormLayout, QCheckBox, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QFont, QColor, QPalette

class SettingsDialog(QDialog):
    """Settings dialog"""
    def __init__(self, current_theme, auto_start, parent=None):
        super().__init__(parent)
        self.current_theme = current_theme
        self.auto_start = auto_start
        self.new_theme = current_theme
        self.new_auto_start = auto_start
        self.initUI()
        if current_theme == "dark":
            self.apply_dark_theme()
        
    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Theme section
        theme_label = QLabel('Theme:')
        theme_label.setFont(QFont('Arial', 11, QFont.Bold))
        layout.addWidget(theme_label)
        
        self.theme_group = QButtonGroup()
        self.light_radio = QRadioButton('Light Mode')
        self.dark_radio = QRadioButton('Dark Mode')
        self.theme_group.addButton(self.light_radio, 0)
        self.theme_group.addButton(self.dark_radio, 1)
        
        if self.current_theme == "light":
            self.light_radio.setChecked(True)
        else:
            self.dark_radio.setChecked(True)
            
        layout.addWidget(self.light_radio)
        layout.addWidget(self.dark_radio)
        
        layout.addSpacing(20)
        
        # Auto-start section
        autostart_label = QLabel('Startup:')
        autostart_label.setFont(QFont('Arial', 11, QFont.Bold))
        layout.addWidget(autostart_label)
        
        self.autostart_checkbox = QCheckBox('Launch WireGUI on system startup')
        self.autostart_checkbox.setChecked(self.auto_start)
        layout.addWidget(self.autostart_checkbox)
        
        layout.addSpacing(20)
        
        # Support section
        support_label = QLabel('Support:')
        support_label.setFont(QFont('Arial', 11, QFont.Bold))
        layout.addWidget(support_label)
        
        bug_btn = QPushButton('Report a Bug')
        bug_btn.setStyleSheet("background-color: #ff5c3c; color: white; padding: 10px; border-radius: 3px;")
        bug_btn.clicked.connect(lambda: webbrowser.open('https://github.com/yourusername/issues'))
        layout.addWidget(bug_btn)
        
        help_btn = QPushButton('Need Assistance')
        help_btn.setStyleSheet("background-color: #ff5c3c; color: white; padding: 10px; border-radius: 3px;")
        help_btn.clicked.connect(lambda: webbrowser.open('https://github.com/yourusername'))
        layout.addWidget(help_btn)
        
        layout.addStretch()
        
        # Save/Cancel buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton('Save')
        save_btn.setStyleSheet("background-color: #ff5c3c; color: white; padding: 8px; border-radius: 3px;")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
    def save_settings(self):
        self.new_theme = "light" if self.light_radio.isChecked() else "dark"
        self.new_auto_start = self.autostart_checkbox.isChecked()
        self.accept()
        
    def get_settings(self):
        return self.new_theme, self.new_auto_start
    
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QRadioButton {
                color: #ffffff;
            }
            QCheckBox {
                color: #ffffff;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)

class ConfigEditorDialog(QDialog):
    """Dialog to edit configuration and tunnel name"""
    def __init__(self, tunnel_name, config_content, theme, parent=None):
        super().__init__(parent)
        self.tunnel_name = tunnel_name
        self.config_content = config_content
        self.new_tunnel_name = tunnel_name
        self.theme = theme
        self.initUI()
        if theme == "dark":
            self.apply_dark_theme()
        
    def initUI(self):
        self.setWindowTitle(f'Edit configuration: {self.tunnel_name}')
        self.setGeometry(200, 200, 600, 550)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Form for tunnel name
        form_layout = QFormLayout()
        self.name_input = QLineEdit(self.tunnel_name)
        form_layout.addRow('Tunnel name:', self.name_input)
        layout.addLayout(form_layout)
        
        # Info label
        info = QLabel('Edit the WireGuard configuration below:')
        layout.addWidget(info)
        
        # Editor
        self.editor = QTextEdit()
        self.editor.setPlainText(self.config_content)
        self.editor.setFont(QFont('Courier', 10))
        layout.addWidget(self.editor)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton('Save')
        save_btn.setStyleSheet("background-color: #ea5c1f; color: white; padding: 8px; border-radius: 3px;")
        save_btn.clicked.connect(self.save_and_accept)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
    def save_and_accept(self):
        """Save the new tunnel name and accept"""
        self.new_tunnel_name = self.name_input.text().strip()
        if not self.new_tunnel_name:
            QMessageBox.warning(self, "Error", "Tunnel name cannot be empty!")
            return
        self.accept()
        
    def get_config(self):
        """Get the edited configuration"""
        return self.editor.toPlainText()
    
    def get_tunnel_name(self):
        """Get the new tunnel name"""
        return self.new_tunnel_name
    
    def apply_dark_theme(self):
        """Apply dark theme to dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)

class WireGuardGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_dir = "/etc/wireguard"
        self.settings = QSettings('WireGUI', 'WireGUI')
        self.theme = self.settings.value('theme', 'dark')
        self.auto_start = self.settings.value('auto_start', False, type=bool)
        self.connection_start_time = None
        self.initUI()
        self.apply_theme()
        self.load_tunnels()
        
        # Update status every second for timer and stats
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_status)
        self.timer.start(1000)
        
    def initUI(self):
        self.setWindowTitle('WireGUI')
        self.setGeometry(100, 100, 700, 550)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Tab 1: Tunnels
        tunnels_tab = QWidget()
        tunnels_layout = QHBoxLayout()
        tunnels_tab.setLayout(tunnels_layout)
        
        # Left sidebar with tunnel list
        self.tunnel_list = QListWidget()
        self.tunnel_list.setMaximumWidth(200)
        self.tunnel_list.itemClicked.connect(self.on_tunnel_selected)
        tunnels_layout.addWidget(self.tunnel_list)
        
        # Right panel with tunnel info
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        self.info_label = QLabel("Select a tunnel")
        self.info_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.info_label.setFont(font)
        right_layout.addWidget(self.info_label)
        
        # Info section
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setFont(QFont('Courier', 9))
        right_layout.addWidget(self.info_text)
        
        # Connection status section
        status_widget = QWidget()
        status_layout = QVBoxLayout()
        status_widget.setLayout(status_layout)
        
        # Status indicator
        status_row = QHBoxLayout()
        self.status_dot = QLabel('●')
        self.status_dot.setFont(QFont('Arial', 16))
        self.status_dot.setStyleSheet("color: #666666;")
        status_row.addWidget(self.status_dot)
        
        self.status_label = QLabel('Disconnected')
        self.status_label.setFont(QFont('Arial', 10))
        status_row.addWidget(self.status_label)
        status_row.addStretch()
        status_layout.addLayout(status_row)
        
        # Timer label
        self.timer_label = QLabel('')
        self.timer_label.setFont(QFont('Arial', 9))
        status_layout.addWidget(self.timer_label)
        
        # Data transfer labels
        self.transfer_label = QLabel('')
        self.transfer_label.setFont(QFont('Courier', 9))
        status_layout.addWidget(self.transfer_label)
        
        right_layout.addWidget(status_widget)
        
        # Button layout for Edit and Toggle
        button_layout = QHBoxLayout()
        
        # Edit button
        self.edit_btn = QPushButton('Edit')
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_tunnel_config)
        self.edit_btn.setMinimumHeight(40)
        button_layout.addWidget(self.edit_btn)
        
        # Activate/Deactivate button
        self.toggle_btn = QPushButton('Activate')
        self.toggle_btn.setEnabled(False)
        self.toggle_btn.clicked.connect(self.toggle_tunnel)
        self.toggle_btn.setMinimumHeight(40)
        button_layout.addWidget(self.toggle_btn)
        
        right_layout.addLayout(button_layout)
        
        tunnels_layout.addWidget(right_panel)
        
        self.tabs.addTab(tunnels_tab, "Tunnels")
        
        # Tab 2: Log
        log_tab = QWidget()
        log_layout = QVBoxLayout()
        log_tab.setLayout(log_layout)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        self.tabs.addTab(log_tab, "Log")
        
        # Toolbar at bottom
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar.setLayout(toolbar_layout)
        
        add_btn = QPushButton('Add Tunnel')
        add_btn.clicked.connect(self.create_empty_tunnel)
        toolbar_layout.addWidget(add_btn)
        
        delete_btn = QPushButton('Delete')
        delete_btn.clicked.connect(self.delete_tunnel)
        toolbar_layout.addWidget(delete_btn)
        
        import_btn = QPushButton('Import from file')
        import_btn.clicked.connect(self.import_tunnel)
        toolbar_layout.addWidget(import_btn)
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.refresh_status)
        toolbar_layout.addWidget(refresh_btn)
        
        toolbar_layout.addStretch()
        
        # Settings button (right-aligned)
        settings_btn = QPushButton('Settings')
        settings_btn.clicked.connect(self.open_settings)
        toolbar_layout.addWidget(settings_btn)
        
        main_layout.addWidget(toolbar)
    
    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self.theme, self.auto_start, self)
        
        if dialog.exec_() == QDialog.Accepted:
            new_theme, new_auto_start = dialog.get_settings()
            
            # Save settings
            self.settings.setValue('theme', new_theme)
            self.settings.setValue('auto_start', new_auto_start)
            
            # Apply theme if changed
            if new_theme != self.theme:
                self.theme = new_theme
                self.apply_theme()
                self.log(f"Theme changed to {new_theme} mode")
                
            # Handle auto-start
            if new_auto_start != self.auto_start:
                self.auto_start = new_auto_start
                if new_auto_start:
                    self.log("Auto-start enabled")
                    # Here you would add code to create autostart entry
                else:
                    self.log("Auto-start disabled")
                    
    def apply_theme(self):
        """Apply the current theme"""
        if self.theme == "dark":
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
            
    def apply_dark_theme(self):
        """Apply dark theme to the main window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QListWidget {
                background-color: #252526;
                border: 1px solid #3e3e3e;
                color: #cccccc;
            }
            QListWidget::item:selected {
                background-color: #ff5c3c;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3e3e3e;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:disabled {
                background-color: #2b2b2b;
                color: #666666;
            }
            QTabWidget::pane {
                border: 1px solid #3e3e3e;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #cccccc;
                padding: 8px 20px;
                border: 1px solid #3e3e3e;
            }
            QTabBar::tab:selected {
                background-color: #ff5c3c;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #3c3c3c;
            }
        """)
    
    def apply_light_theme(self):
        """Apply light theme to the main window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QWidget {
                background-color: #f5f5f5;
                color: #000000;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                color: #000000;
            }
            QListWidget::item:selected {
                background-color: #ff5c3c;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e0e0e0;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
            }
            QLabel {
                color: #000000;
            }
            QPushButton {
                background-color: #ff5c3c;
                color: #ffffff;
                border: none;
                padding: 8px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #ff7659;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: #f5f5f5;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #000000;
                padding: 8px 20px;
                border: 1px solid #cccccc;
            }
            QTabBar::tab:selected {
                background-color: #ff5c3c;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
        """)
        
    def load_tunnels(self):
        """Load all WireGuard configurations"""
        self.tunnel_list.clear()
        
        if not os.path.exists(self.config_dir):
            self.log("Warning: /etc/wireguard directory not found")
            return
            
        try:
            files = os.listdir(self.config_dir)
            conf_files = [f[:-5] for f in files if f.endswith('.conf')]
            
            for tunnel_name in sorted(conf_files):
                self.tunnel_list.addItem(tunnel_name)
                
            self.log(f"Loaded: {len(conf_files)} tunnel(s)")
        except PermissionError:
            self.log("Error: No access to /etc/wireguard (permissions required)")
            
    def on_tunnel_selected(self, item):
        """When a tunnel is selected"""
        tunnel_name = item.text()
        self.show_tunnel_info(tunnel_name)
        self.toggle_btn.setEnabled(True)
        self.edit_btn.setEnabled(True)
        
    def show_tunnel_info(self, tunnel_name):
        """Show information about the tunnel - FULL CONFIG"""
        self.info_label.setText(f"Interface: {tunnel_name}")
        
        # Check status
        is_active = self.is_tunnel_active(tunnel_name)
        
        if is_active:
            self.toggle_btn.setText('Deactivate')
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            status_text = ""
            
            # Update status indicator
            self.status_dot.setStyleSheet("color: #4caf50;")  # Green
            self.status_label.setText("Connected")
            
            # Get connection time and data
            if self.connection_start_time is None:
                self.connection_start_time = time.time()
                
            elapsed = int(time.time() - self.connection_start_time)
            self.timer_label.setText(f"Connected for: {str(timedelta(seconds=elapsed))}")
            
            # Get transfer statistics
            transfer_stats = self.get_transfer_stats(tunnel_name)
            self.transfer_label.setText(transfer_stats)
            
        else:
            self.toggle_btn.setText('Activate')
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5c3c;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #ff7659;
                }
            """)
            status_text = ""
            
            # Update status indicator
            self.status_dot.setStyleSheet("color: #dc3545;")  # Red
            self.status_label.setText("Disconnected")
            self.timer_label.setText("")
            self.transfer_label.setText("")
            self.connection_start_time = None
            
        # Read config file and show EVERYTHING
        config_path = f"{self.config_dir}/{tunnel_name}.conf"
        
        try:
            with open(config_path, 'r') as f:
                full_config = f.read()
                
            # Show status + full config
            self.info_text.setText(status_text + full_config)
        except Exception as e:
            self.info_text.setText(f"{status_text}Could not read config: {e}")
    
    def get_transfer_stats(self, tunnel_name):
        """Get data transfer statistics"""
        try:
            result = subprocess.run(['wg', 'show', tunnel_name, 'transfer'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    parts = lines[0].split('\t')
                    if len(parts) >= 3:
                        received = self.format_bytes(int(parts[1]))
                        sent = self.format_bytes(int(parts[2]))
                        return f"↓ Download: {received}\n↑ Upload: {sent}"
        except:
            pass
        return "↓ Download: 0 B\n↑ Upload: 0 B"
    
    def format_bytes(self, bytes_val):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"
    
    def edit_tunnel_config(self):
        """Open editor to edit tunnel configuration and name"""
        current_item = self.tunnel_list.currentItem()
        if not current_item:
            return
            
        tunnel_name = current_item.text()
        config_path = f"{self.config_dir}/{tunnel_name}.conf"
        
        # Check if tunnel is active
        if self.is_tunnel_active(tunnel_name):
            reply = QMessageBox.question(self, 'Tunnel is active',
                                         f'{tunnel_name} is currently active.\n\n'
                                         'You must deactivate the tunnel first to edit.\n'
                                         'Do you want to deactivate it now?',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                result = subprocess.run(['wg-quick', 'down', tunnel_name],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log(f"✓ {tunnel_name} deactivated for editing")
                    self.refresh_status()
                else:
                    QMessageBox.warning(self, "Error", f"Could not deactivate:\n{result.stderr}")
                    return
            else:
                return
        
        # Read current configuration
        try:
            with open(config_path, 'r') as f:
                current_config = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not read configuration:\n{e}")
            return
        
        # Open editor dialog
        dialog = ConfigEditorDialog(tunnel_name, current_config, self.theme, self)
        
        if dialog.exec_() == QDialog.Accepted:
            new_config = dialog.get_config()
            new_name = dialog.get_tunnel_name()
            
            # Check if name changed
            name_changed = new_name != tunnel_name
            new_config_path = f"{self.config_dir}/{new_name}.conf"
            
            if name_changed and os.path.exists(new_config_path):
                QMessageBox.warning(self, "Error", f"A tunnel named '{new_name}' already exists!")
                return
            
            # Make backup
            backup_path = f"{config_path}.backup"
            try:
                import shutil
                shutil.copy(config_path, backup_path)
                
                # Write new configuration
                with open(new_config_path, 'w') as f:
                    f.write(new_config)
                
                # If name changed, delete old file
                if name_changed:
                    os.remove(config_path)
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                    self.log(f"✓ Tunnel renamed from {tunnel_name} to {new_name}")
                    
                self.log(f"✓ Configuration of {new_name} saved")
                
                # Refresh the list and select the tunnel
                self.load_tunnels()
                for i in range(self.tunnel_list.count()):
                    if self.tunnel_list.item(i).text() == new_name:
                        self.tunnel_list.setCurrentRow(i)
                        self.on_tunnel_selected(self.tunnel_list.item(i))
                        break
                
            except PermissionError:
                self.log(f"✗ No write permissions")
                QMessageBox.critical(self, "Error", 
                                   "No write permissions.\n\nStart the application with sudo!")
            except Exception as e:
                self.log(f"✗ Error saving: {e}")
                QMessageBox.critical(self, "Error", f"Could not save:\n{e}")
            
    def is_tunnel_active(self, tunnel_name):
        """Check if a tunnel is active"""
        try:
            result = subprocess.run(['wg', 'show', tunnel_name], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
            
    def toggle_tunnel(self):
        """Activate or deactivate the selected tunnel"""
        current_item = self.tunnel_list.currentItem()
        if not current_item:
            return
            
        tunnel_name = current_item.text()
        is_active = self.is_tunnel_active(tunnel_name)
        
        try:
            if is_active:
                # Deactivate
                result = subprocess.run(['wg-quick', 'down', tunnel_name],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log(f"✓ {tunnel_name} deactivated")
                    self.connection_start_time = None
                else:
                    self.log(f"✗ Error deactivating {tunnel_name}: {result.stderr}")
                    QMessageBox.warning(self, "Error", f"Could not deactivate:\n{result.stderr}")
            else:
                # Activate
                result = subprocess.run(['wg-quick', 'up', tunnel_name],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log(f"✓ {tunnel_name} activated")
                    self.connection_start_time = time.time()
                else:
                    self.log(f"✗ Error activating {tunnel_name}: {result.stderr}")
                    QMessageBox.warning(self, "Error", f"Could not activate:\n{result.stderr}")
                    
            self.refresh_status()
        except Exception as e:
            self.log(f"✗ Error: {e}")
            QMessageBox.critical(self, "Error", f"Something went wrong:\n{e}")
            
    def create_empty_tunnel(self):
        """Create a new empty tunnel configuration"""
        name, ok = QInputDialog.getText(self, 'New Tunnel', 'Tunnel name:')
        
        if ok and name:
            config_path = f"{self.config_dir}/{name}.conf"
            
            # IMPORTANT: Check if file already exists
            if os.path.exists(config_path):
                QMessageBox.warning(self, "Error", "This tunnel already exists! The existing configuration will NOT be overwritten.")
                return
                
            template = """[Interface]
PrivateKey = YOUR_PRIVATE_KEY
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = your.server.com:51820
AllowedIPs = 0.0.0.0/0
"""
            
            try:
                # Only write if file does NOT exist
                if not os.path.exists(config_path):
                    with open(config_path, 'w') as f:
                        f.write(template)
                    self.log(f"✓ Tunnel {name} created")
                    self.load_tunnels()
                    
                    # Select the new tunnel
                    for i in range(self.tunnel_list.count()):
                        if self.tunnel_list.item(i).text() == name:
                            self.tunnel_list.setCurrentRow(i)
                            self.on_tunnel_selected(self.tunnel_list.item(i))
                            break
                else:
                    self.log(f"✗ Tunnel {name} already exists, not overwritten")
                    QMessageBox.warning(self, "Error", "File already exists!")
            except PermissionError:
                self.log(f"✗ No permissions to create {name}")
                QMessageBox.critical(self, "Error", "No write permissions. Run as root or with sudo.")
                
    def import_tunnel(self):
        """Import a tunnel configuration file"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Import Tunnel', 
                                                    '', 'WireGuard Config (*.conf)')
        
        if file_path:
            tunnel_name = os.path.basename(file_path)[:-5]
            dest_path = f"{self.config_dir}/{tunnel_name}.conf"
            
            # Check if already exists
            if os.path.exists(dest_path):
                reply = QMessageBox.question(self, 'File exists',
                                             f'Tunnel "{tunnel_name}" already exists.\n\n'
                                             'Do you want to overwrite it?',
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
                if reply == QMessageBox.No:
                    return
            
            try:
                import shutil
                shutil.copy(file_path, dest_path)
                self.log(f"✓ Tunnel {tunnel_name} imported")
                self.load_tunnels()
            except PermissionError:
                self.log(f"✗ No permissions to import")
                QMessageBox.critical(self, "Error", "No write permissions. Run as root or with sudo.")
            except Exception as e:
                self.log(f"✗ Error importing: {e}")
                QMessageBox.critical(self, "Error", f"Could not import:\n{e}")
                
    def delete_tunnel(self):
        """Delete the selected tunnel"""
        current_item = self.tunnel_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No selection", "Select a tunnel first")
            return
            
        tunnel_name = current_item.text()
        
        reply = QMessageBox.question(self, 'Delete',
                                     f'Are you sure you want to delete "{tunnel_name}"?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # First deactivate if active
            if self.is_tunnel_active(tunnel_name):
                subprocess.run(['wg-quick', 'down', tunnel_name])
                
            config_path = f"{self.config_dir}/{tunnel_name}.conf"
            try:
                os.remove(config_path)
                self.log(f"✓ Tunnel {tunnel_name} deleted")
                self.load_tunnels()
                self.info_label.setText("Select a tunnel")
                self.info_text.clear()
                self.toggle_btn.setEnabled(False)
                self.edit_btn.setEnabled(False)
                self.status_dot.setStyleSheet("color: #666666;")
                self.status_label.setText("Disconnected")
                self.timer_label.setText("")
                self.transfer_label.setText("")
            except PermissionError:
                self.log(f"✗ No permissions to delete")
                QMessageBox.critical(self, "Error", "No permissions to delete. Run as root or with sudo.")
            except Exception as e:
                self.log(f"✗ Error: {e}")
                QMessageBox.critical(self, "Error", f"Could not delete:\n{e}")
                
    def refresh_status(self):
        """Refresh the status of the selected tunnel"""
        current_item = self.tunnel_list.currentItem()
        if current_item:
            self.show_tunnel_info(current_item.text())
            
        # Update colors in the list
        for i in range(self.tunnel_list.count()):
            item = self.tunnel_list.item(i)
            tunnel_name = item.text()
            if self.is_tunnel_active(tunnel_name):
                item.setForeground(QColor(255, 92, 60))  # Orange #ff5c3c
            else:
                if self.theme == "dark":
                    item.setForeground(QColor(204, 204, 204))  # Light gray
                else:
                    item.setForeground(QColor(0, 0, 0))  # Black
                
    def log(self, message):
        """Add message to log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")

def main():
    app = QApplication(sys.argv)
    
    # Check if WireGuard is installed
    try:
        result = subprocess.run(['which', 'wg'], capture_output=True)
        if result.returncode != 0:
            QMessageBox.critical(None, "Error", 
                               "WireGuard not found!\n\nInstall with:\nsudo apt install wireguard")
            sys.exit(1)
    except:
        pass
        
    gui = WireGuardGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()