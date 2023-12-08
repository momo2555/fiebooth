from tenacity import retry, stop_after_attempt
import logging
from drivers import BrotherQLRaster, create_label
from drivers import backend_factory, guess_backend
#from drivers import models, label_type_specs, label_sizes
#from drivers import ENDLESS_LABEL, DIE_CUT_LABEL, ROUND_DIE_CUT_LABEL
#from drivers import OPCODES, chunker, merge_specific_instructions, interpret_response, match_opcode
from PIL import Image
from utils.image_utils import ImageUtils
from config import config

class TestPrinter():
    def __init__(self):
        selected_backend = guess_backend("file:///dev/usb/lp0")
        BACKEND_CLASS = backend_factory(selected_backend)['backend_class']
        self.__qlr = BrotherQLRaster("QL-800")
        self.__be = BACKEND_CLASS("file:///dev/usb/lp0")
        self.__logger = logging.getLogger("fiebooth")
        
    def print(self, image_path: str):
        self.__print(image_path)
        pass

    def __print(self, image_path: str):
        try:
            #tmp_img = ImageUtils.create_temp_resized_image(image_path)
            brightness = 1 + (config.brightness+config.brightness_default)/6
            contrast = 1 + (config.contrast+config.contrast_default)/6
            scale = (config.width_printer, config.height_printer)
            im = ImageUtils.image_transform(image_path, contrast, brightness, scale, config["user_text"])
            #im = Image.open(tmp_img)
            create_label(self.__qlr, im, "62", red=False, threshold=10, cut=True, rotate=90, dither=True)
            self.__be.write(self.__qlr.data)
            # for i in range(7):
            #     res = self.__be.read()
            #     if res != b'':
            #         print( interpret_response(res))
            self.__be.dispose()
            config["total_prints_len"] = config["total_prints_len"] + 1
            config["user_prints_len"] = config["user_prints_len"] + 1
        except Exception as e:
            self.__logger.warning("Printer Error")
            

    
        

        
