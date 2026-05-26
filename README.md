import pandas as pd
import re
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression

# =========================
# LOAD DATASET (SAFE)
# =========================

try:
    data = pd.read_csv("emails.csv")
    print("✅ Real dataset loaded")

    # Detect column names automatically
    if 'text' in data.columns:
        text_col = 'text'
    elif 'email' in data.columns:
        text_col = 'email'
    elif 'message' in data.columns:
        text_col = 'message'
    else:
        raise Exception("No text column found")

    if 'label' in data.columns:
        label_col = 'label'
    elif 'class' in data.columns:
        label_col = 'class'
    else:
        raise Exception("No label column found")

    # Normalize labels
    data[label_col] = data[label_col].astype(str).str.lower()
    data[label_col] = data[label_col].map({
        'phishing': 1, 'spam': 1, 'malicious': 1,
        'safe': 0, 'legitimate': 0, 'ham': 0
    })

    data = data.dropna()

except:
    print("⚠️ emails.csv not found → using built-in dataset")

    data = pd.DataFrame({
        'text': [
            "Win money now click http://fake.com",
            "Congratulations you won a lottery",
            "Urgent update your bank account",
            "Free offer limited time click now",
            "Click here to claim your prize",
            "Earn money fast from home",
            "Verify your account immediately",
            "Reset your password now",

            "Meeting at 5pm",
            "Project discussion tomorrow",
            "Let's have lunch",
            "Submit your assignment",
            "Team meeting scheduled",
            "Your order has been shipped",
            "Dinner plan tonight",
            "See you at college"
        ],
        'label': [1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0]
    })

    text_col = 'text'
    label_col = 'label'

# =========================
# FEATURE ENGINEERING
# =========================

def extract_features(text):
    text = str(text)

    url_count = len(re.findall(r'http[s]?://', text))
    suspicious_words = len(re.findall(r'win|free|money|urgent|click|offer|verify|password', text.lower()))
    special_chars = len(re.findall(r'[!$#@]', text))
    length = len(text)

    return url_count, suspicious_words, special_chars, length

features = data[text_col].apply(lambda x: pd.Series(extract_features(x)))
features.columns = ['url_count', 'suspicious_words', 'special_chars', 'length']

# =========================
# TEXT PROCESSING
# =========================

vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=3000)
X_text = vectorizer.fit_transform(data[text_col])

# Combine features
X = np.hstack((X_text.toarray(), features.values))
y = data[label_col]

# =========================
# TRAIN MODEL
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================

y_pred = model.predict(X_test)

print("\n✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# =========================
# TEST EMAIL FUNCTION
# =========================

def predict_email(email_text):
    f = extract_features(email_text)
    f = np.array(f).reshape(1, -1)

    text_vec = vectorizer.transform([email_text]).toarray()
    final_input = np.hstack((text_vec, f))

    prediction = model.predict(final_input)[0]

    return "🚨 Phishing Email" if prediction == 1 else "✅ Safe Email"

# =========================
# SAMPLE TEST
# =========================

sample = "Your account is compromised! Click here to reset password"
print("\nTest Result:", predict_email(sample))
