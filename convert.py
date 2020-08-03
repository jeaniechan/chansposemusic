
#Website
#API to connect server+client

import music21 as m
from music21 import *
import webbrowser, os, random, pathlib
import xml.etree.ElementTree as ET
#from website import *

song = m.converter.parse('convertkey.xml')
print(song)

osmd_js_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"opensheetmusicdisplay.min.js.txt")

def getPitch(x):
    note = str(x.pitch)
    return note
t=1
def transposenotes(song,t):
    listoforiginal=[]
    listoftransposednotes=[]
    for a in song.recurse().notes:
        if (a.isNote):
            x = a;
            s = note.Note(getPitch(x));
            listoforiginal+=[s]
            a.transpose(t,inPlace=True)
            listoftransposednotes += [a]
            #print(listoforiginal)    
        if (a.isChord):
    	    for x in a._notes:
    	        s = note.Note(getPitch(x));
    	        x.transpose(t,inPlace=True)
    	        listoftransposednotes += [x]
        print(a)

    print(listoforiginal)
    print('transposed')
    print(listoftransposednotes)
transposenotes(song,t)
def changekeysig(song,t):
    for keysig in song.recurse().getElementsByClass('KeySignature'):
    	keysig.transpose(t,inPlace=True)
    return keysig
changekeysig(song,t)

def stream_to_web(song):
    html_template = """
    <html>
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />
            <title>Music21 Fragment</title>
            <script src="{osmd_js_path}"></script>
        </head>
        <body>
            <span>may take a while to load large XML...<span>
            <div id='main-div'></div>
            <pre id='xml-div'></pre>
            <script>
            var data = `{data}`;
            function show_xml() {{
                document.getElementById('xml-div').textContent = data;
            }}

              var openSheetMusicDisplay = new opensheetmusicdisplay.OpenSheetMusicDisplay("main-div");
              openSheetMusicDisplay
                .load(data)
                .then(
                  function() {{
                    console.log(openSheetMusicDisplay.render());
                  }}
                );
            </script>
        </body>

    """

    osmd_js_path = pathlib.Path(osmd_js_file).as_uri()

    filename = song.write('musicxml')
    print("mysicXML filename:",filename)
    print(osmd_js_path)
    if filename is not None:
        with open(filename,'r') as f:
            xmldata = f.read()
        with open(filename+'.html','w') as f_html:
            html = html_template.format(
                data=xmldata.replace('`','\\`'),
                osmd_js_path=osmd_js_path)
            f_html.write(html)
        
        webbrowser.open('file://' + os.path.realpath(filename+'.html'))

def return_xml(file):
    song = m.converter.parse('convertkey.xml')

    osmd_js_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"opensheetmusicdisplay.min.js.txt")

    osmd_js_path = pathlib.Path(osmd_js_file).as_uri()

    filename = song.write('musicxml')
    print("mysicXML filename:",filename)
    print(osmd_js_path)
    if filename is not None:
        with open(filename,'r') as f:
            xmldata = f.read()
    return xmldata

#stream_to_web(song)

# Copyright (c) 2006-2020, Michael Scott Cuthbert and cuthbertLab
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the names music21, Michael Scott Cuthbert, cuthbertLab nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Cuthbert OR cuthbertLab BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

