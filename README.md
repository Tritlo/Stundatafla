Stundatöflu Generator
========

Tekur inn argument sem er listi af kúrsum og litum, i.e. fag1 litur1 fag2 litur2, og býr til stundatöflu með þeim kúrsum og litum. Einnig er hægt að kalla á með -i nafnatoflu.p -e
og þá fer maður í edit-mode, þar sem maður getur bætt við tímum, breytt lit og fjarlægt tíma, og fleira.

Sjá má dæmi um html output á http://mpg.is/hi/hbv5.php

Hægt er að kalla á help fyrir upplýsingar um notkun:

    Usage: usage StundatofluGenerator.py [options] fag1 liturfag1 fag2 liturfag2 ...

    Options:
      -h, --help            show this help message and exit
      -i table.p, --in=table.p
                            Table to change or add to
      -o stundatafla, --out=stundatafla
                            Name of output
      --title=Title         Title of table
      --heading=Heading     Heading of table
      -e, --edit            Edit mode
