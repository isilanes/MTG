import json
import subprocess as sp

with open("tokens.json") as f:
    J = json.load(f)

list = []
for token,n in J.items():
    for i in range(n):
        cell = "\\ig{{{0}}}".format(token)
        list.append(cell)

# This way "list" always has N*M elements. If more,
# it is truncated. If less, padded with empty strings:
N = 2 # elements per line
M = 4 # lines
for i in range(N*M):
    list.append("")
list = list[:N*M]


# Generate contents of LaTeX file:
tex_string  = '\\documentclass[english]{article}\n'
tex_string += '\\usepackage[a4paper,top=15mm,bottom=15mm,textwidth=190mm]{geometry}\n'
tex_string += '\\usepackage[T1]{fontenc}\n'
tex_string += '\\usepackage[dvips]{graphicx}\n'
tex_string += '\\usepackage{amssymb}\n'
tex_string += '\\usepackage[usenames]{color}\n'
tex_string += '\\usepackage[utf8]{inputenc}\n'
tex_string += '\\usepackage{charter}\n'
tex_string += '\\usepackage{babel}\n'
tex_string += '\\input{epsf}\n'
tex_string += '\\begin{document}\n'
tex_string += '\\newcommand{\\mc}{\\multicolumn}\n'
tex_string += '\\newcommand{\\mr}{\\multirow}\n'
tex_string += '\\newcommand{\\cw}{\\columnwidth}\n'
tex_string += '\\newcommand{\\ig}[1]{\\includegraphics[angle=90,width=89mm]{tokens/#1}}\n'
tex_string += '\\thispagestyle{empty}\n'
tex_string += '\\begin{center}\n'
tex_string += '  \\begin{tabular}{ccc}\n'

for i in range(M):
    line = ' & '.join(list[N*i:N*i+N])
    #tex_string += '      {0[0]} & {0[1]} & {0[2]}  \\\\\n'.format(list[3*i:3*i+3])
    tex_string += '      {0} \\\\\n'.format(line)

tex_string += '  \\end{tabular}\n'
tex_string += '\\end{center}\n'
tex_string += '\\end{document}\n'

# Save LaTeX file and compile to PDF:
with open("tokens.tex", "w") as f:
    f.write(tex_string)

cmd = "latex_parser tokens.tex"
s = sp.Popen(cmd, shell=True)
s.communicate()
