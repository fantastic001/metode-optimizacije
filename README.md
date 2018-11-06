
Metode optimizacije
======================

Transportni problem
---------------------

Rešenje transportnog problema je u skripti to.py 

Potrebno je imati instaliran Python 3 i NumPy biblioteku.

pokretanje:

    python to.py 

skripta će upitati za broj izvora i broj potražnji kao i za kapacitet izvora i potražnji i za troškove prenosa. 

Dat je primer unosa u fajlu input.txt a može se učitati direktno u skriptu pomoću:

    python to.py < input.txt

Pored ispisa svakog koraka, na kraju se ispisuje konačno rešenje u obliku matrice gde je svaki red izvor a svaka kolona je zahtev. Tako da 3. red predstavlja količinu robe koja se prenosi svakom zahtevu. 

Algooritam koristi Northwest metodu za izračunavanje inicijalnog rešenja. Potom se računaju potencijali u i v i kazna za svaku ćeliju P(i,j) = u(i) + v(j) - C(i,j) i ako su sve kazne manje ili jednake nuli, algoritam se završava. Ako nisu, koriguje se matrica pomoću metode traženja petlje u grafu koji je inicijalno predstavljen pomoću matrice izračunate iz prethodnog koraka ili iz inicijalnog rešenja. 

NAPOMENA: algoritam radi samo na balansiranom slučaju, nebalansirani slučajevi se mogu transfoormisati u balansirane dodavanjem nove kolone sa za trošak (troškovi ostavljanja resursa na izvoru). 

Algoritam bi trebalo da hendluje i degenerične slučajeve kada je broj alokaciija manji od N+M - 1