from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
import re

app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────────
#  RESPONSE KNOWLEDGE BASE
# ──────────────────────────────────────────────

GREETINGS = [
    "Hi there! 😊 I'm MindEase, your wellness companion. How are you feeling today?",
    "Hello! 👋 I'm here to listen and support you. How has your day been?",
    "Hey! It's great to see you. 🌿 How are you doing emotionally today?",
    "Hi! Welcome to MindEase. I'm here for you — how are you feeling right now?",
]

STRESS_RESPONSES = [
    "I hear you — stress can feel really overwhelming. 💙 Can you tell me a bit more about what's been stressing you out lately?",
    "It sounds like you're carrying a heavy load right now. That's completely valid. What do you think is the main source of your stress?",
    "Stress is tough, and I'm glad you're talking about it. 🌿 Is this something that's been building up for a while, or did something specific trigger it?",
    "I'm sorry you're feeling stressed. Remember, it's okay to feel this way. Would you like to talk about what's going on?",
]

ANXIETY_RESPONSES = [
    "Anxiety can feel really scary, but you're not alone in this. 💙 How long have you been feeling this way?",
    "I understand — anxiety has a way of making everything feel more intense. Can you describe what your anxiety feels like for you?",
    "Thank you for sharing that with me. Anxiety is very common and very real. What situations tend to make it worse for you?",
    "I hear you. That constant worried feeling is exhausting. 🌿 Do you have any moments in the day where you feel more at ease?",
]

SAD_RESPONSES = [
    "I'm really sorry you're feeling sad. 💙 It takes courage to acknowledge that. What do you think has been making you feel this way?",
    "Sadness is a heavy feeling to carry. I want you to know it's okay to feel this — you don't have to pretend to be okay. What's been on your mind?",
    "I hear you, and I'm here with you. 🌿 Sometimes sadness comes without a clear reason too — has anything changed recently in your life?",
    "Thank you for trusting me with this. Feeling sad is part of being human. Would you like to talk about what's been happening?",
]

LONELY_RESPONSES = [
    "Loneliness is one of the hardest feelings to sit with. 💙 Do you feel disconnected from people around you, or is it more of an internal emptiness?",
    "I'm here with you right now, and I want you to know you matter. 🌿 How long have you been feeling lonely?",
    "Feeling lonely doesn't mean you're unlovable — it often means your need for connection isn't being met. Have you been able to talk to anyone about this?",
    "I hear you. That feeling of being alone even in a crowd is really painful. What do you think is making it hard to connect with others?",
]

ANGRY_RESPONSES = [
    "It sounds like you're really frustrated right now. 💙 Anger is a valid emotion — what happened that made you feel this way?",
    "I hear your frustration. It's completely okay to feel angry. Would you like to talk about what triggered it?",
    "Anger often points to something important — a boundary crossed or a need unmet. 🌿 What do you think is underneath the anger?",
    "That sounds really infuriating. I'm here to listen without judgment. Can you tell me more about the situation?",
]

HAPPY_RESPONSES = [
    "That's wonderful to hear! 😊 What's been making you feel good lately?",
    "I love hearing that! 🌿 Positive emotions are so important — what contributed to this good feeling?",
    "That's great! It sounds like things are going well. What would you say is the biggest reason you're feeling happy today?",
    "Wonderful! 😊 Cherish that feeling. Is this a recent change, or have you been feeling this way for a while?",
]

TIRED_RESPONSES = [
    "I'm sorry you're feeling exhausted. 💙 Is this more of a physical tiredness or an emotional/mental drain?",
    "Fatigue — especially emotional fatigue — is really hard. Have you been getting enough sleep, or does the tiredness go deeper than that?",
    "Being tired all the time can really affect everything else. 🌿 How long have you been feeling this way?",
    "That sounds really draining. Sometimes our body and mind are telling us they need rest. What do you think is wearing you out the most?",
]

