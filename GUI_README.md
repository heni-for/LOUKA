# Luca GUI - AI Voice Assistant Interface

## 🎤 Features

### **Modern Graphical Interface**
- Clean, dark-themed interface
- Real-time conversation display
- Voice and text input options
- Quick command buttons

### **Voice Recognition**
- Click "Start Listening" to activate voice input
- Press "Stop Listening" to deactivate
- Real-time speech recognition feedback
- Automatic command processing

### **Text Input**
- Type messages directly in the text box
- Press Enter or click Send to submit
- Full conversation history

### **Quick Commands**
- **Inbox** - List your emails
- **Organize** - Organize emails
- **Draft** - Create email drafts
- **Help** - Show available commands

## 🚀 How to Use

### **Method 1: Double-click the batch file**
```
start_luca.bat
```

### **Method 2: Run from command line**
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start the GUI
python run_luca_gui.py
```

### **Method 3: Run the module directly**
```bash
python -m assistant.gui
```

## 🎯 Interface Overview

### **Main Window**
- **Title Bar**: Shows "Luca - AI Voice Assistant"
- **Status Bar**: Shows current status (Ready/Listening)
- **Microphone Status**: Shows microphone connection status

### **Conversation Area**
- **Real-time Chat**: See your messages and Luca's responses
- **Timestamps**: Each message shows the time it was sent
- **Color Coding**:
  - 🔵 Blue: Your messages
  - 🔴 Red: Luca's responses
  - 🟡 Yellow: System messages
  - 🔴 Red: Error messages

### **Control Panel**
- **🎤 Start/Stop Listening**: Toggle voice input
- **🗑️ Clear**: Clear conversation history
- **Quick Commands**: One-click access to common functions

### **Text Input**
- **Message Box**: Type your messages here
- **Send Button**: Send your message
- **Enter Key**: Quick send (press Enter)

## 🔧 Troubleshooting

### **Microphone Issues**
- Make sure your microphone is connected
- Check Windows microphone permissions
- Try a different microphone if available

### **Voice Recognition Problems**
- Speak clearly and at normal volume
- Reduce background noise
- Try the text input as an alternative

### **GUI Not Starting**
- Make sure Python is installed
- Activate the virtual environment first
- Check that all dependencies are installed

## 📱 Usage Tips

1. **Voice Commands**: Click "Start Listening", speak clearly, then click "Stop Listening"
2. **Text Input**: Type your message and press Enter or click Send
3. **Quick Commands**: Use the colored buttons for common tasks
4. **Clear History**: Click "Clear" to start a fresh conversation

## 🎨 Customization

The GUI uses a dark theme with:
- Background: Dark blue-gray (#2c3e50)
- Text: Light colors for readability
- Buttons: Color-coded for different functions
- Font: Consolas for conversation, Arial for UI

Enjoy using Luca! 🚀
