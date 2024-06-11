import streamlit as st
from pytube import YouTube
from PIL import Image
import os

sidebar_selectbox = st.sidebar.selectbox(
    "...",
    ("YouTube Video Downloader", "YouTube to MP3 Converter", "WebP Image Converter")
)

if sidebar_selectbox == "YouTube Video Downloader":
    youtube_url = st.text_input("Enter YouTube URL")
    quality_options = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
    selected_quality = st.selectbox("Select Quality", quality_options)
    download_video = st.button("Download Video")

    if download_video and youtube_url:
        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(file_extension='mp4', res=selected_quality).first()
            if stream:
                video_file_path = stream.download()
                st.success("Video downloaded successfully!")
                st.download_button(label="Download Video File", data=open(video_file_path, 'rb').read(), file_name=video_file_path.split("/")[-1])
                os.remove(video_file_path)
            else:
                st.error("Selected quality not available.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if sidebar_selectbox == "YouTube to MP3 Converter":
    youtube_url_mp3 = st.text_input("Enter YouTube URL for MP3")
    download_mp3 = st.button("Download MP3")

    if download_mp3 and youtube_url_mp3:
        try:
            yt = YouTube(youtube_url_mp3)
            stream = yt.streams.filter(only_audio=True).first()
            if stream:
                out_file = stream.download()
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                st.success("Audio downloaded successfully as MP3!")
                st.download_button(label="Download Audio File", data=open(new_file, 'rb').read(), file_name=new_file.split("/")[-1])
                os.remove(new_file)
            else:
                st.error("Could not download the audio.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if sidebar_selectbox == "WebP Image Converter":
    uploaded_file = st.file_uploader("Choose a WebP file", type="webp")
    output_format = st.selectbox("Convert to", ["PNG", "JPG"])
    convert_image = st.button("Convert Image")

    if convert_image and uploaded_file:
        try:
            image = Image.open(uploaded_file)
            if output_format == "PNG":
                converted_file = uploaded_file.name.rsplit('.', 1)[0] + '.png'
                image.save(converted_file, "PNG")
            elif output_format == "JPG":
                converted_file = uploaded_file.name.rsplit('.', 1)[0] + '.jpg'
                image = image.convert("RGB")
                image.save(converted_file, "JPEG")
            st.success(f"Image converted successfully to {output_format}!")
            st.download_button(label=f"Download Converted Image ({output_format})", data=open(converted_file, 'rb').read(), file_name=converted_file.split("/")[-1])
            os.remove(converted_file)
        except Exception as e:
            st.error(f"Error: {str(e)}")