HOPELESS_RESPONSES = [
    "I hear you, and I want you to know that feeling hopeless doesn't mean things can't change. 💙 Can you tell me more about what's making you feel this way?",
    "Thank you for trusting me with something so heavy. Hopelessness is a really painful place to be. How long have you been feeling like this?",
    "I'm really glad you're talking about this. 🌿 Even when everything feels dark, reaching out is a brave and important step. What's been happening?",
    "I hear you. That loss of hope is exhausting. You don't have to carry this alone — would you like to share what's been going on?",
]

CRISIS_RESPONSE = """I hear you, and I want you to know you matter deeply. 💙

Please reach out to a crisis helpline right away — trained counselors are available 24/7:

🇮🇳 India: iCall — 9152987821
🌍 International: www.findahelpline.com

You don't have to face this alone. Talking to someone who can really help is the most important step right now."""

SLEEP_RESPONSES = [
    "Sleep issues can really affect your mental health. 🌿 Are you having trouble falling asleep, staying asleep, or both?",
    "I'm sorry to hear that. Poor sleep makes everything harder to cope with. How many hours are you typically getting?",
    "Sleep and mental health are deeply connected. 💙 Has anything changed recently that might be affecting your sleep?",
]

WORK_STUDY_RESPONSES = [
    "Work and study pressure can be really overwhelming. 💙 What specifically is feeling most difficult — deadlines, performance, relationships at work/school?",
    "That kind of pressure builds up fast. 🌿 How are you managing to take breaks during the day?",
    "Academic and professional stress is very real. Are you feeling like the workload is too much, or is it more about fear of failure?",
]

RELATIONSHIP_RESPONSES = [
    "Relationship stress can really take a toll emotionally. 💙 Is this about a romantic relationship, family, or friendship?",
    "I hear you — people we care about have the most power to affect us. 🌿 Would you like to talk more about the situation?",
    "Relationship difficulties are some of the hardest things to navigate. What's been the main source of tension?",
]

FOLLOWUP_QUESTIONS = [
    "How long have you been feeling this way?",
    "Is there someone in your life you've been able to talk to about this?",
    "On a scale of 1 to 10, how would you rate your overall mood today?",
    "What helps you feel a little better when you're going through tough times?",
    "Have these feelings been affecting your daily life — like work, eating, or sleep?",
    "Do you have moments during the day where you feel relief, even briefly?",
]

GENERIC_EMPATHY = [
    "Thank you for sharing that with me. 💙 It sounds like you've been going through a lot. Can you tell me more?",
    "I hear you, and I want you to know what you're feeling is valid. 🌿 What do you think is at the root of all this?",
    "That sounds really difficult. You're doing the right thing by talking about it. What else has been on your mind?",
    "I appreciate you opening up. 💙 Sometimes just naming what we're feeling helps a little. Is there more you'd like to share?",
    "I'm here with you. 🌿 It takes strength to talk about how we're feeling. What would help you most right now — to vent, or to think through solutions?",
]

CLOSING_POSITIVE = [
    "Remember — reaching out and talking about your feelings is already a powerful act of self-care. 🌿",
    "You're doing the right thing by checking in with yourself. That awareness matters. 💙",
    "Whatever you're going through, you don't have to face it alone. I'm here whenever you need to talk. 😊",
]

# ──────────────────────────────────────────────
#  KEYWORD DETECTION ENGINE
# ──────────────────────────────────────────────

