for python3

Requires `tkinter` library installed (`matplotlib` dependency).

For archlinux it is `sudo pacman -S tk`.

# Do a backup

    python download_all.py --host 'http://data.bn.org.pl/api/bibs' --data-dir data/bibs/
    python download_all.py --host 'http://data.bn.org.pl/api/authorities' --data-dir data/authorities/
