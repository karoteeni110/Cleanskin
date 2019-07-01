from shutil import move
from os import walk, listdir, rename
from useFilter import mk_the_dirs

mk_the_dirs(['./notext'])
artdirs = next(walk('.'))[1]
for artdir in artdirs:
    dst = './notext/%s' % artdir
    flist = listdir(artdir)
    extlist = []

    if len(flist) == 1 and flist[0] == 'withdraw':
        move(artdir, dst)
        continue
    for f in flist:
        extension = f.split('.')[-1]
        extlist.append(extension.lower())
        original_name = artdir+ '/' + f
        if not extension.islower() :
            new_name = original_name.lower()
            rename(original_name, new_name)
        if extension == 'ltx':
            new_name = original_name[:-3] + 'tex'
            rename(original_name, new_name)
        if extension == 'latex':
            new_name = original_name[:-5] + 'tex'
            rename(original_name, new_name)
    if set(extlist) <= set(['ps', 'html', 'pdf', 'eps', 'cry', 'gif', 'jpg','doc', 'htm']):
        move(artdir, dst)