def detect_intent(text):
    text = text.lower().strip()

    crisis_keywords = [
        "suicide", "suicidal", "kill myself", "end my life", "want to die",
        "don't want to live", "no reason to live", "harm myself", "self harm",
        "cut myself", "overdose", "worthless", "better off dead"
    ]
    if any(kw in text for kw in crisis_keywords):
        return "crisis"

    if re.search(r'\b(hi|hello|hey|hii|helo|good morning|good evening|good afternoon|howdy)\b', text):
        return "greeting"

    stress_kw = ["stress", "stressed", "stressful", "overwhelm", "pressure", "burden", "too much", "can't handle", "exhausted by"]
    if any(kw in text for kw in stress_kw):
        return "stress"

    anxiety_kw = ["anxious", "anxiety", "nervous", "panic", "panic attack", "worry", "worried", "fear", "scared", "dread", "uneasy", "restless"]
    if any(kw in text for kw in anxiety_kw):
        return "anxiety"

    sad_kw = ["sad", "sadness", "unhappy", "depressed", "depression", "crying", "cry", "tears", "heartbroken", "down", "low", "gloomy", "miserable", "grief", "grieving"]
    if any(kw in text for kw in sad_kw):
        return "sad"

    lonely_kw = ["lonely", "alone", "loneliness", "isolated", "no one", "nobody", "no friends", "disconnected", "left out", "abandoned"]
    if any(kw in text for kw in lonely_kw):
        return "lonely"

    angry_kw = ["angry", "anger", "mad", "furious", "rage", "frustrated", "frustration", "irritated", "annoyed", "hate", "pissed"]
    if any(kw in text for kw in angry_kw):
        return "angry"

    happy_kw = ["happy", "great", "good", "wonderful", "excellent", "fantastic", "amazing", "joy", "joyful", "excited", "blessed", "grateful", "fine", "okay", "alright", "cheerful"]
    if any(kw in text for kw in happy_kw):
        return "happy"

    tired_kw = ["tired", "exhausted", "fatigue", "fatigued", "drained", "burnout", "burnt out", "no energy", "weak", "sleepy", "worn out"]
    if any(kw in text for kw in tired_kw):
        return "tired"

    hopeless_kw = ["hopeless", "helpless", "no hope", "pointless", "meaningless", "nothing matters", "what's the point", "give up", "giving up", "can't go on"]
    if any(kw in text for kw in hopeless_kw):
        return "hopeless"

    sleep_kw = ["sleep", "insomnia", "can't sleep", "nightmares", "nightmare", "awake at night", "not sleeping", "sleepless"]
    if any(kw in text for kw in sleep_kw):
        return "sleep"

    work_kw = ["work", "job", "office", "boss", "deadline", "study", "studies", "exam", "college", "university", "school", "assignment", "marks", "grades", "career"]
    if any(kw in text for kw in work_kw):
        return "work_study"

    relation_kw = ["relationship", "partner", "boyfriend", "girlfriend", "husband", "wife", "family", "parents", "mother", "father", "friend", "friendship", "breakup", "divorce", "fight", "argument"]
    if any(kw in text for kw in relation_kw):
        return "relationship"

    return "generic"


def get_response(intent, conversation_length):
    if intent == "crisis":
        return CRISIS_RESPONSE
    elif intent == "greeting":
        return random.choice(GREETINGS)
    elif intent == "stress":
        return random.choice(STRESS_RESPONSES)
    elif intent == "anxiety":
        return random.choice(ANXIETY_RESPONSES)
    elif intent == "sad":
        return random.choice(SAD_RESPONSES)
    elif intent == "lonely":
        return random.choice(LONELY_RESPONSES)
    elif intent == "angry":
        return random.choice(ANGRY_RESPONSES)
    elif intent == "happy":
        return random.choice(HAPPY_RESPONSES)
    elif intent == "tired":
        return random.choice(TIRED_RESPONSES)
    elif intent == "hopeless":
        return random.choice(HOPELESS_RESPONSES)
    elif intent == "sleep":
        return random.choice(SLEEP_RESPONSES)
    elif intent == "work_study":
        return random.choice(WORK_STUDY_RESPONSES)
    elif intent == "relationship":
        return random.choice(RELATIONSHIP_RESPONSES)
    else:
        if conversation_length > 2 and conversation_length % 3 == 0:
            return random.choice(FOLLOWUP_QUESTIONS)
        return random.choice(GENERIC_EMPATHY)


