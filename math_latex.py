special_chars = ['\\$', '\\%', '\\_', '\\{', '\\}', '\\&', '\\#']

greek_letters = ['\\alpha', '\\beta', '\\gamma', '\\delta', '\\epsilon',
                 '\\zeta', '\\eta', '\\theta', '\\iota', '\\kappa', '\\lambda',
                 '\\mu', '\\nu', '\\xi', '\\omikron', '\\pi', '\\rho', '\\sigma', '\\tau',
                 '\\upsilon', '\\phi', '\\chi', '\\psi', '\\omega']

replace_token = {'~': '\\sim', '∼': '\\sim', 'π': '\\pi', '\\varpi': '\\pi', 'α':'\\alpha', 'λ': '\\lambda', '°': ['^', '\\circ'], 'θ': '\\theta', '\\vartheta': '\\theta', '¬': '\\neg',
                 '∈': '\\in', '≤': '\\le', '\\leq': '\\le', '\\leqq': '\\le', '→': '\\rightarrow', '\\to': '\\rightarrow', '∞': '\\infty', 
                 '∀': '\\forall', 'δ': '\\delta', '≥': '\\ge', '\\geq': '\\ge', '\\geqq': '\\ge', '\\geqslant': '\\ge', '∧': '\\wedge', '\\bigwedge': '\\wedge', '∨': '\\vee', '\\bigvee': '\\vee',
                 '∂': '\\partial', 'φ': '\\phi', 'ϕ': '\\phi', '\\varphi': '\\phi', 'β': '\\beta', 'σ': '\\sigma', '\\varsigma': '\\sigma', '\\Sigma': '\\sigma', 
                 '∩': '\\cap', '\\bigcap': '\\cap', 'ε': '\\epsilon', 'ω': '\\omega', '∃': '\\exists', 'μ': '\\mu', 'γ': '\\gamma', '≡': '\\equiv', '∪': '\\cup',
                 '\\bigcup': '\\cup', '√': '\\sqrt', '`': '\'', 'τ': '\\tau', '±': '\\pm', '≠': '\\neq', '∫': '\\int', 
                 'ϵ': '\\varepsilon', '\\longleftarrow': '\\leftarrow', '⇒': '\\rightarrow', '\\longrightarrow': '\\rightarrow', 'ρ': '\\rho', '\\varrho': '\\rho', 
                 '⊆': '\\subseteq', '⊇': '\\supseteq', '⊂': '\\subset', '⊃': '\\supset', '⊈': '\\nsubseteq', '⊉': '\\nsupseteq', '∉': '\\notin', 
                 '•': '\\bullet', '∇': '\\nabla', '´': '\\acute', '∑': '\\sum', 'ℝ': ['\\mathbb', '{', 'r', '}'], '⟩': '\\rangle', 
                 '⟨': '\\langle', '\\mid': '|', '\\vert': '|', 'ξ': '\\xi', '∘': '\\circ', 'η': '\\eta', '\\vareta': '\\eta', '↑': '\\uparrow', 
                 '↓': '\\downarrow', '←': '\\leftarrow', '‖': '\|', '∥': '\|', '⊕': '\\oplus', '\\bigoplus': '\\oplus', '≈': '\\approx', 'ζ': '\\zeta',
                 'ℤ': ['\\mathbb', '{', 'z', '}'], 'º': ['^', '\\circ'], '∠': '\\angle', '∅': '\\emptyset', 'ø': '\\emptyset', '◦': '\\circ', 
                 '⋯': '\\ldots', '⊗': '\\otimes', '\\bigotimes': '\\otimes', '‘': '\'', '’': '\'', '⇔': '\\leftrightarrow', '⊥': '\\perp', 'µ': '\\mu', 'χ': '\\chi', 
                 '─': '-', 'ℕ': ['\\mathbb', '{', 'n', '}'], '“': '"', '”': '"', '↦': '\\mapsto', '↔': '\\leftrightarrow', 
                 '⟹': '\\rightarrow', '∆': '\\delta', 'κ': '\\kappa', '\\varkappa': '\\kappa', '⊢': '\\vdash', '\cosθ': ['\\cos', '(', '\\theta', ')'], '\sinθ': ['\\sin', '(', '\\theta', ')'], 
                 '≅': '\\cong', '⌊': '\\lfoor', '⌋': '\\rfloor', '△': '\\triangle', '\\bigtriangleup': '\\triangle', '\\bigtriangledown': '\\triangledown', 
                 '，': ',', 'ℚ': ['\\mathbb', '{', 'q', '}'], '≦': '\\le', '\\leqslant': '\\le', '│': '|', '□': '\\square', '）': ')', '＝': '=', '⌈': '\\lceil', '⌉': '\\rceil', '\\bar': '\\overline', 
                 '\\ne': '\\neq', '\\lvert': '|', '\\rvert': '|', '\\land': '\\wedge', '\\gt': '>','\\lt': '<', '\\cr': '\\\\', '\\prime': '\'', '\\colon': ':', '\\bmod': '\\mod', 
                 '\\lbrace': '\{', '\\rbrace': '\}', '\\widehat': '\\hat', '\\widetilde': '\\tilde', '\\backslash': '\\', '\\longleftrightarrow': '\\leftrightarrow', '\\varnothing': '\\emptyset', '\\dbinom': '\\binom', '\\tbinom': '\\binom',
                 '\\bot': '\\perp', '\\lbrack': '[', '\\rbrack': ']', '\\parallel': '\|', '\\longmapsto': '\\mapsto', '\\intercal': 't', '\\bigsqcup': '\\sqcup', '\\bigtriangleup': '\\triangle', '\\intop': '\\int', '\\eps': '\\epsilon', 
                 '\\gets': '\\leftarrow', '\\bbbk': ['\\mathbb', '{', 'k', '}'], '\\thicksim': '\\sim', '\\biguplus': '\\uplus', '\\vartriangle': '\\triangle', '\\triangleleft': '\\lhd', '\\triangleright': '\\rhd', '\\vartriangleleft': '\\lhd',
                 '\\arrowvert': '|', 'é': ['\\\'', '{', 'e', '}'], '\\acute': '\\\'', '\\varsubsetneq': '\\subsetneq', '∞': '\infty', '–':'-', '−': '-'}

