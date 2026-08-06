"""
Customer Support Chatbot
Rule-Based NLP Chatbot using Python
"""

import re
import string
import random
from datetime import datetime

# STEP 1: Intent Dataset (50+ sample queries)

INTENTS = {
    "order_tracking": {
        "keywords": ["order", "track", "shipment", "shipping", "delivery", "package", "parcel", "dispatch", "courier", "shipped"],
        "patterns": [r"where.*order", r"track.*order", r"delivery.*status", r"when.*deliver", r"package.*status"],
        "responses": [
            "To track your order, please visit our website and enter your Order ID in the 'Track Order' section. You'll get real-time updates on your shipment.",
            "Your order can be tracked using the tracking number sent to your email. Visit our tracking page or the courier's website for live updates.",
            "Please share your Order ID and I'll help you check the delivery status. You can also track it at our website under 'My Orders'."
        ]
    },
    "refund_policy": {
        "keywords": ["refund", "return", "money back", "cancel", "cancellation", "exchange", "replacement", "reimburse", "cashback", "want cancel"],
        "patterns": [r"refund.*policy", r"how.*return", r"want.*refund", r"can.*cancel", r"return.*product", r"want.*cancel", r"cancel.*order"],
        "responses": [
            "Our refund policy allows returns within 30 days of purchase. The item must be unused and in original packaging. Refunds are processed within 5-7 business days.",
            "You can request a refund within 30 days of delivery. Simply go to 'My Orders', select the item, and click 'Request Return'. Our team will arrange a pickup.",
            "For refunds: (1) Log in to your account, (2) Go to My Orders, (3) Select the order, (4) Click 'Return/Refund'. You'll receive the refund in 5-7 business days."
        ]
    },
    "login_issues": {
        "keywords": ["login", "password", "sign in", "account", "forgot", "reset", "access", "locked", "username", "credentials", "otp", "verification"],
        "patterns": [r"can.*login", r"forgot.*password", r"reset.*password", r"account.*locked", r"cannot.*sign"],
        "responses": [
            "For login issues, click 'Forgot Password' on the login page and enter your registered email. You'll receive a password reset link within 2 minutes.",
            "If your account is locked, it may be due to multiple failed attempts. Please wait 15 minutes and try again, or use the 'Forgot Password' option.",
            "To reset your password: (1) Go to login page, (2) Click 'Forgot Password', (3) Enter your email, (4) Check your inbox for the reset link."
        ]
    },
    "payment_issues": {
        "keywords": ["payment", "pay", "transaction", "charge", "bill", "invoice", "debit", "credit", "upi", "wallet", "failed", "declined"],
        "patterns": [r"payment.*failed", r"transaction.*failed", r"charge.*wrong", r"double.*charge", r"not.*charged"],
        "responses": [
            "If your payment failed but money was deducted, please don't worry — it will be auto-refunded within 3-5 business days. If not, contact us with your transaction ID.",
            "For payment issues, please share your transaction ID and order number. Common issues are resolved within 24-48 hours by our billing team.",
            "Payment failures can occur due to bank issues or network errors. Please try again with a different payment method, or contact your bank if the amount was debited."
        ]
    },
    "product_inquiry": {
        "keywords": ["product", "item", "price", "cost", "available", "stock", "specification", "feature", "detail", "buy", "purchase", "offer", "discount"],
        "patterns": [r"is.*available", r"price.*of", r"how much", r"product.*detail", r"tell.*about"],
        "responses": [
            "Please search for the product on our website for detailed specifications, pricing, and availability. You can also filter by category to find what you need.",
            "Our product catalog is available on the website with up-to-date pricing and stock information. Would you like me to help you find a specific category?",
            "For product inquiries, visit our website or app. You can compare products, read reviews, and check current offers and discounts in real-time."
        ]
    },
    "complaint": {
        "keywords": ["complaint", "issue", "problem", "damaged", "broken", "wrong", "defective", "poor", "bad", "worst", "terrible", "not working", "faulty", "received"],
        "patterns": [r"received.*wrong", r"product.*damaged", r"damaged.*product", r"not.*working", r"raise.*complaint", r"file.*complaint"],
        "responses": [
            "I'm sorry to hear about this issue! Please raise a complaint by going to 'My Orders' → Select Item → 'Report Issue'. Our team will respond within 24 hours.",
            "We sincerely apologize for the inconvenience. Could you please share your order number and describe the issue? We'll prioritize resolving this for you.",
            "For damaged or wrong products, please take a photo and go to My Orders → Report Issue. We'll arrange a free replacement or full refund within 3-5 business days."
        ]
    },
    "business_hours": {
        "keywords": ["hours", "timing", "time", "open", "close", "working", "available", "support", "contact", "helpline", "call"],
        "patterns": [r"what.*time", r"when.*open", r"support.*hours", r"contact.*number", r"customer.*care"],
        "responses": [
            "Our customer support is available Monday to Saturday, 9 AM to 9 PM. For urgent issues, you can also email support@company.com — we respond within 4 hours.",
            "Support hours: Mon–Sat: 9:00 AM – 9:00 PM | Sunday: 10:00 AM – 6:00 PM. You can also reach us via email or this chatbot 24/7 for basic queries.",
            "We're available for live support from 9 AM to 9 PM on weekdays. Outside these hours, this chatbot can assist you with common queries."
        ]
    },
    "greeting": {
        "keywords": ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "greet", "sup", "howdy"],
        "patterns": [r"^hi$", r"^hello$", r"^hey$"],
        "responses": [
            "Hello! Welcome to Customer Support. I'm here to help you with orders, refunds, payments, and more. What can I assist you with today?",
            "Hi there! How can I help you today? I can assist with order tracking, refunds, login issues, product queries, and more.",
            "Hey! Welcome. I'm your virtual support assistant. Feel free to ask me anything about your orders, account, or products!"
        ]
    },
    "farewell": {
        "keywords": ["bye", "goodbye", "thanks", "thank you", "exit", "quit", "done", "that's all", "no more", "see you"],
        "patterns": [r"bye", r"thank.*you", r"that.*all"],
        "responses": [
            "Thank you for reaching out! Have a wonderful day. Feel free to return if you need any more help.",
            "Goodbye! We hope your issue was resolved. Don't hesitate to reach out again anytime. Take care!",
            "Thanks for contacting support! Your satisfaction matters to us. Have a great day!"
        ]
    }
}

