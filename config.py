"""
Configuration settings for the Interview Assistant application.
"""

# Default system prompt for the AI assistant
DEFAULT_SYSTEM_PROMPT = """
You are an AI assistant helping a job candidate during an interview. 
Your task is to provide helpful, concise, and professional responses to interview questions.
Focus on showcasing the candidate's skills and experience in the best possible light.
Provide specific examples and achievements when possible.
Keep responses between 100-200 words unless the question requires a more detailed answer.
Avoid generic answers and try to personalize responses based on the context of the question.
"""

# Audio recording settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
RECORD_SECONDS = 5

# API settings
MAX_TOKENS = 500
TEMPERATURE = 0.7
MODEL = "gpt-3.5-turbo"
WHISPER_MODEL = "whisper-1"

# Web interface settings
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True
