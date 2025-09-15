#!/usr/bin/env python3
"""
Gamification System for Luca
Jokes, trivia, games, and fun interactions in Derja
"""

import random
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from .conversational_personality import get_personality_response
from .ai_chatty_brain import chat_naturally
from .emotional_tts import speak_with_emotion

@dataclass
class GameScore:
    """Game score for a user."""
    user_id: str
    game_type: str
    score: int
    level: int
    achievements: List[str]
    last_played: float
    total_plays: int

@dataclass
class TriviaQuestion:
    """Trivia question."""
    id: str
    question: str
    options: List[str]
    correct_answer: int
    difficulty: str  # easy, medium, hard
    category: str
    explanation: str

class GamificationSystem:
    """Gamification system for fun interactions."""
    
    def __init__(self):
        self.scores = {}
        self.achievements = self._load_achievements()
        self.trivia_questions = self._load_trivia_questions()
        self.jokes = self._load_jokes()
        self.games = self._load_games()
        self.scores_file = "game_scores.json"
        self._load_scores()
    
    def _load_achievements(self) -> List[Dict[str, Any]]:
        """Load achievement definitions."""
        return [
            {
                "id": "first_joke",
                "name": "نكتة أولى",
                "description": "سمعت أول نكتة من لوكا",
                "condition": "joke_count >= 1",
                "reward": "🎭"
            },
            {
                "id": "trivia_master",
                "name": "خبير المعلومات",
                "description": "أجبت على 10 أسئلة صحيحة",
                "condition": "correct_answers >= 10",
                "reward": "🧠"
            },
            {
                "id": "daily_player",
                "name": "لاعب يومي",
                "description": "لعبت كل يوم لمدة أسبوع",
                "condition": "daily_streak >= 7",
                "reward": "📅"
            },
            {
                "id": "email_expert",
                "name": "خبير الإيميلات",
                "description": "أرسلت 50 إيميل",
                "condition": "emails_sent >= 50",
                "reward": "📧"
            },
            {
                "id": "voice_master",
                "name": "سيد الصوت",
                "description": "استخدمت الصوت 100 مرة",
                "condition": "voice_commands >= 100",
                "reward": "🎤"
            }
        ]
    
    def _load_trivia_questions(self) -> List[TriviaQuestion]:
        """Load trivia questions."""
        return [
            TriviaQuestion(
                id="tunisia_capital",
                question="شنو هي عاصمة تونس؟",
                options=["تونس", "صفاقس", "سوسة", "قابس"],
                correct_answer=0,
                difficulty="easy",
                category="جغرافيا",
                explanation="تونس هي عاصمة تونس"
            ),
            TriviaQuestion(
                id="tunisia_independence",
                question="متى استقلت تونس؟",
                options=["1956", "1957", "1958", "1959"],
                correct_answer=0,
                difficulty="medium",
                category="تاريخ",
                explanation="تونس استقلت في 20 مارس 1956"
            ),
            TriviaQuestion(
                id="derja_hello",
                question="شنو معنى 'أهلا وسهلا' في الدارجة؟",
                options=["مرحبا", "وداعا", "شكرا", "معذرة"],
                correct_answer=0,
                difficulty="easy",
                category="لغة",
                explanation="أهلا وسهلا تعني مرحبا"
            ),
            TriviaQuestion(
                id="tunisia_currency",
                question="شنو هي العملة التونسية؟",
                options=["دينار", "درهم", "ليرة", "فرنك"],
                correct_answer=0,
                difficulty="easy",
                category="اقتصاد",
                explanation="الدينار التونسي هو العملة الرسمية"
            ),
            TriviaQuestion(
                id="tunisia_population",
                question="كم عدد سكان تونس تقريبا؟",
                options=["10 مليون", "12 مليون", "15 مليون", "18 مليون"],
                correct_answer=1,
                difficulty="medium",
                category="جغرافيا",
                explanation="عدد سكان تونس حوالي 12 مليون نسمة"
            )
        ]
    
    def _load_jokes(self) -> List[Dict[str, Any]]:
        """Load jokes in Derja."""
        return [
            {
                "id": "joke_1",
                "text": "شنو الفرق بين المدرس و الطبيب؟ المدرس يقول 'افتح كتابك' و الطبيب يقول 'افتح فمك'! هههه",
                "category": "مدرسة",
                "difficulty": "easy"
            },
            {
                "id": "joke_2",
                "text": "واحد قعد يتفرج في التلفزة، جاتو مرتو قالتلو: 'يا حسرة، شوف شكون هذاك اللي في التلفزة، عندو نفس لون شعرك!' قالها: 'باهي، وشنوة؟ هو أحسن مني!' هههه",
                "category": "عائلة",
                "difficulty": "easy"
            },
            {
                "id": "joke_3",
                "text": "واحد قال لصاحبو: 'يا حسرة، زوجتي صارت تتكلم معايا بكل هدوء!' صاحبو قال لو: 'أها و شنوة اللي خليك مضايق؟' قاللو: 'لأنها صارت تتكلم معايا من ورا الباب!' هههه",
                "category": "زواج",
                "difficulty": "medium"
            },
            {
                "id": "joke_4",
                "text": "واحد دخل على الطبيب قاللو: 'دكتور، أنا مش قادر أنام!' قاللو الطبيب: 'اشرب كاس حليب دافئ قبل النوم.' قاللو: 'جربت و مش نافع!' قاللو الطبيب: 'جرب كاسين!' هههه",
                "category": "صحة",
                "difficulty": "easy"
            },
            {
                "id": "joke_5",
                "text": "واحد قال لصاحبو: 'يا حسرة، أنا مش قادر أشتغل!' قاللو: 'ليش؟' قاللو: 'لأني مش قادر أشتغل!' قاللو: 'أها، وشنو تريد تعمل؟' قاللو: 'أريد أشتغل!' هههه",
                "category": "عمل",
                "difficulty": "medium"
            }
        ]
    
    def _load_games(self) -> List[Dict[str, Any]]:
        """Load game definitions."""
        return [
            {
                "id": "word_guess",
                "name": "تخمين الكلمة",
                "description": "تخمن كلمة من الحروف المعطاة",
                "difficulty": "medium",
                "max_score": 100
            },
            {
                "id": "number_guess",
                "name": "تخمين الرقم",
                "description": "تخمن رقم بين 1 و 100",
                "difficulty": "easy",
                "max_score": 50
            },
            {
                "id": "memory_game",
                "name": "لعبة الذاكرة",
                "description": "تتذكر تسلسل الأرقام",
                "difficulty": "hard",
                "max_score": 200
            },
            {
                "id": "derja_quiz",
                "name": "مسابقة الدارجة",
                "description": "أسئلة عن الدارجة التونسية",
                "difficulty": "medium",
                "max_score": 150
            }
        ]
    
    def _load_scores(self):
        """Load game scores."""
        try:
            if os.path.exists(self.scores_file):
                with open(self.scores_file, "r", encoding="utf-8") as f:
                    scores_data = json.load(f)
                
                for score_data in scores_data:
                    score = GameScore(**score_data)
                    self.scores[f"{score.user_id}_{score.game_type}"] = score
                
                print(f"✅ Loaded {len(self.scores)} game scores")
        except Exception as e:
            print(f"Error loading scores: {e}")
    
    def _save_scores(self):
        """Save game scores."""
        try:
            scores_data = [asdict(score) for score in self.scores.values()]
            with open(self.scores_file, "w", encoding="utf-8") as f:
                json.dump(scores_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving scores: {e}")
    
    def get_random_joke(self, category: str = None) -> Dict[str, Any]:
        """Get a random joke."""
        try:
            if category:
                category_jokes = [joke for joke in self.jokes if joke["category"] == category]
                if category_jokes:
                    joke = random.choice(category_jokes)
                else:
                    joke = random.choice(self.jokes)
            else:
                joke = random.choice(self.jokes)
            
            # Add personality response
            personality_response = get_personality_response(
                "joke", 
                joke["text"],
                last_action="joke_told",
                mood="playful"
            )
            
            return {
                "joke": joke,
                "personality_response": personality_response
            }
        except Exception as e:
            print(f"Joke error: {e}")
            return {"joke": None, "personality_response": "مش قادر أقول نكتة توا!"}
    
    def get_trivia_question(self, difficulty: str = None, category: str = None) -> TriviaQuestion:
        """Get a trivia question."""
        try:
            filtered_questions = self.trivia_questions
            
            if difficulty:
                filtered_questions = [q for q in filtered_questions if q.difficulty == difficulty]
            
            if category:
                filtered_questions = [q for q in filtered_questions if q.category == category]
            
            if not filtered_questions:
                filtered_questions = self.trivia_questions
            
            return random.choice(filtered_questions)
        except Exception as e:
            print(f"Trivia question error: {e}")
            return self.trivia_questions[0]
    
    def check_trivia_answer(self, question_id: str, answer: int, user_id: str = "default") -> Dict[str, Any]:
        """Check trivia answer and update score."""
        try:
            question = next((q for q in self.trivia_questions if q.id == question_id), None)
            if not question:
                return {"correct": False, "message": "سؤال غير موجود"}
            
            is_correct = answer == question.correct_answer
            
            # Update score
            score_key = f"{user_id}_trivia"
            if score_key not in self.scores:
                self.scores[score_key] = GameScore(
                    user_id=user_id,
                    game_type="trivia",
                    score=0,
                    level=1,
                    achievements=[],
                    last_played=time.time(),
                    total_plays=0
                )
            
            score = self.scores[score_key]
            score.total_plays += 1
            score.last_played = time.time()
            
            if is_correct:
                score.score += 10
                score.level = (score.score // 100) + 1
                
                # Check for achievements
                self._check_achievements(score)
                
                message = f"صح! {question.explanation} 🎉"
                personality_response = get_personality_response(
                    "trivia_correct",
                    message,
                    last_action="trivia_correct",
                    mood="happy"
                )
            else:
                message = f"غلط! الجواب الصحيح هو: {question.options[question.correct_answer]}. {question.explanation}"
                personality_response = get_personality_response(
                    "trivia_wrong",
                    message,
                    last_action="trivia_wrong",
                    mood="encouraging"
                )
            
            self._save_scores()
            
            return {
                "correct": is_correct,
                "message": message,
                "personality_response": personality_response,
                "score": score.score,
                "level": score.level,
                "achievements": score.achievements
            }
            
        except Exception as e:
            print(f"Trivia answer check error: {e}")
            return {"correct": False, "message": "خطأ في التحقق من الإجابة"}
    
    def play_word_guess_game(self, user_id: str = "default") -> Dict[str, Any]:
        """Play word guess game."""
        try:
            # Derja words for guessing
            words = [
                {"word": "تونس", "hint": "البلد اللي نحنا فيه"},
                {"word": "دارجة", "hint": "اللغة اللي نحنا نتكلم بيها"},
                {"word": "لوكا", "hint": "اسم المساعد الذكي"},
                {"word": "إيميل", "hint": "الرسائل اللي تجيك في البريد"},
                {"word": "ميتينغ", "hint": "الاجتماعات في العمل"}
            ]
            
            selected_word = random.choice(words)
            word = selected_word["word"]
            hint = selected_word["hint"]
            
            # Create scrambled word
            scrambled = list(word)
            random.shuffle(scrambled)
            scrambled_word = "".join(scrambled)
            
            return {
                "game_id": "word_guess",
                "scrambled_word": scrambled_word,
                "hint": hint,
                "original_word": word,
                "max_attempts": 3,
                "score": 100
            }
            
        except Exception as e:
            print(f"Word guess game error: {e}")
            return {"error": "خطأ في لعبة تخمين الكلمة"}
    
    def play_number_guess_game(self, user_id: str = "default") -> Dict[str, Any]:
        """Play number guess game."""
        try:
            target_number = random.randint(1, 100)
            
            return {
                "game_id": "number_guess",
                "target_number": target_number,
                "range": "1-100",
                "max_attempts": 7,
                "score": 50
            }
            
        except Exception as e:
            print(f"Number guess game error: {e}")
            return {"error": "خطأ في لعبة تخمين الرقم"}
    
    def play_memory_game(self, user_id: str = "default") -> Dict[str, Any]:
        """Play memory game."""
        try:
            # Generate sequence of numbers
            sequence_length = 4
            sequence = [random.randint(1, 9) for _ in range(sequence_length)]
            
            return {
                "game_id": "memory_game",
                "sequence": sequence,
                "sequence_length": sequence_length,
                "score": 200
            }
            
        except Exception as e:
            print(f"Memory game error: {e}")
            return {"error": "خطأ في لعبة الذاكرة"}
    
    def get_daily_challenge(self) -> Dict[str, Any]:
        """Get daily challenge."""
        try:
            challenges = [
                {
                    "id": "email_master",
                    "name": "سيد الإيميلات",
                    "description": "أرسل 5 إيميلات اليوم",
                    "target": 5,
                    "reward": "📧",
                    "type": "email"
                },
                {
                    "id": "voice_commander",
                    "name": "قائد الصوت",
                    "description": "استخدم 10 أوامر صوتية",
                    "target": 10,
                    "reward": "🎤",
                    "type": "voice"
                },
                {
                    "id": "trivia_champion",
                    "name": "بطل المعلومات",
                    "description": "أجب على 5 أسئلة صحيحة",
                    "target": 5,
                    "reward": "🧠",
                    "type": "trivia"
                }
            ]
            
            challenge = random.choice(challenges)
            
            return {
                "challenge": challenge,
                "message": f"تحدي اليوم: {challenge['name']} - {challenge['description']}",
                "reward": challenge["reward"]
            }
            
        except Exception as e:
            print(f"Daily challenge error: {e}")
            return {"error": "خطأ في التحدي اليومي"}
    
    def get_user_stats(self, user_id: str = "default") -> Dict[str, Any]:
        """Get user statistics."""
        try:
            user_scores = {k: v for k, v in self.scores.items() if v.user_id == user_id}
            
            total_score = sum(score.score for score in user_scores.values())
            total_plays = sum(score.total_plays for score in user_scores.values())
            total_achievements = sum(len(score.achievements) for score in user_scores.values())
            
            # Calculate level
            level = (total_score // 1000) + 1
            
            return {
                "user_id": user_id,
                "total_score": total_score,
                "level": level,
                "total_plays": total_plays,
                "total_achievements": total_achievements,
                "scores": {score.game_type: score.score for score in user_scores.values()},
                "achievements": [achievement for score in user_scores.values() for achievement in score.achievements]
            }
            
        except Exception as e:
            print(f"User stats error: {e}")
            return {"error": "خطأ في إحصائيات المستخدم"}
    
    def _check_achievements(self, score: GameScore):
        """Check for new achievements."""
        try:
            for achievement in self.achievements:
                if achievement["id"] in score.achievements:
                    continue
                
                # Check achievement condition
                if self._evaluate_achievement_condition(achievement["condition"], score):
                    score.achievements.append(achievement["id"])
                    print(f"🎉 Achievement unlocked: {achievement['name']}")
            
        except Exception as e:
            print(f"Achievement check error: {e}")
    
    def _evaluate_achievement_condition(self, condition: str, score: GameScore) -> bool:
        """Evaluate achievement condition."""
        try:
            # Simple condition evaluation
            if "joke_count" in condition:
                return score.total_plays >= 1
            elif "correct_answers" in condition:
                return score.score >= 100  # 10 correct answers * 10 points
            elif "daily_streak" in condition:
                return score.total_plays >= 7
            elif "emails_sent" in condition:
                return score.total_plays >= 50
            elif "voice_commands" in condition:
                return score.total_plays >= 100
            
            return False
        except Exception as e:
            print(f"Condition evaluation error: {e}")
            return False
    
    def get_leaderboard(self, game_type: str = None) -> List[Dict[str, Any]]:
        """Get leaderboard."""
        try:
            scores = list(self.scores.values())
            
            if game_type:
                scores = [s for s in scores if s.game_type == game_type]
            
            # Sort by score
            scores.sort(key=lambda x: x.score, reverse=True)
            
            leaderboard = []
            for i, score in enumerate(scores[:10]):  # Top 10
                leaderboard.append({
                    "rank": i + 1,
                    "user_id": score.user_id,
                    "score": score.score,
                    "level": score.level,
                    "achievements": len(score.achievements)
                })
            
            return leaderboard
            
        except Exception as e:
            print(f"Leaderboard error: {e}")
            return []
    
    def get_fun_response(self, user_input: str) -> str:
        """Get fun response based on user input."""
        try:
            user_input_lower = user_input.lower()
            
            if any(word in user_input_lower for word in ["نكتة", "joke", "ضحك"]):
                joke_data = self.get_random_joke()
                return joke_data["personality_response"]
            
            elif any(word in user_input_lower for word in ["سؤال", "question", "مسابقة"]):
                question = self.get_trivia_question()
                return f"سؤال: {question.question}\nالخيارات: {', '.join(question.options)}"
            
            elif any(word in user_input_lower for word in ["لعبة", "game", "لعب"]):
                return "تريد تلعب شنو؟ تقدر تقولي 'تخمين الكلمة' أو 'تخمين الرقم' أو 'لعبة الذاكرة'"
            
            elif any(word in user_input_lower for word in ["تحدي", "challenge", "تحدي اليوم"]):
                challenge = self.get_daily_challenge()
                return challenge["message"]
            
            elif any(word in user_input_lower for word in ["إحصائيات", "stats", "نقاط"]):
                stats = self.get_user_stats()
                return f"نقاطك: {stats['total_score']}, مستوى: {stats['level']}, إنجازات: {stats['total_achievements']}"
            
            else:
                return "تريد تسمع نكتة؟ ولا تريد تلعب لعبة؟ ولا تريد تشوف تحديك اليوم؟"
                
        except Exception as e:
            print(f"Fun response error: {e}")
            return "مش قادر أرد توا!"


# Global instance
gamification_system = GamificationSystem()

def get_random_joke(category: str = None) -> Dict[str, Any]:
    """Get random joke."""
    return gamification_system.get_random_joke(category)

def get_trivia_question(difficulty: str = None, category: str = None) -> TriviaQuestion:
    """Get trivia question."""
    return gamification_system.get_trivia_question(difficulty, category)

def check_trivia_answer(question_id: str, answer: int, user_id: str = "default") -> Dict[str, Any]:
    """Check trivia answer."""
    return gamification_system.check_trivia_answer(question_id, answer, user_id)

def play_word_guess_game(user_id: str = "default") -> Dict[str, Any]:
    """Play word guess game."""
    return gamification_system.play_word_guess_game(user_id)

def play_number_guess_game(user_id: str = "default") -> Dict[str, Any]:
    """Play number guess game."""
    return gamification_system.play_number_guess_game(user_id)

def play_memory_game(user_id: str = "default") -> Dict[str, Any]:
    """Play memory game."""
    return gamification_system.play_memory_game(user_id)

def get_daily_challenge() -> Dict[str, Any]:
    """Get daily challenge."""
    return gamification_system.get_daily_challenge()

def get_user_stats(user_id: str = "default") -> Dict[str, Any]:
    """Get user stats."""
    return gamification_system.get_user_stats(user_id)

def get_leaderboard(game_type: str = None) -> List[Dict[str, Any]]:
    """Get leaderboard."""
    return gamification_system.get_leaderboard(game_type)

def get_fun_response(user_input: str) -> str:
    """Get fun response."""
    return gamification_system.get_fun_response(user_input)
