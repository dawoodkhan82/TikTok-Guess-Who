# TikTok Game

A fun interactive game built with Gradio that tests your knowledge of TikTok users' liked videos. The game presents you with a TikTok video and asks you to guess which user liked it from a list of options.

## Features

- Fetches liked videos from multiple TikTok users
- Presents random videos in a game format
- Interactive UI built with Gradio
- Supports multiple rounds of gameplay
- Tracks scores and provides feedback

## Prerequisites

- Python 3.12+
- TikTokApi
- Gradio
- asyncio

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the game:
   ```bash
   python tiktok_game.py
   ```
2. The game will open in your default web browser
3. Add TikTok usernames to create a pool of users
4. Start playing by clicking the "Start Round" button
5. Watch the video and guess which user liked it
6. Get feedback on your answer and continue playing

## How to Play

1. Add TikTok usernames in the input field
2. Click "Start Round" to begin
3. Watch the video that appears
4. Select which user you think liked the video
5. Submit your answer to see if you're correct
6. Continue playing to improve your score

## Note

This game requires a valid MS_TOKEN for the TikTok API to function properly. Make sure to update the MS_TOKEN in the code if it expires.

## License

This project is open source and available under the MIT License.
