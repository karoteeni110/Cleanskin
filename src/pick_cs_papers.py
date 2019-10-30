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
    '''Exclude nums and puncts, characters lower cased'''
    # return ' '.join((re.findall(r"(?:(?<=\s)|(?<=^))\d*[a-zA-Z]+(?:[-'\.][a-zA-Z]+)*)", text))).lower()
    return ' '.join(re.findall(r"\d*[a-zA-Z]+(?:[-'\.][a-zA-Z]+)*", text)).lower()

def rm_backmatter(docroot):
    elems = docroot.findall('.//*')
    for elem in elems:
        if elem.tag in ('title', 'abstract', 'author', 'acknowledgements', 'bibliography') \
            or re.search(r'(\b(references?|acknowledge?ments?)\b)' , elem.get('title', ''), flags=re.I):
            elem.clear()
    return docroot

def tk_ratio(txt):
    return len(txt) / (len(txt.split()) or 1)

def pick_cs_papers(tarfn):
    dirn = join(TARS_COPY_TO, rm_tar_ext(tarfn))
    skipped, allpaper = 0, 0
    for xml in listdir(dirn):
        xmlpath = join(dirn, xml)
        _, root = get_root(xmlpath)
        
        if is_cs(root):
            allpaper += 1
            # Check abstract
            ab = root.find('abstract')
            if ab is None: 
                logging.info('Skipped: %s (abstract not found)' % xml)
                skipped += 1
                continue
            else:
                abtxt = nmlz(''.join(ab.itertext()))
                fulltext, garbled_len= '', 0
                # secelems = (root[3:] if root.get('categories') else root)
                secelems = rm_backmatter(root)
                for sec in secelems: # root[3:] does not include metadata
                    sectext = nmlz(''.join(sec.itertext()))
                    if tk_ratio(sectext) < 10:
                        fulltext += sectext + '\n'
                    elif len(sectext)>300 : # if len(sectext.split()) < 10: # some short notes may be weird; just exclude it
                        garbled_len += len(sectext)
                
                if garbled_len/(len(fulltext)+garbled_len) < 0.5: 
                    txtfname = xmlext2txt(xml)
                    abstract_path = join(ABSTRACT_DST, txtfname)
                    with open(abstract_path, 'w') as absfile :
                        absfile.write(abtxt)
                    
                    fulltext_path = join(FULLTEXT_DST, txtfname)
                    with open(fulltext_path, 'w') as ftfile:
                        ftfile.write(fulltext)
                else:
                    logging.info('Skipped: %s (too few tokens in fulltext)' % xml)
                    skipped += 1

    extracted = allpaper-skipped
    logging.info('Papers extracted: %s / %s' % (extracted, allpaper))
    return extracted, allpaper

def clear_picked_dir(tarfn):
    """Clear the content of the dir and keeps the empty dir"""
    unzipped_dirn = rm_tar_ext(tarfn)
    unzipped_dir_path = join(TARS_COPY_TO, unzipped_dirn)
    for xml in listdir(unzipped_dir_path):
        remove(join(unzipped_dir_path, xml))
    # rmtree(join(TARS_COPY_TO, unzipped_dirn))
    logging.info('Old dir %s/%s cleared' % (TARS_COPY_TO, unzipped_dirn))

def pick_cs_headings(tarfn):
    dirn = join(TARS_COPY_TO, rm_tar_ext(tarfn))
    skipped, allpaper = 0, 0
    for xml in listdir(dirn):
        xmlpath = join(dirn, xml)
        _, root = get_root(xmlpath)
        
        if is_cs(root):
            allpaper += 1
            
            fulltext, garbled_len= '', 0
            # secelems = (root[3:] if root.get('categories') else root)
            secelems = rm_backmatter(root)
            for sec in secelems: # root[3:] does not include metadata
                sectext = nmlz(''.join(sec.itertext()))
                if tk_ratio(sectext) < 10:
                    fulltext += sectext + '\n'
                elif len(sectext)>300 : # if len(sectext.split()) < 10: # some short notes may be weird; just exclude it
                    garbled_len += len(sectext)
            
            if garbled_len/(len(fulltext)+garbled_len) < 0.5: 
                
                cs_headings_txt_path = join(results_path, 'cs_headings.txt')
                with open(cs_headings_txt_path, 'a') as hdtxt:
                    for sec in root.findall('.//section'):
                        heading = sec.get('title')
                        hdtxt.write(heading+'\n')
            else:
                logging.info('Skipped: %s (too few tokens in fulltext)' % xml)
                skipped += 1

    extracted = allpaper-skipped
    logging.info('Papers extracted: %s / %s' % (extracted, allpaper))
    return extracted, allpaper

def main(tar_fn):
    cp_1tar(tar_fn)
    unzip_1tar(tar_fn)
    rm_oldtar(tar_fn)
    extracted, allpaper = pick_cs_headings(tar_fn) # pick_cs_papers(tar_fn)
    clear_picked_dir(tar_fn)
    return extracted, allpaper


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
    
    tarlist = [fn for fn in listdir(CLEANED_XML) if fn not in listdir(TARS_COPY_TO)] 
    # tarlist = ['1801.tar.gz']
    EXTRACTED_SUM, ALLPAPER_SUM = 0, 0
   
    for i, tarfn in enumerate(tarlist):
        logging.info('Tarball %s of %s ...' % (i+1, len(tarlist)))
        extracted, allpaper = main(tarfn)
        EXTRACTED_SUM += extracted
        ALLPAPER_SUM += allpaper
    logging.info('Summary: paper extracted: %s of %s' % (EXTRACTED_SUM, ALLPAPER_SUM))
        

