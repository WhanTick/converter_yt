import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import tkinter.font as tkfont
import pygame
import os
import cv2
from PIL import Image, ImageTk
import subprocess  # For opening the folder
import time
import ffmpeg


class YTDLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Microsoft Word")
        self.root.geometry("800x600")

        # Load background image
        self.bg_image = Image.open("brainrot.jpg")  # Replace with your image file
        self.bg_image = self.bg_image.resize((800,  600))  # Resize to fit the window

        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Canvas widget and set it as the background
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Set the background image on the Canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Initialize music and video
        pygame.mixer.init()
        self.music = pygame.mixer.Sound("music.mp3")
        self.music.play(loops=-1, fade_ms=3000)  # Play music in a loop with a fade-in effect
        self.finishsound = pygame.mixer.Sound("finish.mp3")


        self.is_muted = False
        self.video_file = "video.mp4"  # Path to your MP4 file

        pygame.display.init()


        # Set up video player (this will run in a separate thread)
        self.video_playing = False

        # Load custom font
        try:
            self.custom_font = tkfont.Font(family="Comic Sans MS", size=12)  # Use your custom font
        except Exception as e:
            messagebox.showerror("Error", f"Font file not found or couldn't be loaded. {e}")
            self.custom_font = None

        # Add widgets above the background image
        self.video_label = tk.Label(root, text="app buat eee convert lupa",
                                    font=tkfont.Font(family="Comic Sans MS", size=15))
        self.video_label2 = tk.Label(root, text="link video yucub",
                                    font=tkfont.Font(family="Comic Sans MS", size=11))
        self.video_label3 = tk.Label(root, text="format video",
                                    font=tkfont.Font(family="Comic Sans MS", size=11))
        self.canvas.create_window(400, 30, window=self.video_label)  # Position at the top



        self.url_entry = tk.Entry(root, width=50, font=self.custom_font)
        self.canvas.create_window(400, 70, window=self.url_entry)  # Position URL entry field
        self.canvas.create_window(80, 67, window=self.video_label2)  # Position URL entry field
        self.canvas.create_window(230, 113, window=self.video_label3)  # Position URL entry field


        self.format_options = ttk.Combobox(root, values=["MP4", "MP3"], state="readonly", font=self.custom_font)
        self.format_options.set("MP4")  # Default to MP4
        self.canvas.create_window(400, 110, window=self.format_options)  # Position format selection

        # Cookies File Selection Button
        self.cookies_button = tk.Button(root, text="masukin file cookies.txt disini", command=self.select_cookies_file,
                                        font=self.custom_font)
        self.canvas.create_window(400, 150, window=self.cookies_button)  # Position cookies button

        # Show selected cookies file path
        self.cookies_label = tk.Label(root, text="No file selected.", font=self.custom_font)
        self.canvas.create_window(400, 190, window=self.cookies_label)  # Position cookies label

        # Download Button
        self.download_button = tk.Button(root, text="Download", command=self.start_download, font=self.custom_font)
        self.canvas.create_window(400, 570, window=self.download_button)  # Position download button

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.canvas.create_window(400, 270, window=self.progress)  # Position progress bar

        # Output Label
        self.output_label = tk.Label(root, text="No video downloaded", font=self.custom_font)
        self.canvas.create_window(400, 310, window=self.output_label)  # Position output label

        # Mute Button
        self.mute_button = tk.Button(root, text="Mute", command=self.toggle_mute, font=self.custom_font)
        self.canvas.create_window(30, 570, window=self.mute_button)  # Position Mute button

        self.cookies_path = None  # Placeholder for the cookies file path

        # Output Folder Selection Button
        self.output_folder_button = tk.Button(root, text="Select Output Folder", command=self.select_output_folder,
                                              font=self.custom_font)
        self.canvas.create_window(400, 230, window=self.output_folder_button)  # Position output folder button

        # Show selected output folder path
        self.output_folder_label = tk.Label(root, text="No folder selected.", font=self.custom_font)
        self.canvas.create_window(120, 270, window=self.output_folder_label)  # Position output folder label

        # Start video playing in a separate thread
        threading.Thread(target=self.play_video, daemon=True).start()

    def play_video(self):
        """Play video using OpenCV and display in Tkinter"""
        if not os.path.exists(self.video_file):
            messagebox.showerror("Error", "Video file not found.")
            return

        # Open the video using OpenCV
        cap = cv2.VideoCapture(self.video_file)

        # Get the frame width and height
        frame_width = 400
        frame_height = 200

        # Create an empty Tkinter image label to display frames
        self.video_frame_label = tk.Label(self.root)
        self.video_frame_label.pack()



        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video when finished
                continue  # Continue looping

            # Resize the frame to fit within the window size (without cropping)
            frame_resized = cv2.resize(frame, (frame_width, frame_height))

            # Convert the frame to RGB (Tkinter uses RGB format)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(image=frame_image)

            # Update the video label with the new frame
            self.video_frame_label.config(image=frame_tk)
            self.video_frame_label.image = frame_tk
            self.video_x = 400  # Set the x-coordinate to 50px from the left
            self.video_y = 430  # Set the y-coordinate to 150px from the top
            self.video_frame = self.canvas.create_window(self.video_x, self.video_y,
                                                         window=self.video_frame_label)  # Position video display

            # Update the Tkinter window
            self.root.update_idletasks()
            self.root.update()

            # Pause for a short time (to simulate 30 FPS)
            cv2.waitKey(30)

        # Release video capture after completion
        cap.release()

    def select_cookies_file(self):
        """Open file dialog to choose cookies.txt"""
        self.cookies_path = filedialog.askopenfilename(
            title="Select Cookies File",
            filetypes=[("Text Files", "*.txt")]
        )
        if self.cookies_path:
            self.cookies_label.config(text=f"Selected: {self.cookies_path}")
        else:
            self.cookies_label.config(text="No file selected.")

    def convert_webm_to_mp4(self, input_path, output_path):
        """Convert a WebM file to MP4 format using FFmpeg."""
        try:
            # Use FFmpeg to convert the file
            ffmpeg.input(input_path).output(output_path, vcodec='libx264', acodec='aac').run()
            print(f"Conversion successful! File saved at {output_path}")
        except ffmpeg.Error as e:
            print(f"Error during conversion: {e}")

    def convert_webm_to_mp3(self, input_path, output_path):
        """Convert a WebM file to MP3 format using FFmpeg."""
        try:
            # Use FFmpeg to convert from WebM to MP3
            ffmpeg.input(input_path).output(output_path, acodec='libmp3lame', audio_bitrate='192k').run()
            print(f"Conversion successful! MP3 saved at {output_path}")
        except ffmpeg.Error as e:
            print(f"Error during conversion: {e}")
            print(e.stderr.decode())  # Optionally print out the error message from FFmpeg

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        if not self.output_folder:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        self.download_button.config(state=tk.DISABLED)
        threading.Thread(target=self.download, args=(url,)).start()

    def select_output_folder(self):
        """Open folder dialog to select output folder"""
        self.output_folder = filedialog.askdirectory(title="Select Output Folder")
        if self.output_folder:
            self.output_folder_label.config(text=f"Selected: {self.output_folder}")
        else:
            self.output_folder_label.config(text="No folder selected.")
    def download(self, url):
        def progress_hook(d):
            if d['status'] == 'downloading':
                self.progress['value'] = d.get('percent', 0)
                self.root.update_idletasks()
            elif d['status'] == 'finished':
                self.progress['value'] = 100
                self.output_label.config(text="Download complete!")
                self.download_button.config(state=tk.NORMAL)
                self.finishsound.play()


                # Check if the downloaded file is in WebM format and convert it to MP4
                downloaded_file = d['filename']
                if downloaded_file.endswith('.webm') and format_choice == 'mp4':
                    output_file = os.path.splitext(downloaded_file)[0] + '.mp4'
                    self.convert_webm_to_mp4(downloaded_file, output_file)
                    os.remove(downloaded_file)  # Remove the original WebM file if desired
                else:
                    output_file = os.path.splitext(downloaded_file)[0] + '.mp3'
                    self.convert_webm_to_mp3(downloaded_file, output_file)
                    os.remove(downloaded_file)  # Remove the original WebM file if desired


        # Get format based on user selection (MP4 or MP3)
        format_choice = self.format_options.get().lower()

        timestamp = int(time.time())  # Get a timestamp
        filename = f'%(title)s_%d_{timestamp}.%(ext)s'  # Append the timestamp to the filename

        # Set download options
        ydl_opts = {
            # For video, select the best video and audio streams
            # For audio, select the best audio stream
            'format': 'bestvideo' if format_choice == 'mp4' else 'bestaudio/best',
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(self.output_folder, filename),  # Save to selected folder
        }

        # If the user selected a cookies.txt file, add it to options
        if self.cookies_path:
            ydl_opts['cookiefile'] = self.cookies_path

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.download_button.config(state=tk.NORMAL)

    def open_output_folder(self):
        """Open the output folder using the default file manager"""
        if os.name == 'nt':  # For Windows
            subprocess.run(['explorer', self.output_folder])
        elif os.name == 'posix':  # For macOS and Linux
            subprocess.run(['xdg-open', self.output_folder])
    def toggle_mute(self):
        """Toggle mute state"""
        if self.is_muted:
            pygame.mixer.unpause()  # Unmute
            self.mute_button.config(text="Mute")
        else:
            pygame.mixer.pause()  # Mute
            self.mute_button.config(text="Unmute")

        self.is_muted = not self.is_muted


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = YTDLApp(root)
    root.mainloop()
