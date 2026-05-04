import shutil
import os
import subprocess
from tempfile import NamedTemporaryFile

import xml.etree.ElementTree as et

from xml_konwerter import konwertujdok

_LINIE = ""
_LINIE1 = "1"
_LINIE2 = "2"
_LINIE3 = "3"
_LINIE4 = "4"
_LINIETPOD = "TPOD"
_LINIETNAD = "TNAD"

_LISTA = "linie"
_LISTA1 = "linie1"
_LISTA2 = "linie2"
_LISTA3 = "linie3"
_LISTA4 = "linie4"
_LISTATPOD = "linietpod"
_LISTATNAD = "linietnad"

_LI_CH = ["nbsp", "oacute", "hellip", "Oacute"]

_htmlkeypairing = [
    (_LINIE, _LISTA),
    (_LINIE1, _LISTA1),
    (_LINIE2, _LISTA2),
    (_LINIE3, _LISTA3),
    (_LINIE4, _LISTA4),
    (_LINIETPOD, _LISTATPOD),
    (_LINIETNAD, _LISTATNAD)
]


def _replace_ch(tname, ch):
    command = ["sed", "-i", "-e", f's/\&{ch};/{ch};/g', tname]
    subprocess.call(command)


def _replace_ch_back(tname, ch):
    command = ["sed", "-i", "-e", f's/{ch};/\&{ch};/g', tname]
    subprocess.call(command)


def _replace_tag(tname, tag):
    pars = f's/<{tag}\([^>]*\)>/<{tag}\\1\\/>/g'
    command = ["sed", "-i", "-e", pars, tname]
    subprocess.call(command)


def _replace_page_break(tname):
    before = "page-break-before:always;display:none;"
    after = "page-break-before:always;"
    pars = f's/{before}/{after}/g'
    command = ["sed", "-i", "-e", pars, tname]
    subprocess.call(command)


def _remove_meta(htmltemplate, tname):
    shutil.copyfile(htmltemplate, tname)
    _replace_tag(tname, "meta")
    _replace_tag(tname, "img")
    _replace_tag(tname, "hr")
    _replace_page_break(tname)
    for ch in _LI_CH:
        _replace_ch(tname, ch)


def _restore_nbsp(output):
    for ch in _LI_CH:
        _replace_ch_back(output, ch)


def parsehtml(htmltemplate: str, outputdir: str, outputhtml: str, d: dict):
    with NamedTemporaryFile() as tfile:
        tname = tfile.name
        _remove_meta(htmltemplate, tname)
        htmloutputfile = os.path.join(outputdir, outputhtml)
        konwertujdok(tname, htmloutputfile, d,
                     htmlkeypairing=_htmlkeypairing)
    _restore_nbsp(htmloutputfile)
