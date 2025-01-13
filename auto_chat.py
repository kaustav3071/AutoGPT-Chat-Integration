import pyautogui
import time
import pyperclip
import openai
from config import OPENAI_API_KEY  # Import your OpenAI API key from config.py

# Set up OpenAI API key for authentication
openai.api_key = OPENAI_API_KEY

def capture_chat_history():
    """
    Captures the chat history from the screen by simulating mouse and keyboard actions.
    """
    # Simulate a click to focus the chat window at a specific coordinate on your screen
    pyautogui.click(1130, 35)
    time.sleep(1)  # Wait for the chat window to open

    # Simulate dragging the mouse to select text (adjust coordinates as needed)
    pyautogui.moveTo(922, 345)
    pyautogui.dragTo(1836, 906, duration=2, button='left')  # Drag to select text
    time.sleep(0.5)  # Give it a moment to finish the selection

    # Simulate pressing Ctrl+C to copy the selected text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Allow some time for the text to be copied to the clipboard

    # Retrieve and return the copied text from the clipboard
    selected_text = pyperclip.paste()
    return selected_text

def get_openai_response(chat_history):
    """
    Sends the captured chat history to OpenAI and retrieves a response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use GPT-3.5 for chat completion
        messages=[  # Prepare the system and user messages for the model
            {
                "role": "system",  # Define system behavior
                "content": "You are a helpful assistant named Kaustav who speaks Hindi and English. Your task is to analyze the chat and provide the best answer to the user."
            },
            {"role": "user", "content": chat_history},  # Send the user's chat history as input
        ]
    )
    
    # Return the response from the model
    return response['choices'][0]['message']['content']

def send_response_to_chatbot(gpt_response):
    """
    Simulates typing the response from GPT back into the chat.
    """
    # Copy the response to the clipboard for pasting
    pyperclip.copy(gpt_response)
    
    # Click on the text input field to focus it (adjust the coordinates)
    pyautogui.click(1062, 962)
    time.sleep(0.5)

    # Paste the response into the chat input field and send it
    pyautogui.hotkey('ctrl', 'v')  # Paste the response
    time.sleep(0.5)  # Wait for the paste to complete
    pyautogui.press('enter')  # Press Enter to send the message

def main():
    """
    The main function that runs the entire chat automation process in a loop.
    """
    while True:
        # Step 1: Capture chat history from the screen
        chat_history = capture_chat_history()
        print("Captured Chat History:", chat_history)

        # Step 2: Get a response from OpenAI based on the chat history
        gpt_response = get_openai_response(chat_history)
        print("OpenAI Response:", gpt_response)

        # Step 3: Send the response back to the chat
        send_response_to_chatbot(gpt_response)

        # Wait for a few seconds before checking for new messages (adjust as needed)
        time.sleep(5)

if __name__ == "__main__":
    main()
