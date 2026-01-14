import requests
import time
import logging
import json
import re
import requests
from pathlib import Path
import psutil
import signal
import os
import time
import subprocess
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import re
import datetime
import io
from pydub import AudioSegment
from livekit.plugins.azure import STT, TTS
import azure.cognitiveservices.speech as speechsdk
import  glob
from livekit import rtc
import wave
import asyncio
import fasttext
import numpy as np
from langdetect import detect
logger = logging.getLogger("info")
    
def detect_lang(text,sd):
    try:
        model = fasttext.load_model(sd['lang_detect_model'])
        lang = model.predict(text, k=1)[0][0].replace("__label__", "")
        logger.info(f"#### fasttext ####  Detected: {lang} ")
        # ✅ Convert safely with NumPy 2
        
        return lang
    except Exception:
        lang = detect(text)
        logger.info(f"#### detect ####  Detected: {lang} ")
        return lang
        
            
def del_wav(path):
    
    os.remove(path)



url_pattern = re.compile(
    r'^(https?:\/\/)?'                 # http:// or https:// (optional)
    r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain name
    r'(\/\S*)?$'                       # optional path
)


def has_non_arabic(text: str) -> bool:
    return bool(re.search(r'[A-Za-z]', text))
 
def is_url(text: str) -> bool:
    return re.match(url_pattern, text) is not None

def url_responds_ok(url: str, timeout: int = 5) -> bool:
    """Check if URL returns status code 200."""
    if not is_url(url):
        return False
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        if response.status_code == 200:
            return True
        # Fallback: some servers don't handle HEAD requests properly
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False


async def safe_get_api_response(text, thread_id, agent_id,room_id,sd,timeout=300,tts='azure'):
    try:
        # Run in thread to avoid blocking the event loop
        return await asyncio.wait_for(
            asyncio.to_thread(get_api_response, text, thread_id,agent_id,room_id,sd,tts),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        
        res={"answer": ["عذرًا، تأخر الرد قليلاً، يرجى المحاولة مرة أخرى."], "thread_id": thread_id,"agent_id":agent_id}
        res['answer']=per_answer(res['answer'])
        waffile=f"{sd["audio_sys_path"]}/ex_timeout__11.wav"

        if tts=='azure':
            x =azure_tts_to_wav(" ".join(res['answer']),waffile,sd,True)
        elif tts=='11lab':
            x =elevenlabs_tts_to_wav(" ".join(res['answer']),waffile,sd['ElevenLabs_key'])
        res['audio_buffer']=x
        return res
    except Exception as e:
        logger.exception("Error in get_api_response")
        res= {"answer": ["حدث خطأ أثناء معالجة الطلب."], "thread_id": thread_id,"agent_id":agent_id}
        res['answer']=per_answer(res['answer'])
        waffile=f"{sd["audio_sys_path"]}/ex_timeout__11.wav"
        if tts=='azure':
            x =azure_tts_to_wav(" ".join(res['answer']),waffile,sd,True)
        elif tts=='11lab':
            x =elevenlabs_tts_to_wav(" ".join(res['answer']),waffile,sd['ElevenLabs_key'])
        res['audio_buffer']=x
        return res





def per_answer(val):
    val=str(val).strip()
    cleaned = re.sub(r"[^\w\s]", "", val)      
    cleaned = re.sub(r"[\r\n]+", " ", cleaned) 
    mx=5
    res=[]
    tl=cleaned.strip().split(" ")
    for n,i in enumerate(range(0,len(tl),mx)):
        
        x_ch=tl[i:i+mx]
        res.append(" ".join(x_ch))
    
    return res

def get_audio(fpath,test=False):
    with wave.open(str(fpath), 'rb') as wav_file:
        num_channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())

    audio_frame = rtc.AudioFrame(
        data=frames,
        sample_rate=sample_rate,
        num_channels=num_channels,
        samples_per_channel=wav_file.getnframes()
    )

    return audio_frame

