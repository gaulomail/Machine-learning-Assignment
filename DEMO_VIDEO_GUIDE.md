# Demo Video Script & Recording Guide

## 🎬 Demo Video Requirements

**Duration:** 5-10 minutes  
**Format:** Screen-share recording  
**Content:** Web application demo + CI/CD pipeline explanation  
**Note:** No need to show ID or personal information

---

## 📋 Pre-Recording Checklist

### Technical Setup
- [ ] Application deployed to public URL (Render/Railway/Fly.io)
- [ ] Test deployment URL works
- [ ] Prepare browser tabs:
  - Tab 1: Deployed application
  - Tab 2: GitHub repository (Actions tab)
  - Tab 3: Local terminal (optional for pytest demo)
- [ ] Close unnecessary browser tabs and applications
- [ ] Set browser zoom to 100%
- [ ] Clear browser history/bookmarks bar (optional for privacy)

### Recording Tools
- [ ] **Recommended:** Loom (loom.com) - Free, easy to use
- [ ] **Alternative:** OBS Studio - More control
- [ ] **Alternative:** Zoom - Record local meeting
- [ ] Test microphone audio quality
- [ ] Test screen recording quality (1080p recommended)

### Content Preparation
- [ ] Have `sample_test.csv` ready for upload
- [ ] Know location of "Seed Malware" and "Seed Goodware" buttons
- [ ] Identify a recent GitHub Actions workflow run to show
- [ ] Practice timing (aim for 7-8 minutes)

---

## 🎯 Demo Script (7-8 minutes)

### **Introduction (30 seconds)**

> "Hello, I'm [Name], and today I'm demonstrating GuardAI - an advanced malware detection system that uses machine learning to analyze PE header features from Windows executables. Our system achieves 99.65% AUC using an XGBoost classifier trained on the Brazilian Malware Dataset."

**Screen:** Show deployed application homepage

---

### **Section 1: Web Application Demo (3-4 minutes)**

#### Part A: Manual Prediction - Malware (1 minute)

> "Let me demonstrate the manual prediction feature. I'll click 'Seed Malware' to populate the input field with a known malicious sample."

**Actions:**
1. Click "Seed Malware" button
2. Briefly show the populated features (22 PE header values)
3. Click "Analyze Threat"

> "Notice the integrated heuristic console appears, showing real-time analysis steps: data extraction, normalization, feature encoding, XGBoost inference, and threat evaluation."

**Actions:**
4. Point to the console showing step-by-step progress
5. Wait for result to appear

> "The system correctly identifies this as a CRITICAL THREAT with 99.8% confidence. The result is also automatically added to the scan history in the sidebar."

**Actions:**
6. Point to the "CRITICAL THREAT" result
7. Point to the scan history entry

#### Part B: Manual Prediction - Goodware (1 minute)

> "Now let's test with a clean file. I'll click 'Seed Goodware'."

**Actions:**
1. Click "Seed Goodware" button
2. Click "Analyze Threat"
3. Show the console processing

> "The system correctly identifies this as SIGNATURE SECURE with high confidence. Both predictions are now visible in the scan history."

**Actions:**
4. Point to the "SIGNATURE SECURE" result
5. Show both entries in scan history

#### Part C: Batch Upload (1-2 minutes)

> "For security analysts processing multiple files, we have a batch intelligence hub. I'll upload a CSV file containing multiple samples."

**Actions:**
1. Scroll down to "Batch Intelligence Hub"
2. Click the drop zone or "Upload Manifest"
3. Select `sample_test.csv`

> "The system processes the entire batch, showing a progress indicator. Once complete, we see a summary: X threats found and Y verified safe."

**Actions:**
4. Wait for processing to complete
5. Point to the summary cards (threats/safe counts)
6. Scroll through the results list

> "Analysts can export these results as a forensic report in CSV format for further analysis."

**Actions:**
7. Click "Export Forensic Report"
8. Show the downloaded file (optional)

---

### **Section 2: CI/CD Pipeline & Testing (2-3 minutes)**

> "Now let me show you our automated testing and deployment pipeline. I'll navigate to our GitHub repository."

**Actions:**
1. Switch to GitHub repository tab
2. Navigate to "Actions" tab

#### Part A: GitHub Actions Workflow (1.5 minutes)

