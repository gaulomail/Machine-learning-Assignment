# GuardAI | Advanced Threat Intelligence System

GuardAI is a high-performance, machine learning-based malware detection platform designed to analyze Portable Executable (PE) headers for malicious indicators. Using a gradient-boosted decision forest (XGBoost), it achieves 99.6% AUC on the Brazilian Malware Dataset.

## 🚀 Quick Start

### One-Command Setup & Run (Recommended)
The easiest way to get started - this single command will set up everything and launch the dashboard:

```bash
chmod +x setup.sh && ./setup.sh
```

**What this does:**
- ✅ Creates Python virtual environment
- ✅ Installs all dependencies
- ✅ Trains the XGBoost model (~30 seconds)
- ✅ Runs automated tests
- 🚀 **Automatically starts the dashboard**

Once complete, open your browser to **`http://localhost:5000`** to access GuardAI.

### Running After Initial Setup
After the first setup, you can quickly restart the application anytime:

```bash
./run.sh
```

This checks for the model and starts the dashboard immediately.

### Manual Setup

#### 1. Prerequisites
- Python 3.9+
- Virtual Environment (recommended)

#### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd new-assignemnt

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Model Training
To train the production model:
```bash
# Full training (Cross-Validation + Multiple Models)
PYTHONPATH=. python src/train_models.py

# Quick training (XGBoost only)
PYTHONPATH=. python src/train_quick.py
```

#### 4. Running the Dashboard
```bash
# Start the Flask application
PYTHONPATH=. python -m src.app
```
Then visit `http://localhost:5000` in your browser.

## 🛠 Features

- **Heuristic Intelligence Console**: Persistent on-page terminal showing real-time analysis steps.
- **XGBoost Inference Engine**: Optimized for high-precision malware classification.
- **Batch Intelligence Hub**: Secure drag-and-drop CSV upload for cluster analysis with forensic reporting (Export to CSV).
- **Premium UI/UX**: Immersion through dark mode, glassmorphism, mouse-parallax effects, and responsive design.

## 🧪 Testing
Run the automated test suite to verify backend and model integrity:
```bash
pytest tests/
```

## 📊 Evaluation Results
| Metric | Value |
| --- | --- |
| Accuracy | 98.31% |
| AUC | 0.9965 |
| Precision | 97.4% |
| Recall | 99.1% |

---
*Developed for the Advanced Malware Analysis Course.*