# STEP 2: NLP Preprocessing Functions

STOPWORDS = {
    "is", "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "my", "me", "i", "it", "this", "that", "was",
    "are", "be", "been", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "not",
    "no", "yes", "please", "help", "want", "need", "get", "how", "what",
    "when", "where", "who", "why", "your", "our", "their", "its", "we"
}

def preprocess(text: str) -> list:
    """
    NLP Preprocessing Pipeline:
    1. Lowercase conversion
    2. Punctuation removal
    3. Tokenization (split into words)
    4. Stopword removal
    Returns: list of cleaned tokens
    """
    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Step 3: Tokenization — split into words
    tokens = text.split()

    # Step 4: Remove stopwords
    tokens = [word for word in tokens if word not in STOPWORDS]

    return tokens

# STEP 3: Intent Detection


def detect_intent(user_input: str) -> str:
    """
    Rule-Based Intent Detection:
    - First checks regex patterns (higher priority)
    - Then checks keyword matching
    - Returns best matching intent or 'unknown'
    """
    text_lower = user_input.lower()
    tokens = preprocess(user_input)

    best_intent = "unknown"
    best_score = 0

    for intent_name, intent_data in INTENTS.items():
        score = 0

        # Pattern matching (weight: 3 each)
        for pattern in intent_data["patterns"]:
            if re.search(pattern, text_lower):
                score += 3

        # Keyword matching (weight: 1 each)
        for keyword in intent_data["keywords"]:
            keyword_tokens = keyword.lower().split()
            if any(token in tokens for token in keyword_tokens):
                score += 1
            if keyword in text_lower:
                score += 1

        if score > best_score:
            best_score = score
            best_intent = intent_name

    return best_intent if best_score >= 1 else "unknown"



# STEP 4: Response Mapping

UNKNOWN_RESPONSES = [
    "I'm sorry, I didn't quite understand that. Could you rephrase your question?",
    "I'm not sure about that. Please contact our support team at support@company.com or call 1800-XXX-XXXX.",
    "That query is outside my current knowledge. For complex issues, please chat with a live agent using the 'Connect Agent' button.",
    "Hmm, I couldn't find a match for your query. Try asking about: order tracking, refunds, payments, login issues, or product info."
]

def get_response(intent: str) -> str:
    """Returns a random response from the matched intent's response pool."""
    if intent == "unknown":
        return random.choice(UNKNOWN_RESPONSES)
    return random.choice(INTENTS[intent]["responses"])

# Main Chatbot Engine

class CustomerSupportChatbot:
    def __init__(self):
        self.conversation_history = []
        self.session_start = datetime.now()
        print("\n" + "="*60)
        print("   CUSTOMER SUPPORT CHATBOT")
        print("   Built with Python + NLP")
        print("="*60)
        print("   Type your query below. Type 'exit' to quit.\n")

    def chat(self, user_input: str) -> str:
        """Process one user message and return a response."""
        user_input = user_input.strip()

        if not user_input:
            return "Please type a message so I can help you."

        intent = detect_intent(user_input)
        response = get_response(intent)

        self.conversation_history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "user": user_input,
            "intent": intent,
            "bot": response
        })

        return response

    def get_stats(self) -> dict:
        """Return session statistics."""
        intent_counts = {}
        for entry in self.conversation_history:
            intent = entry["intent"]
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        return {
            "total_messages": len(self.conversation_history),
            "session_duration": str(datetime.now() - self.session_start).split(".")[0],
            "intent_breakdown": intent_counts
        }

    def run(self):
        """Run the chatbot in interactive terminal mode."""
        bot_intro = get_response("greeting")
        print(f"Bot: {bot_intro}\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["exit", "quit", "q"]:
                    print(f"\nBot: {get_response('farewell')}")
                    stats = self.get_stats()
                    print(f"\nSession Stats: {stats['total_messages']} messages | Duration: {stats['session_duration']}")
                    break

                if not user_input:
                    continue

                response = self.chat(user_input)
                intent = self.conversation_history[-1]["intent"]
                print(f"Bot [{intent}]: {response}\n")

            except KeyboardInterrupt:
                print("\n\nBot: Goodbye! Have a great day!")
                break

# Entry Point

if __name__ == "__main__":
    bot = CustomerSupportChatbot()
    bot.run()