# -*- coding: cp1252 -*-
import re
def escapeParenthesys(texto):
	close = 0
	while (1):
		#print "main while"
		open1 = texto.find("'", close+1)
		close = texto.find("'", open1+1)
		#print 'open '+str(open1)
		#print 'close '+str(close)
		
		if open1 == -1 or close == -1:
			return texto
		
		while (1):
			#print "small while"
			parentesis1 = texto.find('(', open1, close+1)
			parentesis2 = texto.find(')', open1, close+1)
			#print parentesis1
			#print parentesis2
			#raw_input("Press Enter to continue...")

			if parentesis1 == -1 and parentesis2 == -1:
				break
			
			texto = list(texto)

			if parentesis1 != -1:
				texto[parentesis1] = '·';
			if parentesis2 != -1:
				texto[parentesis2] = '·';
				
			texto = "".join(texto)
			

f = open("C:\MigracionesOscar\datos\sonia ramos\SONIA RAMOS PEÑIN_mn 29-07-2015.part1_20150730_140404_Comprobación_de_Datos\DocumentosJudigest.sql", 'r')
tablaAbierta = "";
reInsert = re.compile(r'.*?insert into .*? values', re.DOTALL) # ? -> no greedy
reTabla = re.compile(r'.*?insert into ([^\s]*)', re.DOTALL)
reValue = re.compile(r'(\(.*?\))')
l = ''
tabla = ''
while (True):
	#print "hola"
	if len(l) < 59000004:
		lnuevo = f.read(20000).lower()
		l += lnuevo
		#print l
		raw_input("Press Enter to continue...")
		l = escapeParenthesys(l)
		#print l
		#raw_input("Press Enter to continue...")
	if l == "":
		break
	if tabla == '':
		if lnuevo == '':
			break
		m = reTabla.match(l)
		if m == None:
			continue
		tabla = m.group(1).replace("`", "")
		
		print tabla
		output = open(tabla + ".csv", 'a')
		l = reInsert.sub("", l, 1)
		print "creado archivo " + tabla + ".csv"
	if l.find(';') != -1:
		print "hemos encontrado punto y coma;"
		valuesStr = l[:l.find(';')] # cogemos solo hasta el punto y coma
		l = l[l.find(';')+1:] # de l eliminamos lo que ya vamos a coger
		tabla = ''
	else:
		# hay que seguir parseando
		valuesStr = l;
		m = re.search(r'\([^\)]*$', l)
		if (m == None):
			print "Error near (, parenthesis between quotes not handles\n"
			print l
			l = ''
		else:
			l = m.group()
	
	values = re.findall(r'\(.*?\)', valuesStr)
	for value in values:
		#print value
		value = value.replace('(', '')
		value = value.replace(')', '')
		output.write('\n' + value) # TODO: hay que volver a reemplazar los caracteres especiales
		

				
			
