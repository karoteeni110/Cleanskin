from newCleaner import *
from subprocess import run, PIPE, CalledProcessError
from shutil import copyfile, copytree, rmtree, move
from os import listdir, remove
from os.path import join
from paths import results_path
import logging

level    = logging.INFO
format   = '%(message)s'
handlers = [logging.FileHandler('tmp_tar.log'), logging.StreamHandler()]

logging.basicConfig(level = level, format = format, handlers = handlers)

def run_and_report_done(done_msg, cmd):
    try:
        run(cmd, shell=True, stderr=PIPE, check=True)
    except CalledProcessError as e:
        logging.info(e.stderr.decode('utf-8'))
    else: 
        logging.info(done_msg)

def cp_1tar(tar_fn):
    src_tarpath = join('/cs/group/grp-glowacka/arxiv/xml', tar_fn)
    dst_tarpath = join('/tmp/arxiv', tar_fn)
    _ = copyfile(src_tarpath, dst_tarpath)

def unzip_1tar(tar_fn):
    cmd = 'if cd %s ; then tar -xzf %s; fi' % ('/tmp/arxiv', tar_fn)
    run_and_report_done('%s unzipped ...' % tar_fn, cmd)
    
def rm_oldtar(tar_fn):
    remove(join('/tmp/arxiv', tar_fn))
    logging.info('Old tar /tmp/arxiv/%s removed' % tar_fn)

def cleanse(tar_fn):
    src_dst_dir = '/tmp/arxiv'
    xmlpath_list = get_xmlpathlist(join(src_dst_dir, tarn_no_ext(tar_fn)))
    cleanlog_path = join(results_path, 'tmplog.txt')

    begin = time.time()
    logging.info('Cleaning... %s' % tar_fn)
    with open(cleanlog_path, 'a') as cleanlog:
        for i, xmlpath in enumerate(xmlpath_list):
            writeout = True
            xml = basename(xmlpath)

            # === Get title, author, abstract, categories from metadata ===
            artid = fname2artid(xml)
            try:
                metadata = id2meta.pop(artid) # Use `pop` to get retriving faster
            except KeyError:
                metadata = defaultdict(str)
                # logging.info('Metadata not found:', e)
            # === 

            try:
                tree, root = get_root(xmlpath)
            except ET.ParseError:
                logging.info('Skipped: ParseError at %s' % xml)
                remove(xmlpath)
                cleanlog.write(xml + ' \n' + 'ParseError \n' + '================================== \n')
                continue
            clean(root)
            add_metamsg(root, xml, metadata)
            postcheck(root, cleanlog, xml)
            if writeout:
                tree.write(xmlpath)

            if VERBOSE:
                if (i+1) % REPORT_EVERY == 0 or i+1 == len(xmlpath_list):
                    logging.info('%s of %s ...' % (i+1, len(xmlpath_list)))

    t = time.time() - begin
    t = t/60
    logging.info('%s files in %s mins' % (len(xmlpath_list), t))

def tarn_no_ext(tar_fn):
    """Return the first 4 chars"""
    return tar_fn[:4]

def tarback(tar_fn):
    cmd = 'if cd %s; then tar -czf ../new_arxiv/%s %s/; fi' % ('/tmp/arxiv', tar_fn, tarn_no_ext(tar_fn))  
    run_and_report_done('%s of %s Done: /tmp/new_arxiv/%s' % (i+1, len(tarlist),tar_fn), cmd)

def rm_cleansed_dir(tar_fn):
    dirn = tarn_no_ext(tar_fn)
    rmtree(join('/tmp/arxiv', dirn))
    logging.info('Old dir /tmp/arxiv/%s removed' % dirn)

def main(tar_fn):
    cp_1tar(tar_fn)
    unzip_1tar(tar_fn)
    rm_oldtar(tar_fn)
    cleanse(tar_fn)
    tarback(tar_fn)
    rm_cleansed_dir(tar_fn)

if __name__ == "__main__":
    # tarlist = ['0001.tar.gz']
    tarlist = [fn for fn in listdir('/cs/group/grp-glowacka/arxiv/xml') \
                if fn[-2:] == 'gz' and fn not in listdir('/tmp/new_arxiv')]

    # Set verbose
    VERBOSE, REPORT_EVERY = True, 500

    # Read metadata for all articles
    id2meta = get_urlid2meta() # 1 min

    for i, tarfn in enumerate(tarlist):
        logging.info('Tarball %s of %s ...' % (i+1, len(tarlist)))
        main(tarfn)

    # run_and_report_done('TRY ECHO:', 'hahahahha')

