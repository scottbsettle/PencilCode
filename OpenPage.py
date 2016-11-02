import webbrowser

def OpenPage():
	new = 2 # open in a new tab, if possible
	#url = 'http://127.0.0.1:8000/About%20Me%20website/About%20Me.html'
	url = 'http://127.0.0.1:8000/pencilcode/content/welcome.html'
	# open a public URL, in this case, the webbrowser docs
	webbrowser.open(url,new=new)
