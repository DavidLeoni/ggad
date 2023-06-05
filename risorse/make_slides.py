#/usr/bin/python3

""" Given a number N, reads parteN-sol.ipynb and generates parteN.slides.html  (without the -sol!)

DIRTY script! 


June 2023: works fine with nbconvert 7.4.0  (6.5.0 didn't show alert boxes properly and added wrong <p><style></p>)
Installing collected packages: mistune, nbconvert
  Attempting uninstall: mistune
    Found existing installation: mistune 0.8.4
    Uninstalling mistune-0.8.4:
      Successfully uninstalled mistune-0.8.4
  Attempting uninstall: nbconvert
    Found existing installation: nbconvert 6.4.0
    Uninstalling nbconvert-6.4.0:
      Successfully uninstalled nbconvert-6.4.0
Successfully installed mistune-2.0.5 nbconvert-7.4.0

TO CHECK:  
    - commands like 
      jupyter nbconvert --to slides parte2-sol.ipynb --SlidesExporter.reveal_theme=sky --SlidesExporter.reveal_transition=fade     
      Current supported options are here:
      https://github.com/jupyter/nbconvert/blob/68b496b7fcf4cfbffe9e1656ac52400a24cacc45/nbconvert/exporters/slides.py
    - currently (oct 2022) this option is NOT supported: --SlidesExporter.reveal_navigationMode=linear
    - how to specify a custom made theme from command line   
    - offline browsing

"""


custom_css = ["risorse/css/softpython-slides.css",
              "risorse/css/fidia-slides.css"]


from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('slide', metavar='N', type=str, nargs='?', default=-1,
                    help='a string for the slide number')
args = parser.parse_args()
print(args.slide)
sn = args.slide

if sn == -1:
    print("Please specify a slide number. Aborting.")
    exit(1)

prefix = f'parte{sn}'

import subprocess


import tempfile
import os

tempdir = tempfile.gettempdir() 

raw_slides_html = os.path.join(tempdir, f'{prefix}-sol')

#NOTA: ho fissato la versione di reveal perchè altrimenti mi dava pagina bianca
cmd = ['jupyter', 'nbconvert', '--to', 'slides', f'{prefix}-sol.ipynb', '--output', raw_slides_html]
        #"--reveal-prefix", "./risorse/reveal"] #"https://unpkg.com/reveal.js@4.0.2"]
print(' '.join(cmd))
res = subprocess.check_output(cmd)

print(res)


dest = f'{prefix}.slides.html'

print("Reading", raw_slides_html)
with open(f'{raw_slides_html}.slides.html', encoding='utf8') as fr:
    s = fr.read()
    
    ps = s
    rev = '<div class="reveal">'    

    css_links = ''
    for css in custom_css:
        the_id = css.split('/')[-1][:-4]
        css_links += f'\n <link rel="stylesheet" href="{css}" id="{the_id}-theme">'
    print(css_links)

    ps = ps.replace(rev, rev + css_links)
                    
    
    ps = ps.replace('transition: "slide",',
    """
            transition: "fade",
            navigationMode: "linear",                
    """)
    
    ps = ps.replace('slideNumber: "",', 
                    'slideNumber: true,')
    

    manual_reveal = """
<script type="text/javascript" src="risorse/reveal/dist/reveal.js"></script>
<script type="text/javascript" src="risorse/reveal/plugin/notes/notes.js"></script>"""

    #ps = ps.replace('</head>',  manual_reveal + '\n</head>')
    #ps = ps.replace('require(',  'console.log("DAV:About to run require..."); require(')
    #ps = ps.replace('</body>', '')
    #ps = ps.replace('</html>',  '<div>SGURIMPO</div></body></html>')
    #ps = ps.replace('<html>', '<html><script>console.log("DAV: after HTML"); </script>')

    #Fixes crap of nbconvert 6.5.0 I guess - WITHOUT THIS REQUIRE <script> AT THE BOTTOM DOESN'T RUN !!!!
   # ps = ps.replace('<p><style></p>','<p><style></style></p>')

    with open(dest, 'w', encoding='utf8') as fw:
        fw.write(ps)
        print("Done writing", dest)