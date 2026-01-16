

from hspf.uci import UCI
from hspf.hspfModel import hspfModel
from hspf.parser import graph
%load_ext autoreload
%autoreload 2
from pathlib import Path
THIS_DIR = Path(__file__).parent

uci = UCI(THIS_DIR / './data/Clearwater.uci')



uci.add_parameter_template('PERLND','PWAT-PARM2',0,'LZSN')


schematic = uci.table('SCHEMATIC')
extsources = uci.table('EXT SOURCES')

mass_links = []
for table_name in uci.table_names('MASS-LINK'):
    mass_link = uci.table('MASS-LINK',table_name)
    mass_link['mlno'] = table_name.split('MASS-LINK')[1]
    mass_links.append(mass_link)

mass_links = pd.concat(mass_links)   

#%%
uci_file = 'c:/Users/mfratki/Documents/calibrations/Nemadji/model/Nemadji_2.uci'
model = hspfModel(uci_file)


from hspf import reports

