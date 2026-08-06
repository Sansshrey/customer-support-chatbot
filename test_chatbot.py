"""
test_chatbot.py — Unit Tests for Customer Support Chatbot
Run with: python test_chatbot.py
"""

import sys
sys.path.insert(0, '.')
from chatbot import preprocess, detect_intent, get_response, INTENTS

test_results = []

def test(name, condition):
    status = "PASS" if condition else "FAIL"
    test_results.append((name, condition))
    print(f"  [{status}]  {name}")


print("\n" + "="*55)
print("  CHATBOT TEST SUITE")
print("="*55)

print("\n--- NLP Preprocessing Tests ---")
tokens_raw = preprocess("ORDER STATUS Check")
test("Lowercase conversion", "order" in tokens_raw)
tokens = preprocess("Where is my order?")
test("Punctuation removal", "?" not in " ".join(tokens))
test("Stopword removal ('my' removed)", "my" not in tokens)
test("Tokenization produces list", isinstance(tokens, list))
test("Meaningful token retained ('order')", "order" in tokens)

print("\n--- Intent Detection Tests ---")
test_cases = [
    ("Where is my order?",                "order_tracking"),
    ("Track my shipment",                  "order_tracking"),
    ("How do I get a refund?",             "refund_policy"),
    ("I want to cancel my order",          "refund_policy"),
    ("I forgot my password",               "login_issues"),
    ("My account is locked",               "login_issues"),
    ("Payment failed but money deducted",  "payment_issues"),
    ("What is the price of this item?",    "product_inquiry"),
    ("I received a damaged product",       "complaint"),
    ("Hi there",                           "greeting"),
    ("Thank you, bye",                     "farewell"),
    ("What are your support hours?",       "business_hours"),
]

for query, expected_intent in test_cases:
    detected = detect_intent(query)
    test(f"'{query[:40]}' -> {expected_intent}", detected == expected_intent)

print("\n--- Response Generation Tests ---")
for intent_name in INTENTS:
    response = get_response(intent_name)
    test(f"Response for '{intent_name}' is non-empty", len(response) > 10)

unknown_resp = get_response("unknown")
test("Unknown intent returns fallback response", len(unknown_resp) > 10)

passed = sum(1 for _, r in test_results if r)
total = len(test_results)
print(f"\n{'='*55}")
print(f"  Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
print(f"{'='*55}\n")
