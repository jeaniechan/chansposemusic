from flask import Flask, render_template, make_response, request, redirect, url_for
from convert import *
import json
import requests
import music21 as m
from music21 import *
from werkzeug.utils import secure_filename
import os


app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    app.route('/')
    if request.method=='POST':
    	selectedValue=request.form['newkey']
    	selectedFile=request.form['myfile']
    return render_template("home.html")

@app.route('/display')
def display():
	return render_template('display.html')
@app.route('/wrongfile')
def wrongfile():
	return render_template('wrongfile.html') 
@app.route('/error')
def error():
	return render_template('error.html')
@app.route('/output',methods=['GET','POST'])
def output():
	selectedValue = request.values.get('newkey')
	if str(selectedValue)=="None":
		return redirect(url_for('error'))
	possiblekeys=['cMam','c#Mb-m','dMbm','e-Mcm','eMc#m','fMdm','f#Me-m','gMem','a-Mfm','aMf#m','b-Mgm','bMa-m']
	new_index=possiblekeys.index(selectedValue)
	fileuploaded=request.files['myfile']
	byte_stream = fileuploaded.stream.read()
	if str(byte_stream)=="b''":
		return redirect(url_for('error'))
	if str(fileuploaded.filename[len(str(fileuploaded.filename))-3:])!='mid' and str(fileuploaded.filename[len(str(fileuploaded.filename))-3:])!='xml':
		return redirect(url_for('wrongfile'))
	song=m.converter.parse(byte_stream)
	print(type(song))
	print('Done parsing')
	old_index=new_index
	for keysig in song.recurse().getElementsByClass('KeySignature'):
		if str(keysig)=='C major' or str(keysig)=='a minor':
			old_index=0
		elif str(keysig)=='C# major' or str(keysig)=='b- minor':
			old_index=1
		elif str(keysig)=='D major' or str(keysig)=='b minor':
			old_index=2
		elif str(keysig)=='E- major' or str(keysig)=='c minor':
			old_index=3
		elif str(keysig)=='E major' or str(keysig)=='c# minor':
			old_index=4
		elif str(keysig)=='F major' or str(keysig)=='d minor':
			old_index=5
		elif str(keysig)=='F# major' or str(keysig)=='e- minor':
			old_index=6
		elif str(keysig)=='G major' or str(keysig)=='e minor':
			old_index=7
		elif str(keysig)=='A- major' or str(keysig)=='f minor':
			old_index=8
		elif str(keysig)=='A major' or str(keysig)=='f# minor':
			old_index=9
		elif str(keysig)=='B- major' or str(keysig)=='g minor':
			old_index=10
		else:
			old_index=11
		break
	t = new_index-old_index	
	transposenotes(song,t)
	changekeysig(song,t)

	if request.method == 'POST':
		
		osmd_js_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"opensheetmusicdisplay.min.js.txt")
		html_template=''
		osmd_js_path = pathlib.Path(osmd_js_file).as_uri()
		filename = song.write('musicxml')
		print(filename)
		if filename is not None:
			with open(filename,'r') as f:
				xmldata = f.read()
			with open(filename+'.html','w') as f_html:
				html = html_template.format(
					data=xmldata.replace('`','\\`'),
					osmd_js_path=osmd_js_path)
				f_html.write(html)
		print('Show HTML')
		return render_template("show.html",data=json.dumps(xmldata))
	
	

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=False)
    
