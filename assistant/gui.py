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
from .email_integration import EmailIntegration
from .multilang_voice import MultiLanguageVoiceRecognizer
from .language_switcher import LanguageSwitcher
from .llm import chat_with_ai
from .smart_features import handle_smart_command, is_smart_command
from .intent_library import detect_intent


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
        
        # Email integration
        self.email_integration = EmailIntegration()
        
        # Initialize multi-language voice recognizer
        self.voice_recognizer = MultiLanguageVoiceRecognizer()
        
        # Push-to-talk settings
        self.ptt_active = False
        self.ptt_key = 'l'  # Press 'L' for push-to-talk
        
        self.setup_ui()
        self.setup_voice_recognition()
        self.setup_push_to_talk()
    
    def setup_push_to_talk(self):
        """Setup push-to-talk functionality."""
        # Bind key events
        self.root.bind('<KeyPress-l>', self.on_ptt_press)
        self.root.bind('<KeyRelease-l>', self.on_ptt_release)
        self.root.focus_set()  # Make sure the window can receive key events
        
        # Add PTT status label
        self.ptt_status_label = tk.Label(
            self.root,
            text="🎤 Press and hold 'L' to talk",
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        self.ptt_status_label.pack(pady=5)
    
    def on_ptt_press(self, event):
        """Handle push-to-talk key press."""
        if not self.ptt_active:
            self.ptt_active = True
            self.ptt_status_label.config(text="🎤 Listening... (Hold 'L')", fg='#e74c3c')
            self.start_ptt_listening()
    
    def on_ptt_release(self, event):
        """Handle push-to-talk key release."""
        if self.ptt_active:
            self.ptt_active = False
            self.ptt_status_label.config(text="🎤 Press and hold 'L' to talk", fg='#95a5a6')
            self.stop_ptt_listening()
    
    def start_ptt_listening(self):
        """Start listening for voice command."""
        def listen_thread():
            try:
                # Get current language
                current_lang = self.language_switcher.get_current_language()
                self.voice_recognizer.set_language(current_lang)
                
                # Update status to show listening
                self.root.after(0, lambda: self.ptt_status_label.config(
                    text="🎤 Listening... Speak now!", fg='#e74c3c'
                ))
                
                # Listen for command
                command = self.voice_recognizer.listen_for_command(timeout=5.0)
                if command:
                    # Process the command
                    self.root.after(0, lambda: self.process_ptt_command(command))
                else:
                    self.root.after(0, lambda: self.ptt_status_label.config(
                        text="🎤 No command heard. Press 'L' to try again", fg='#f39c12'
                    ))
            except Exception as e:
                self.root.after(0, lambda: self.ptt_status_label.config(
                    text=f"❌ Error: {str(e)}", fg='#e74c3c'
                ))
        
        # Start listening in a separate thread
        threading.Thread(target=listen_thread, daemon=True).start()
    
    def stop_ptt_listening(self):
        """Stop listening for voice command."""
        self.voice_recognizer.stop_listening()
    
    def process_ptt_command(self, command: str):
        """Process voice command from push-to-talk."""
        # Add user message with what was heard
        self.add_message("user", f"🎤 Heard: '{command}'")
        
        # Check if it's just a wake word without command
        if command.lower().strip() in ["luca", "hey luca", "ok luca", "لوكا", "مرحبا لوكا", "greeting"]:
            self.add_message("assistant", "Yes? How can I help you?")
            # Reset PTT status
            self.ptt_status_label.config(text="🎤 Press and hold 'L' to talk", fg='#95a5a6')
            return
        
        # Check for "read my last email" command
        if any(phrase in command.lower() for phrase in [
            "read my last email", "read last email", "last email", "recent email",
            "اقرأ آخر بريد", "آخر بريد إلكتروني", "قراءة آخر بريد"
        ]):
            self.add_message("assistant", "قراءة آخر بريد إلكتروني...")
            last_email_result = self.email_integration.read_last_email()
            self.add_message("assistant", last_email_result)
        else:
            # Process other commands
            self.process_command(command)
        
        # Reset PTT status
        self.ptt_status_label.config(text="🎤 Press and hold 'L' to talk", fg='#95a5a6')
        
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
        
        # Language switcher
        self.language_switcher = LanguageSwitcher(control_frame, self.voice_recognizer)
        self.language_switcher.pack(fill='x', pady=5)
        
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
                # Use the new voice recognition system
                utterance = self.rec.listen_for_command()
                if utterance and len(utterance.strip()) > 1:
                    print(f"🎤 GUI received command: {utterance}")
                    # Process the voice input
                    self.root.after(0, lambda u=utterance: self.add_message("user", f"🎤 Heard: '{u}'"))
                    self.root.after(0, lambda u=utterance: self.process_command(u))
                    break  # Stop listening after getting input
        except Exception as e:
            error_msg = str(e)
            print(f"❌ GUI Error: {error_msg}")
            self.root.after(0, lambda: self.add_message("error", error_msg))
        finally:
            self.root.after(0, self.stop_listening)
    
    def process_command(self, command: str):
        """Process a voice or text command."""
        try:
            print(f"🔍 Processing command: '{command}'")
            
            # Check if it's an email command first
            if command.lower().strip() in ["inbox", "organize", "organise", "read", "draft", "help"]:
                self.handle_email_command(command.lower().strip())
                return
            
            # Check for specific email reading commands
            # Check for Arabic email commands
            arabic_commands = [
                "آخر بريد إلكتروني", "قراءة آخر بريد", "آخر رسالة", "بريد إلكتروني",
                "read my last email", "read last email", "last email", "recent email"
            ]
            
            if any(phrase in command.lower() for phrase in arabic_commands) or any(phrase in command for phrase in ["آخر بريد", "قراءة آخر"]):
                self.add_message("assistant", "قراءة آخر بريد إلكتروني...")
                last_email_result = self.email_integration.read_last_email()
                self.add_message("assistant", last_email_result)
                return
            
            # Check if it's a draft request
            if "draft" in command.lower() and len(command.split()) > 1:
                self.add_message("assistant", "Drafting your email...")
                draft_result = self.email_integration.draft_email(command)
                self.add_message("assistant", draft_result)
                return
            
            # Check if it's an email summary request
            if "summarize" in command.lower() and "email" in command.lower():
                self.add_message("assistant", "I can help summarize emails! Please paste the email content here and I'll analyze it for you.")
                return
            
            # Check if user pasted email content (long text with email-like content)
            if len(command) > 100 and any(keyword in command.lower() for keyword in ["subject:", "from:", "to:", "sent:", "received:"]):
                self.add_message("assistant", "I see you've pasted email content! Let me summarize it for you...")
                summary_result = self.email_integration.summarize_email_content(command)
                self.add_message("assistant", summary_result)
                return
            
            # Check for smart commands first using comprehensive intent library
            smart_intent = is_smart_command(command, self.language_switcher.get_current_language())
            print(f"🧠 Smart intent detected: {smart_intent}")
            if smart_intent:
                self.add_message("assistant", "Sure! Let me help you with that.")
                response = handle_smart_command(smart_intent, command)
                print(f"💬 Smart response: {response}")
                self.add_message("assistant", response)
                return
            
            # Try AI chat for other commands
            try:
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
                inbox_summary = self.email_integration.get_inbox_summary()
                self.add_message("assistant", inbox_summary)
            elif command in ["organize", "organise"]:
                self.add_message("assistant", "Organizing your emails...")
                organize_result = self.email_integration.organize_emails()
                self.add_message("assistant", organize_result)
            elif command == "read":
                self.add_message("assistant", "Reading emails...")
                read_result = self.email_integration.read_email()
                self.add_message("assistant", read_result)
            elif command == "draft":
                self.add_message("assistant", "What would you like to draft? Please provide details...")
                # For now, we'll ask for more details in the next message
            elif command == "help":
                self.add_message("assistant", "Available commands: inbox, organize, read, draft, help")
                status = self.email_integration.get_status()
                self.add_message("assistant", status)
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
