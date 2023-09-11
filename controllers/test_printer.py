import brother_ql

from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend
from brother_ql.devicedependent import models, label_type_specs, label_sizes
from brother_ql.devicedependent import ENDLESS_LABEL, DIE_CUT_LABEL, ROUND_DIE_CUT_LABEL
from brother_ql.reader import OPCODES, chunker, merge_specific_instructions, interpret_response, match_opcode
from PIL import Image
from utils.image_utils import ImageUtils

class TestPrinter():
    def __init__(self):
        selected_backend = guess_backend("file:///dev/usb/lp0")
        BACKEND_CLASS = backend_factory(selected_backend)['backend_class']
        self.__qlr = BrotherQLRaster("QL-800")
        self.__be = BACKEND_CLASS("file:///dev/usb/lp0")
        
        
    
    def print(self, image_path: str):
        tmp_img = ImageUtils.create_temp_resized_image(image_path)
        im = Image.open(tmp_img)
        create_label(self.__qlr, im, "62", red=False, threshold=10, cut=True, rotate=90, dither=True)
        self.__be.write(self.__qlr.data)
        for i in range(7):
            res = self.__be.read()
            if res != b'':
                print( interpret_response(res))
        self.__be.dispose()

        
