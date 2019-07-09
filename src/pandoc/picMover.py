from shutil import move
from os import walk, listdir, rename
from regexCleaner import subout, bibpt

artdirs = next(walk('.'))[1]

for artdir in artdirs:
    if artdir[-1].isdigit():
        dst = './notext/%s' % artdir
        flist = listdir(artdir)
        extlist = []
        
        # Filter 'withdraw'
        if len(flist) == 1 and flist[0] == 'withdraw':
            move(artdir, dst)
            continue
        

        for f in flist:
            extension = f.split('.')[-1].lower()
            extlist.append(extension)
            original_name = artdir+ '/' + f
            new_name = original_name.lower()
            
            # Normalize file names
            normalize_fname(extension, original_name, new_name)

            # Replace non-utf-8 chars & remove bibliography
            if new_name[-3:] == 'tex':
                subout(new_name, new_name, bibpt)
                
        if set(extlist) <= set(['ps', 'html', 'pdf', 'eps', 'cry', 'gif', 'jpg','doc', 'htm']):
            move(artdir, dst)
        