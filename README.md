# Generator diet służbowych / Diet generator

Prosty skrypt pythonowy, który generuje estetyczne raporty rozliczeń kosztów podróży służbowej.

Skrypt obejmuje jedynie kalkulator diet na podstawie dość zawiłych zasad. Liczy zarówno diety krajowe, jak i zagraniczne.

Logika jest momentami uproszczona (trzeba dodać sobie miasto do skryptu by to działało) więc warto zajrzeć w skrypt i szablon w LaTeXu i zorientować się co się dzieje.

W folderach `descriptions` i `outputs` znajdziecie przykłady (descriptions to inputy).

## Instalacja

Potrzebujecie `pdflatex` oraz `pip install -r requirements.txt` (python w wersji 3.7 powinien wystarczyć, możliwe że działa na 3.5)

## Użycie

```bash
python pydeleg.py --file descriptions/example_ams_2021_05_05.txt
```

## Przykłady

Przykłady outputów znajdziecie w katalogu `outputs`. Jeśli po kliknięciu na githubie nie widzicie podglądu, spróbujcie w innej przeglądarce (Firefox mi nie działa, ale Chromium już tak).

## Licencja

MIT

## Uwagi

**UŻYCIE NA WŁASNĄ ODPOWIEDZIALNOŚĆ. Autor kodu nie ponosi żadnej odpowiedzialności za źle policzone diety lub jakiekolwiek inne wady formalne, których dopuścić może się używający tego programu. Używający program powinien sam zweryfikować czy dokument jest poprawny i może zostać użyty zgodnie z prawem. Jeśli użycie niniejszego kodu doprowadzi do uchybień względem jakiegokolwiek prawa, strat używającego program lub osób trzecich, lub jakichkolwiek innych szkód czy efektów, które mogłyby skutkować odpowiedzialnością względem prawa, autor kodu nie może zostać pociągnięty do jakiejkolwiek odpowiedzialności i całkowita wina spoczywa na używającym kod.**
