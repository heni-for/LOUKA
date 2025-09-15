#!/usr/bin/env python3
"""
Enhanced GUI for Luca with Derja NLU Integration
Modern interface with Tunisian Derja support
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
from typing import Optional, Dict, Any

from .enhanced_voice import EnhancedVoiceRecognizer, find_best_microphone
from .derja_nlu import detect_derja_intent
from .action_mapper import execute_derja_action
from .derja_tts import speak_derja, speak_derja_with_emotion, stop_derja_speech
from .memory_manager import get_memory_manager, add_conversation_memory
from .config import VOSK_MODEL_PATH, ARABIC_MODEL_PATH

class EnhancedLucaGUI:
    """Enhanced GUI for Luca with Derja support."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Luca - AI Voice Assistant (Enhanced)")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        # Voice recognition
        self.voice_recognizer: Optional[EnhancedVoiceRecognizer] = None
        self.is_listening = False
        self.current_language = "en"
        
        # Memory manager
        self.memory_manager = get_memory_manager()
        
        # Conversation state
        self.conversation_history = []
        self.current_context = {}
        
        # Push-to-talk
        self.ptt_active = False
        self.ptt_key = 'l'
        
        self.setup_ui()
        self.setup_voice_recognition()
        self.setup_push_to_talk()
        self.load_conversation_state()
    
    def setup_ui(self):
        """Create the enhanced user interface."""
        # Title section
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="🎤 Luca - AI Voice Assistant",
            font=('Arial', 28, 'bold'),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Your intelligent voice assistant with Tunisian Derja support",
            font=('Arial', 12),
            fg='#cccccc',
            bg='#1a1a1a'
        )
        subtitle_label.pack()
        
        # Status section
        status_frame = tk.Frame(self.root, bg='#2d2d2d')
        status_frame.pack(fill='x', padx=20, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to listen",
            font=('Arial', 12, 'bold'),
            fg='#00ff88',
            bg='#2d2d2d'
        )
        self.status_label.pack(side='left')
        
        self.language_label = tk.Label(
            status_frame,
            text="Language: English",
            font=('Arial', 10),
            fg='#888888',
            bg='#2d2d2d'
        )
        self.language_label.pack(side='right')
        
        # Language switcher
        lang_frame = tk.Frame(self.root, bg='#1a1a1a')
        lang_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(lang_frame, text="Language:", font=('Arial', 10, 'bold'),
                fg='#ffffff', bg='#1a1a1a').pack(side='left')
        
        self.language_var = tk.StringVar(value="en")
        language_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=["en", "ar", "tn"],
            state="readonly",
            width=10
        )
        language_combo.pack(side='left', padx=10)
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Conversation area
        conv_frame = tk.Frame(self.root, bg='#1a1a1a')
        conv_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        conv_label = tk.Label(
            conv_frame,
            text="Conversation",
            font=('Arial', 14, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        conv_label.pack(anchor='w')
        
        # Conversation text area
        self.conversation_text = scrolledtext.ScrolledText(
            conv_frame,
            height=20,
            font=('Consolas', 11),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            selectbackground='#00ff88',
            wrap='word',
            state='disabled'
        )
        self.conversation_text.pack(fill='both', expand=True, pady=5)
        
        # Configure text tags
        self.conversation_text.tag_configure("user", foreground="#00aaff", font=('Consolas', 11, 'bold'))
        self.conversation_text.tag_configure("assistant", foreground="#00ff88", font=('Consolas', 11, 'bold'))
        self.conversation_text.tag_configure("system", foreground="#ffaa00", font=('Consolas', 10, 'italic'))
        self.conversation_text.tag_configure("error", foreground="#ff4444", font=('Consolas', 10, 'bold'))
        self.conversation_text.tag_configure("intent", foreground="#ff88ff", font=('Consolas', 9, 'italic'))
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Voice control buttons
        self.listen_button = tk.Button(
            control_frame,
            text="🎤 Start Listening",
            font=('Arial', 12, 'bold'),
            bg='#00ff88',
            fg='#000000',
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
            bg='#ff4444',
            fg='#ffffff',
            command=self.clear_conversation,
            relief='flat',
            padx=20,
            pady=10
        )
        self.clear_button.pack(side='left', padx=5)
        
        self.context_button = tk.Button(
            control_frame,
            text="📋 Context",
            font=('Arial', 12),
            bg='#ffaa00',
            fg='#000000',
            command=self.show_context,
            relief='flat',
            padx=20,
            pady=10
        )
        self.context_button.pack(side='left', padx=5)
        
        # Quick commands
        quick_frame = tk.Frame(control_frame, bg='#1a1a1a')
        quick_frame.pack(side='right')
        
        tk.Label(quick_frame, text="Quick Commands:", font=('Arial', 10, 'bold'),
                fg='#ffffff', bg='#1a1a1a').pack(anchor='w')
        
        button_frame = tk.Frame(quick_frame, bg='#1a1a1a')
        button_frame.pack(fill='x', pady=2)
        
        commands = [
            ("📧 Inbox", "inbox"),
            ("✍️ Draft", "draft"),
            ("📖 Read", "read"),
            ("🗂️ Organize", "organize"),
            ("❓ Help", "help")
        ]
        
        for text, cmd in commands:
            btn = tk.Button(
                button_frame,
                text=text,
                font=('Arial', 9),
                bg='#444444',
                fg='#ffffff',
                command=lambda c=cmd: self.send_quick_command(c),
                relief='flat',
                padx=10,
                pady=5
            )
            btn.pack(side='left', padx=2)
        
        # Text input
        input_frame = tk.Frame(self.root, bg='#1a1a1a')
        input_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(input_frame, text="Type a message:", font=('Arial', 10, 'bold'),
                fg='#ffffff', bg='#1a1a1a').pack(anchor='w')
        
        input_control_frame = tk.Frame(input_frame, bg='#1a1a1a')
        input_control_frame.pack(fill='x', pady=5)
        
        self.text_input = tk.Entry(
            input_control_frame,
            font=('Arial', 12),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat'
        )
        self.text_input.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.text_input.bind('<Return>', self.send_text_message)
        
        self.send_button = tk.Button(
            input_control_frame,
            text="Send",
            font=('Arial', 12, 'bold'),
            bg='#00aaff',
            fg='#ffffff',
            command=self.send_text_message,
            relief='flat',
            padx=20,
            pady=5
        )
        self.send_button.pack(side='right')
        
        # PTT status
        self.ptt_status_label = tk.Label(
            self.root,
            text="🎤 Press and hold 'L' to talk",
            font=('Arial', 10),
            fg='#888888',
            bg='#1a1a1a'
        )
        self.ptt_status_label.pack(pady=5)
        
        # Add initial message
        self.add_message("system", "Luca Enhanced is ready! Choose your language and start talking!")
    
    def setup_voice_recognition(self):
        """Initialize voice recognition."""
        try:
            mic_index = find_best_microphone()
            if mic_index is None:
                raise Exception("No suitable microphone found")
            
            self.voice_recognizer = EnhancedVoiceRecognizer(
                input_device=mic_index,
                language=self.current_language
            )
            
            if not self.voice_recognizer.start():
                raise Exception("Failed to start voice recognizer")
            
            self.add_message("system", f"Voice recognition ready! Language: {self.current_language}")
            
        except Exception as e:
            self.add_message("error", f"Voice recognition error: {str(e)}")
            messagebox.showerror("Voice Error", f"Could not initialize voice recognition:\n{str(e)}")
    
    def setup_push_to_talk(self):
        """Setup push-to-talk functionality."""
        self.root.bind('<KeyPress-l>', self.on_ptt_press)
        self.root.bind('<KeyRelease-l>', self.on_ptt_release)
        self.root.focus_set()
    
    def on_language_change(self, event):
        """Handle language change."""
        new_language = self.language_var.get()
        if new_language != self.current_language:
            self.current_language = new_language
            if self.voice_recognizer:
                self.voice_recognizer.set_language(new_language)
            
            # Update language label
            lang_names = {"en": "English", "ar": "Arabic", "tn": "Tunisian"}
            self.language_label.config(text=f"Language: {lang_names.get(new_language, new_language)}")
            
            self.add_message("system", f"Language changed to: {lang_names.get(new_language, new_language)}")
    
    def on_ptt_press(self, event):
        """Handle push-to-talk key press."""
        if not self.ptt_active and self.voice_recognizer:
            self.ptt_active = True
            self.ptt_status_label.config(text="🎤 Listening... (Hold 'L')", fg='#ff4444')
            self.start_ptt_listening()
    
    def on_ptt_release(self, event):
        """Handle push-to-talk key release."""
        if self.ptt_active:
            self.ptt_active = False
            self.ptt_status_label.config(text="🎤 Press and hold 'L' to talk", fg='#888888')
            self.stop_ptt_listening()
    
    def start_ptt_listening(self):
        """Start push-to-talk listening."""
        def listen_thread():
            try:
                intent = self.voice_recognizer.listen_for_command(timeout=5.0)
                if intent:
                    self.root.after(0, lambda: self.process_voice_intent(intent))
                else:
                    self.root.after(0, lambda: self.ptt_status_label.config(
                        text="🎤 No command heard. Press 'L' to try again", fg='#ffaa00'
                    ))
            except Exception as e:
                self.root.after(0, lambda: self.ptt_status_label.config(
                    text=f"❌ Error: {str(e)}", fg='#ff4444'
                ))
        
        threading.Thread(target=listen_thread, daemon=True).start()
    
    def stop_ptt_listening(self):
        """Stop push-to-talk listening."""
        if self.voice_recognizer:
            self.voice_recognizer.is_listening = False
    
    def process_voice_intent(self, intent):
        """Process voice intent."""
        # Add user message
        self.add_message("user", f"🎤 Heard: '{intent.original_text}'")
        self.add_message("intent", f"Intent: {intent.intent} (confidence: {intent.confidence:.2f})")
        
        # Process command
        response = self.voice_recognizer.process_voice_command(intent)
        
        # Add assistant response
        self.add_message("assistant", response)
        
        # Speak response
        self.voice_recognizer.speak_response(response)
        
        # Reset PTT status
        self.ptt_status_label.config(text="🎤 Press and hold 'L' to talk", fg='#888888')
    
    def toggle_listening(self):
        """Toggle voice listening."""
        if not self.voice_recognizer:
            messagebox.showerror("Error", "Voice recognition not available")
            return
        
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start voice listening."""
        self.is_listening = True
        self.listen_button.config(text="🛑 Stop Listening", bg='#ff4444')
        self.status_label.config(text="Listening... Speak now!", fg='#ff4444')
        
        def listen_loop():
            try:
                while self.is_listening and self.voice_recognizer:
                    intent = self.voice_recognizer.listen_for_command(timeout=1.0)
                    if intent:
                        self.root.after(0, lambda: self.process_voice_intent(intent))
                        break
            except Exception as e:
                self.root.after(0, lambda: self.add_message("error", f"Listening error: {str(e)}"))
            finally:
                self.root.after(0, self.stop_listening)
        
        threading.Thread(target=listen_loop, daemon=True).start()
    
    def stop_listening(self):
        """Stop voice listening."""
        self.is_listening = False
        self.listen_button.config(text="🎤 Start Listening", bg='#00ff88')
        self.status_label.config(text="Ready to listen", fg='#00ff88')
    
    def send_quick_command(self, command: str):
        """Send quick command."""
        self.add_message("user", command)
        self.process_text_command(command)
    
    def send_text_message(self, event=None):
        """Send text message."""
        message = self.text_input.get().strip()
        if message:
            self.add_message("user", message)
            self.process_text_command(message)
            self.text_input.delete(0, 'end')
    
    def process_text_command(self, command: str):
        """Process text command."""
        try:
            # Detect intent
            intent = detect_derja_intent(command)
            
            # Add intent info
            self.add_message("intent", f"Intent: {intent.intent} (confidence: {intent.confidence:.2f})")
            
            # Process command
            response = execute_derja_action(intent)
            
            # Add response
            self.add_message("assistant", response)
            
            # Speak response
            speak_derja_with_emotion(response, "neutral")
            
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            self.add_message("error", error_msg)
    
    def add_message(self, sender: str, message: str):
        """Add message to conversation."""
        self.conversation_text.config(state='normal')
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        self.conversation_text.insert('end', f"[{timestamp}] ", "system")
        
        # Add message with appropriate tag
        if sender == "user":
            self.conversation_text.insert('end', f"You: {message}\n", "user")
        elif sender == "assistant":
            self.conversation_text.insert('end', f"Luca: {message}\n", "assistant")
        elif sender == "system":
            self.conversation_text.insert('end', f"{message}\n", "system")
        elif sender == "error":
            self.conversation_text.insert('end', f"Error: {message}\n", "error")
        elif sender == "intent":
            self.conversation_text.insert('end', f"  → {message}\n", "intent")
        
        self.conversation_text.config(state='disabled')
        self.conversation_text.see('end')
        
        # Add to conversation history
        if sender in ["user", "assistant"]:
            self.conversation_history.append({"role": sender, "content": message})
    
    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_text.config(state='normal')
        self.conversation_text.delete(1.0, 'end')
        self.conversation_text.config(state='disabled')
        self.conversation_history = []
        self.add_message("system", "Conversation cleared.")
    
    def show_context(self):
        """Show current context."""
        context = self.memory_manager.get_context_summary()
        self.add_message("system", f"Current Context:\n{context}")
    
    def load_conversation_state(self):
        """Load conversation state from memory."""
        try:
            state = self.memory_manager.load_conversation_state()
            if state:
                self.current_context = state
                self.add_message("system", "Conversation state loaded from memory.")
        except Exception as e:
            self.add_message("error", f"Error loading conversation state: {str(e)}")
    
    def save_conversation_state(self):
        """Save conversation state to memory."""
        try:
            self.memory_manager.update_conversation_state(self.current_context)
        except Exception as e:
            self.add_message("error", f"Error saving conversation state: {str(e)}")
    
    def on_closing(self):
        """Handle window closing."""
        if self.voice_recognizer:
            self.voice_recognizer.stop()
        self.save_conversation_state()
        self.root.destroy()


def main():
    """Main function to run the enhanced GUI."""
    root = tk.Tk()
    app = EnhancedLucaGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
