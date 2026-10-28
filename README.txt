# passgen

Secure password generator using Python's `secrets` module.

    usage: passgen [-h] [-l LENGTH] [-U] [-L] [-S] [-N] [-c COUNT] [-x]

Generate secure random passwords.

options:
  -h, --help           show this help message and exit
  -l, --length LENGTH  password length
  -U, --upper          include Uppercase letters
  -L, --lower          include Lowercase letters
  -S, --symbols        include Symbols
  -N, --numbers        include Numbers
  -c, --count COUNT    how many passwords (default 1)
  -x, --no-ambiguous   exclude look-alike characters (O/0, l/1/I, quotes, etc.)

Example: passgen.py -l 16 -ULS

/* When downloaded into ~/<Directory>
chmod +x passgen.py
cp ~/path/to/password.py ~/.local/bin/passgen
*/
    
