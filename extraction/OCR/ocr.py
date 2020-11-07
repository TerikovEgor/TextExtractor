import easyocr


class OCR:

	def __init__(self):
		self.reader = easyocr.Reader(['ru','en'], gpu=True, model_storage_directory ='extraction/OCR/src/model/', download_enabled=False)
		
	def extract_text(self, path):
		print(path)
		bounds = self.reader.readtext(path,workers = 4, contrast_ths=0.6, adjust_contrast = 0.6,width_ths = 3.0, text_threshold=0.8, height_ths = 0.7, slope_ths = 0.2,detail = 0)
		return bounds
