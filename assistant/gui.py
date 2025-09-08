#!/usr/bin/env python3
"""
Graphical User Interface for Luca Voice Assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
from typing import Optional

from .voice import SpeechRecognizer, say, parse_command, find_best_microphone
from .tts import speak
from .config import VOSK_MODEL_PATH


class LucaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Luca - AI Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Voice recognition
        self.rec: Optional[SpeechRecognizer] = None
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Conversation history
        self.conversation_history = []
        
        self.setup_ui()
        self.setup_voice_recognition()
        
    def setup_ui(self):
        """Create the user interface."""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🎤 Luca - AI Voice Assistant", 
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Your intelligent voice assistant for emails and general chat",
            font=('Arial', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#34495e')
        status_frame.pack(fill='x', padx=20, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to listen",
            font=('Arial', 12, 'bold'),
            fg='#27ae60',
            bg='#34495e'
        )
        self.status_label.pack(side='left')
        
        self.mic_status_label = tk.Label(
            status_frame,
            text="🎤 Microphone: Ready",
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#34495e'
        )
        self.mic_status_label.pack(side='right')
        
        # Conversation area
        conv_frame = tk.Frame(self.root, bg='#2c3e50')
        conv_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        conv_label = tk.Label(
            conv_frame,
            text="Conversation",
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        conv_label.pack(anchor='w')
        
        # Conversation text area
        self.conversation_text = scrolledtext.ScrolledText(
            conv_frame,
            height=20,
            font=('Consolas', 11),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1',
            selectbackground='#3498db',
            wrap='word',
            state='disabled'
        )
        self.conversation_text.pack(fill='both', expand=True, pady=5)
        
        # Configure text tags for different message types
        self.conversation_text.tag_configure("user", foreground="#3498db", font=('Consolas', 11, 'bold'))
        self.conversation_text.tag_configure("assistant", foreground="#e74c3c", font=('Consolas', 11, 'bold'))
        self.conversation_text.tag_configure("system", foreground="#f39c12", font=('Consolas', 10, 'italic'))
        self.conversation_text.tag_configure("error", foreground="#e74c3c", font=('Consolas', 10, 'bold'))
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Voice control buttons
        self.listen_button = tk.Button(
            control_frame,
            text="🎤 Start Listening",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.toggle_listening,
            relief='flat',
            padx=20,
            pady=10
        )
        self.listen_button.pack(side='left', padx=5)
        
        self.clear_button = tk.Button(
            control_frame,
            text="🗑️ Clear",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            command=self.clear_conversation,
            relief='flat',
            padx=20,
            pady=10
        )
        self.clear_button.pack(side='left', padx=5)
        
        # Quick command buttons
        quick_frame = tk.Frame(control_frame, bg='#2c3e50')
        quick_frame.pack(side='right')
        
        tk.Label(quick_frame, text="Quick Commands:", font=('Arial', 10, 'bold'), 
                fg='#ecf0f1', bg='#2c3e50').pack(anchor='w')
        
        button_frame = tk.Frame(quick_frame, bg='#2c3e50')
        button_frame.pack(fill='x', pady=2)
        
        commands = ["inbox", "organize", "draft", "help"]
        for cmd in commands:
            btn = tk.Button(
                button_frame,
                text=cmd.title(),
                font=('Arial', 9),
                bg='#3498db',
                fg='white',
                command=lambda c=cmd: self.send_command(c),
                relief='flat',
                padx=10,
                pady=5
            )
            btn.pack(side='left', padx=2)
        
        # Text input frame
        input_frame = tk.Frame(self.root, bg='#2c3e50')
        input_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(input_frame, text="Type a message:", font=('Arial', 10, 'bold'), 
                fg='#ecf0f1', bg='#2c3e50').pack(anchor='w')
        
        input_control_frame = tk.Frame(input_frame, bg='#2c3e50')
        input_control_frame.pack(fill='x', pady=5)
        
        self.text_input = tk.Entry(
            input_control_frame,
            font=('Arial', 12),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1',
            relief='flat'
        )
        self.text_input.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.text_input.bind('<Return>', self.send_text_message)
        
        self.send_button = tk.Button(
            input_control_frame,
            text="Send",
            font=('Arial', 12, 'bold'),
            bg='#9b59b6',
            fg='white',
            command=self.send_text_message,
            relief='flat',
            padx=20,
            pady=5
        )
        self.send_button.pack(side='right')
        
        # Add initial message
        self.add_message("system", "Luca is ready! Click 'Start Listening' or type a message.")
        
    def setup_voice_recognition(self):
        """Initialize voice recognition."""
        try:
            # Auto-detect best microphone
            mic_index = find_best_microphone()
            if mic_index is None:
                raise Exception("No suitable microphone found")
            
            self.rec = SpeechRecognizer(VOSK_MODEL_PATH, mic_index)
            self.rec.start()
            self.mic_status_label.config(text=f"🎤 Microphone: Ready (Device {mic_index})", fg='#27ae60')
        except Exception as e:
            self.mic_status_label.config(text=f"🎤 Microphone: Error - {str(e)}", fg='#e74c3c')
            messagebox.showerror("Microphone Error", f"Could not initialize microphone:\n{str(e)}")
    
    def add_message(self, sender: str, message: str):
        """Add a message to the conversation."""
        self.conversation_text.config(state='normal')
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        self.conversation_text.insert('end', f"[{timestamp}] ", "system")
        
        # Add message with appropriate tag
        if sender == "user":
            self.conversation_text.insert('end', f"You: {message}\n", "user")
        elif sender == "assistant":
            self.conversation_text.insert('end', f"Luca: {message}\n", "assistant")
            # Add voice output for assistant messages
            try:
                speak(message)
            except Exception as e:
                print(f"TTS Error: {e}")
        elif sender == "system":
            self.conversation_text.insert('end', f"{message}\n", "system")
        elif sender == "error":
            self.conversation_text.insert('end', f"Error: {message}\n", "error")
        
        self.conversation_text.config(state='disabled')
        self.conversation_text.see('end')
        
        # Add to conversation history
        if sender in ["user", "assistant"]:
            self.conversation_history.append({"role": sender, "content": message})
    
    def toggle_listening(self):
        """Toggle voice listening on/off."""
        if not self.rec:
            messagebox.showerror("Error", "Voice recognition not available")
            return
            
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start voice listening."""
        self.is_listening = True
        self.listen_button.config(text="🛑 Stop Listening", bg='#e74c3c')
        self.status_label.config(text="Listening... Speak now!", fg='#e74c3c')
        
        # Start listening in a separate thread
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """Stop voice listening."""
        self.is_listening = False
        self.listen_button.config(text="🎤 Start Listening", bg='#27ae60')
        self.status_label.config(text="Ready to listen", fg='#27ae60')
    
    def listen_loop(self):
        """Main listening loop."""
        try:
            while self.is_listening and self.rec:
                utterance = self.rec.listen_text(mode="free")
                if utterance and len(utterance.strip()) > 1:
                    # Process the voice input
                    self.root.after(0, lambda u=utterance: self.add_message("user", u))
                    self.root.after(0, lambda u=utterance: self.process_command(u))
                    break  # Stop listening after getting input
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.add_message("error", error_msg))
        finally:
            self.root.after(0, self.stop_listening)
    
    def process_command(self, command: str):
        """Process a voice or text command."""
        try:
            # Check if it's an email command first
            if command.lower().strip() in ["inbox", "organize", "organise", "read", "draft", "help"]:
                self.handle_email_command(command.lower().strip())
                return
            
            # Try AI chat for other commands
            try:
                from .llm import chat_with_ai
                response = chat_with_ai(command, self.conversation_history)
                self.add_message("assistant", response)
                
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": command})
                self.conversation_history.append({"role": "assistant", "content": response})
                
                # Keep only last 10 exchanges to manage memory
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                    
            except Exception as ai_error:
                error_msg = str(ai_error)
                if "API key not found" in error_msg or "quota" in error_msg.lower() or "proxies" in error_msg.lower():
                    self.add_message("error", "Gemini API key issue. Please check your API key or billing. Email commands still work!")
                else:
                    self.add_message("error", f"AI Error: {error_msg}")
            
        except Exception as e:
            self.add_message("error", f"Error processing command: {str(e)}")
    
    def handle_email_command(self, command: str):
        """Handle email-specific commands."""
        try:
            if command == "inbox":
                self.add_message("assistant", "Checking your inbox...")
                # Here you would call the actual inbox function
                self.add_message("assistant", "Inbox command received. (Email integration needs Outlook setup)")
            elif command in ["organize", "organise"]:
                self.add_message("assistant", "Organizing your emails...")
                self.add_message("assistant", "Organize command received. (Email integration needs Outlook setup)")
            elif command == "read":
                self.add_message("assistant", "Reading emails...")
                self.add_message("assistant", "Read command received. (Email integration needs Outlook setup)")
            elif command == "draft":
                self.add_message("assistant", "Drafting email...")
                self.add_message("assistant", "Draft command received. (Email integration needs Outlook setup)")
            elif command == "help":
                self.add_message("assistant", "Available commands: inbox, organize, read, draft, help")
                self.add_message("assistant", "Voice commands work! AI chat needs valid Gemini API key.")
        except Exception as e:
            self.add_message("error", f"Email command error: {str(e)}")
    
    def send_command(self, command: str):
        """Send a quick command."""
        self.add_message("user", command)
        self.process_command(command)
    
    def send_text_message(self, event=None):
        """Send a text message."""
        message = self.text_input.get().strip()
        if message:
            self.add_message("user", message)
            self.process_command(message)
            self.text_input.delete(0, 'end')
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_text.config(state='normal')
        self.conversation_text.delete(1.0, 'end')
        self.conversation_text.config(state='disabled')
        self.conversation_history = []
        self.add_message("system", "Conversation cleared.")
    
    def on_closing(self):
        """Handle window closing."""
        if self.rec:
            self.rec.stop()
        self.root.destroy()


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = LucaGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
