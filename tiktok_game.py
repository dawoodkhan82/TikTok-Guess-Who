import gradio as gr
import asyncio
from TikTokApi import TikTokApi
import random
from typing import List

current_video = None
current_answer = None
liked_videos = []
used_videos = set()
MS_TOKEN = ""

async def fetch_user_likes(username: str) -> List[dict]:
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[MS_TOKEN], num_sessions=1, headless=False)
        user = api.user(username=username)
        user_info = await user.info()
        is_private = user_info.get("userInfo", {}).get("user", {}).get("privateAccount", False)
        if is_private:
            print("PRIVATE ACCOUNT: ", username)
            return []
        videos = []
        async for video in user.liked():
            print("VIDEO:", username, video)
            videos.append(video)
            if len(videos) >= 10:
                break
        
        for video in videos:
            try:
                if video is not None and video.id is not None:
                    liked_videos.append({
                        'username': username,
                        'video_id': video.id,
                    })
            except AttributeError as e:
                print(f"Error processing video: {e}")
            except Exception as e:
                print(f"Unexpected error processing video: {e}")

        return videos


def add_user(username: str):
    existing_usernames = list(set(video['username'] for video in liked_videos))
    if username in existing_usernames:
        return gr.Markdown(value=f"User {username} is already added!", visible=True), gr.Textbox(value="\n".join(existing_usernames), visible=True)
    try:
        user_videos = asyncio.run(fetch_user_likes(username))
        if len(user_videos) > 0:
            updated_usernames = list(set(video['username'] for video in liked_videos))
            return None, gr.Textbox(value="\n".join(updated_usernames))
        else:
            return gr.Markdown(value=f"User {username} liked videos are private!", visible=True), gr.Textbox(value="\n".join(existing_usernames), visible=True)
    except Exception as e:
        return gr.Markdown(value=f"Error adding user: {str(e)}", visible=True), gr.Textbox(value="\n".join(existing_usernames), visible=True)

def get_random_video():
    global current_video, current_answer
    unused_videos = [v for v in liked_videos if v['video_id'] not in used_videos]
    if not unused_videos:
        used_videos.clear()
        unused_videos = liked_videos
    
    current_video = random.choice(unused_videos)
    used_videos.add(current_video['video_id'])
    current_answer = current_video['username']
    html = f'<div style="display: flex; justify-content: center;"><iframe src="https://www.tiktok.com/embed/v3/{current_video["video_id"]}" width="350px" height="600px" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>'
    return html

def start_round() -> tuple:
    existing_usernames = list(set(video['username'] for video in liked_videos))
    global current_video, current_answer

    if not existing_usernames or existing_usernames == []:
        return gr.Markdown(value="# <div style='text-align: center;'>Please add some users first!</div>", visible=True), None, [], gr.Button(visible=False)

    current_video = random.choice(liked_videos)
    used_videos.add(current_video['video_id'])
    current_answer = current_video['username']
    choices = list(set(video['username'] for video in liked_videos))
    html = f'<div style="display: flex; justify-content: center;"><iframe src="https://www.tiktok.com/embed/v3/{current_video["video_id"]}" width="350px" height="600px" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>'
    return gr.Markdown(value="# <div style='text-align: center;'>Make your guess!</div>", visible=True), html, gr.Radio(choices=choices, visible=True), gr.Button(visible=True)

