# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
import os
import os.path
import subprocess

def pause():
    scriptdir=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'caster'),'stream2chromecast.py')
    generalparams = ' -devicename ' + sys.argv[2] + ' -pause'
    cmd = '/usr/bin/python ' +scriptdir + generalparams
    print cmd
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def volup():
    scriptdir=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'caster'),'stream2chromecast.py')
    generalparams = ' -devicename ' + sys.argv[2] + ' -volup'
    cmd = 'sudo /usr/bin/python ' +scriptdir + generalparams
    print cmd
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def voldown():
    scriptdir=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'caster'),'stream2chromecast.py')
    generalparams = ' -devicename ' + sys.argv[2] + ' -voldown'
    cmd = '/usr/bin/python ' +scriptdir + generalparams
    print cmd
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def volume():
    scriptdir=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'caster'),'stream2chromecast.py')
    generalparams = ' -devicename ' + sys.argv[2] + ' -setvol ' + sys.argv[3]
    cmd = '/usr/bin/python ' +scriptdir + generalparams
    print cmd
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def joue():
    # sys.argv[1] action joue/volume 
    # sys.argv[2] deviceIP
    # sys.argv[3] text ou vol ou fichier
    # sys.argv[4]     # sy;s.argv[4] local web root url 
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__) ,'caster')))
    from stream2chromecast import playurl
    playurl(sys.argv[4]+'/plugins/gcast/sound/'+sys.argv[3]+'.mp3' , device_name=sys.argv[2])
    #file = sys.argv[3]+'.mp3'
    #urltoplay='-playurl '+sys.argv[4]+'/plugins/gcast/sound/'+file  
    #scriptdir=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'caster'),'stream2chromecast.py')
    #generalparams = ' -devicename ' + sys.argv[2] + ' ' + urltoplay 
    #cmd = '/usr/bin/python ' +scriptdir + generalparams
    #print cmd
    #proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    #(out, err) = proc.communicate()
    #return out

    
def parle():
    cachepath=os.path.abspath(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp'), 'cache'))
    tmppath=os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp'))
    try:
        os.stat(tmppath)
    except:
        os.mkdir(tmppath)
    import hashlib
    file = hashlib.md5(sys.argv[3]+sys.argv[5]+sys.argv[6]).hexdigest()
    found = 0
    filename=os.path.join(cachepath,'tts.wav')
    filenamemp3=os.path.join(cachepath,file+'.mp3')
    if not os.path.isfile(filenamemp3):
        try:
            os.stat(cachepath)
        except:
            os.mkdir(cachepath)
        from pydub import AudioSegment
        if sys.argv[6]== 'picotts':
            os.system('pico2wave -l '+sys.argv[5]+' -w '+filename+ ' "' +sys.argv[3]+ '"')
            song = AudioSegment.from_wav(filename)
        elif sys.argv[6]== 'webserver':
            import requests
            filetts = requests.get('http://192.168.1.56:8089/?method=getTTS&text='+sys.argv[3]+'&voice=voxygen.tts.helene')
            output = open(filename,'wb')
            output.write(filetts.content)
            output.close()
            song = AudioSegment.from_wav(filename)
        else:
            from gtts import gTTS
            tts = gTTS(text=sys.argv[3].decode('utf-8'), lang=sys.argv[5])
            tts.save(filenamemp3)
            song = AudioSegment.from_mp3(filenamemp3)
        song.export(filenamemp3, format="mp3", bitrate="128k", tags={'albumartist': 'Jeedom', 'title': 'TTS', 'artist':'Jeedom'}, parameters=["-ar", "44100","-vol", "200"])
    urltoplay=sys.argv[4]+'/plugins/gcast/tmp/cache/'+file+'.mp3'
    scriptdir=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'caster'),'stream2chromecast.py')
    generalparams = ' -devicename ' + sys.argv[2] + ' ' + filenamemp3 
    cmd = '/usr/bin/python ' +scriptdir + generalparams
    print cmd
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def oogtomp3():
    from pydub import AudioSegment
    song = AudioSegment.from_ogg(sys.argv[2]+'.ogg')
    song.export(sys.argv[2]+'.mp3', format="mp3", bitrate="128k", tags={'albumartist': 'Jeedom', 'title': 'Sound', 'artist':'Jeedom'}, parameters=["-ar", "44100","-vol", "200"])
    os.remove(sys.argv[2]+'.ogg')

def webmtomp3():
    from pydub import AudioSegment
    song = AudioSegment.from_file(sys.argv[2]+'.webm','webm')
    song.export(sys.argv[2]+'.mp3', format="mp3", bitrate="128k", tags={'albumartist': 'Jeedom', 'title': 'Sound', 'artist':'Jeedom'}, parameters=["-ar", "44100","-vol", "200"])
    os.remove(sys.argv[2]+'.webm')

actions = {
           "pause" : pause,
           "volup" : volup,
           "voldown" : voldown,
           "joue" : joue,
           "parle" : parle,
           "volume" : volume,
           "oogtomp3" : oogtomp3,
           "webmtomp3" : webmtomp3,
}
actions[sys.argv[1]]()
