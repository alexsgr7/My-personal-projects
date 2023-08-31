import tkinter as tk
from tkinter import filedialog
import pygame
from tkinter import ttk


class MediaPlayer:

    def __init__(self, root):

        self.root = root
        self.music_playing = False
        self.current_media = None
        self.queue = []
        pygame.init()

        self.play_pause_button = tk.Button(root, text="Play/Pause", command=self.play_pause_function)
        self.play_pause_button.pack()
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_function)
        self.stop_button.pack()
        self.next_song_button = tk.Button(root, text="Next", command=self.next_song_function)
        self.next_song_button.pack()
        self.previous_song_button = tk.Button(root, text='Previous', command=self.previous_song_function)
        self.previous_song_button.pack()
        self.to_queue_button = tk.Button(root, text="Add to queue", command=self.add_to_queue_function)
        self.to_queue_button.pack()
        self.remove_from_button = tk.Button(root, text="Remove from queue", command=self.remove_from_queue_function)
        self.remove_from_button.pack()
        self.open_file_button = tk.Button(root, text="Open File", command=self.open_file_dialog)
        self.open_file_button.pack()

        self.media_window = None
        self.media_label = tk.Label(self.media_window, text="Media Display")
        self.media_label.pack()

        self.queue_window = None
        self.queue_label = tk.Label(self.queue_window, text="My queue")
        self.queue_label.pack()

        self.progress_bar_widget = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")
        self.progress_bar_widget.pack(side="bottom")

        self.update_progress()

    def play_pause_function(self):

        if self.current_media:
            if not self.music_playing:  # Load and play if not playing
                pygame.mixer.music.load(self.current_media)
                pygame.mixer.music.play()
                self.music_playing = True
                self.play_pause_button.config(text="Pause")  # Update button text
                self.update_progress()
            else:  # Pause if already playing
                pygame.mixer.music.pause()
                self.music_playing = False
                self.play_pause_button.config(text="Play")  # Update button text

    def stop_function(self):

        pygame.mixer.music.stop()
        self.music_playing = False
        self.play_pause_button.config(text="Play")  # Update button text

    def update_progress(self):
        if self.music_playing:
            current_position = pygame.mixer.music.get_pos()
            minutes = current_position // 60000
            seconds = (current_position // 1000) % 60

            if self.media_window and self.media_label:
                self.media_label.config(text=f"Media Display - {minutes:02d}:{seconds:02d}")

            self.progress_bar_widget["value"] = current_position
            self.root.after(1000, self.update_progress)

    def next_song_function(self):

        if self.current_media:
            current_index = self.queue.index(self.current_media)
            next_index = (current_index + 1) % len(self.queue)  # Circular queue behavior
            next_music = self.queue[next_index]
            self.current_media = next_music
            self.display_media(next_music)

    def previous_song_function(self):

        if self.current_media:
            current_index = self.queue.index(self.current_media)
            previous_index = (current_index - 1) % len(self.queue)  # Circular queue behavior
            previous_music = self.queue[previous_index]
            self.current_media = previous_music
            self.display_media(previous_music)

    def add_to_queue_function(self):

        if self.current_media:
            self.queue.append(self.current_media)
            self.to_queue_button.config(text="Added to queue")

    def remove_from_queue_function(self):

        if self.current_media:
            if self.current_media in self.queue:
                self.queue.remove(self.current_media)
                self.remove_from_button.config(text="Removed from queue")

    def open_file_dialog(self):

        file_path = filedialog.askopenfilename(filetypes=[("Audio/Video Files", "*.mp3 *.mp4")])
        if file_path:
            self.current_media = file_path
            self.display_media(file_path)

    def display_media(self, media_path):

        if self.media_window is None:
            self.media_window = tk.Toplevel(self.root)
            self.media_label = tk.Label(self.media_window, text="Media Display")
            self.media_label.pack()
        self.media_label.config(text=media_path)

    def __del__(self):

        pygame.quit()


def main():

    root = tk.Tk()
    MediaPlayer(root)
    root.mainloop()


if __name__ == "__main__":

    main()
