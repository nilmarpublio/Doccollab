from babel.messages.pofile import read_po
from babel.messages.mofile import write_mo

langs = ['en', 'es', 'pt']

for lang in langs:
    po_path = f'translations/{lang}/LC_MESSAGES/messages.po'
    mo_path = f'translations/{lang}/LC_MESSAGES/messages.mo'
    
    with open(po_path, 'rb') as po_file:
        catalog = read_po(po_file)
    
    with open(mo_path, 'wb') as mo_file:
        write_mo(mo_file, catalog)
    
    print(f'[OK] {lang} compilado')

print('\n[DONE] Todas as traducoes compiladas!')

