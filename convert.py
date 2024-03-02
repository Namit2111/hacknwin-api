from pydub import AudioSegment
import os

def convert_to_wav(input_file, output_file):
    # Load audio file
    audio = AudioSegment.from_file(input_file)

    # Convert to WAV format
    audio.export(output_file, bitrate="64k",format="wav")
    print(f"Audio file converted to {output_file}")

if __name__ == "__main__":
    # Provide the path to the input and output audio files
    input_file_path = "path_to_input_audio_file"
    output_file_path = "path_to_output_wav_file"

    # Check if the input file exists
    if not os.path.exists(input_file_path):
        print("Input file does not exist")
    else:
        # Convert audio file to WAV format
        convert_to_wav(input_file_path, output_file_path)
