from .pdf2image import convert_from_path

class ScienceOCR:
	def __init__(self, use_gpu: bool = True):
		if not use_gpu:
			import os
			os.environ["TORCH_DEVICE"] = "cpu"
			
		from .engine import SuryaOCREngine

		self.engine = SuryaOCREngine()

	def parse_text(self, path, first_page=0, last_page=None, dpi=196):
		raw_images = convert_from_path(path, dpi=dpi, first_page=first_page, last_page=last_page)
		full_text = self.engine.layout_driven_ocr(raw_images)

		return full_text

