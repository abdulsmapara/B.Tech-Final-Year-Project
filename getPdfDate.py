from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from datetime import datetime

def getPdfDate(path):
	def convertPdfDatetime(pdf_date_extracted):
	    dtformat = "%Y%m%d%H%M%S"
	    clean = pdf_date_extracted.decode("utf-8").replace("D:","").split('+')[0]
	    return datetime.strptime(clean,dtformat)
	fp = open(path, 'rb')
	parser = PDFParser(fp)
	doc = PDFDocument(parser)
	fp.close()
	return str.split(str(convertPdfDatetime(doc.info[0]["CreationDate"])) , " ")[0]

if __name__ == '__main__':
	pdf_name = "SBI_DEC_19.pdf"
	print("Date for the pdf: " + pdf_name + ": " + getPdfDate('DATA/' + pdf_name))