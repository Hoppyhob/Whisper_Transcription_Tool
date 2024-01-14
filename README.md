# Whisper.cpp Transcription tool
 This tool was created to use Whipser.cpp to transcribe DND recording audios.
 The purpose is to have a windows task that can call this program and will pick up and transcribe any wav audio files while keeping track and skipping audio files that have already run.
## How to use
 See Models and Whisper.cpp to setup necessary files
 Place Audios in same folder as Main.py 
 Run with "Python3 ./Main.py"
 A Transcripts and Summaries folder will be generated and transcripts will be placed there.
# Models
You can find compatible models at https://huggingface.co/ggerganov/whisper.cpp/tree/main
Place the downloaded model in the models folder and change the Model variable in Main.py to match the model name.
# Whisper.cpp
You can find the whisper.cpp release at https://github.com/ggerganov/whisper.cpp/releases
Add whisper.dll and main.exe to the Whisper.cpp folder.

Instructions to build whisper.cpp on windows with Cuda
https://github.com/ggerganov/whisper.cpp/issues/878#issuecomment-1586192170

Fixing Cuda Compile issues if you have Build tools installed
https://stackoverflow.com/questions/56636714/cuda-compile-problems-on-windows-cmake-error-no-cuda-toolset-found
