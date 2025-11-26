# Buyvia Voice API

Voice command processing API powered by **Google Speech Recognition** with Ghanaian accent support.

## Features

- **Google Speech Recognition** - Primary speech-to-text engine
- **Ghanaian Accent Normalization** - 200+ accent mappings for local speech patterns
- **Command Parsing** - 100+ voice commands (navigation, search, cart, checkout)
- **FastAPI Backend** - Fast, async Python API
- **Real-time Processing** - Transcription + intent parsing in one request

## Deploy to Render

### Step 1: Push to GitHub

Create a new GitHub repository and push the `voice-api` folder:

```bash
cd voice-api
git init
git add .
git commit -m "Initial commit - Buyvia Voice API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/buyvia-voice-api.git
git push -u origin main
```

### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com) and sign in
2. Click **New +** → **Web Service**
3. Connect your GitHub account and select the `buyvia-voice-api` repository
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `buyvia-voice-api` |
| **Region** | Choose closest to Ghana (e.g., Frankfurt) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free (or Starter for production) |

5. Click **Create Web Service**

### Step 3: Wait for Deployment

Render will automatically:
- Install Python dependencies
- Start the FastAPI server
- Provide you with a URL like `https://buyvia-voice-api.onrender.com`

### Step 4: Update React Native App

Add the Render URL to your Buyvia app's `.env` file:

```
EXPO_PUBLIC_VOICE_API_URL=https://buyvia-voice-api.onrender.com
```

### Step 5: Test the API

Visit `https://buyvia-voice-api.onrender.com/health` in your browser. You should see:

```json
{"status": "healthy", "service": "buyvia-voice-api"}
```

## Local Development (Optional)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8000
```

## API Endpoints

### `GET /`
API information and available endpoints.

### `GET /health`
Health check endpoint.

### `POST /transcribe`
Transcribe audio file to text and parse command.

**Request**: Multipart form with audio file
**Response**:
```json
{
  "success": true,
  "raw_text": "serch fo snekas",
  "normalized_text": "search for sneakers",
  "command": {
    "type": "search_product",
    "params": {"query": "sneakers"},
    "confidence": 0.9
  }
}
```

### `POST /parse`
Parse text directly to command.

**Request**:
```json
{
  "text": "add to cart"
}
```

### `GET /commands`
List all available voice commands with examples.

### `GET /accent-map`
Get the full Ghanaian accent mapping dictionary.

## Voice Commands

### Navigation (20+)
- "go home", "open cart", "my profile", "show orders"

### Search (30+)
- "search for phones", "find sneakers", "show electronics category"

### Cart (25+)
- "add to cart", "remove from cart", "increase quantity", "clear cart"

### Checkout (15+)
- "checkout", "pay with mobile money", "pay with card"

### Wishlist (10+)
- "add to wishlist", "save for later", "move to cart"

## Accent Mappings

The API includes 200+ Ghanaian English accent mappings:

| Ghanaian | Standard |
|----------|----------|
| "cut" | "cart" |
| "snekas" | "sneakers" |
| "fone" | "phone" |
| "dis" | "this" |
| "fo" | "for" |

## License

MIT License - Buyvia Project