> "We have a GitHub Actions workflow that runs on every push and pull request. Let me show you a recent run."

**Actions:**
1. Click on the most recent workflow run (should be green ✓)
2. Show the workflow steps

> "The workflow performs several steps: sets up Python, installs dependencies, and runs our test suite. Let me expand the test results."

**Actions:**
3. Click on the "Run tests" step
4. Show pytest output with 6 tests passing

> "All 6 tests passed in under 3 seconds. These include unit tests for data processing and integration tests for our API endpoints."

#### Part B: Test Coverage Explanation (1 minute)

> "Our test suite covers:
> - Data preprocessing and label identification
> - Model loading and metadata handling
> - API health checks
> - Manual prediction flow
> - File upload functionality
>
> The deployment only proceeds if all tests pass, ensuring code quality."

**Actions:**
- Point to the green checkmarks
- Show the deployment step (if visible)

#### Part C: Reproducibility (30 seconds)

> "For reproducibility, we provide a one-command setup script. Running `./setup.sh` creates the environment, installs dependencies, trains the model, runs tests, and starts the application automatically."

**Actions:**
- Optionally show `setup.sh` file in repository
- Or show README.md with setup instructions

---

### **Conclusion (30 seconds)**

> "To summarize, GuardAI provides:
> - 99.65% AUC malware detection using XGBoost
> - A production-ready web interface with real-time analysis
> - Comprehensive automated testing with CI/CD
> - Full reproducibility with one-command setup
>
> Thank you for watching. The application is live at [your-deployment-url] and the code is available on GitHub."

**Screen:** Show the deployed application one final time

---

## 🎥 Recording Tips

### Do's ✅
- **Speak clearly** at a moderate pace
- **Highlight key metrics** (99.65% AUC, 6 tests passing)
- **Show actual functionality** - don't just describe it
- **Keep transitions smooth** between sections
- **Mention the deployment URL** at the end

### Don'ts ❌
- Don't show personal information or IDs
- Don't apologize for minor UI glitches
- Don't spend too long on any single section
- Don't read directly from a script (sound natural)
- Don't go over 10 minutes

### Technical Quality
- **Resolution:** 1920x1080 (Full HD)
- **Audio:** Clear, minimal background noise
- **Cursor:** Make cursor movements deliberate and visible
- **Pace:** Not too fast - viewers need time to see what you're showing

---

## 📤 After Recording

### 1. Review the Video
- Watch the entire video
- Check audio quality
- Verify all key points were covered
- Ensure timing is 5-10 minutes

### 2. Upload
- **Recommended:** Upload to YouTube (unlisted)
- **Alternative:** Upload to Loom
- **Alternative:** Upload to Google Drive (public link)

### 3. Include in Submission
- Add video URL to submission package
- Verify link is accessible (test in incognito mode)

---

## 🔄 Backup Plan

If something goes wrong during recording:

**Plan A:** Re-record the section that failed  
**Plan B:** Have screenshots ready as backup  
**Plan C:** Use localhost if deployment fails (explain deployment would be next step)

---

## ⏱️ Time Breakdown

| Section | Time | Key Points |
|---------|------|------------|
| Introduction | 30s | Project overview, 99.65% AUC |
| Manual Prediction (Malware) | 1m | Seed, analyze, show result |
| Manual Prediction (Goodware) | 1m | Seed, analyze, show result |
| Batch Upload | 1-2m | Upload CSV, show results, export |
| GitHub Actions | 1.5m | Show workflow, test results |
| Test Coverage | 1m | Explain test types |
| Reproducibility | 30s | Mention setup.sh |
| Conclusion | 30s | Summary, URLs |
| **Total** | **7-8m** | |

---

## 📝 Sample Opening Lines

**Option 1 (Technical):**
> "This is GuardAI, a machine learning-based malware detection system achieving 99.65% AUC by analyzing 22 PE header features using XGBoost."

**Option 2 (Problem-Focused):**
> "Malware detection is critical for cybersecurity. GuardAI uses machine learning to identify malicious Windows executables with 99.65% accuracy."

**Option 3 (Demo-Focused):**
> "Today I'm demonstrating a production-ready malware detection system with a premium web interface, automated testing, and CI/CD pipeline."

---

Good luck with your recording! 🎬
