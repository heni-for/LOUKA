#!/usr/bin/env python3
"""
Language switcher for Luca GUI
"""

import tkinter as tk
from tkinter import ttk
from .multilang_voice import MultiLanguageVoiceRecognizer

class LanguageSwitcher:
    """Language switcher widget for Luca GUI."""
    
    def __init__(self, parent, voice_recognizer):
        self.parent = parent
        self.voice_recognizer = voice_recognizer
        self.current_language = 'en'
        
        # Create language selection frame
        self.frame = ttk.Frame(parent)
        
        # Language label
        ttk.Label(self.frame, text="Language:").pack(side=tk.LEFT, padx=5)
        
        # Language combobox
        self.language_var = tk.StringVar(value="English")
        self.language_combo = ttk.Combobox(
            self.frame, 
            textvariable=self.language_var,
            state="readonly",
            width=15
        )
        
        # Populate languages
        available_languages = self.voice_recognizer.get_available_languages()
        language_names = []
        self.language_map = {}
        
        for lang_code in available_languages:
            if lang_code == 'en':
                name = "English"
            elif lang_code == 'ar':
                name = "Arabic"
            elif lang_code == 'tn':
                name = "Tunisian Arabic"
            else:
                name = lang_code.upper()
            
            language_names.append(name)
            self.language_map[name] = lang_code
        
        self.language_combo['values'] = language_names
        self.language_combo.pack(side=tk.LEFT, padx=5)
        
        # Bind selection event
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Status label
        self.status_label = ttk.Label(self.frame, text="✅ Ready")
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def on_language_change(self, event):
        """Handle language selection change."""
        selected_name = self.language_var.get()
        if selected_name in self.language_map:
            lang_code = self.language_map[selected_name]
            self.voice_recognizer.set_language(lang_code)
            self.current_language = lang_code
            self.status_label.config(text=f"🌍 {selected_name}")
    
    def get_current_language(self):
        """Get current language code."""
        return self.current_language
    
    def pack(self, **kwargs):
        """Pack the language switcher."""
        self.frame.pack(**kwargs)
