from extraction.content_extract import ContentExtractor
from extraction.OCR.ocr import OCR
import os

class TextExtractor:
	
	def __init__(self):
		self.file = ''
		self.content = ContentExtractor()
		self.ocr = OCR()
		self.text = []
		
	def extract_text(self, path):
		self.file = path
		res, image_list = self.content.parse(self.file)
		print(image_list)
		if res == True: # image_to_ocr
			self.text = self.ocr.extract_text(image_list[0])
			for i in image_list:
				os.remove(i)
			return self.text
		elif type(res)==str: #text to cv fields
			self.text = res
			return self.text
		else:
			return 'Error'
			
			
