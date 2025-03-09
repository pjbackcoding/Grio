# Interview Assistant

An AI-powered tool that transcribes job interview questions and provides written answers for candidates in real-time. Supports multiple languages including English, French, Spanish, German, Italian, Japanese, and Chinese.

## Features

- Real-time speech-to-text transcription of interview questions
- Continuous speech recognition with intelligent pause detection
- Multilingual support (English, French, Spanish, German, Italian, Japanese, Chinese)
- AI-generated responses to common interview questions
- Simple web interface for easy interaction
- Support for various interview contexts and job roles

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8+
- An OpenAI API key

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd interview-assistant
```

2. Install the required Python packages:
```
pip install -r requirements.txt
```

3. Create a `.env` file in the project root directory based on the example template:
```
cp .env.example .env
```

4. Edit the `.env` file to add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```
python app.py
```

2. Open your web browser and navigate to `http://localhost:5001`

3. Configure your settings:
   - Enter your job role (optional)
   - Add any additional context (optional)
   - Select your preferred language from the dropdown

4. Click the "Start Listening" button to begin transcribing interview questions

5. The application will continuously listen and transcribe spoken questions, automatically detecting pauses to process each question

6. AI-generated responses will appear in the conversation area

7. Click the "Stop Listening" button when you're done, or the "Clear Conversation" button to start fresh

## Configuration

You can customize the AI behavior by modifying the prompt in the `config.py` file. This allows you to tailor the responses to specific job roles or interview contexts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [OpenAI](https://openai.com/) for providing the GPT and Whisper APIs
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for the speech recognition functionality
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) for browser-based continuous speech recognition
- [Flask](https://flask.palletsprojects.com/) for the web framework

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Open a Pull Request

### Note on Environment Variables

This project uses environment variables for configuration. The `.env` file is excluded from version control for security reasons. Always use the `.env.example` file as a template and never commit sensitive API keys to the repository.
