import os 
import tika
from tika import parser
from tika import unpack
from tika import detector
from preproc.image_preproc import check_size
import fitz

ext_to_mime = {'docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
           'doc':  'application/msword',
           'jpeg': 'image/jpeg',
            'png': 'image/png',
            'pdf': 'application/pdf',
            'rtf': 'application/rtf'}
            
ext_type = {'image':['jpeg','png','pdf','']}

mime_to_ext = dict((v,k) for k,v in ext_to_mime.items())   

class ContentExtractor:
	
	def __init__(self):
		self.file = ''
		
	def extract_text(self):
		raw = parser.from_file(self.file)
		return (raw['content'], None)
	
	def extract_image_pdf(self):
		cnt = 0
		doc = fitz.open(self.file)
		for i in range(len(doc)):
			image_list = doc.getPageImageList(i)
			if image_list:
				for img in image_list:
					cnt+=1
					save_path = 'tmp/image'+str(i)
					xref = img[0]
					imf = doc.extractImage(xref)['image']
					open(save_path, 'wb').write(imf)
					if not check_size(save_path):
						os.remove(save_path)
						cnt-=1
		if cnt>0:
			return (True, ['tmp/'+i for i in os.listdir('tmp/')])
		else:
			return (False, None)
						
	
	def extract_image_txt(self):
		cnt =0
		raw = unpack.from_file(self.file)
		images = raw['attachments']
		if images:
			for i in images.keys():
				cnt+=1
				save_path = 'tmp/'+str(i)
				open(save_path, 'wb').write(images[i])
				if not check_size(save_path):
					os.remove(save_path)
					cnt-=1
		if cnt>0:
			return (True, ['tmp/'+i for i in os.listdir('tmp/')])
		else:
			return (False, None)
		
    	
	def detect_ext(self):
		raw = detector.from_file(self.file)
		return mime_to_ext[raw]


	def parse_txt(self):
		content, image_list = self.extract_text()
		images, image_list = self.extract_image_txt()
		if len(content)<200 and images:
			print('есть изображения, мало текста')
			return (images, image_list)
		elif len(content)>200:
			print('текст')
			return (content, image_list)
		else:
			print('пустой')
			return None


	def parse_pdf(self):
		content, image_list = self.extract_text()
		images, image_list = self.extract_image_pdf() 
		if content and len(content)>200:
			print('текст')
			return (content, image_list)
		elif images:
			print('изображения')
			return (images, image_list)
		else:
			print('пустой')
			return None


	def parse(self, path):
		self.file = path
		ext = self.detect_ext()
		if ext == 'pdf':
			return self.parse_pdf()
		elif ext in ['doc','docx','rtf']:
			return self.parse_txt()
		else:
			print('изображение')
			return (True, [self.file])
