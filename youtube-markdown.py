from pytube import YouTube
import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_info(youtube_urls):
    video_info = []
    for url in youtube_urls:
        try:
            yt = YouTube(url)
            transcript = get_video_transcript(yt.video_id)
            video_info.append({'title': yt.title, 'url': yt.watch_url, 'description': transcript})
        except Exception as e:
            print(f"Error extracting info for {url}: {e}")

    return video_info

def get_video_transcript(video_id):
    try:
        # Try fetching transcript with language code 'en'
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        if not transcript:
            # If 'en' transcript is not available, try 'en-US'
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US'])

        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        print(f"Error fetching transcript for video_id {video_id}: {e}")
        return ''

def get_emojis_for_keywords(text):
    if text:
        keywords_emojis = {
            'tools': '🛠️',
            'hack': '🤖',
            'hackers': '👩‍💻',
            'hacking': '👩‍💻',
            'code': '💻',
            'coding': '💻',
            'javascript': '🔧',
            'html': '🔧',
            'python': '🐍',
            'linux': '🐧',
            'kali': '🔓',
            'burpsuite': '🔄',
            'sqli': '🚧',
            'rce': '💥',
            'xss': '🔍',
            'html': '🌐',
            'css': '🎨',
        }

        added_emojis = set()
        emojis = []
        for word in re.findall(r'\w+', text):
            for keyword, emoji in keywords_emojis.items():
                if keyword.lower() in word.lower() and emoji not in added_emojis:
                    emojis.append(emoji)
                    added_emojis.add(emoji)

        return emojis
    return []


def extract_hashtags(description):
    if description:
        hashtags = re.findall(r'#(\w+)', description)
        return hashtags
    return []

def create_markdown_file(video_info, output_file='youtube_videos.md'):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("# YouTube Video List\n\n")
        for index, info in enumerate(video_info, start=1):
            shields = "[![Cybersecurity Shield](https://img.shields.io/badge/Cybersecurity-Video-red)](info['url']) [![Computer Science Shield](https://img.shields.io/badge/Computer%20Science-Video-brightgreen)](info['url'])"
            emojis_in_title = get_emojis_for_keywords(info['title'])
            emojis_in_description = get_emojis_for_keywords(info.get('description', ''))
            all_emojis = emojis_in_title + emojis_in_description
            hashtags = extract_hashtags(info.get('description', ''))

            file.write(f"{index}. {' '.join(all_emojis)} [{info['title']}]({info['url']}) {shields}\n")
            if hashtags:
                file.write(f"   - Hashtags: {' '.join(hashtags)}\n")

if __name__ == "__main__":
    youtube_urls = [
        "https://www.youtube.com/watch?v=MUWTd6Gx2zE",
        "https://www.youtube.com/watch?v=4kK9tX_u33U",
        "https://www.youtube.com/watch?v=7oEX_V7inMU",
        "https://www.youtube.com/watch?v=pj_jyVG7sB4",
        "https://www.youtube.com/watch?v=TY7I26NUrg8",
        "https://www.youtube.com/watch?v=_uTe7cwe1XQ",
        "https://www.youtube.com/watch?v=nUOFXOflZwk",
        "https://www.youtube.com/watch?v=j0f1A8jrgTc",
        "https://www.youtube.com/watch?v=ru3U8MHbFFI",
        "https://www.youtube.com/watch?v=3EfiJJzeRWU",
        "https://www.youtube.com/watch?v=AZnGRKFUU0c",
        "https://www.youtube.com/watch?v=NUeCNvYY_x4",
        "https://www.youtube.com/watch?v=MTY6-VULk4c",
        "https://www.youtube.com/watch?v=dqeCvLlvnmw",
        "https://www.youtube.com/watch?v=7HMKphim2jg",
        "https://www.youtube.com/watch?v=jVao4UdOFHk",
        "https://www.youtube.com/watch?v=oG5qB80NOeE",
        "https://www.youtube.com/watch?v=XWuP5Yf5ILI",
        "https://www.youtube.com/watch?v=hJmNAjSHcAo",
        "https://www.youtube.com/watch?v=EFLvHMJ5PHk",
        "https://www.youtube.com/watch?v=0n3Li63PwnQ",
        "https://www.youtube.com/watch?v=24nhC1TMEV4",
        "https://www.youtube.com/watch?v=mVKAyw0xqxw",
        "https://www.youtube.com/watch?v=CFRhGnuXG-4",
    ]

    video_info = get_video_info(youtube_urls)
    create_markdown_file(video_info)
