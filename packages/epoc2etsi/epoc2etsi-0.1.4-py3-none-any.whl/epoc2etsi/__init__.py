import logging
from uuid import uuid4
from pathlib import Path
from sys import argv, stdin, stderr
from datetime import datetime
from pprint import pformat

import argparse

from lxml import objectify, etree

from .hi1.generators import *
from .hi1.helpers import etsify_datetime
from .xml import xml
from .hi1.context import EpocContext

from .forms import form1, form2, form3, form5, form6

sender_cc = "XX"
sender_id = "RI_API"
receiver_cc = "XX"
receiver_id = "ServiceProviderID"

def main() -> None:
    args = argparse.ArgumentParser()
    args.add_argument("input", type=argparse.FileType("r"), default=stdin, help = "Path to input file, or '-' to read from stdin")
    args.add_argument("-v", "--verbose", action="count", default=0)
    pargs = args.parse_args(argv[1:])

    log_level = logging.WARNING
    match pargs.verbose:
        case 0:
            log_level = logging.WARNING
        case 1: 
            log_level = logging.INFO
        case _ if pargs.verbose >= 2:
            log_level = logging.DEBUG

    logging.basicConfig(stream=stderr, level=log_level)
    logging.info(f"Verbosity: {pargs.verbose}")
    logging.debug(f"Input arguments: {pargs}")

    logging.info(f"Parsing {pargs.input}")
    input_obj = objectify.parse(pargs.input, parser=None)

    _input_root = input_obj.getroot()
    ctx = EpocContext(
        input_root = _input_root,
        global_case_id = _input_root.globalCaseId.text,
        form_id = _input_root.formId,
        parent_form_id = str(_input_root.parentFormId) if hasattr(_input_root, "parentFormId") else None,
        form_obj = _input_root.form.getchildren()[0],
        ri_to_sp = True
    )

    logging.debug(f"Context:\n{pformat(ctx)}")

    match ctx.form_obj.tag.split("}")[1]:
        case "epocForm1" :      hi1 = form1.processForm1(ctx)
        case "epocPrForm2" :    hi1 = form2.processForm2(ctx)
        case "epocForm3" :      
            hi1 = form3.processForm3(ctx)
            ri_to_sp = False
        case "epocPrForm5" :    hi1 = form5.processForm5(ctx)
        case "epocPrForm6" :    hi1 = form6.processForm6(ctx)
        case _ :
            print (f"No matching form found for {ctx.form_obj.tag}")
            exit(-1)
    
    hi1.Header.SenderIdentifier.CountryCode = sender_cc if ctx.ri_to_sp else receiver_cc
    hi1.Header.SenderIdentifier.UniqueIdentifier = sender_id if ctx.ri_to_sp else receiver_id
    hi1.Header.ReceiverIdentifier.CountryCode = receiver_cc if ctx.ri_to_sp else sender_cc
    hi1.Header.ReceiverIdentifier.UniqueIdentifier = receiver_id if ctx.ri_to_sp else sender_id
    hi1.Header.Timestamp = etsify_datetime(datetime.now())
    hi1.Header.TransactionIdentifier = str(uuid4())

    print(xml(hi1))

