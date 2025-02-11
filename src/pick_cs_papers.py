"""Copy and decompress tarballs from .../grp/cleaned_xml/ to /tmp
   After immediately removing tarballs, pick pick papers of specified field
   Delete all the xmls after picking; 
   empty directory is left as a record of progress"""
import xml.etree.ElementTree as ET
import logging, re, time
from newCleaner import get_root
from clean_at_tmp import run_and_report_done, rm_tar_ext
from categorise_sections import is_backmatter
from shutil import copyfile, rmtree
from os import listdir, remove
from os.path import join 
from paths import results_path
from random import shuffle
from sortLabels import final

phys_cate_acros = r'\b(astro|cond-mat|gr|hep|math\-ph|nlin|nucl|physics|quant)'

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

def is_cs(docroot, xmlname):
    cateinfo = docroot.get('categories', '')
    
    if PICKABLE_PIDS:
        pid = xmlname[:-4]
        if pid in PICKABLE_PIDS:
            return True
    else:
        if re.search(r'\bcs', cateinfo):
        # if re.search(phys_cate_acros, cateinfo):
        # if re.search(r'\bmath\.', cateinfo):
            return True
    return False

def xmlext2txt(xmlname):
    return xmlname[:-3] + 'txt'

def nmlz(text):
    '''Exclude nums and puncts, characters lower cased'''
    return ' '.join(re.findall(r"\d*[a-zA-Z]+(?:[-'\.][a-zA-Z]+)*", text)).lower()

def rm_backmatter(docroot):
    """Clear <title>,<date>,<author>,<bibliography>"""
    elems = docroot.findall('.//*')
    for elem in elems:
        if elem.tag in ('title', 'date', 'author', 'bibliography'):
            elem.clear()
        # if re.match(r'(abstract$)', elem.get('title', '').strip(), flags=re.I):
        #     elem.clear()
    return docroot
    
def tk_ratio(txt):
    return len(txt) / (len(txt.split()) or 1)

def pick_cs_papers(tarfn):
    dirn = join(TARS_COPY_TO, rm_tar_ext(tarfn))
    skipped, allpaper = 0, 0
    for xml in listdir(dirn):
        xmlpath = join(dirn, xml)
        _, root = get_root(xmlpath)
        
        if is_cs(root, xml):
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

def rm_bmtext(docroot):
    """Clear title, author, abstract, acknowledgements, bibliography texts"""
    elems = docroot.findall('.//*')
    for elem in elems:
        if elem.tag in ('title', 'abstract', 'author', 'acknowledgements', 'bibliography') \
            or re.search(r'(\b(references?|acknowledge?ments?)\b)' , elem.get('title', ''), flags=re.I):
            t = elem.get('title')
            elem.clear()
            elem.set('title', t)
    return docroot

def pick_cs_headings(tarfn):
    dirn = join(TARS_COPY_TO, rm_tar_ext(tarfn))
    skipped, allpaper = 0, 0
    headingstr, pid_heading_str = '', ''

    for xml in listdir(dirn):
        xmlpath = join(dirn, xml)
        _, root = get_root(xmlpath)
        
        if is_cs(root, xml):
            allpaper += 1
            
            fulltext, garbled_len= '', 0
            # secelems = (root[3:] if root.get('categories') else root)
            secelems = rm_bmtext(root)
            for sec in secelems: # root[3:] does not include metadata
                sectext = nmlz(''.join(sec.itertext()))
                if tk_ratio(sectext) < 10:
                    fulltext += sectext + '\n'
                elif len(sectext)>300 : # if len(sectext.split()) < 10: # some short notes may be weird; just exclude it
                    garbled_len += len(sectext)
            
            if garbled_len/(len(fulltext)+garbled_len) < 0.5: 
                secs = root.findall('.//section')
                for sec in secs:
                    headingstr += sec.get('title', '') + '\n'
                    pid_heading_str += xml + ' ' + sec.get('title', '') + '\n'

            else:
                logging.info('Skipped: %s (too few tokens in fulltext)' % xml)
                skipped += 1

    with open(cs_headings_txt_path, 'a') as hdtxt:
        hdtxt.write(headingstr)
    with open(pid_heading_txt_path, 'a') as pidtxt:
        pidtxt.write(pid_heading_str)

    extracted = allpaper-skipped
    logging.info('Papers extracted: %s / %s' % (extracted, allpaper))
    return extracted, allpaper

