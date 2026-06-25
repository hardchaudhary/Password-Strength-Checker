import re
import math

COMMON_PASSWORDS = [
    "password", "123456", "12345678",
    "qwerty", "admin", "welcome",
    "password123", "abc123"
]

def calculate_entropy(password):
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"[0-9]", password):
        charset += 10

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

def has_sequence(password):
    sequences = [
        "123456789",
        "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiop"
    ]

    password = password.lower()

    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in password:
                return True

    return False

def analyze_password(password):

    score = 0
    suggestions = []

    if len(password) >= 12:
        score += 20
    else:
        suggestions.append("Use at least 12 characters")

    if re.search(r"[A-Z]", password):
        score += 15
    else:
        suggestions.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 15
    else:
        suggestions.append("Add lowercase letters")

    if re.search(r"\d", password):
        score += 15
    else:
        suggestions.append("Add numbers")

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        score += 20
    else:
        suggestions.append("Add special characters")

    if password.lower() in COMMON_PASSWORDS:
        score -= 40
        suggestions.append("Avoid common passwords")

    if re.search(r"(.)\1\1", password):
        score -= 10
        suggestions.append("Avoid repeated characters")

    if has_sequence(password):
        score -= 15
        suggestions.append("Avoid sequential patterns")

    score = max(0, min(score, 100))

    entropy = calculate_entropy(password)

    if score < 40:
        strength = "Weak"
    elif score < 70:
        strength = "Medium"
    elif score < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "strength": strength,
        "score": score,
        "entropy": entropy,
        "suggestions": suggestions
    }

password = input("Enter Password: ")

result = analyze_password(password)

print("\n===== PASSWORD SECURITY REPORT =====")
print("Password Strength :", result["strength"])
print("Security Score    :", result["score"], "/100")
print("Entropy           :", result["entropy"], "bits")

if result["suggestions"]:
    print("\nSuggestions:")
    for item in result["suggestions"]:
        print("-", item)

print("====================================")