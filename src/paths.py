# NEVER MOVE THIS FILE!!!!!!
from os.path import dirname, join, realpath, basename
src_path = dirname(realpath(__file__))
repo_path = dirname(src_path)
data_path = join(repo_path,'data')
results_path = join(repo_path, 'results')

data0001 = join(data_path, '0001')
data0002 = join(data_path, '0002')
data1701 = join(data_path, '1701')
cate_path = join(data_path, 'arxiv_cate')

rawxmls_path = join(results_path, 'latexml')
errcase_path = join(results_path, 'latexml/errcp')

cleanedxml_path = join(results_path, 'cleaned_xml')
# cleanlog_path = join(results_path, 'cleaned_xml/logs/cleanlog.txt')
cleanlog_path = join(results_path, 'tmplog.txt')

no_sec_latex_path = join(results_path, 'no_section_latex')
no_sec_xml = join(results_path, 'no_sec_xml')
cleaned_nonsecs = join(results_path, 'cleaned_nonsecs')
metadatas_path = join(data_path, 'arxiv_metadata')

cs_lda_dir = join(results_path, 'cs_lda')
fulltext_dir = join(cs_lda_dir, 'fulltext')
kldiv_dir = join(src_path, 'KLdiv')
perpsets_testdir = join(results_path, 'perpsets/10test')
perpsets_traindir = join(results_path, 'perpsets/90train')
secklds = join(data_path, 'cs_sec_klds')
f_sectitles = join(data_path, 'sec_titles.txt')
models_path = '/cs/group/grp-glowacka/arxiv/models/cs_5ktpc'


if __name__ == "__main__":
    # Check that we are reading the correct file
    print('src', src_path)
    print('repo', repo_path)
    print('data', data_path)
    print('results', results_path)
    print('datapath basename:', basename(data_path))