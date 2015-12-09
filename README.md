# NGS Workflow #

## O aplikacji ##

Praca inżynierska: _Narzędzia wspierające równoległe obliczenia na sekwencjach DNA_

* Mikołaj Nowak
* Piotr Oleksy
* Piotr Oramus

Opiekun pracy: [dr inż Maciej Malawski](http://www.icsr.agh.edu.pl/~malawski/)


Część BATCH znajduje się w repozytorium pod adresem: https://bitbucket.org/pioole/dna


## Korzystanie z aplikacji ##

* Aktualnie aplikacja znajduję się [pod tym adresem](http://powerful-beach-7411.herokuapp.com/).
* Jeżeli jeszcze tego nie zrobiłeś - załóż konto używając opcji **_Sign Up_**
* Zaloguj się używając danych podanych przy rejestracji
* Aby dokonać zsekwencjonowania genomu:
  * Przygotuj genom w formacie _fastq.gz_ - musi mieć on możliwość pobrania z sieci. Przykładowe genomy spełniające powyższe kryteria znajdują się [tutaj](ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/NA19726/sequence_read).
  * W aplikacji wybierz z paska menu pozycję **_Submit a new job_**.
  * Wybierz dowolną nazwę dla job'u, który dokona sekwencjonowania w klastrze PL-GRID.
  * Podaj URL, pod którym dostępny jest Twój genom.
  * Podaj PROXY.
     * Jeżeli nie wiesz skąd je wziąć - skorzystaj z [dokumentacji PL-GRID](https://docs.cyfronet.pl/pages/viewpage.action?pageId=16025029) w celu wygenerowania nowego PROXY
     * Jeżeli przechowujesz PROXY w pliku `proxy_file`, to aby zmienić go na tekst użyj polecenia:
     ```
     cat proxy_file | base64 | tr -d '\n'
     ```
     * Uzyskany tekst wklej do odpowiedniego pola tekstowego w aplikacji.
  * Jeżeli masz bezpośredni dostęp do klastra (np. poprzez SSH) i wiesz co robisz, po kliknięciu **_Click here to expand more options_** możesz ustawić również ściężkę (absolutną), w której pojawi się output job'u oraz ścieżkę absolutną do katalogu, w którym wykonywane będę obliczenia (workspace directory).
  * Naciśnij **_Submit_**.
  * Jeżeli wszystko zakończy się poprawnie, powinieneś zostać przekierowany na stronę z komunikatem o sukcesie. Job został zakolejkowany.
  * Na stronie **_All jobs_** możesz śledzić postęp job'u.
