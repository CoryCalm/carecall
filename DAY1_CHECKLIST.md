# 📋 Day 1 Checklist - Get CareCall Running!

## ✅ What We've Done So Far:

- [x] Created project structure
- [x] Set up FastAPI backend skeleton
- [x] Created requirements.txt with all dependencies
- [x] Built test script for Deepgram API
- [x] Created demo webpage
- [x] Set up environment configuration
- [x] Created documentation

## 🎯 YOUR IMMEDIATE ACTION ITEMS:

### 1. Register for Hackathon (5 minutes)
- [ ] Go to: https://developerweek-2026-hackathon.devpost.com/
- [ ] Click "Register for this hackathon"
- [ ] Create/login to Devpost account
- [ ] Complete registration

### 2. Get Deepgram API Key (5 minutes)
- [ ] Go to: https://console.deepgram.com/signup
- [ ] Sign up for free account
- [ ] Navigate to API Keys section
- [ ] Copy your API key
- [ ] **You get $200 in FREE credits!** (40+ hours of voice time)

### 3. Run Setup (5 minutes)
```bash
# In the carecall directory
cd /Volumes/LaCie/grove/carecall

# Run the setup script
./SETUP.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure Environment (2 minutes)
```bash
# Copy example env
cp .env.example .env

# Edit the .env file and add your Deepgram API key
nano .env  # or use your favorite editor

# Add this line:
DEEPGRAM_API_KEY=your_actual_key_here
```

### 5. Test Deepgram Connection (2 minutes)
```bash
# Make sure venv is activated
source venv/bin/activate

# Run the test script
python test_deepgram.py
```

**Expected output:** "✅ SUCCESS! Deepgram API is working!"

### 6. Start the Server (1 minute)
```bash
# Start FastAPI backend
uvicorn src.main:app --reload
```

### 7. View Demo (1 minute)
- [ ] Open browser to: http://localhost:8000
- [ ] Check API status
- [ ] Open demo page: http://localhost:8000/demo
- [ ] Celebrate! 🎉

## 🎉 Once Everything Works:

You should see:
- ✅ FastAPI server running on port 8000
- ✅ Deepgram API test passes
- ✅ Demo page loads and looks good
- ✅ Ready to build voice features!

## 📊 Progress Check:

**Time invested:** ~30 minutes
**Time remaining:** 9.5 days
**Status:** Foundation complete, ready to build features!

## 🚀 What's Next (Day 2):

Tomorrow we'll build:
1. Basic voice agent with Deepgram Voice Agent API
2. Command parsing ("Hey CareCall...")
3. First real feature: Medication reminder
4. Test end-to-end voice interaction

## 💡 Tips:

- **Stuck on setup?** Just message me and I'll help!
- **Missing dependencies?** Run `./SETUP.sh` again
- **Deepgram not working?** Double-check API key in .env
- **Port already in use?** Change PORT in .env or kill the process

## 🆘 Quick Troubleshooting:

**"Module not found" errors:**
```bash
source venv/bin/activate  # Make sure venv is active!
pip install -r requirements.txt
```

**"Connection refused" to Deepgram:**
- Check internet connection
- Verify API key is correct in .env
- Make sure you have credits in Deepgram account

**FastAPI won't start:**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
uvicorn src.main:app --reload --port 8001
```

---

## 📞 Ready to Continue?

Once you've completed this checklist, you'll have:
- ✅ A working FastAPI backend
- ✅ Deepgram API access and tested
- ✅ Development environment ready
- ✅ Foundation to build CareCall!

**Let's build something that helps people! 💙**

---

**Current Status:** Day 1 - Setup Phase
**Next:** Day 2 - Build Voice Agent Core
**Deadline:** Feb 20, 10 AM PST (9 days from now)
