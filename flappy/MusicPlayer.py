import wave
import pyaudio
import threading


class MusicPlayer:
    """A simple music player to play and stop WAV files."""

    def __init__(self, file_path):
        self.file_path = file_path
        self._is_playing = False
        self._playback_thread = None
        self._audio_stream = None
        self._audio_player = pyaudio.PyAudio()
        self._wav_file = None

    def _play_loop(self):
        """Private method to play the WAV file in a loop."""
        try:
            # Open the WAV file
            self._wav_file = wave.open(self.file_path, 'rb')

            # Open the audio stream
            self._audio_stream = self._audio_player.open(
                format=self._audio_player.get_format_from_width(self._wav_file.getsampwidth()),
                channels=self._wav_file.getnchannels(),
                rate=self._wav_file.getframerate(),
                output=True
            )

            # Play in a loop while _is_playing is True
            while self._is_playing:
                self._wav_file.rewind()  # Start playback from the beginning
                data = self._wav_file.readframes(1024)
                while data and self._is_playing:
                    self._audio_stream.write(data)
                    data = self._wav_file.readframes(1024)
        except Exception as e:
            print(f"Error during playback: {e}")
        finally:
            # Cleanup
            self._cleanup()

    def play(self):
        """Starts playing the WAV file in a loop."""
        if not self._is_playing:
            print(f"Starting playback: {self.file_path}")
            self._is_playing = True
            self._playback_thread = threading.Thread(target=self._play_loop, daemon=True)
            self._playback_thread.start()
        else:
            print("Music is already playing.")

    def stop(self):
        """Stops playing the WAV file."""
        if self._is_playing:
            print("Stopping playback.")
            self._is_playing = False
            if self._playback_thread:
                self._playback_thread.join()  # Wait for the playback thread to finish
        else:
            print("Music is not playing.")

    def _cleanup(self):
        """Closes audio resources."""
        if self._audio_stream:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
        if self._wav_file:
            self._wav_file.close()
        self._audio_stream = None
        self._wav_file = None

    def __del__(self):
        """Ensure resources are released when the object is deleted."""
        self._cleanup()
        if self._audio_player:
            self._audio_player.terminate()


# Example Usage
if __name__ == "__main__":
    music_player = MusicPlayer("background_music.wav")  # Replace with your WAV file path

    try:
        music_player.play()
        print("Press Ctrl+C to stop the program.")
        while True:
            pass  # Keep the main program alive
    except KeyboardInterrupt:
        music_player.stop()