# ──────────────────────────────────────────────
#  ASSESSMENT GENERATOR
# ──────────────────────────────────────────────

def generate_assessment(messages):
    user_texts = " ".join([m["content"] for m in messages if m["role"] == "user"]).lower()

    negative_signals = ["stress", "anxious", "sad", "depressed", "lonely", "angry",
                        "tired", "hopeless", "overwhelm", "panic", "cry", "helpless",
                        "sleep", "fear", "worried", "hurt", "frustrated", "burnout"]

    positive_signals = ["happy", "good", "okay", "better", "grateful", "fine",
                        "great", "hopeful", "calm", "peaceful", "joy", "excited"]

    neg_count = sum(1 for kw in negative_signals if kw in user_texts)
    pos_count = sum(1 for kw in positive_signals if kw in user_texts)

    base_score = 7
    score = max(2, min(10, base_score + pos_count - neg_count))

    observations = []
    if "stress" in user_texts or "overwhelm" in user_texts:
        observations.append("Signs of elevated stress levels detected.")
    if "anxious" in user_texts or "panic" in user_texts or "worry" in user_texts:
        observations.append("Anxiety-related concerns were expressed.")
    if "sad" in user_texts or "depress" in user_texts or "cry" in user_texts:
        observations.append("Feelings of sadness or low mood were noted.")
    if "lonely" in user_texts or "alone" in user_texts:
        observations.append("Feelings of isolation or loneliness were expressed.")
    if "sleep" in user_texts:
        observations.append("Sleep-related difficulties were mentioned.")
    if "work" in user_texts or "study" in user_texts or "exam" in user_texts:
        observations.append("Work or academic pressure appears to be a concern.")
    if not observations:
        observations.append("No major areas of concern detected in this conversation.")
    if pos_count > 2:
        observations.append("Several positive emotional expressions were noticed.")

    suggestions = []
    if neg_count > pos_count:
        suggestions += [
            "Practice deep breathing or simple meditation for 5-10 minutes daily.",
            "Try journaling your thoughts — it helps process emotions.",
            "Reach out to a trusted friend, family member, or counselor.",
        ]
    else:
        suggestions += [
            "Continue the positive habits and routines that are working for you.",
            "Practice gratitude journaling to reinforce positive feelings.",
            "Stay connected with people who support you.",
        ]
    suggestions.append("Aim for 7-8 hours of sleep and regular physical activity.")

    needs_professional = neg_count >= 3 or "hopeless" in user_texts or "suicide" in user_texts

    obs_text = "\n".join(f"• {o}" for o in observations)
    sug_text = "\n".join(f"• {s}" for s in suggestions)
    prof_text = "Yes — speaking with a licensed mental health professional is recommended." if needs_professional else "Not urgent, but always beneficial if feelings persist or worsen."

    report = f"""EMOTIONAL STATE SCORE: {score}/10

OBSERVATIONS:
{obs_text}

SUGGESTIONS:
{sug_text}

PROFESSIONAL HELP RECOMMENDED:
{prof_text}"""

    return report


# ──────────────────────────────────────────────
#  FLASK ROUTES
# ──────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    user_messages = [m for m in messages if m["role"] == "user"]
    if not user_messages:
        return jsonify({"response": random.choice(GREETINGS), "success": True})

    latest_message = user_messages[-1]["content"]
    intent = detect_intent(latest_message)
    response = get_response(intent, len(user_messages))

    if len(user_messages) > 0 and len(user_messages) % 5 == 0:
        response += "\n\n" + random.choice(CLOSING_POSITIVE)

    return jsonify({"response": response, "success": True})


@app.route("/assess", methods=["POST"])
def assess():
    data = request.json
    messages = data.get("messages", [])

    if len(messages) < 2:
        return jsonify({
            "response": "Please share a bit more about how you're feeling before I generate an assessment.",
            "success": True
        })

    report = generate_assessment(messages)
    return jsonify({"response": report, "success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
