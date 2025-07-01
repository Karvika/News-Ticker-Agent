# AI News Ticker Agent

A modern web-based AI news ticker that fetches the latest artificial intelligence news using Google's Agent Development Kit (ADK) and displays them in a beautiful, real-time interface.

## 🌟 Features

- **Real-time AI News**: Fetches current AI news using Google Search through ADK agents
- **Modern UI**: Beautiful, responsive news ticker interface
- **Auto-refresh**: Automatically updates every 5 minutes
- **Manual Refresh**: One-click refresh without page reload
- **Chronological Order**: Displays 5 latest articles sorted by publication date
- **Detailed Articles**: Each article includes date, source, headline, and description
- **Mock Mode**: Fallback demo mode when API key is not available

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API Key for Gemini
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Karvika/News-Ticker-Agent.git
   cd News-Ticker-Agent
   ```

2. **Run the setup script**
   ```bash
   # On Windows
   setup.bat
   
   # Or manually:
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   - Create a `.env` file in the `greeting_agent/` directory
   - Add your Google API key:
     ```
     GOOGLE_GENAI_USE_VERTEXAI=FALSE
     GOOGLE_API_KEY=your_api_key_here
     ```
   - Get your API key from: https://aistudio.google.com/app/apikey

4. **Run the application**
   ```bash
   # On Windows
   run.bat
   
   # Or manually:
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── setup.bat             # Windows setup script
├── run.bat               # Windows run script
├── templates/
│   └── index.html        # Frontend news ticker interface
├── greeting_agent/
│   ├── agent.py          # ADK agent configuration
│   └── .env              # Environment variables (API key)
└── README.md             # This file
```

## 🔧 How It Works

### Backend (Flask)
- **`app.py`**: Main Flask server with `/api/news` and `/api/refresh` endpoints
- **Agent Integration**: Uses ADK agents to fetch real AI news
- **Mock Mode**: Provides demo data when API key is missing

### AI Agent System
- **Search Specialist**: Uses Google Search to find current AI news
- **Formatter Agent**: Formats articles into consistent structure
- **Root Agent**: Orchestrates the news fetching process

### Frontend
- **Modern UI**: Responsive design with news cards
- **Auto-refresh**: Updates every 5 minutes automatically
- **Manual Refresh**: Click button for immediate updates
- **Real-time Display**: Shows 5 most recent articles

## 🎯 Features in Detail

### News Format
Each news article displays:
- **Date**: Actual publication date
- **Source**: News publication name
- **Headline**: Full article headline
- **Description**: 2-3 sentence summary

### Refresh Modes
- **Initial Load**: Shows loading overlay
- **Manual Refresh**: Silent update without loading screen
- **Auto Refresh**: Background updates every 5 minutes

## 🛠️ Configuration

### Environment Variables
Create `greeting_agent/.env`:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_google_api_key
```

### Agent Configuration
The system uses three specialized agents:
1. **Search Specialist**: Finds recent AI news using Google Search
2. **Formatter Agent**: Structures articles consistently
3. **Root Agent**: Coordinates the entire process

## 🌐 API Endpoints

- `GET /` - Main news ticker interface
- `GET /api/news` - Fetch latest AI news (JSON)
- `POST /api/refresh` - Manual refresh endpoint

## 📱 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🔒 Security

- API keys stored in environment variables
- No sensitive data in frontend
- CORS enabled for development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with Google's Agent Development Kit (ADK)
- Uses Google Search for news retrieval
- Modern UI inspired by contemporary news platforms

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the console logs for debugging
- Ensure your API key is properly configured

---

**Made with ❤️ for staying updated with the latest in AI**