customize_operator = ['\\operatorname', '\\newcommand', '\\mathop', '\\def', '\\require', 
                      '\\declaremathoperator', '\\mathrel', '\\renewcommand', '\\eqref', '\\ref', '\\newenvironment']

format_operator = {'\\displaystyle abc', '\\color{}{}', '\\rm abc', '\\bf abc', '\\large abc', '\\cal abc', '\\small abc', 
                   '\\bbox[red]{abc}', '\\label{delete content}', '\\fbox{}', '\\mathbin{}', '\\scriptstyle{}', '\\unicode{need to delete}', 
                   '\\tt abc', '\\rlap{}', '\\scriptsize{}', '\\smash{}', '\\normalsize abc', '\\mathord{}', '\\srrc{}', '\\textstyle abc'}

deleted = {'\\pr': 33101, '\\re': 9919, '\\im': 6739, '\\of': 1233, '\\f': 1081, '\\cl': 1008, '\\rr': 516, '\\nn': 434, '\\u': 422, '\\ord': 249, '\\ann': 149, '\\vol': 144, '\\dosc': 142, '\\csod': 142, 
           '\\ass': 114, '\\cssid': 109}

not_optimized = {'\\over', '\\choose', '\\mod', '\\hspace', '\\boxed', '\\eqalign', '\\matrix', '\\phantom', '\\vphantom', '\\cases', '\\brace', '\\mkern', '\\hphantom', '\\verb',
                 '\\kern', '\\surd', '\\brack', '\\xleftarrow', '\\enclose', '\\array', '\\raise'}
