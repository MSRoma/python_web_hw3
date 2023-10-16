import re
import argparse
#from collections import UserDict
#import sys
from pathlib import Path
from threading import Thread
import shutil
#import os.path
import os
import logging
current_path = Path('.')


class Trans: # класс створює словник відповідності символів латиниці та кирилиці
    cyrillic_symbol = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    latin_symbol = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    TRANS = {}
    def trans_dict(self):
        for c, l in zip(self.cyrillic_symbol, self.latin_symbol):
            self.TRANS[ord(c)] = l
            self.TRANS[ord(c.upper())] = l.upper()
        return self.TRANS


class Normalize(Trans): # функція видаляє непотрібні символи з назви файлу
    def normalize(self, name: str):
        t_name = name.translate(self.TRANS)
        t_name = re.sub(r'[^a-zA-Z0-9.]', '_', t_name)
        return t_name



class ReplaseFile(Normalize): # перенесення файлів в відповідні папки

    REGISTER_EXTENSION = {
        'JPEG': "images",'JPG': "images",'PNG': "images",'SVG': "images",
        'MP3': "audio",'OGG': "audio",'WAV': "audio",'AMR': "audio",
        'AVI': "video",'MP4': "video",'MOV': "video",'MKV': "video",
        'DOC': "documents",'DOCX': "documents",'TXT': "documents",'PDF': "documents",'XLSX': "documentsS",'PPTX': "documents",
        'ZIP': "archives",'GZ': "archives",'TAR': "archives",
        }
 
    def copy_file(self, path: Path) -> None:
        for el in path.iterdir():
            if el.is_file():
                ext = el.suffix[1:].upper()
                try:
                
                    self.REGISTER_EXTENSION[ext]
                    folder = self.REGISTER_EXTENSION[ext]
                    ext_folder = output / folder / ext
                  
                    try:
                        ext_folder.mkdir(exist_ok=True, parents=True)
                        el.replace(ext_folder / normalize_init.normalize(el.name))
                    except OSError as err:
                        logging.error(err)
                except KeyError:
                    output_others.mkdir(exist_ok=True, parents=True)
                    el.replace(output_others / el.name)
    
class Main(Thread,ReplaseFile):
 
    threads = []

    def scan(self, folder: Path) -> None:
#        print(folder)
        for item in folder.iterdir():
            if item.is_dir():
             #   print(item)
                th = Thread(target=self.copy_file, args=(item,))
                th.start()
                self.threads.append(th)
            #    print(self.threads)
                self.scan(item)

        [th.join() for th in self.threads]    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s") 
   
    t = Trans()
    r = ReplaseFile()
    normalize_init = Normalize()

    parser = argparse.ArgumentParser(description="Sorting folder")
    parser.add_argument("--source", "-s", help="Source folder", required=True)
    parser.add_argument("--output", "-o", help="Output folder", default="dist")
    parser.add_argument("--output_others", "-ot", help="Other file", default="others")

  #  print(parser.parse_args())
    args = vars(parser.parse_args())
    print(args)

    source = Path(args.get("source"))
    output = Path(args.get("output"))
    output_others = Path(args.get("output_others"))
    m = Main()
    
 
    m.scan(source)