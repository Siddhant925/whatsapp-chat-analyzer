# 💬 WhatsApp Chat Analyzer

A Python-based data analytics application that analyzes exported WhatsApp conversations and transforms chat data into meaningful insights and visualizations.

## 📌 Overview

The WhatsApp Chat Analyzer helps users understand their messaging patterns by analyzing exported WhatsApp chat files. It provides statistics and visualizations about messages, words, media, links, emojis, and frequently used words.

The application is built using Python, Pandas, Matplotlib, and Streamlit.

## ✨ Features

* **Message Statistics:** View the total number of messages and words.
* **Media Analysis:** Count messages containing media placeholders.
* **Link Analysis:** Identify and count shared URLs.
* **Most Active Users:** Discover who sends the most messages in a group.
* **Word Cloud:** Visualize frequently used words.
* **Most Common Words:** Find the most frequently used words in conversations.
* **Emoji Analysis:** Explore emoji usage and frequency.
* **Individual User Analysis:** Analyze the conversation statistics of a selected participant.
* **Interactive Dashboard:** Explore chat insights through a Streamlit interface.

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend / Dashboard:** Streamlit
* **Data Processing:** Pandas
* **Data Visualization:** Matplotlib
* **Word Cloud:** WordCloud
* **URL Extraction:** urlextract
* **Emoji Processing:** emoji

## 📂 Project Structure

```text
whatsapp-chat-analyzer/
│
├── app.py               # Main Streamlit application
├── preprocess.py        # Chat parsing and preprocessing
├── helper.py            # Data analysis functions
├── stop_hinglish.txt    # Stop words for word analysis
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Files excluded from Git
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Siddhant925/whatsapp-chat-analyzer.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Navigate to the project directory

```bash
cd whatsapp-chat-analyzer
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📱 How to Use

1. Open WhatsApp and select the individual or group conversation you want to export.
2. Export the chat **without media** to obtain a `.txt` file.
3. Open the WhatsApp Chat Analyzer application.
4. Upload the exported `.txt` file using the sidebar.
5. Select **Overall** or an individual participant.
6. Click **Analyze Chat** to explore the available statistics and visualizations.

*Note: Export formatting may differ across devices and WhatsApp versions. The parser must support the format of your exported chat.*

## 🔮 Future Enhancements

* Message activity by day, month, and hour.
* Sentiment analysis of conversations.
* Most-used emoji for each participant.
* Response time and conversation pattern analysis.
* Shared link categorization.
* Improved mobile-friendly dashboard.
* Deploy the application online.

## 🔒 Privacy

WhatsApp exports may contain personal and sensitive information. Use your own exported chats or obtain permission before analyzing other people's conversations.

Do not upload private chat exports to this public repository. Process sensitive conversations locally and review the data-handling practices before deploying the application online.

## 🎯 Learning Objectives

This project helps demonstrate practical experience with:

* Python programming and data preprocessing.
* Pandas-based data analysis.
* Data visualization.
* Text processing and basic natural language processing.
* Building interactive applications with Streamlit.

## 👨‍💻 Author

**SIDDHANT**

* GitHub: https://github.com/Siddhant925

---

If you find this project useful, consider giving the repository a ⭐ on GitHub!
