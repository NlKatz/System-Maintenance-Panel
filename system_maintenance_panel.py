import sys
import subprocess
import ctypes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QGroupBox, 
                             QMessageBox, QProgressDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()


class CommandThread(QThread):
    finished = pyqtSignal(str, bool)
    
    def __init__(self, command):
        super().__init__()
        self.command = command
    
    def run(self):
        try:
            result = subprocess.run(
                ["powershell", "-Command", self.command],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            self.finished.emit(output, success)
        except subprocess.TimeoutExpired:
            self.finished.emit("Command timed out", False)
        except Exception as e:
            self.finished.emit(str(e), False)


class SystemMaintenancePanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("System Maintenance Panel")
        self.setMinimumSize(500, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("System Maintenance Panel")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Software Updates Section
        updates_group = self.create_section("Software Updates", [
            ("Check for Updates", self.check_updates),
            ("Uninstall a Program", self.uninstall_program),
            ("Install Updates", self.install_updates),
            ("Clean Up", self.cleanup)
        ])
        main_layout.addWidget(updates_group)
        
        # System Administration Section
        admin_group = self.create_section("System Administration", [
            ("VPN Configuration", self.vpn_wizard),
            ("Network Status", self.network_status),
            ("Manage Passwords", self.manage_passwords),
            ("Manage Users", self.manage_users),
            ("Manage Autologin", self.manage_autologin),
            ("Check System Status", self.check_system_status),
            ("Windows Features", self.windows_features),
            ("Search Logs", self.search_logs)
        ])
        main_layout.addWidget(admin_group)
        
        # Misc Section
        misc_group = self.create_section("Misc", [
            ("Open Terminal", self.open_terminal),
            ("Reboot", self.reboot),
            ("Lock Screen", self.lock_screen),
            ("Shut Down", self.shutdown),
            ("Exit", self.exit_app)
        ])
        main_layout.addWidget(misc_group)
        
        main_layout.addStretch()
        
        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 8px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
                border: 1px solid #999999;
            }
            QPushButton:pressed {
                background-color: #d9d9d9;
            }
        """)
    
    def create_section(self, title, buttons):
        """Create a section group with buttons."""
        group = QGroupBox(title)
        layout = QVBoxLayout()
        
        # Create buttons in rows of 2
        for i in range(0, len(buttons), 2):
            row_layout = QHBoxLayout()
            
            # First button
            btn1 = QPushButton(buttons[i][0])
            btn1.clicked.connect(buttons[i][1])
            row_layout.addWidget(btn1)
            
            # Second button if exists
            if i + 1 < len(buttons):
                btn2 = QPushButton(buttons[i + 1][0])
                btn2.clicked.connect(buttons[i + 1][1])
                row_layout.addWidget(btn2)
            
            layout.addLayout(row_layout)
        
        group.setLayout(layout)
        return group
    
    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        """Show a message box."""
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()
    
    def confirm_action(self, message):
        """Show a confirmation dialog."""
        reply = QMessageBox.question(
            self, 'Confirm Action', message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
    
    # Software Updates Methods
    def check_updates(self):
        """Check for Windows updates."""
        try:
            subprocess.Popen(["start", "ms-settings:windowsupdate"], shell=True)
            self.show_message("Windows Update", "Windows Update settings opened. Check for updates there.")
        except Exception as e:
            self.show_message("Error", f"Failed to open Windows Update: {e}", 
                            QMessageBox.Icon.Critical)
    
    def uninstall_program(self):
        """Open Programs and Features."""
        try:
            subprocess.Popen(["appwiz.cpl"], shell=True)
        except Exception as e:
            self.show_message("Error", f"Failed to open Programs and Features: {e}", 
                            QMessageBox.Icon.Critical)
    
    def install_updates(self):
        """Install Windows updates."""
        try:
            subprocess.Popen(["start", "ms-settings:windowsupdate"], shell=True)
            self.show_message("Windows Update", "Windows Update settings opened. Click 'Install now' to install pending updates.")
        except Exception as e:
            self.show_message("Error", f"Failed to open Windows Update: {e}", 
                            QMessageBox.Icon.Critical)
    
    def cleanup(self):
        """Run disk cleanup."""
        if self.confirm_action("This will clean up temporary files and system cache. Continue?"):
            try:
                subprocess.Popen(["cleanmgr", "/sagerun:1"], shell=True)
                self.show_message("Cleanup", "Disk Cleanup utility launched.")
            except Exception as e:
                self.show_message("Error", f"Failed to launch Disk Cleanup: {e}", 
                                QMessageBox.Icon.Critical)
    
    # System Administration Methods
    def vpn_wizard(self):
        """Open VPN settings."""
        try:
            subprocess.Popen(["start", "ms-settings:network-vpn"], shell=True)
        except Exception as e:
            self.show_message("Error", f"Failed to open VPN settings: {e}", 
                            QMessageBox.Icon.Critical)
    
    def network_status(self):
        """Show network status."""
        command = "Get-NetAdapter | Select-Object Name, Status, LinkSpeed | Format-Table -AutoSize"
        self.run_command(command, "Getting network status...")
    
    def manage_passwords(self):
        """Open Windows Credential Manager."""
        try:
            subprocess.Popen(["control", "/name", "Microsoft.CredentialManager"], shell=True)
        except Exception as e:
            self.show_message("Error", f"Failed to open Credential Manager: {e}", 
                            QMessageBox.Icon.Critical)
    
    def manage_users(self):
        """Open User Accounts to manage users."""
        try:
            subprocess.Popen(["netplwiz"], shell=True)
            self.show_message("User Management", 
                            "You can create, modify, or remove user accounts here.")
        except Exception as e:
            self.show_message("Error", f"Failed to open User Accounts: {e}", 
                            QMessageBox.Icon.Critical)
    
    def manage_autologin(self):
        """Open User Accounts to manage autologin."""
        try:
            subprocess.Popen(["netplwiz"], shell=True)
            self.show_message("Auto-login", 
                            "Uncheck 'Users must enter a user name and password' to enable auto-login.")
        except Exception as e:
            self.show_message("Error", f"Failed to open User Accounts: {e}", 
                            QMessageBox.Icon.Critical)
    
    def check_system_status(self):
        """Check system status."""
        command = """
        Write-Output '=== System Information ==='
        $comp = Get-ComputerInfo
        Write-Output "Computer Name: $($comp.CsName)"
        Write-Output "Windows Version: $($comp.WindowsVersion)"
        Write-Output "OS Architecture: $($comp.OsArchitecture)"
        Write-Output ''
        Write-Output '=== Memory Usage ==='
        $os = Get-CimInstance Win32_OperatingSystem
        $totalMem = [math]::Round($os.TotalVisibleMemorySize/1MB,2)
        $freeMem = [math]::Round($os.FreePhysicalMemory/1MB,2)
        $usedMem = [math]::Round($totalMem - $freeMem,2)
        Write-Output "Total Memory: $totalMem GB"
        Write-Output "Used Memory: $usedMem GB"
        Write-Output "Free Memory: $freeMem GB"
        Write-Output ''
        Write-Output '=== Disk Space ==='
        Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Used -ne $null} | ForEach-Object {
            $used = [math]::Round($_.Used/1GB,2)
            $free = [math]::Round($_.Free/1GB,2)
            $total = [math]::Round(($_.Used + $_.Free)/1GB,2)
            Write-Output "Drive $($_.Name): Total: $total GB, Used: $used GB, Free: $free GB"
        }
        Write-Output ''
        Write-Output '=== CPU Information ==='
        $cpu = Get-CimInstance Win32_Processor
        Write-Output "Processor: $($cpu.Name)"
        Write-Output "Cores: $($cpu.NumberOfCores)"
        Write-Output "Logical Processors: $($cpu.NumberOfLogicalProcessors)"
        """
        self.run_command(command, "Checking system status...")
    
    def windows_features(self):
        """Open Windows Features."""
        try:
            subprocess.Popen(["optionalfeatures"], shell=True)
        except Exception as e:
            self.show_message("Error", f"Failed to open Windows Features: {e}", 
                            QMessageBox.Icon.Critical)
    
    def manage_software(self):
        """Open Windows software management."""
        try:
            subprocess.Popen(["start", "ms-settings:appsfeatures"], shell=True)
            self.show_message("Software Management", 
                            "Apps & Features opened. You can manage installed software there.\n\n"
                            "Tip: You can also use 'winget' command in PowerShell for advanced package management.")
        except Exception as e:
            self.show_message("Error", f"Failed to open Apps & Features: {e}", 
                            QMessageBox.Icon.Critical)
    
    def search_logs(self):
        """Open Event Viewer."""
        try:
            subprocess.Popen(["eventvwr.msc"], shell=True)
        except Exception as e:
            self.show_message("Error", f"Failed to open Event Viewer: {e}", 
                            QMessageBox.Icon.Critical)
    
    # Misc Methods
    def open_terminal(self):
        """Open PowerShell terminal."""
        try:
            subprocess.Popen(["powershell"], shell=True)
        except Exception as e:
            self.show_message("Error", f"Failed to open terminal: {e}", 
                            QMessageBox.Icon.Critical)
    
    def reboot(self):
        """Reboot the system."""
        if self.confirm_action("Are you sure you want to reboot the system?"):
            try:
                subprocess.run(["shutdown", "/r", "/t", "5"], shell=True)
                self.show_message("Reboot", "System will reboot in 5 seconds.")
            except Exception as e:
                self.show_message("Error", f"Failed to reboot: {e}", 
                                QMessageBox.Icon.Critical)
    
    def lock_screen(self):
        """Lock the workstation."""
        try:
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            self.show_message("Error", f"Failed to lock screen: {e}", 
                            QMessageBox.Icon.Critical)
    
    def shutdown(self):
        """Shut down the system."""
        if self.confirm_action("Are you sure you want to shut down the system?"):
            try:
                subprocess.run(["shutdown", "/s", "/t", "5"], shell=True)
                self.show_message("Shutdown", "System will shut down in 5 seconds.")
            except Exception as e:
                self.show_message("Error", f"Failed to shut down: {e}", 
                                QMessageBox.Icon.Critical)
    
    def exit_app(self):
        """Exit the application."""
        if self.confirm_action("Are you sure you want to exit the System Maintenance Panel?"):
            QApplication.quit()
    
    def run_command(self, command, progress_text):
        """Run a PowerShell command in a separate thread."""
        # Create and show progress dialog
        progress = QProgressDialog(progress_text, "Cancel", 0, 0, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.setCancelButton(None)
        progress.show()
        
        # Create and start thread
        thread = CommandThread(command)
        
        def on_finished(output, success):
            progress.close()
            if success:
                self.show_message("Success", output if output.strip() else "Command completed successfully.")
            else:
                self.show_message("Error", f"Command failed:\n{output}", 
                                QMessageBox.Icon.Warning)
        
        thread.finished.connect(on_finished)
        thread.start()
        
        # Keep reference to prevent garbage collection
        self.current_thread = thread


def main():
    # Check for admin privileges
    if not is_admin():
        reply = QMessageBox.question(
            None, 'Administrator Rights Required',
            'This application requires administrator privileges for most functions.\n\n'
            'Do you want to restart with administrator rights?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        if reply == QMessageBox.StandardButton.Yes:
            run_as_admin()
        # Continue anyway if user chooses No
    
    app = QApplication(sys.argv)
    window = SystemMaintenancePanel()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
