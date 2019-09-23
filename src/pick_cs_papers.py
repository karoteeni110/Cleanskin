import xml.etree.ElementTree as ET
import logging, re
from newCleaner import get_root
from clean_at_tmp import run_and_report_done, rm_tar_ext
from categorise_sections import is_backmatter
from shutil import copyfile, rmtree
from os import listdir, remove
from os.path import join 
from paths import results_path

def cp_1tar(tarfn):
    src = join(CLEANED_XML, tarfn)
    dst = join(TARS_COPY_TO, tarfn)
    copyfile(src, dst)

def unzip_1tar(tar_fn):
    cmd = 'if cd %s ; then tar -xzf %s; fi' % (TARS_COPY_TO, tar_fn)
    run_and_report_done('%s unzipped' % tar_fn, cmd)

def rm_oldtar(tar_fn):
    remove(join(TARS_COPY_TO, tar_fn))
    logging.info('Old tar %s/%s removed' % (TARS_COPY_TO, tar_fn))

def is_cs(docroot):
    cateinfo = docroot.get('categories', '')
    if re.search(r'\bcs\.', cateinfo):
        return True
    return False

def xmlext2txt(xmlname):
    return xmlname[:-3] + 'txt'

def nmlz(text):
    return ' '.join(re.findall(r"[a-zA-Z]+(?:[-'\.][a-zA-Z]+)*", text)).lower()

def pick_cs_papers(tarfn):
    dirn = join(TARS_COPY_TO, rm_tar_ext(tarfn))
    for xml in listdir(dirn):
        xmlpath = join(dirn, xml)
        _, root = get_root(xmlpath)
        
        if is_cs(root):
            # Check abstract
            ab = root.find('abstract')
            if ab is None: 
                logging.info('Skipped: %s (abstract not found)' % xml)
                continue
            else:
                fulltext = ''
                # secelems = (root[3:] if root.get('categories') else root)

                for sec in root[3:]: # root[3:] does not include metadata
                    if not is_backmatter(sec):
                        sectext = ''.join(sec.itertext())
                        tkratio = len(sectext) / len(sectext.split())
                        if tkratio < 10:
                            fulltext += nmlz(sectext) + '\n'
                        else:
                            logging.info('Skipped: %s (abnormal long tokens)' % xml)
                            fulltext = ''
                            break

                if fulltext:
                    txtfname = xmlext2txt(xml)
                    abstract_path = join(ABSTRACT_DST, txtfname)
                    with open(abstract_path, 'w') as absfile :
                        absfile.write(''.join(ab.itertext()))
                    
                    fulltext_path = join(FULLTEXT_DST, txtfname)
                    with open(fulltext_path, 'w') as ftfile:
                        ftfile.write(fulltext)

def rm_picked_dir(tarfn):
    unzipped_dirn = rm_tar_ext(tarfn)
    rmtree(join(TARS_COPY_TO, unzipped_dirn))
    logging.info('Old dir %s/%s removed' % (TARS_COPY_TO, unzipped_dirn))

def get_topic_probs():
    pass

def main(tar_fn):
    # cp_1tar(tar_fn)
    # unzip_1tar(tar_fn)
    # rm_oldtar(tar_fn)
    pick_cs_papers(tar_fn)
    # rm_picked_dir(tar_fn)
    # get_topic_probs() 
    # Finally get `cs_ft_composition.txt`, `cs_abt_composition.txt`, `cs_ft_keys.txt`


if __name__ == "__main__":
    # Set verbose
    VERBOSE, REPORT_EVERY = True, 500

    # ===== 
    level    = logging.INFO
    format   = '%(message)s'
    handlers = [logging.FileHandler('topicmodel.log'), logging.StreamHandler()]
    logging.basicConfig(level = level, format = format, handlers = handlers)

    CLEANED_XML = '/cs/group/grp-glowacka/arxiv/cleaned_xml'
    TARS_COPY_TO = '/tmp/arxiv'
    ABSTRACT_DST = join(results_path, 'cs_lda/abstract')
    FULLTEXT_DST = join(results_path, 'cs_lda/fulltext')

    # tarlist = [fn for fn in listdir(CLEANED_XML) if fn not in listdir(cs_lda_dir)] 
    tarlist = ['1801.tar.gz']

    for i, tarfn in enumerate(tarlist):
        logging.info('Tarball %s of %s ...' % (i+1, len(tarlist)))
        main(tarfn)