def pick_cs_secs(tarfn):
    dirn = join(TARS_COPY_TO, rm_tar_ext(tarfn))
    skipped, allpaper = 0, 0
    for xml in listdir(dirn):
        pid = xml[:-4]
        xmlpath = join(dirn, xml)
        _, root = get_root(xmlpath)
        
        if is_cs(root, xml):
            allpaper += 1
            hd2text = dict()
            fulltext, garbled_len= '', 0
            secelems = rm_backmatter(root) # remove title, author, date, bibliography
            
            # Put sections into `fulltext` and `label2text`
            for sec in secelems:
                normed_sectitle = sec.get('title','').lower().strip().replace(' ','_')
                sectext = nmlz(' '.join(sec.itertext()))
                
                # Skip section if it is garbled or too short
                if tk_ratio(sectext) >= 10:
                    if len(sectext) > 300: # but don't include those too short into `garbled_len`
                        garbled_len += len(sectext)
                    continue 
                    
                # If not, add section to `fulltext` and `hd2text`
                else:
                    # Add to `fulltext`
                    if hd2text.get('abstract') != None and normed_sectitle == 'abstract':
                        continue # avoid repeating abstract
                    else:
                        hd2text['fulltext'] = hd2text.get('fulltext','') + sectext + '\n'

                    # Add to `section` only if it is abstract/acknowledgements or has a title
                        if sec.get('title') != None:
                            hd2text[normed_sectitle] = sectext
                        elif sec.tag in ('abstract', 'acknowledgements'):
                            hd2text[sec.tag] = sectext
                           
            # All labels & fulltext collected, write out to subcate dirs 
            if garbled_len/(len(hd2text['fulltext'])+garbled_len+0.0001) < 0.5:
                sec_idx = 0
                for hd in hd2text:
                    if hd != 'fulltext':
                        txtfname = xml[:-4] + '_%s' % sec_idx + '.txt'
                        sec_idx += 1
                        sec_text_dst = join(DST_DIRS, 'sections/'+txtfname)

                        # Write out section text
                        with open(sec_text_dst, 'w') as sec_txt: 
                            sec_txt.write(hd2text.get(hd, ''))
                        # Record section title
                        with open(join(DST_DIRS, 'sec_titles.txt'), 'a') as sec_hds: 
                            sec_hds.write(txtfname+','+hd+'\n')
                
                # Write out fulltext 
                ft_dst = join(DST_DIRS, 'fulltext/'+xmlext2txt(xml))
                with open(ft_dst, 'w') as ft_txt: 
                    ft_txt.write(hd2text['fulltext'])

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
    # extracted, allpaper =  pick_cs_papers(tar_fn) # pick_cs_headings(tar_fn) 
    extracted, allpaper = pick_cs_secs(tar_fn)
    clear_picked_dir(tar_fn)
    return extracted, allpaper


if __name__ == "__main__":
    # Set verbose
    VERBOSE, REPORT_EVERY = True, 500

    # Set logging 
    level    = logging.INFO
    format   = '%(message)s'
    handlers = [logging.FileHandler('cs_secsplit.log'), logging.StreamHandler()]
    logging.basicConfig(level = level, format = format, handlers = handlers)

    CLEANED_XML = '/cs/group/grp-glowacka/arxiv/cleaned_xml'
    TARS_COPY_TO = '/tmp/arxiv_cs'
    DST_DIRS = join(results_path, 'cs_lbsec') # Dir for 
    TITLE2LABEL = final

    # Decaprecated:
    # with open(join(results_path, 'pickable_pids_phy.pkl'), 'rb') as pickablelst:
    PICKABLE_PIDS = False # join(results_path, 'pickable_pids_phy.pkl')
    # cs_headings_txt_path = join(results_path, 'cs_headings.txt')
    # pid_heading_txt_path = join(results_path, 'pid_headings.txt')

    tarlist = [fn for fn in listdir(CLEANED_XML) if fn not in listdir(TARS_COPY_TO)] 
    # tarlist = ['0504.tar.gz']
    # shuffle(tarlist)
    EXTRACTED_SUM, ALLPAPER_SUM = 0, 0
   
    for i, tarfn in enumerate(tarlist):
        logging.info('Tarball %s of %s ...' % (i+1, len(tarlist)))
        extracted, allpaper = main(tarfn)
        EXTRACTED_SUM += extracted
        ALLPAPER_SUM += allpaper
        # if EXTRACTED_SUM > 131703:
        #     break
    
    logging.info('Summary: paper extracted: %s of %s' % (EXTRACTED_SUM, ALLPAPER_SUM))
        

