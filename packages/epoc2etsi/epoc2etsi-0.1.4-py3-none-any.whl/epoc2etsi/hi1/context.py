from dataclasses import dataclass
from lxml.objectify import ObjectifiedElement

@dataclass
class EpocContext:
    input_root : ObjectifiedElement
    global_case_id : str
    form_id : str
    parent_form_id : str | None
    form_obj : ObjectifiedElement
    ri_to_sp : bool
