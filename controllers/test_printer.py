import brother_ql
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend
from brother_ql.devicedependent import models, label_type_specs, label_sizes
from brother_ql.devicedependent import ENDLESS_LABEL, DIE_CUT_LABEL, ROUND_DIE_CUT_LABEL
from PIL import Image

class TestPrinter():
    def __init__(self):
        selected_backend = guess_backend("file:///dev/usb/lp0")
        BACKEND_CLASS = backend_factory(selected_backend)['backend_class']
        qlr = BrotherQLRaster("QL-800")
        im = Image.open(r"/tmp/fiebooth/fb_1694349238.png")
        create_label(qlr, im, "29", red=False, threshold=70, cut=True, rotate=90)
        be = BACKEND_CLASS("file:///dev/usb/lp0")
        be.write(qlr.data)
        be.dispose()
        