def check_answer(choice: str):
    global current_answer
    if not current_answer:
        return gr.Markdown(value="# <div style='text-align: center;'>Please start a new round first!</div>")
    if choice == current_answer:
        overlay_html = """
        <div class="overlay" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            animation: fadeIn 0.5s ease-in-out;
            cursor: pointer;
        " onclick="this.style.display='none'">
            <div style="
                background: white;
                padding: 2rem;
                border-radius: 1rem;
                text-align: center;
                animation: scaleIn 0.5s ease-in-out;
                position: relative;
            ">
                <button style="
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: none;
                    border: none;
                    font-size: 1.5em;
                    cursor: pointer;
                    color: black;
                " onclick="this.parentElement.parentElement.style.display='none'">×</button>
                <h1 style="font-size: 3em; margin: 0;"><span style="color: black;">Correct!</span> 💯</h1>
            </div>
        </div>
        <style>
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes scaleIn {
                from { transform: scale(0.5); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
        </style>
        """
        return gr.HTML(value=overlay_html)
    else:
        overlay_html = f"""
        <div class="overlay" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            animation: fadeIn 0.5s ease-in-out;
            cursor: pointer;
        " onclick="this.style.display='none'">
            <div style="
                background: white;
                padding: 2rem;
                border-radius: 1rem;
                text-align: center;
                animation: scaleIn 0.5s ease-in-out;
                position: relative;
            ">
                <button style="
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: none;
                    border: none;
                    font-size: 1.5em;
                    cursor: pointer;
                    color: black;
                " onclick="this.parentElement.parentElement.style.display='none'">×</button>
                <h1 style="font-size: 3em; margin: 0;">😢 <span style="color: black;">Wrong!</span></h1>
                <p style="font-size: 1.5em; margin: 1rem 0; color: black;">This video was liked by <span style="color: #fe2c55;">{current_answer}</span></p>
            </div>
        </div>
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            @keyframes scaleIn {{
                from {{ transform: scale(0.5); opacity: 0; }}
                to {{ transform: scale(1); opacity: 1; }}
            }}
        </style>
        """
        return gr.HTML(value=overlay_html, visible=True)

with gr.Blocks(title="TikTok Likes Guessing Game") as demo:    
    with gr.Sidebar():
        gr.Markdown("# <div style='text-align: center;'> 🤖 Add TikTok usernames</div> \n **Note: Make sure the user's profile and liked videos are public.**")
        username_input = gr.Textbox(label="Enter TikTok Username")
        add_user_btn = gr.Button("➕ Add User")
        with gr.Accordion(open=False, label="🧑‍🧑‍🧒‍🧒 Players"):
            status_text = gr.Markdown(show_label=False, visible=False)
            users_list = gr.Textbox(show_label=False)
        start_btn = gr.Button("▶️ Start Game")
    gr.Markdown("<div style='text-align: center; display: flex; align-items: center; justify-content: center; gap: 20px;'><img src='https://cdn4.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Tiktok-512.png' style='width: 50px; height: auto;'><h1 style='font-size: 2.5em; margin: 0;'>TikTok Guess Who</h1><img src='https://cdn4.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Tiktok-512.png' style='width: 50px; height: auto;'></div>")
    make_guess = gr.Markdown(visible=False)
    video_display = gr.HTML(label="Mystery Video")
    choices = gr.Radio(visible=False, show_label=False)
    submit_btn = gr.Button("Submit", visible=False)
    result_overlay = gr.HTML(visible=True)
    next_video_btn = gr.Button("🎥 Next Video", visible=False)

    add_user_btn.click(
        add_user,
        inputs=[username_input],
        outputs=[status_text, users_list]
    ).then(
        lambda: gr.Textbox(""), None, [username_input]
    )
    
    start_btn.click(
        start_round,
        outputs=[make_guess, video_display, choices, submit_btn]
    )
    
    submit_btn.click(
        check_answer,
        inputs=[choices],
        outputs=[result_overlay]
    ).then(
        lambda: (gr.Button(visible=False), gr.Radio(visible=False), gr.Button(visible=True)), None, [submit_btn, choices, next_video_btn]
    )

    next_video_btn.click(
        get_random_video,
        outputs=[video_display]
    ).then(
        lambda: (gr.Button(visible=False), gr.Button(visible=True), gr.Radio(visible=True), gr.HTML(value="")), None, [next_video_btn, submit_btn, choices, result_overlay]
    )

if __name__ == "__main__":
    demo.launch()
