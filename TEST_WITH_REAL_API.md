# 🎤 Testing CareCall with Real Deepgram API

## ✅ Prerequisites

You said you have a Deepgram API key! Let's use it!

## 📝 Step 1: Add Your API Key

Edit the `.env` file:

```bash
nano .env
```

Replace `your_deepgram_key_here` with your actual key:

```
DEEPGRAM_API_KEY=your_actual_key_from_deepgram
```

Save and exit (Ctrl+X, then Y, then Enter)

## 🧪 Step 2: Test Deepgram Connection

```bash
source venv/bin/activate
python test_deepgram.py
```

**Expected output:**
```
✅ SUCCESS! Deepgram API is working!
📝 Test transcription: 'Yeah, as much as it pains me to say it, the guy...'
🎉 You're ready to build CareCall!
```

## 🎤 Step 3: Test with Real Voice (Coming Soon)

Once we confirm your API key works, I'll build a live voice test where you can:
- Speak into your microphone
- CareCall responds in real-time
- Test all commands with actual voice!

## 🐛 Troubleshooting

### Error: "Invalid API key"
- Double-check your key in .env
- Make sure there are no extra spaces
- Key should start with something like `sk-` or similar format

### Error: "No audio input device"
- Make sure you have a microphone
- Grant microphone permissions if prompted
- Check system audio settings

### Error: "Module not found"
- Run: `pip install -r requirements-minimal.txt`
- Make sure venv is activated: `source venv/bin/activate`

## 🎯 What to Test

Once live:

1. **Medication Commands**
   - "Did I take my medicine?"
   - "I just took my blood pressure pill"
   - "Remind me about my medications"

2. **Calling Commands**
   - "Call Sarah"
   - "Call my daughter"
   - "Call Dr. Johnson"

3. **Information**
   - "What time is it?"
   - "What's the weather?"

4. **Emergency (be careful, will trigger alerts!)**
   - "Help, I fell!"
   - "I'm having chest pain"

## 📊 Success Criteria

✅ Deepgram API connects
✅ Voice transcription works
✅ Commands are recognized
✅ Responses are natural
✅ Emergencies are detected
✅ Contacts are alerted (in demo mode)

---

**Ready? Let's test your API key!** 🚀
