# FlawHunt CLI

**The smart CLI for cybersecurity professionals and ethical hackers**

FlawHunt CLI is an AI-powered terminal assistant that transforms natural language into safe, effective cybersecurity operations. Built with security-first principles, it provides three specialized modes for different use cases while maintaining comprehensive safety controls.

## 🎯 Quick Summary

- **🤖 SAGE Mode**: Direct cybersecurity knowledge and guidance without tools
- **⚒️ FORGE Mode**: Command generation with confirmation for precise operations  
- **🎯 HUNTER Mode**: Full AI agent with advanced tools for complete tactical operations
- **🔒 Security-First**: Safe by default with dangerous command blocking
- **🧠 Smart Memory**: Conversation history with semantic search and context awareness
- **🎨 Customizable**: Multiple themes, verbose controls, and personalization options

## ⚡ Quick Start

1. **Download** the zip file for your platform:
   - **macOS**: [flawhunt-cli-macos.zip](https://github.com/gamkers/FlawHunt_CLI/releases/download/v1.1/flawhunt-cli-macos.zip)
   - **Linux**: [flawhunt-cli-linux.zip](https://github.com/gamkers/FlawHunt_CLI/releases/download/v1.1/flawhunt-cli-linux.zip)
   - **Windows & Android**: Coming soon!
2. **Extract** the zip file: `unzip flawhunt-cli-[platform].zip`
3. **Get API Keys**: Groq API key (recommended) or Google Gemini API key
4. **Get License**: FlawHunt license key for full features
5. **Run**: `./flawhunt` and follow the setup wizard
6. **Start Hacking**: Choose your mode and begin your cybersecurity operations!

## 🚀 Key Features

### 🛡️ Security & Safety
- **Safe by Default**: Automatically blocks dangerous commands and requires confirmation
- **Security Patterns**: Built-in detection of potentially harmful operations
- **Ethical Focus**: Designed for defensive security and ethical hacking practices
- **Command Validation**: All shell operations are security-checked before execution

### 🤖 Three Operating Modes

#### 1. 🤖 SAGE Mode (Ask Mode)
Your cybersecurity study buddy for direct knowledge and guidance.
- Pure knowledge responses without tool execution
- Perfect for learning concepts, theory, and best practices
- Fast answers to security questions and explanations

#### 2. ⚒️ FORGE Mode (Generate Mode)  
The command craftsman for precision-crafted tools.
- Generates commands with detailed explanations
- Requires user confirmation before execution
- Perfect for learning command syntax and understanding operations

#### 3. 🎯 HUNTER Mode (Agent Mode)
Elite operative with full tool access for complete operations.
- Advanced AI agent with comprehensive tool suite
- Autonomous execution with safety controls
- Complete cybersecurity workflow automation

### 🧠 Intelligent Memory System
- **Conversation History**: Persistent memory across sessions with metadata
- **Semantic Search**: Find past conversations by meaning and context
- **Session Management**: Organize conversations by topics or projects
- **Context Awareness**: AI remembers and builds on previous discussions
- **Vector Storage**: Advanced similarity matching for relevant context injection

### 🛠️ Comprehensive Tool Suite
- **Shell Operations**: Safe command execution with explanations
- **File Management**: Read, write, and navigate filesystem operations
- **Git Integration**: Version control operations and workflow automation
- **Docker Support**: Container management and deployment operations
- **Package Management**: Multi-platform package installation and management
- **Cybersecurity Tools**: Automated installation and usage of security tools
- **Environment Setup**: Complete development environment configuration
- **Script Generation**: Custom script creation for specific tasks

### 🎨 Customization & Themes
- **Multiple Themes**: Professional, hacker, minimal, and custom themes
- **Verbose Control**: Toggle between detailed reasoning and clean output
- **Animation Effects**: Matrix rain, glitch effects, and terminal animations
- **Progress Tracking**: Visual progress bars and status indicators
- **Personalization**: Configurable prompts, colors, and interface elements

### 📊 Advanced Features
- **Backup & Sync**: Cloud backup of conversation history across devices
- **Statistics**: Detailed usage analytics and security metrics
- **Learning Mode**: Built-in cybersecurity tool education and tutorials
- **Auto-completion**: Intelligent command and path completion
- **File Monitoring**: Real-time filesystem change detection
- **Cross-Platform**: Full support for Windows, macOS, and Linux

## 📦 Installation

### 🚀 Quick Install (Recommended)

**No Python installation required!** Download the pre-built binary for your platform:

#### macOS ✅
```bash
# Download and extract FlawHunt CLI for macOS
curl -L -o flawhunt-cli-macos.zip https://github.com/gamkers/FlawHunt_CLI/releases/download/v1.1/flawhunt-cli-macos.zip
unzip flawhunt-cli-macos.zip
chmod +x flawhunt
# Run: ./flawhunt
```

#### Linux ✅
```bash
# Download and extract FlawHunt CLI for Linux
curl -L -o flawhunt-cli-linux.zip https://github.com/gamkers/FlawHunt_CLI/releases/download/v1.1/flawhunt-cli-linux.zip
unzip flawhunt-cli-linux.zip
chmod +x flawhunt
# Run: ./flawhunt
```

#### Windows 🔄
```bash
# Coming Soon!
# Windows binary is currently being prepared and will be available shortly
```

#### Android (Termux) 🔄
```bash
# Coming Soon!
# Android binary is currently being prepared and will be available shortly
```

### 📋 Requirements
You only need:
- **Groq API Key** (primary, recommended) OR **Google Gemini API Key** (alternative)
- **FlawHunt License Key** (for full features)

### 🛠️ Advanced: Install from Source
For developers who want to modify the code:
```bash
git clone https://github.com/gamkers/GAMKERS_CLI.git
cd GAMKERS_CLI
pip install -r requirements.txt
pip install -e .
```

## 🔧 Configuration

### 🔑 API Keys Setup
Set up your API keys using environment variables or during first run:

```bash
# Primary provider (recommended)
export GROQ_API_KEY=your_groq_key_here

# Alternative provider
export GOOGLE_API_KEY=your_gemini_key_here

# FlawHunt license key
export FLAWHUNT_KEY=your_flawhunt_key_here
```

### 🚀 First Run
After downloading and extracting the zip file:

```bash
# Windows
./flawhunt.exe

# macOS/Linux/Android
./flawhunt
```

The application will guide you through:
1. API key configuration (if not set via environment variables)
2. FlawHunt license key setup
3. Initial mode selection and preferences

## 💡 Usage Examples

### Basic Operations
```bash
# Start FlawHunt CLI
./flawhunt  # (or ./flawhunt.exe on Windows)

# Select mode (1=SAGE, 2=FORGE, 3=HUNTER)
Mode choice: 3

# Natural language commands
> scan this network for open ports
> install nmap and show me how to use it
> what are the best tools for web application testing?
> create a python script to parse log files
> explain what this command does: nmap -sS -O target
```

### Mode Switching
```bash
# Switch between modes anytime
:mode sage     # Switch to SAGE mode
:mode forge    # Switch to FORGE mode  
:mode hunter   # Switch to HUNTER mode
```

### Meta Commands
```bash
# System controls
:help          # Show all available commands
:safe on/off   # Toggle safety mode
:verbose on/off # Toggle detailed output
:clear         # Clear screen
:quit          # Exit application

# Customization
:theme         # Show available themes
:theme hacker  # Switch to hacker theme
:animation matrix # Run matrix animation

# Memory & History
:history       # Show recent conversations
:history search nmap # Search for nmap-related conversations
:session new "Web Testing" # Create new conversation session
:backup        # Create cloud backup

# Learning & Tools
:learn nmap    # Learn about nmap tool
:packages      # Show available security tools
:stats         # Show usage statistics
```

### Advanced Workflows
```bash
# Cybersecurity reconnaissance workflow
> install and configure nmap for network discovery
> scan 192.168.1.0/24 for live hosts
> perform service detection on discovered hosts
> generate a report of findings

# Web application testing
> set up burp suite for web app testing
> install and configure sqlmap
> test this URL for SQL injection: http://example.com/page?id=1
> document findings in a structured report

# Environment setup
> set up a complete penetration testing environment
> install all essential cybersecurity tools
> configure my development environment for security research
```

## 🎨 Themes & Customization

### Available Themes
- **Professional**: Clean, business-appropriate interface
- **Hacker**: Green-on-black terminal aesthetic  
- **Minimal**: Simplified, distraction-free design
- **Custom**: User-defined color schemes and layouts

### Verbose Mode Control
```bash
:verbose off   # Clean, direct answers
:verbose on    # Detailed reasoning and steps
```

### Animation Effects
```bash
:animation matrix           # Matrix digital rain
:animation glitch <text>    # Glitch text effect
:animation typewriter <text> # Typewriter effect
:animation scan            # Network scan simulation
```

## 🔒 Security Features

### Built-in Safety Controls
- Dangerous command pattern detection
- Confirmation prompts for destructive operations
- Safe mode toggle for additional protection
- Command explanation before execution

### Ethical Guidelines
- Designed for defensive security practices
- Educational focus on cybersecurity learning
- No offensive capabilities or attack tools
- Compliance with responsible disclosure principles

## 📁 Project Structure

```
FlawHunt CLI/
├── main.py                 # Main application entry point
├── ai_terminal/           # Core application modules
│   ├── __init__.py        # Package initialization
│   ├── agent.py           # AI agent implementation
│   ├── llm.py             # Language model wrapper
│   ├── tools.py           # Tool implementations
│   ├── safety.py          # Security and safety controls
│   ├── themes.py          # Theme management
│   ├── config.py          # Configuration management
│   ├── conversation_history.py # Memory system
│   ├── vector_store.py    # Semantic search
│   ├── animations.py      # Visual effects
│   └── utils.py           # Utility functions
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── docs/                 # Additional documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with appropriate tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Setup
For contributors and developers:
```bash
git clone https://github.com/gamkers/GAMKERS_CLI.git
cd GAMKERS_CLI
pip install -r requirements.txt
pip install -e .
python main.py  # Run from source
python -m pytest tests/  # Run tests
```

## 📄 License

MIT License - see [LICENSE.md](LICENSE.md) for details.

## 🆘 Support & Documentation

- **Issues**: [GitHub Issues](https://github.com/gamkers/GAMKERS_CLI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/gamkers/GAMKERS_CLI/discussions)
- **Documentation**: See `/docs` folder for detailed guides
- **Security**: Report security issues privately via email

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) for AI agent capabilities
- Powered by [Groq](https://groq.com/) and [Google Gemini](https://ai.google.dev/) APIs
- UI powered by [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- Command completion via [prompt-toolkit](https://python-prompt-toolkit.readthedocs.io/)

---

**FlawHunt CLI** - Empowering ethical hackers with AI-assisted cybersecurity operations.