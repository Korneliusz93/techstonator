#!/usr/local/bin/python3
#zaimportowanie modulu random odpowiadajacego za losowanie
import random
from flask import Flask, redirect
from flask import render_template
from flask import request
from flask import current_app
from flask_bootstrap import Bootstrap
app = Flask(__name__) #ustawienie srodowiska produkcyjny
bootstrap = Bootstrap(app)
@app.route('/redirMilosz')
def redirMilosz():
	return redirect('https://pl.wikipedia.org/wiki/Czesław_Miłosz')
@app.route('/redirGenLit')
def redirGenLit():
	return redirect('https://en.wikipedia.org/wiki/Digital_poetry')
@app.route('/')
def greet():
	return render_template('homepage.html')
@app.route('/index')
def index():

	czyste_dane_podmioty = open("./podmioty.txt").readlines()
	dane_podmioty = czyste_dane_podmioty[0]
	podmiot = dane_podmioty.split()

#if end is:
#(a)	l.p.z. 	gr1
#(i/y)	l.m.	gr2
#(o)	l.p.r.n.gr3
#(*)	l.p.m.  gr4

	czyste_dane_orzeczenia = open("./orzeczenia.txt").readlines()
	dane_orzeczenia = czyste_dane_orzeczenia[0]
	orzeczenie = dane_orzeczenia.split()

#gr1 end != ł,ą,o
#gr2 end = ą
#gr3 end = ą
#gr4 end != ą

	czyste_dane_przydawki = open("./przydawki.txt").readlines()
	dane_przydawki = czyste_dane_przydawki[0]
	przydawka = dane_przydawki.split()

	czyste_dane_dopelnienia = open("./dopelnienia.txt").readlines()
	dane_dopelnienia = czyste_dane_dopelnienia[0]
	dopelnienie = dane_dopelnienia.split()

	def divideFractions(strng):
		contrl_lst=['w','na','do','ze','nad','od','z']
		wyrazenie = ""
		strng_div = []
		for ch in strng:
			if ch.isalpha() is True:
				wyrazenie = wyrazenie + ch
			else:
				if wyrazenie in contrl_lst:
					wyrazenie = wyrazenie + ' '
				else:
					strng_div.append(wyrazenie)
					wyrazenie = ""
		return strng_div

	czyste_dane_okoliczniki = open("./okolicznik.txt").readlines()
	dane_okoliczniki = czyste_dane_okoliczniki[0]
	okolicznik = divideFractions(dane_okoliczniki)

	class Poem():
		def __init__(self):
			self.poem = []
		def appendWord(self,wrd):
        		self.poem.append(wrd)
		def getPoem(self):
        		puzzles = self.poem[:]
        		poetry = []
        		for element in puzzles:
        			construction=''
        			for part in element:
        				construction = construction+' '+part
        			poetry.append(construction)
        		return poetry
	class Words(Poem):
		def __init__(self):
			self.phrase = ''
			self.v = ''
		def createClassicExpression(self,line_position,ending = ''):
			if line_position is 0: self.phrase = random.choice(przydawka)
			if line_position is 1:
				self.phrase = random.choice(podmiot)
				self.v = self.phrase
			if line_position is 2:
				if self.v[-1] == 'a':
					self.phrase = random.choice(orzeczenie)
					while self.phrase[-1] in 'łąo':
						self.phrase = random.choice(orzeczenie)
				if self.v[-1] in 'iyo':
					self.phrase = random.choice(orzeczenie)
					while self.phrase[-1] != 'ą':
						self.phrase = random.choice(orzeczenie)
				else:
					self.phrase = random.choice(orzeczenie)
					while self.phrase[-1] == 'ą':
						self.phrase = random.choice(orzeczenie)
			if line_position is 3:
             			self.phrase = random.choice(dopelnienie)
			if line_position is 4:
				self.phrase = random.choice(okolicznik)
		def produceClassicPoem(self):
         		#n_o_w = int(input('Podaj ilosc wyrazow '))
         		#n_o_l = int(input('Podaj ilosc linii '))
			n_o_w = 5
			n_o_l = 5
			piece = Poem()
			expression = Words()
			for i in range(n_o_l):
				line = []
				for i in range(n_o_w):
					expression.createClassicExpression(len(line))
					line.append(expression.phrase)
				piece.appendWord(line)
			return piece.getPoem()
	W_list = Words()
	art_piece = W_list.produceClassicPoem()
	return render_template('index.html',art_piece=art_piece)
@app.route('/about')
def about():
	return render_template('about.html')
if __name__ == '__main__':
	app.run()
