import os, json, fnmatch, subprocess, tempfile
from datetime import datetime

#print("----Program Started----")

#Configuration
CWD = "./"
Model = "ggml-model-whisper-large.bin"

#Setup Errors folder
Errors = {}
Errorspath = CWD + "Errors/"
if (not os.path.exists(Errorspath)):
    os.makedirs(Errorspath, 777, True)

def getDateTimeUnderscore():
    return "{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())

#Setup Temp folder to store FFMPEG output
Whisper = CWD + "Whisper.cpp/"
if (not os.path.exists(Whisper) or not os.path.exists(Whisper + "main.exe") or not os.path.exists(Whisper + "whisper.dll")):
    print("Missing Whisper files, cannot continue.")
    Errors[getDateTimeUnderscore()] = {
                "Error":"Missing Whisper files, cannot continue.",
                "Whisper.cpp Folder": os.path.exists(Whisper),
                "main.exe": os.path.exists(Whisper) and os.path.exists(Whisper + "main.exe"),
                "Whisper.dll": os.path.exists(Whisper) and os.path.exists(Whisper + "whisper.dll")
            }
    with open(Errorspath + getDateTimeUnderscore() + "_Log.json", "w") as out:
        json.dump(Errors, out)
    exit(-1)

#Setup Temp folder to store FFMPEG output
#Temp = CWD + "Temp/"
Temp = tempfile.gettempdir()
if (not os.path.exists(Temp)):
    os.makedirs(Temp, 777, True)

#Setup Transcripts folder for output
Transcripts = CWD + "Transcripts and Summaries/"
if (not os.path.exists(Transcripts)):
    os.makedirs(Transcripts, 777, True)

#Setup Transcripts folder for output
Models = CWD + "models/"
if (not os.path.exists(Models)):
    os.makedirs(Models, 777, True)

#Command Configuration
ffmpegIn = ["-i"]
ffmpegSettings = ["-ar", "16000", "-ac", "1", "-y", "-c:a", "pcm_s16le"]
ffmpegOut = [Temp + "output.wav"]
WhisperCMD = [(Whisper + "main.exe").replace("/", "\\")]
DuplicateFix = ["-bs", "5", "-et", "2.8", "-mc", "64"]
PrintColor = ["-pc"]
OutputCmd = ["-otxt", "-of"]
InputCmd = ["-f"] + ffmpegOut
ModelCmd = ["-m", Models + Model]


Audios = {"Version":1, "Files":{ "-1":"requirements.txt"}}

#Load Manfest File
Manifest = CWD + "Manifest.json"
if (os.path.exists(Manifest)):
    with open(Manifest, "r") as input:
        Audios = json.load(input)
    #Do not summarize requirements.txt
    if(len(fnmatch.filter(list(Audios["Files"].values()), "requirements.txt")) < 1):
       Audios["Files"]["-1"] = "requirements.txt"

def W_Manifest(AudioFile):
    Audios["Files"][str(len (Audios["Files"]))] = AudioFile
    with open(Manifest, "w") as out:
        json.dump(Audios, out)

def Add_Error(Error, item):
    Errors[item] = {
                "CMD":Error.cmd,
                "Output":Error.output,
                "Error":Error.stderr,
                "Time":getDateTimeUnderscore()
            }
    
def W_Error():
    if(len(Errors) > 0):
        with open(Errorspath + getDateTimeUnderscore() + "_Log.json", "w") as out:
            json.dump(Errors, out)

files = fnmatch.filter(os.listdir(CWD), "*.wav")
files = set(files).difference(Audios["Files"].values())

if (len(files) > 0 ):
    for item in files:
        #Convert with FFMPEG
        try:
            subprocess.run(["ffmpeg" ] + ffmpegIn + [CWD + item] + ffmpegSettings + ffmpegOut, shell=True, check=True)
        except subprocess.CalledProcessError as E:
            Add_Error(E, item)
            continue
        
        Filename = item.removesuffix(".wav")
        #Run Whisper.CPP with Cuda
        try:
            subprocess.run(WhisperCMD + OutputCmd + [Transcripts + Filename] + InputCmd + ModelCmd + PrintColor + DuplicateFix, shell=True, check=True)
        except subprocess.CalledProcessError as E:
            Add_Error(E, item)
            continue

        #List in Manifest to prevent rerunning
        W_Manifest(item)

W_Error()