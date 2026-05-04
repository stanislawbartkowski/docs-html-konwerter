import os
import unittest

import helper as H

from docs_html_konwerter import parsehtml


_TESTDOKUMENT = "TestDokument1.html"
_DOKUMENTPROSTEPOWT = "ProstePowtorz1.html"
_TESTDOKUMENT2 = "TestDokument2.html"
_TESTDOKUMENT3 = "TestDokument3.html"
_TDOKUMENT = "TestDokumentTLinie.html"
_HELLOPAGE = "TestHelloPage.html"


class TestHtmlKonwerter(unittest.TestCase):

    def _prosty_html(self, htmltemplate, lista=False):
        htmlfile = H.html_file(htmltemplate)
        print(htmlfile)
        outputdir = H.tmpdir()
        liniepod = [{"LPOD": f"To jest linia pod o numerz {no}"}
                    for no in range(100)]
        d = {
            "IMIE": "Juliusz",
            "NAZWISKO": "Cezar",
            "linietpod": liniepod,
            "linie": [
                        {
                            "NAZWA": "Artykuł",
                            "KWOTA": "999 USD"
                        }
            ]

        }
        parsehtml(htmltemplate=htmlfile, outputdir=outputdir,
                  outputhtml=htmltemplate, d=d)
        outfile = os.path.join(outputdir, htmltemplate)
        with open(outfile) as f:
            xml = f.read()
        print(xml)
        self.assertIn("Juliusz", xml)
        self.assertIn("Cezar", xml)
        if lista:
            self.assertIn("Artyku", xml)
            self.assertIn("999 USD", xml)
        return xml

    def test_proste(self):
        self._prosty_html(_TESTDOKUMENT)

    def test_proste2(self):
        self._prosty_html(_TESTDOKUMENT2, lista=True)

    def test_proste3(self):
        self._prosty_html(_TESTDOKUMENT3, lista=True)

    def test_proste4(self):
        xml = self._prosty_html(_TDOKUMENT, lista=True)
        self.assertIn("To jest linia pod o numerz 99", xml)

    def test_proste_linie(self):
        htmlfile = H.html_file(_DOKUMENTPROSTEPOWT)
        print(htmlfile)
        outputdir = H.tmpdir()
        d = {
            "linie": [
                {
                    "IMIE": "Juliusz",
                    "NAZWISKO": "Cezar",
                    "linie": [
                        {
                            "NAZWA": "Artykuł",
                            "KWOTA": "999 USD"
                        }
                    ]
                }
            ]
        }
        parsehtml(htmltemplate=htmlfile, outputdir=outputdir,
                  outputhtml=_DOKUMENTPROSTEPOWT, d=d)
        outfile = os.path.join(outputdir, _DOKUMENTPROSTEPOWT)
        with open(outfile) as f:
            xml = f.read()
        print(xml)
        self.assertIn("Juliusz", xml)
        self.assertIn("Cezar", xml)
        self.assertIn("Artyku", xml)
        self.assertIn("999 USD", xml)

    def test_proste_linie_2(self):
        htmlfile = H.html_file(_DOKUMENTPROSTEPOWT)
        print(htmlfile)
        outputdir = H.tmpdir()
        linie = [
            {
                "NAZWA": "Artykuł",
                "KWOTA": "999 USD"
            },
            {
                "NAZWA": "Rower",
                "KWOTA": "888 USD"
            }
        ]

        d = {
            "linie": [{"IMIE": f"Juliusz {no}", "NAZWISKO": f"Cezar {no}", "linie": linie} for no in range(100)]
        }
        parsehtml(htmltemplate=htmlfile, outputdir=outputdir,
                  outputhtml=_DOKUMENTPROSTEPOWT, d=d)
        outfile = os.path.join(outputdir, _DOKUMENTPROSTEPOWT)
        with open(outfile) as f:
            xml = f.read()
        print(xml)
        self.assertIn("Juliusz 0", xml)
        self.assertIn("Cezar", xml)
        self.assertIn("Artyku", xml)
        self.assertIn("999 USD", xml)
        self.assertIn("Juliusz 99", xml)

    def test_hello_page(self):
        htmlfile = H.html_file(_HELLOPAGE)
        print(htmlfile)
        outputdir = H.tmpdir()
        parsehtml(htmltemplate=htmlfile, outputdir=outputdir,
                  outputhtml=_HELLOPAGE, d={})
        # tylko test, ze się nie wywala
