# 🚀 CareCall Quick Start Guide

## Day 1: Get Up and Running (30 minutes)

### Step 1: Get Your API Keys ✅

**Deepgram ($200 free credits!):**
1. Go to: https://console.deepgram.com/signup
2. Sign up for free account
3. Copy your API key from the console
4. You get $200 in credits = 40+ hours of voice agent time!

**OpenAI (optional but recommended):**
1. Go to: https://platform.openai.com/signup
2. Get API key
3. Needed for smart conversation handling

### Step 2: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

### Step 4: Test Deepgram Connection

```bash
# Run the test script
python test_deepgram.py
```

If you see "✅ Deepgram API connected!" - you're ready to build!

### Step 5: Run the Demo

```bash
# Start the backend server
uvicorn src.main:app --reload

# In another terminal, open the demo page
open http://localhost:8000/demo
```

## Next Steps

- [ ] Register for DeveloperWeek hackathon on Devpost
- [ ] Get Deepgram API key
- [ ] Get OpenAI API key (optional)
- [ ] Run test_deepgram.py successfully
- [ ] Start building core features!

## Resources

- [Deepgram Voice Agent Docs](https://developers.deepgram.com/docs/voice-agent)
- [Deepgram Node Starter](https://github.com/deepgram-starters/node-voice-agent)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Need Help?

Check the main README.md or ask questions in the project!

---

**Current Status:** Setting up development environment
**Next:** Test Deepgram API connection
