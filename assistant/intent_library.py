#!/usr/bin/env python3
"""
Comprehensive Intent Recognition Library for Voice Commands
Detects common phrases and commands in multiple languages
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class IntentMatch:
    intent: str
    confidence: float
    matched_phrase: str
    language: str

class IntentLibrary:
    """Comprehensive intent recognition library for voice commands."""
    
    def __init__(self):
        self.intents = self._build_intent_library()
        self.languages = ['en', 'ar', 'tn']
    
    def _build_intent_library(self) -> Dict[str, Dict[str, List[str]]]:
        """Build comprehensive intent library with common phrases."""
        return {
            # TIME AND DATE INTENTS
            'time': {
                'en': [
                    'what time', 'current time', 'time now', 'what\'s the time',
                    'tell me the time', 'show me the time', 'time please',
                    'what time is it', 'time check', 'clock time'
                ],
                'ar': [
                    'كم الساعة', 'ما الوقت', 'الساعة كم', 'الوقت الحالي',
                    'أخبرني بالوقت', 'أظهر لي الوقت', 'وقت من فضلك',
                    'كم الساعة الآن', 'فحص الوقت', 'وقت الساعة'
                ],
                'tn': [
                    'كماش الساعة', 'واش الوقت', 'الساعة شكون', 'الوقت الحالي',
                    'قل لي الوقت', 'وريني الوقت', 'وقت من فضلك',
                    'كماش الساعة دابا', 'فحص الوقت', 'وقت الساعة'
                ]
            },
            
            'date': {
                'en': [
                    'what date', 'current date', 'date today', 'what\'s the date',
                    'tell me the date', 'show me the date', 'date please',
                    'what day is it', 'today\'s date', 'calendar date'
                ],
                'ar': [
                    'ما التاريخ', 'التاريخ الحالي', 'تاريخ اليوم', 'كم التاريخ',
                    'أخبرني بالتاريخ', 'أظهر لي التاريخ', 'تاريخ من فضلك',
                    'أي يوم اليوم', 'تاريخ اليوم', 'تاريخ التقويم'
                ],
                'tn': [
                    'واش التاريخ', 'التاريخ الحالي', 'تاريخ اليوم', 'كماش التاريخ',
                    'قل لي التاريخ', 'وريني التاريخ', 'تاريخ من فضلك',
                    'أي يوم اليوم', 'تاريخ اليوم', 'تاريخ التقويم'
                ]
            },
            
            # GREETINGS AND CONVERSATION
            'greeting': {
                'en': [
                    'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
                    'how are you', 'how\'s it going', 'what\'s up', 'how do you do',
                    'nice to meet you', 'pleased to meet you', 'good to see you'
                ],
                'ar': [
                    'مرحبا', 'أهلا', 'سلام', 'صباح الخير', 'مساء الخير', 'مساء النور',
                    'كيف حالك', 'كيف أنت', 'كيف الحال', 'كيف حالك اليوم',
                    'تشرفنا', 'سعيد بلقائك', 'منور'
                ],
                'tn': [
                    'أهلا', 'سلام', 'صباح الخير', 'مساء الخير', 'مساء النور',
                    'كيفاش حالك', 'كيفاش أنت', 'كيفاش الحال', 'كيفاش حالك اليوم',
                    'تشرفنا', 'سعيد بلقائك', 'منور'
                ]
            },
            
            'how_are_you': {
                'en': [
                    'how are you', 'how are you doing', 'how\'s it going', 'how do you feel',
                    'are you okay', 'are you fine', 'how\'s everything', 'how\'s life'
                ],
                'ar': [
                    'كيف حالك', 'كيف أنت', 'كيف الحال', 'كيف تشعر',
                    'هل أنت بخير', 'هل أنت جيد', 'كيف كل شيء', 'كيف الحياة'
                ],
                'tn': [
                    'كيفاش حالك', 'كيفاش أنت', 'كيفاش الحال', 'كيفاش تحس',
                    'واش أنت بخير', 'واش أنت زين', 'كيفاش كل شيء', 'كيفاش الحياة'
                ]
            },
            
            # WEATHER INTENTS
            'weather': {
                'en': [
                    'what\'s the weather', 'how\'s the weather', 'weather today', 'weather forecast',
                    'is it raining', 'is it sunny', 'temperature', 'weather report',
                    'weather conditions', 'climate', 'weather update'
                ],
                'ar': [
                    'كيف الطقس', 'ما الطقس', 'طقس اليوم', 'توقعات الطقس',
                    'هل تمطر', 'هل مشمس', 'درجة الحرارة', 'تقرير الطقس',
                    'حالة الطقس', 'المناخ', 'تحديث الطقس'
                ],
                'tn': [
                    'كيفاش الطقس', 'واش الطقس', 'طقس اليوم', 'توقعات الطقس',
                    'واش كتمطر', 'واش مشمس', 'درجة الحرارة', 'تقرير الطقس',
                    'حالة الطقس', 'المناخ', 'تحديث الطقس'
                ]
            },
            
            # EMAIL INTENTS
            'email_inbox': {
                'en': [
                    'check email', 'read email', 'open email', 'show email', 'email inbox',
                    'new email', 'unread email', 'email messages', 'check mail', 'open mail',
                    'check my email', 'show my email', 'email notifications', 'list emails',
                    'show all emails', 'check inbox', 'email list'
                ],
                'ar': [
                    'تحقق من البريد', 'اقرأ البريد', 'افتح البريد', 'أظهر البريد', 'صندوق البريد',
                    'بريد جديد', 'بريد غير مقروء', 'رسائل البريد', 'تحقق من البريد', 'افتح البريد',
                    'اقرأ بريدي', 'تحقق من بريدي', 'أظهر بريدي', 'إشعارات البريد'
                ],
                'tn': [
                    'تحقق من البريد', 'اقرأ البريد', 'افتح البريد', 'وريني البريد', 'صندوق البريد',
                    'بريد جديد', 'بريد ما يقراش', 'رسائل البريد', 'تحقق من البريد', 'افتح البريد',
                    'اقرأ بريدي', 'تحقق من بريدي', 'وريني بريدي', 'إشعارات البريد'
                ]
            },
            
            'email_compose': {
                'en': [
                    'compose email', 'write email', 'draft email', 'create email', 'new email',
                    'send email', 'email someone', 'write message', 'compose message',
                    'draft message', 'create message', 'send message'
                ],
                'ar': [
                    'اكتب بريد', 'أرسل بريد', 'مسودة بريد', 'إنشاء بريد', 'بريد جديد',
                    'أرسل بريد', 'راسل شخص', 'اكتب رسالة', 'إنشاء رسالة',
                    'مسودة رسالة', 'إنشاء رسالة', 'أرسل رسالة'
                ],
                'tn': [
                    'اكتب بريد', 'أرسل بريد', 'مسودة بريد', 'إنشاء بريد', 'بريد جديد',
                    'أرسل بريد', 'راسل شخص', 'اكتب رسالة', 'إنشاء رسالة',
                    'مسودة رسالة', 'إنشاء رسالة', 'أرسل رسالة'
                ]
            },
            
            'email_summary_and_respond': {
                'en': [
                    'summarize my last email', 'summary of last email', 'summarize last email',
                    'read my last email and respond', 'summarize and respond to last email',
                    'auto respond to last email', 'generate response for last email',
                    'summarize last email and send response', 'read last email and reply',
                    'analyze last email and respond', 'process last email and respond',
                    'read my last email', 'check my last email', 'show my last email',
                    'what is my last email', 'tell me about my last email',
                    'read email from', 'check email from', 'show email from',
                    'read last email from', 'check last email from', 'show last email from',
                    'email from', 'last email from', 'read from'
                ],
                'ar': [
                    'لخص آخر بريد', 'ملخص آخر بريد', 'لخص آخر رسالة',
                    'اقرأ آخر بريدي ورد', 'لخص ورد على آخر بريد',
                    'رد تلقائي على آخر بريد', 'أنشئ رد على آخر بريد',
                    'لخص آخر بريد وأرسل رد', 'اقرأ آخر بريد ورد',
                    'حلل آخر بريد ورد', 'عالج آخر بريد ورد'
                ],
                'tn': [
                    'لخص آخر بريد', 'ملخص آخر بريد', 'لخص آخر رسالة',
                    'اقرا آخر بريدي ورد', 'لخص ورد على آخر بريد',
                    'رد تلقائي على آخر بريد', 'اعمل رد على آخر بريد',
                    'لخص آخر بريد وابعث رد', 'اقرا آخر بريد ورد',
                    'حلل آخر بريد ورد', 'عالج آخر بريد ورد'
                ]
            },
            
            'email_summary_only': {
                'en': [
                    'summarize my email', 'email summary', 'brief email summary',
                    'quick email summary', 'short email summary', 'email overview',
                    'summarize email', 'email brief', 'email digest'
                ],
                'ar': [
                    'لخص بريدي', 'ملخص البريد', 'ملخص سريع للبريد',
                    'ملخص مختصر للبريد', 'نظرة عامة على البريد',
                    'ملخص البريد', 'نبذة عن البريد', 'ملخص البريد'
                ],
                'tn': [
                    'لخص بريدي', 'ملخص البريد', 'ملخص سريع للبريد',
                    'ملخص مختصر للبريد', 'نظرة عامة على البريد',
                    'ملخص البريد', 'نبذة عن البريد', 'ملخص البريد'
                ]
            },
            
            'gmail': {
                'en': [
                    'open gmail', 'gmail', 'google mail', 'gmail inbox', 'check gmail',
                    'read gmail', 'gmail messages', 'gmail notifications', 'gmail app'
                ],
                'ar': [
                    'افتح جيميل', 'جيميل', 'جوجل ميل', 'صندوق جيميل', 'تحقق من جيميل',
                    'اقرأ جيميل', 'رسائل جيميل', 'إشعارات جيميل', 'تطبيق جيميل'
                ],
                'tn': [
                    'افتح جيميل', 'جيميل', 'جوجل ميل', 'صندوق جيميل', 'تحقق من جيميل',
                    'اقرأ جيميل', 'رسائل جيميل', 'إشعارات جيميل', 'تطبيق جيميل'
                ]
            },
            
            # CALCULATOR INTENTS
            'calculate': {
                'en': [
                    'calculate', 'compute', 'math', 'add', 'subtract', 'multiply', 'divide',
                    'plus', 'minus', 'times', 'divided by', 'equals', 'what is', 'how much is',
                    'solve', 'work out', 'figure out'
                ],
                'ar': [
                    'احسب', 'حساب', 'رياضيات', 'جمع', 'طرح', 'ضرب', 'قسمة',
                    'زائد', 'ناقص', 'ضرب', 'مقسوم على', 'يساوي', 'ما هو', 'كم يساوي',
                    'حل', 'اعمل', 'فكر'
                ],
                'tn': [
                    'احسب', 'حساب', 'رياضيات', 'جمع', 'طرح', 'ضرب', 'قسمة',
                    'زائد', 'ناقص', 'ضرب', 'مقسوم على', 'يساوي', 'واش هو', 'كماش يساوي',
                    'حل', 'اعمل', 'فكر'
                ]
            },
            
            # JOKES AND ENTERTAINMENT
            'joke': {
                'en': [
                    'tell me a joke', 'joke', 'make me laugh', 'funny story', 'humor',
                    'laugh', 'comedy', 'funny', 'amuse me', 'entertain me'
                ],
                'ar': [
                    'احك لي نكتة', 'نكتة', 'اضحكني', 'قصة مضحكة', 'فكاهة',
                    'ضحك', 'كوميديا', 'مضحك', 'امتعني', 'سليني'
                ],
                'tn': [
                    'احك لي نكتة', 'نكتة', 'اضحكني', 'قصة مضحكة', 'فكاهة',
                    'ضحك', 'كوميديا', 'مضحك', 'امتعني', 'سليني'
                ]
            },
            
            'quote': {
                'en': [
                    'motivational quote', 'inspire me', 'quote', 'motivation', 'inspiration',
                    'wise words', 'famous quote', 'motivational words', 'encourage me'
                ],
                'ar': [
                    'اقتباس تحفيزي', 'حفزني', 'اقتباس', 'تحفيز', 'إلهام',
                    'كلمات حكيمة', 'اقتباس مشهور', 'كلمات تحفيزية', 'شجعني'
                ],
                'tn': [
                    'اقتباس تحفيزي', 'حفزني', 'اقتباس', 'تحفيز', 'إلهام',
                    'كلمات حكيمة', 'اقتباس مشهور', 'كلمات تحفيزية', 'شجعني'
                ]
            },
            
            # NEWS AND INFORMATION
            'news': {
                'en': [
                    'news', 'latest news', 'current events', 'what\'s happening', 'headlines',
                    'news update', 'breaking news', 'world news', 'local news', 'news today'
                ],
                'ar': [
                    'أخبار', 'آخر الأخبار', 'الأحداث الجارية', 'ماذا يحدث', 'العناوين',
                    'تحديث الأخبار', 'أخبار عاجلة', 'أخبار العالم', 'أخبار محلية', 'أخبار اليوم'
                ],
                'tn': [
                    'أخبار', 'آخر الأخبار', 'الأحداث الجارية', 'واش كيحدث', 'العناوين',
                    'تحديث الأخبار', 'أخبار عاجلة', 'أخبار العالم', 'أخبار محلية', 'أخبار اليوم'
                ]
            },
            
            # HELP AND SUPPORT
            'help': {
                'en': [
                    'help', 'assist me', 'support', 'guide me', 'what can you do',
                    'how do you work', 'instructions', 'tutorial', 'user guide', 'manual'
                ],
                'ar': [
                    'مساعدة', 'ساعدني', 'دعم', 'وجهني', 'ماذا يمكنك أن تفعل',
                    'كيف تعمل', 'تعليمات', 'دروس', 'دليل المستخدم', 'دليل'
                ],
                'tn': [
                    'مساعدة', 'ساعدني', 'دعم', 'وجهني', 'واش تقدر تعمل',
                    'كيفاش تعمل', 'تعليمات', 'دروس', 'دليل المستخدم', 'دليل'
                ]
            },
            
            # SYSTEM COMMANDS
            'open_app': {
                'en': [
                    'open', 'launch', 'start', 'run', 'execute', 'begin', 'activate'
                ],
                'ar': [
                    'افتح', 'شغل', 'ابدأ', 'نفذ', 'فعل', 'نشط'
                ],
                'tn': [
                    'افتح', 'شغل', 'ابدأ', 'نفذ', 'فعل', 'نشط'
                ]
            },
            
            'close_app': {
                'en': [
                    'close', 'exit', 'quit', 'stop', 'end', 'terminate', 'shut down'
                ],
                'ar': [
                    'أغلق', 'اخرج', 'توقف', 'انهي', 'أوقف', 'أغلق'
                ],
                'tn': [
                    'أغلق', 'اخرج', 'توقف', 'انهي', 'أوقف', 'أغلق'
                ]
            },
            
            # SEARCH INTENTS
            'search': {
                'en': [
                    'search', 'find', 'look for', 'seek', 'hunt for', 'google', 'look up'
                ],
                'ar': [
                    'ابحث', 'جد', 'ابحث عن', 'اطلب', 'اطلب', 'جوجل', 'ابحث عن'
                ],
                'tn': [
                    'ابحث', 'جد', 'ابحث على', 'اطلب', 'اطلب', 'جوجل', 'ابحث على'
                ]
            },
            
            # DEFINITIONS
            'define': {
                'en': [
                    'define', 'what is', 'what does mean', 'definition', 'meaning',
                    'explain', 'describe', 'tell me about'
                ],
                'ar': [
                    'عرّف', 'ما هو', 'ماذا يعني', 'تعريف', 'معنى',
                    'اشرح', 'صف', 'أخبرني عن'
                ],
                'tn': [
                    'عرّف', 'واش هو', 'واش يعني', 'تعريف', 'معنى',
                    'اشرح', 'صف', 'قل لي على'
                ]
            },
            
            # REMINDERS AND TASKS
            'reminder': {
                'en': [
                    'remind me', 'set reminder', 'create reminder', 'schedule', 'alarm',
                    'notify me', 'wake me up', 'call me', 'alert me'
                ],
                'ar': [
                    'ذكرني', 'ضع تذكير', 'أنشئ تذكير', 'جدول', 'منبه',
                    'أعلمني', 'أيقظني', 'اتصل بي', 'حذرني'
                ],
                'tn': [
                    'ذكرني', 'ضع تذكير', 'أنشئ تذكير', 'جدول', 'منبه',
                    'أعلمني', 'أيقظني', 'اتصل بي', 'حذرني'
                ]
            },
            
            # MUSIC AND MEDIA
            'music': {
                'en': [
                    'play music', 'music', 'song', 'play song', 'playlist', 'radio',
                    'spotify', 'youtube music', 'play audio', 'sound'
                ],
                'ar': [
                    'شغل موسيقى', 'موسيقى', 'أغنية', 'شغل أغنية', 'قائمة تشغيل', 'راديو',
                    'سبوتيفاي', 'يوتيوب موسيقى', 'شغل صوت', 'صوت'
                ],
                'tn': [
                    'شغل موسيقى', 'موسيقى', 'أغنية', 'شغل أغنية', 'قائمة تشغيل', 'راديو',
                    'سبوتيفاي', 'يوتيوب موسيقى', 'شغل صوت', 'صوت'
                ]
            },
            
            # WEATHER SPECIFIC
            'weather_specific': {
                'en': [
                    'is it raining', 'is it sunny', 'is it cloudy', 'is it cold', 'is it hot',
                    'temperature', 'humidity', 'wind', 'forecast', 'weather tomorrow'
                ],
                'ar': [
                    'هل تمطر', 'هل مشمس', 'هل غائم', 'هل بارد', 'هل حار',
                    'درجة الحرارة', 'رطوبة', 'رياح', 'توقعات', 'طقس الغد'
                ],
                'tn': [
                    'واش كتمطر', 'واش مشمس', 'واش غائم', 'واش بارد', 'واش سخون',
                    'درجة الحرارة', 'رطوبة', 'رياح', 'توقعات', 'طقس غدا'
                ]
            },
            
            'dont_understand': {
                'en': [
                    'dont understand', 'not understand', 'unclear', 'confused', 'what', 'huh'
                ],
                'ar': [
                    'لا أفهم', 'غير واضح', 'مش واضح', 'إيش', 'شنوة'
                ],
                'tn': [
                    'ما نفهمش', 'مش واضح', 'شنوة', 'واش'
                ]
            }
        }
    
    def detect_intent(self, text: str, language: str = 'en') -> Optional[IntentMatch]:
        """Detect intent from text with confidence scoring."""
        text_lower = text.lower().strip()
        
        best_match = None
        best_confidence = 0.0
        
        for intent_name, languages in self.intents.items():
            if language in languages:
                phrases = languages[language]
                
                for phrase in phrases:
                    # Exact match
                    if phrase.lower() in text_lower:
                        confidence = 1.0
                        if confidence > best_confidence:
                            best_match = IntentMatch(
                                intent=intent_name,
                                confidence=confidence,
                                matched_phrase=phrase,
                                language=language
                            )
                            best_confidence = confidence
                    
                    # Partial match with word boundaries
                    elif self._partial_match(text_lower, phrase.lower()):
                        confidence = 0.8
                        if confidence > best_confidence:
                            best_match = IntentMatch(
                                intent=intent_name,
                                confidence=confidence,
                                matched_phrase=phrase,
                                language=language
                            )
                            best_confidence = confidence
                    
                    # Fuzzy match
                    elif self._fuzzy_match(text_lower, phrase.lower()):
                        confidence = 0.6
                        if confidence > best_confidence:
                            best_match = IntentMatch(
                                intent=intent_name,
                                confidence=confidence,
                                matched_phrase=phrase,
                                language=language
                            )
                            best_confidence = confidence
        
        return best_match if best_confidence >= 0.6 else None
    
    def _partial_match(self, text: str, phrase: str) -> bool:
        """Check for partial match with word boundaries."""
        words = phrase.split()
        text_words = text.split()
        
        # Check if all words in phrase are present in text
        for word in words:
            if not any(word in text_word for text_word in text_words):
                return False
        return True
    
    def _fuzzy_match(self, text: str, phrase: str) -> bool:
        """Fuzzy matching for pronunciation variations."""
        # Remove common filler words
        text_clean = re.sub(r'\b(um|uh|ah|er|like|you know)\b', '', text).strip()
        
        # Check for similar words
        phrase_words = phrase.split()
        text_words = text_clean.split()
        
        matches = 0
        for phrase_word in phrase_words:
            for text_word in text_words:
                if self._words_similar(phrase_word, text_word):
                    matches += 1
                    break
        
        return matches >= len(phrase_words) * 0.7  # 70% of words must match
    
    def _words_similar(self, word1: str, word2: str) -> bool:
        """Check if two words are similar (for fuzzy matching)."""
        if word1 == word2:
            return True
        
        # Check for common variations
        variations = {
            'what': ['wut', 'wat', 'whut'],
            'time': ['tym', 'tme'],
            'you': ['u', 'yu'],
            'are': ['r', 'ar'],
            'the': ['da', 'tha'],
            'and': ['n', 'nd'],
            'for': ['4', 'fr'],
            'to': ['2', 'too'],
            'be': ['b'],
            'have': ['hav', 'hve'],
            'with': ['wth', 'wit'],
            'this': ['dis', 'tis'],
            'that': ['dat', 'tat'],
            'will': ['wil', 'wll'],
            'your': ['ur', 'yur'],
            'can': ['cn', 'kan'],
            'all': ['al', 'awl'],
            'get': ['gt', 'git'],
            'make': ['mak', 'mke'],
            'come': ['cum', 'cme'],
            'know': ['no', 'kno'],
            'take': ['tak', 'tke'],
            'see': ['c', 'sea'],
            'go': ['g', 'goo'],
            'say': ['sai', 'sae'],
            'use': ['us', 'uze'],
            'find': ['fnd', 'fid'],
            'give': ['giv', 'gve'],
            'tell': ['tel', 'tll'],
            'work': ['wrk', 'wok'],
            'call': ['cal', 'cll'],
            'try': ['tri', 'try'],
            'ask': ['as', 'aks'],
            'need': ['ned', 'nid'],
            'feel': ['fel', 'fll'],
            'become': ['becm', 'becum'],
            'leave': ['leav', 'leve'],
            'put': ['pt', 'put'],
            'mean': ['men', 'meen'],
            'keep': ['kep', 'kee'],
            'let': ['lt', 'let'],
            'begin': ['begn', 'begi'],
            'seem': ['sem', 'seem'],
            'help': ['hlp', 'hel'],
            'talk': ['tal', 'tolk'],
            'turn': ['trn', 'torn'],
            'start': ['strt', 'stert'],
            'show': ['sho', 'shw'],
            'hear': ['her', 'hear'],
            'play': ['pla', 'pley'],
            'run': ['rn', 'run'],
            'move': ['mov', 'muv'],
            'live': ['liv', 'lif'],
            'believe': ['beliv', 'beleev'],
            'hold': ['hld', 'hol'],
            'bring': ['brng', 'brig'],
            'happen': ['hapn', 'hapen'],
            'write': ['writ', 'wryt'],
            'provide': ['provid', 'provde'],
            'sit': ['st', 'sit'],
            'stand': ['stnd', 'stand'],
            'lose': ['los', 'loos'],
            'pay': ['pa', 'pay'],
            'meet': ['met', 'meet'],
            'include': ['includ', 'inclue'],
            'continue': ['continu', 'contnue'],
            'set': ['st', 'set'],
            'learn': ['lern', 'lear'],
            'change': ['chang', 'chage'],
            'lead': ['led', 'lead'],
            'understand': ['understnd', 'undrstand'],
            'watch': ['wch', 'watc'],
            'follow': ['follw', 'folow'],
            'stop': ['stp', 'stop'],
            'create': ['creat', 'creat'],
            'speak': ['spek', 'spak'],
            'read': ['red', 'read'],
            'allow': ['alow', 'alow'],
            'add': ['ad', 'add'],
            'spend': ['spnd', 'spen'],
            'grow': ['gro', 'grow'],
            'open': ['opn', 'open'],
            'walk': ['wlk', 'walk'],
            'win': ['wn', 'win'],
            'offer': ['ofr', 'ofer'],
            'remember': ['remembr', 'rememr'],
            'love': ['lov', 'luv'],
            'consider': ['considr', 'consder'],
            'appear': ['appear', 'apear'],
            'buy': ['by', 'buy'],
            'wait': ['wat', 'wait'],
            'serve': ['serv', 'srv'],
            'die': ['dy', 'die'],
            'send': ['snd', 'send'],
            'expect': ['expect', 'expt'],
            'build': ['bild', 'buld'],
            'stay': ['sta', 'stay'],
            'fall': ['fal', 'fall'],
            'cut': ['ct', 'cut'],
            'reach': ['rech', 'reac'],
            'kill': ['kil', 'kil'],
            'remain': ['remain', 'remn']
        }
        
        # Check if words are in variations
        for base_word, variants in variations.items():
            if word1 == base_word and word2 in variants:
                return True
            if word2 == base_word and word1 in variants:
                return True
        
        # Check for common typos and phonetic similarities
        if len(word1) > 2 and len(word2) > 2:
            # Simple Levenshtein distance check
            if self._levenshtein_distance(word1, word2) <= 2:
                return True
        
        return False
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def get_all_intents(self) -> List[str]:
        """Get list of all available intents."""
        return list(self.intents.keys())
    
    def get_intent_phrases(self, intent: str, language: str = 'en') -> List[str]:
        """Get all phrases for a specific intent and language."""
        if intent in self.intents and language in self.intents[intent]:
            return self.intents[intent][language]
        return []
    
    def add_custom_intent(self, intent_name: str, phrases: Dict[str, List[str]]):
        """Add custom intent with phrases in multiple languages."""
        self.intents[intent_name] = phrases
    
    def detect_multiple_intents(self, text: str, language: str = 'en') -> List[IntentMatch]:
        """Detect multiple intents from text."""
        matches = []
        text_lower = text.lower().strip()
        
        for intent_name, languages in self.intents.items():
            if language in languages:
                phrases = languages[language]
                
                for phrase in phrases:
                    if phrase.lower() in text_lower:
                        matches.append(IntentMatch(
                            intent=intent_name,
                            confidence=1.0,
                            matched_phrase=phrase,
                            language=language
                        ))
        
        # Remove duplicates and sort by confidence
        unique_matches = {}
        for match in matches:
            if match.intent not in unique_matches or match.confidence > unique_matches[match.intent].confidence:
                unique_matches[match.intent] = match
        
        return sorted(unique_matches.values(), key=lambda x: x.confidence, reverse=True)

# Global instance
intent_library = IntentLibrary()

def detect_intent(text: str, language: str = 'en') -> Optional[IntentMatch]:
    """Convenience function to detect intent."""
    return intent_library.detect_intent(text, language)

def get_intent_phrases(intent: str, language: str = 'en') -> List[str]:
    """Convenience function to get intent phrases."""
    return intent_library.get_intent_phrases(intent, language)
