__version__ = '0.1'
__author__ = 'Ying Dai'


from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__, __cake__

from .crf_model import CRF
from .convert_data import convert
from .convert_data import crf2human
