# LocalBiz AI 🚀

### Your AI-Powered Marketing Assistant for Small Businesses

LocalBiz AI is an AI-powered marketing content generator designed to help small businesses create promotional content quickly and efficiently. From Instagram captions to product descriptions and promotional emails, it helps business owners generate content tailored to their audience, platform, and brand tone.

The application integrates **FastAPI with Ollama and the open-weight Gemma 3 1B model** to support local AI inference. It also includes a template-based fallback, allowing users to generate content even when the local model is unavailable.

## ✨ Features

* **AI-Powered Content Generation:** Generate marketing copy for different business needs.
* **Multiple Content Types:** Create social media posts, product descriptions, promotional emails, and marketing messages.
* **Customizable Content:** Specify business details, target audience, platform, tone, and key information.
* **Local AI Inference:** Run Gemma 3 1B locally through Ollama.
* **Offline Fallback:** Use template-based generation when Ollama is unavailable.
* **Generation History:** Store generated content in a local SQLite database.
* **REST API:** Use FastAPI endpoints to integrate content generation into other applications.
* **Responsive Interface:** Access the application through a browser on desktop or mobile.
* **Open-Source Stack:** Built using accessible tools and technologies.

## 🛠️ Tech Stack

| Technology            | Purpose                    |
| --------------------- | -------------------------- |
| Python                | Core application logic     |
| FastAPI               | Backend and REST API       |
| Ollama                | Local model execution      |
| Gemma 3 1B            | Open-weight language model |
| SQLite                | Generation history storage |
| HTML, CSS, JavaScript | Frontend interface         |
| Pytest                | API testing                |

## 🏗️ Architecture

```text
User
 │
 ▼
Responsive Web Interface
 │
 ▼
FastAPI Backend
 │
 ├── Validate User Input
 │
 ├── Ollama + Gemma 3 1B
 │       │
 │       └── AI-Generated Marketing Content
 │
 └── Template-Based Fallback
         │
         ▼
   Generated Content
         │
         ▼
   SQLite History
```

The backend attempts to generate content using the locally running model. If the model is unavailable, the application can use its template-based fallback.

## 📂 Project Structure

```text
LocalBizAI/
├── app/
│   └── main.py
├── static/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
│   └── test_app.py
├── requirements.txt
├── requirements-dev.txt
├── run_windows.bat
├── run.sh
├── setup_ollama_windows.bat
├── README.md
├── DEV_SUBMISSION.md
└── LICENSE
```

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.10 or a compatible version supported by the project dependencies
* pip
* [Ollama](https://ollama.com/download)
* Sufficient memory and disk space to run the selected language model

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/LocalBizAI.git
cd LocalBizAI
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

**Windows — PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the project's Windows launcher instead.

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Local AI Model

Install Ollama from its official download page:

https://ollama.com/download

Then download Gemma 3 1B:

```bash
ollama pull gemma3:1b
```

Start the model:

```bash
ollama run gemma3:1b
```

Once the model is downloaded, Ollama can run inference locally without sending prompts to a hosted language-model API.

### 5. Start the Application

**Windows**

```powershell
.\run_windows.bat
```

**Linux/macOS**

```bash
chmod +x run.sh
./run.sh
```

If you prefer to start the backend manually, use the launch command documented in the application configuration.

Open your browser and visit:

**http://127.0.0.1:8000**

> **Note:** Keep Ollama available when you want model-generated content. If it is unavailable, the application can fall back to its template-based generation path.

## 🧪 Running Tests

Install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the test suite:

```bash
pytest tests/ -v
```

## 💡 Example Use Case

Imagine a local café that wants to promote a weekend discount on Instagram.

**Sample Input**

| Field           | Value                                       |
| --------------- | ------------------------------------------- |
| Business Name   | GreenLeaf Cafe                              |
| Business Type   | Cafe                                        |
| Platform        | Instagram                                   |
| Content Type    | Promotional Post                            |
| Target Audience | College students and young professionals    |
| Product/Service | Organic coffee and healthy snacks           |
| Tone            | Friendly                                    |
| Key Details     | 20% discount on organic coffee this weekend |

**Expected Result**

The application generates a promotional draft tailored to the café, its target audience, the Instagram platform, and the requested tone.

*The exact generated content depends on the model response or fallback template.*

## 🌱 Why Open Innovation Matters

Small businesses often lack the time, budget, and technical expertise needed to create effective marketing content consistently.

LocalBiz AI explores how open-weight models and open-source software can make AI-powered tools more accessible.

* **Accessibility:** Helps small businesses experiment with AI-assisted marketing.
* **Local Inference:** Supports running the language model on a user's own machine.
* **Transparency:** Uses an understandable application architecture built on widely used technologies.
* **Customization:** Provides a foundation for adapting content generation to different industries and business requirements.
* **Community Collaboration:** Encourages developers to improve the application, add features, and contribute enhancements.

## 🔮 Future Improvements

* Support for additional local language models.
* Hindi and multilingual marketing content generation.
* Brand voice profiles and reusable business settings.
* Download generated content in TXT, Markdown, and PDF formats.
* Content quality evaluation and duplicate detection.
* Improved model selection and inference configuration.
* Docker-based deployment.
* User authentication and persistent business profiles.
* Analytics to track content generation and usage.

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request describing the improvement.

Ideas for contributions include additional content templates, improved prompts, localization, UI enhancements, and support for more open-weight models.

## 📄 License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

## 👨‍💻 Author

**Jitin Kumar**

B.Tech CSE — Artificial Intelligence Specialization

Interested in AI/ML, backend development, and building practical AI-powered products.

* **GitHub:** [Jitin2102](https://github.com/Jitin2102)

---

**LocalBiz AI — Making AI-powered marketing more accessible to small businesses.** 🚀