def elevenlabs_tts_to_wav(text: str, output_path: str, api,voice_id= "yrPIy5b3iLnVLIBfUSw8") :
    """
    Convert text to speech using ElevenLabs API, save as .wav file,
    and return the audio as an in-memory BytesIO buffer.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/wav",
        "Content-Type": "application/json",
        "xi-api-key": api,
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # Arabic supported here
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8,
        }
    }

    # === Call ElevenLabs API ===
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs TTS failed: {response.status_code} - {response.text}")

    # === Save to WAV file ===
    with open(output_path, "wb") as f:
        f.write(response.content)
    sound = AudioSegment.from_file(output_path)  
    sound.export(output_path, format="wav")
    print(f"✅ Audio saved at: {output_path}")

    # === Load into BytesIO ===
    audio_buffer = io.BytesIO(response.content)

    audio_frame=get_audio(output_path)
    return audio_frame

def azure_tts_to_wav(text: str,output_path,sd,sys_ins=False,test=False) :
    """
    Convert text to speech using Azure TTS, save it as a .wav file,
    and return the audio as an in-memory BytesIO buffer.
    """
    # === Azure Speech Config ===
    logger.info("=== Azure Speech Config === 1")
    if sys_ins==False:
        speech_config = speechsdk.SpeechConfig(
            subscription=sd["AZURE_SPEECH_KEY"],
            region=sd["AZURE_SPEECH_REGION"]
        )
        logger.info("=== Azure Speech Config === 2")
        speech_config.speech_synthesis_voice_name = "ar-EG-SalmaNeural"
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )
        logger.info("=== Azure Speech Config === 3")
        # === Let Azure write directly to a WAV file ===
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        logger.info("=== Azure Speech Config === 4")
        # === Generate speech ===
        result = synthesizer.speak_text_async(text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise RuntimeError(f"Azure TTS failed: {result.reason}")
        logger.info("=== Azure Speech Config === 5")
        print(f"✅ Audio saved at: {output_path}")
        
        # === Load into BytesIO ===
        with open(output_path, "rb") as f:
            audio_buffer = io.BytesIO(f.read())
        logger.info("=== Azure Speech Config === 6")
    dir_path, filename = os.path.split(output_path)
    audio_frame=get_audio(output_path,test)
    del_wav(output_path)
    return audio_frame

    
    



def get_api_response(user_text: str,thred_id: str,agent_id: str,room_id: str,sd,tts) -> str:

   
    lang=detect_lang(user_text,sd)    
    logger.info(f"""##########      LLLLLL
                        
                        {user_text} --

                        {lang}
                        
                        #######################""")
    
    ar_cheek = has_non_arabic(user_text)
    if ar_cheek ==True:
        res= {"answer":["تعرف خاطئ علي الصوت . برجاء اعادة السؤال"],
                "agent_id":"",
                "thread_id":""}
    elif sd["op_type"]==1:
          
        payload= {
        "message": user_text,
        "agent_id": str(agent_id),
        "thread_id": str(thred_id)
        }
        #payload = {
        #"query": user_text
        #}

        headers = {
            "Content-Type": "application/json"
        }

        response_ =  requests.post(sd['LLM_API'], json=payload, headers=headers,timeout=120)
        logger.info(f"""
                ###############
                # 
                #  API
                            

                            {response_}
                # ###################""")
        
        t1=datetime.datetime.now()
        response_=response_.json()
        t2=datetime.datetime.now()
        logger.info(f""" ####  request time


        {(t2 - t1).total_seconds()}


        """)
        res={}
        for i in sd['fields']:
            res[i]= response_[i]
        logger.info(f"""res     {res}""")
        logger.info(f"""final res 
        
        
        {res['answer']}
                    """)
        res['answer']=per_answer(res['answer'])

        logger.info("##########   azure_tts_say  ##########")
        # === 1. Azure Speech Config ===
        logger.info(f"##########   azure_tts_say  ########## {1}")
        
    waffile=f"{sd["audio_path"]}/{res['thread_id']}_{res['agent_id']}_{room_id}.wav"

    if tts=='azure':
        x =azure_tts_to_wav(" ".join(res['answer']),waffile,sd)
    elif tts=='11lab':
        x =elevenlabs_tts_to_wav(" ".join(res['answer']),waffile,sd['ElevenLabs_key'])
    res['audio_buffer']=x
    return res
    
        
    


