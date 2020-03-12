from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from datetime import datetime
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO


import spacy

nlp = spacy.load('en_core_web_sm')

'''
	Extracts creation date YYYY-MM-DD of a pdf present at the given path
'''
def getPdfDate(path):
	# Using metadata
	success_metadata = True
	date_metadata = ""
	try:
		def convertPdfDatetime(pdf_date_extracted):
			dtformat = "%Y%m%d%H%M%S"
			clean = pdf_date_extracted.decode("utf-8").replace("D:","").split('+')[0]
			return datetime.strptime(clean,dtformat)
		fp = open(path, 'rb')
		parser = PDFParser(fp)
		doc = PDFDocument(parser)
		date_metadata = str.split(str(convertPdfDatetime(doc.info[0]["CreationDate"])) , " ")[0]
	except:
		success_metadata = False
		pass
	finally:
		fp.close()

	# Using NER
	rsrcmgr = PDFResourceManager()
	sio = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	# Extract text
	fp = open(path, 'rb')
	for page in PDFPage.get_pages(fp):
	    interpreter.process_page(page)
	    break
	fp.close()

	# Get text from StringIO
	text = sio.getvalue()

	# Cleanup
	device.close()
	sio.close()

	parsed_text = nlp(text)
	for ent in parsed_text.ents:
		if ent.label_ == "DATE":
			date = ent.text
			break

	# Compare the dates
	
	print(date)

	return date_metadata
	

if __name__ == '__main__':
	pdf_name = "SBI_DEC_19.pdf"
	print("Date for the pdf: " + pdf_name + ": " + getPdfDate('DATA/' + pdf_name))