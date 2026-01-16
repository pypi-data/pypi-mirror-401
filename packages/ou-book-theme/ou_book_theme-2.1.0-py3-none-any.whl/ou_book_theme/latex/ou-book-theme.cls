\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ou-book-theme}[OU Book Theme v1]

\LoadClass{book}

\usepackage{tcolorbox}

% Define custom fonts
\usepackage{fontspec}
\setfontfamily{\poppinsbold}{Poppins-Bold.ttf}

% Define custom colours
\usepackage[dvipsnames]{xcolor}
\definecolor{ou-primary-blue}{RGB}{36, 40, 92}

\renewcommand{\sffamily}{\fontspec{Poppins}[
    Extension = .ttf ,
    UprightFont = *-Regular ,
    BoldFont = *-Bold ,
    ItalicFont = *-Italic ,
    BoldItalicFont = *-BoldItalic
  ]}

% OU title page definition
\renewcommand{\maketitle}{%
  \setmainfont{Poppins}[
    Extension = .ttf ,
    UprightFont = *-Regular ,
    BoldFont = *-Bold ,
    ItalicFont = *-Italic ,
    BoldItalicFont = *-BoldItalic
  ]

  \thispagestyle{empty}

  \hspace{0.75\textwidth}%
  \begin{minipage}[c][1.3cm][t]{0.25\textwidth}
    \includegraphics[width=5cm]{ou_primary_logo.png}
  \end{minipage} \\

  \vspace{4em}
  {\Huge\color{ou-primary-blue} \@title} \\
}

% OU chapter styling
\usepackage{fncychap}
