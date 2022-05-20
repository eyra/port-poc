"Main program to test whatsapp script"
from pathlib import Path
from __init__ import process


if __name__ == '__main__':
    file_data = Path('tests/data/WhatsApp chat with UU WhatsApp project ☑️_Javier.txt')
    #file_data = Path('tests/data/WhatsApp chat with UU WhatsApp project ☑️_Javier.zip')
    #file_data = Path('tests/data/uu_chat.txt')
    result = process(file_data)
    print(result)
    
