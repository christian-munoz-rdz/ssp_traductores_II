# Gramática del compilador

# (estado, entrada): (acción, siguiente_estado o producción)
action_table = {
    (0, 'tipo'): ('s', 5),
    (0, '$'): ('r', 'Definiciones -> \e'),
    (1, '$'): ('r', 'R0'),
    (2, '$'): ('r', 'programa -> Definiciones'),
    (3, 'tipo'): ('s', 5),
    (3, '$'): ('r', 'Definiciones -> \e'),
    (4, 'tipo'): ('r', 'Definicion -> DefVar'),
    (4, '$'): ('r', 'Definicion -> DefVar'),
    (5, 'identificador'): ('s', 8),
    (6,  'tipo'): ('r', 'Definicion -> DefFunc'),
    (6, '$'): ('r', 'Definicion -> DefFunc'),
    (7, '$'): ('r', 'Definiciones -> Definicion Definiciones'),
    (8, ';'): ('r', 'ListaVar -> \e'),
    (8, ','): ('s', 10),
    (8, '('): ('s', 11),
    (9, ';'): ('s', 12),
    (10, 'identificador'): ('s', 13),
    (11, 'tipo'): ('s', 15),
    (11, ')'): ('r', 'Parametros -> \e'),
    (12, 'identificador'): ('r', 'DefVar -> tipo identificador ListaVar ;'),
    (12, 'tipo'): ('r', 'DefVar -> tipo identificador ListaVar ;'),
    (12, '}'): ('r', 'DefVar -> tipo identificador ListaVar ;'),
    (12, 'if'): ('r', 'DefVar -> tipo identificador ListaVar ;'),
    (12, 'while'): ('r', 'DefVar -> tipo identificador ListaVar ;'),
    (12, 'return'): ('r', 'DefVar -> tipo identificador ListaVar ;'),
    (12, '$'): ('r', 'DefVar -> tipo identificador ListaVar ;'),
    (13, ';'): ('r', 'ListaVar -> \e'),
    (13, ','): ('s', 10),
    (14, ')'): ('s', 17),
    (15, 'identificador'): ('s', 18),
    (16, ';'): ('r', 'ListaVar -> , identificador ListaVar'),
    (17, '{'): ('s', 20),
    (18, ','): ('s', 22),
    (18, ')'): ('r', 'ListaParam -> \e'),
    (19, 'tipo'): ('r', 'DefFunc -> tipo identificador ( Parametros ) BloqFunc'),
    (19, '$'): ('r', 'DefFunc -> tipo identificador ( Parametros ) BloqFunc'),
    (20, 'identificador'): ('s', 27),
    (20, 'tipo'): ('s', 5),
    (20, '}'): ('r', 'DefLocales -> \e'),
    (20, 'if'): ('s', 28),
    (20, 'while'): ('s', 29),
    (20, 'return'): ('s', 30),
    (21, ')'): ('r', 'Parametros -> tipo identificador ListaParam'),
    (22, 'tipo'): ('s', 32),
    (23, '}'): ('s', 33),
    (24, 'identificador'): ('s', 27),
    (24, 'tipo'): ('s', 5),
    (24, '}'): ('r', 'DefLocales -> \e'),
    (24, 'if'): ('s', 28),
    (24, 'while'): ('s', 29),
    (24, 'return'): ('s', 30),
    (25, 'identificador'): ('r', 'DefLocal -> DefVar'),
    (25, 'tipo'): ('r', 'DefLocal -> DefVar'),
    (25, '}'): ('r', 'DefLocal -> DefVar'),
    (25, 'if'): ('r', 'DefLocal -> DefVar'),
    (25, 'while'): ('r', 'DefLocal -> DefVar'),
    (25, 'return'): ('r', 'DefLocal -> DefVar'),
    (26, 'identificador'): ('r', 'DefLocal -> Sentencia'),
    (26, 'tipo'): ('r', 'DefLocal -> Sentencia'),
    (26, '}'): ('r', 'DefLocal -> Sentencia'),
    (26, 'if'): ('r', 'DefLocal -> Sentencia'),
    (26, 'while'): ('r', 'DefLocal -> Sentencia'),
    (26, 'return'): ('r', 'DefLocal -> Sentencia'),
    (27, '('): ('s', 36),
    (27, '='): ('s', 35),
    (28, '('): ('s', 37),
    (29, '('): ('s', 38),
    (30, 'identificador'): ('s', 46),
    (30, 'entero'): ('s', 47),
    (30, 'real'): ('s', 48),
    (30, 'cadena '): ('s', 49),
    (30, 'opSuma '): ('s', 42),
    (30, 'opNot '): ('s', 43),
    (30, ';'): ('r', 'ValorRegresa -> \e'),
    (30, '('): ('s', 41),
    (31, ';'): ('s', 50),
    (31, 'identificador'): ('s', 51),
    (33, 'tipo'): ('r', 'BloqFunc -> { DefLocales }'),
    (33, '$'): ('r', 'BloqFunc -> { DefLocales }'),
    (34, '}'): ('r', 'DefLocales -> DefLocal DefLocales'),
    (35, 'identificador'): ('s', 46),
    (35, 'entero'): ('s', 47),
    (35, 'real'): ('s', 48),
    (35, 'cadena'): ('s', 49),
    (35, 'opSuma'): ('s', 42),
    (35, 'opNot'): ('s', 43),
    (35, '('): ('s', 41),
    (36, 'identificador'): ('s', 46),
    (36, 'entero'): ('s', 47),
    (36, 'real'): ('s', 48),
    (36, 'cadena'): ('s', 49),
    (36, 'opSuma'): ('s', 42),
    (36, 'opNot'): ('s', 43),
    (36, '('): ('s', 41),
    (36, ')'): ('r', 'Argumentos -> \e'),
    (37, 'identificador'): ('s', 46),
    (37, 'entero'): ('s', 47),
    (37, 'real'): ('s', 48),
    (37, 'cadena'): ('s', 49),
    (37, 'opSuma'): ('s', 42),
    (37, 'opNot'): ('s', 43),
    (37, '('): ('s', 41),
    (38, 'identificador'): ('s', 46),
    (38, 'entero'): ('s', 47),
    (38, 'real'): ('s', 48),
    (38, 'cadena'): ('s', 49),
    (38, 'opSuma'): ('s', 42),
    (38, 'opNot'): ('s', 43),
    (38, '('): ('s', 41),
    (39, ';'): ('s', 57),
    (40, 'opSuma'): ('s', 59),
    (40, 'opMul'): ('s', 58),
    (40, 'opRelac'): ('s', 60),
    (40, 'opOr'): ('s', 63),
    (40, 'opAnd'): ('s', 62),
    (40, 'opIgualdad'): ('s', 61),
    (40, ';'): ('r', 'ValorRegresa -> Expresion'),
    (41, 'identificador'): ('s', 46),
    (41, 'entero'): ('s', 47),
    (41, 'real'): ('s', 48),
    (41, 'cadena'): ('s', 49),
    (41, 'opSuma'): ('s', 42),
    (41, 'opNot'): ('s', 43),
    (41, '('): ('s', 41),
    (42, 'identificador'): ('s', 46),
    (42, 'entero'): ('s', 47),
    (42, 'real'): ('s', 48),
    (42, 'cadena'): ('s', 49),
    (42, 'opSuma'): ('s', 42),
    (42, 'opNot'): ('s', 43),
    (42, '('): ('s', 41),
    (43, 'identificador'): ('s', 46),
    (43, 'entero'): ('s', 47),
    (43, 'real'): ('s', 48),
    (43, 'cadena'): ('s', 49),
    (43, 'opSuma'): ('s', 42),
    (43, 'opNot'): ('s', 43),
    (43, '('): ('s', 41),
    (44, 'opSuma'): ('r', 'Expresion -> Termino'),
    (44, 'opMul'): ('r', 'Expresion -> Termino'),
    (44, 'opRelac'): ('r', 'Expresion -> Termino'),
    (44, 'opOr'): ('r', 'Expresion -> Termino'),
    (44, 'opAnd'): ('r', 'Expresion -> Termino'),
    (44, 'opIgualdad'): ('r', 'Expresion -> Termino'),
    (44, ';'): ('r', 'Expresion -> Termino'),
    (44, ','): ('r', 'Expresion -> Termino'),
    (44, ')'): ('r', 'Expresion -> Termino'),
    (45, 'opSuma'): ('r', 'Termino -> LlamadaFunc'),
    (45, 'opMul'): ('r', 'Termino -> LlamadaFunc'),
    (45, 'opRelac'): ('r', 'Termino -> LlamadaFunc'),
    (45, 'opOr'): ('r', 'Termino -> LlamadaFunc'),
    (45, 'opAnd'): ('r', 'Termino -> LlamadaFunc'),
    (45, 'opIgualdad'): ('r', 'Termino -> LlamadaFunc'),
    (45, ';'): ('r', 'Termino -> LlamadaFunc'),
    (45, ','): ('r', 'Termino -> LlamadaFunc'),
    (45, ')'): ('r', 'Termino -> LlamadaFunc'),
    (46, 'opSuma'): ('r', 'Termino -> identificador'),
    (46, 'opMul'): ('r', 'Termino -> identificador'),
    (46, 'opRelac'): ('r', 'Termino -> identificador'),
    (46, 'opOr'): ('r', 'Termino -> identificador'),
    (46, 'opAnd'): ('r', 'Termino -> identificador'),
    (46, 'opIgualdad'): ('r', 'Termino -> identificador'),
    (46, ';'): ('r', 'Termino -> identificador'),
    (46, ','): ('r', 'Termino -> identificador'),
    (46, '('): ('s', 36),
    (46, ')'): ('r', 'Termino -> identificador'),
    (47, 'opSuma'): ('r', 'Termino -> entero'),
    (47, 'opMul'): ('r', 'Termino -> entero'),
    (47, 'opRelac'): ('r', 'Termino -> entero'),
    (47, 'opOr'): ('r', 'Termino -> entero'),
    (47, 'opAnd'): ('r', 'Termino -> entero'),
    (47, 'opIgualdad'): ('r', 'Termino -> entero'),
    (47, ';'): ('r', 'Termino -> entero'),
    (47, ','): ('r', 'Termino -> entero'),
    (47, ')'): ('r', 'Termino -> entero'),
    (48, 'opSuma'): ('r', 'Termino -> real'),
    (48, 'opMul'): ('r', 'Termino -> real'),
    (48, 'opRelac'): ('r', 'Termino -> real'),
    (48, 'opOr'): ('r', 'Termino -> real'),
    (48, 'opAnd'): ('r', 'Termino -> real'),
    (48, 'opIgualdad'): ('r', 'Termino -> real'),
    (48, ';'): ('r', 'Termino -> real'),
    (48, ','): ('r', 'Termino -> real'),
    (48, ')'): ('r', 'Termino -> real'),
    (49, 'opSuma'): ('r', 'Termino -> cadena'),
    (49, 'opMul'): ('r', 'Termino -> cadena'),
    (49, 'opRelac'): ('r', 'Termino -> cadena'),
    (49, 'opOr'): ('r', 'Termino -> cadena'),
    (49, 'opAnd'): ('r', 'Termino -> cadena'),
    (49, 'opIgualdad'): ('r', 'Termino -> cadena'),
    (49, ';'): ('r', 'Termino -> cadena'),
    (49, ','): ('r', 'Termino -> cadena'),
    (49, ')'): ('r', 'Termino -> cadena'),
    (50, 'identificador'): ('r', 'Sentencia -> LlamadaFunc ;'),
    (50, 'tipo'): ('r', 'Sentencia -> LlamadaFunc ;'),
    (50, '}'): ('r', 'Sentencia -> LlamadaFunc ;'),
    (50, 'if'): ('r', 'Sentencia -> LlamadaFunc ;'),
    (50, 'while'): ('r', 'Sentencia -> LlamadaFunc ;'),
    (50, 'return'): ('r', 'Sentencia -> LlamadaFunc ;'),
    (50, 'else'): ('r', 'Sentencia -> LlamadaFunc ;'),
    (51, ','): ('s', 22),
    (51, ')'): ('r', 'ListaParam -> \e'),
    (52, 'opSuma'): ('s', 59),
    (52, 'opMul'): ('s', 58),
    (52, 'opRelac'): ('s', 60),
    (52, 'opOr'): ('s', 63),
    (52, 'opAnd'): ('s', 62),
    (52, 'opIgualdad'): ('s', 61),
    (52, ';'): ('s', 68),
    (53, ')'): ('s', 69),
    (54, 'opSuma'): ('s', 59),
    (54, 'opMul'): ('s', 58),
    (54, 'opRelac'): ('s', 60),
    (54, 'opOr'): ('s', 63),
    (54, 'opAnd'): ('s', 62),
    (54, 'opIgualdad'): ('s', 61),
    (54, ','): ('s', 71),
    (54, ')'): ('r', 'ListaArgumentos -> \e'),
    (55, 'opSuma'): ('s', 59),
    (55, 'opMul'): ('s', 58),
    (55, 'opRelac'): ('s', 60),
    (55, 'opOr'): ('s', 63),
    (55, 'opAnd'): ('s', 62),
    (55, 'opIgualdad'): ('s', 61),
    (55, ')'): ('s', 72),
    (56, 'opSuma'): ('s', 59),
    (56, 'opMul'): ('s', 58),
    (56, 'opRelac'): ('s', 60),
    (56, 'opOr'): ('s', 63),
    (56, 'opAnd'): ('s', 62),
    (56, 'opIgualdad'): ('s', 61),
    (56, ')'): ('s', 73),
    (57, 'identificador'): ('r', 'Sentencia -> return ValorRegresa ;'),
    (57, 'tipo'): ('r', 'Sentencia -> return ValorRegresa ;'),
    (57, '}'): ('r', 'Sentencia -> return ValorRegresa ;'),
    (57, 'if'): ('r', 'Sentencia -> return ValorRegresa ;'),
    (57, 'while'): ('r', 'Sentencia -> return ValorRegresa ;'),
    (57, 'return'): ('r', 'Sentencia -> return ValorRegresa ;'),
    (57, 'else'): ('r', 'Sentencia -> return ValorRegresa ;'),
    (58, 'identificador'): ('s', 46),
    (58, 'entero'): ('s', 47),
    (58, 'real'): ('s', 48),
    (58, 'cadena'): ('s', 49),
    (58, 'opSuma'): ('s', 42),
    (58, 'opNot'): ('s', 43),
    (58, '('): ('s', 41),
    (59, 'identificador'): ('s', 46),
    (59, 'entero'): ('s', 47),
    (59, 'real'): ('s', 48),
    (59, 'cadena'): ('s', 49),
    (59, 'opSuma'): ('s', 42),
    (59, 'opNot'): ('s', 43),
    (59, '('): ('s', 41),
    (60, 'identificador'): ('s', 46),
    (60, 'entero'): ('s', 47),
    (60, 'real'): ('s', 48),
    (60, 'cadena'): ('s', 49),
    (60, 'opSuma'): ('s', 42),
    (60, 'opNot'): ('s', 43),
    (60, '('): ('s', 41),
    (61, 'identificador'): ('s', 46),
    (61, 'entero'): ('s', 47),
    (61, 'real'): ('s', 48),
    (61, 'cadena'): ('s', 49),
    (61, 'opSuma'): ('s', 42),
    (61, 'opNot'): ('s', 43),
    (61, '('): ('s', 41),
    (62, 'identificador'): ('s', 46),
    (62, 'entero'): ('s', 47),
    (62, 'real'): ('s', 48),
    (62, 'cadena'): ('s', 49),
    (62, 'opSuma'): ('s', 42),
    (62, 'opNot'): ('s', 43),
    (62, '('): ('s', 41),
    (63, 'identificador'): ('s', 46),
    (63, 'entero'): ('s', 47),
    (63, 'real'): ('s', 48),
    (63, 'cadena'): ('s', 49),
    (63, 'opSuma'): ('s', 42),
    (63, 'opNot'): ('s', 43),
    (63, '('): ('s', 41),
    (64, 'opSuma'): ('s', 59),
    (64, 'opMul'): ('s', 58),
    (64, 'opRelac'): ('s', 60),
    (64, 'opOr'): ('s', 63),
    (64, 'opAnd'): ('s', 62),
    (64, 'opIgualdad'): ('s', 61),
    (64, ')'): ('s', 80),
    (65, 'opSuma'): ('r', 'Expresion -> opSuma Expresion'),
    (65, 'opMul'): ('r', 'Expresion -> opSuma Expresion'),
    (65, 'opRelac'): ('r', 'Expresion -> opSuma Expresion'),
    (65, 'opOr'): ('r', 'Expresion -> opSuma Expresion'),
    (65, 'opAnd'): ('r', 'Expresion -> opSuma Expresion'),
    (65, 'opIgualdad'): ('r', 'Expresion -> opSuma Expresion'),
    (65, ';'): ('r', 'Expresion -> opSuma Expresion'),
    (65, ','): ('r', 'Expresion -> opSuma Expresion'),
    (65, ')'): ('r', 'Expresion -> opSuma Expresion'),
    (66, 'opSuma'): ('r', 'Expresion -> opNot Expresion'),
    (66, 'opMul'): ('r', 'Expresion -> opNot Expresion'),
    (66, 'opRelac'): ('r', 'Expresion -> opNot Expresion'),
    (66, 'opOr'): ('r', 'Expresion -> opNot Expresion'),
    (66, 'opAnd'): ('r', 'Expresion -> opNot Expresion'),
    (66, 'opIgualdad'): ('r', 'Expresion -> opNot Expresion'),
    (66, ';'): ('r', 'Expresion -> opNot Expresion'),
    (66, ','): ('r', 'Expresion -> opNot Expresion'),
    (66, ')'): ('r', 'Expresion -> opNot Expresion'),
    (67, ')'): ('r', 'ListaParam -> , tipo identificador ListaParam'),
    (68, 'identificador'): ('r', 'Sentencia -> identificador = Expresion ;'),
    (68, 'tipo'): ('r', 'Sentencia -> identificador = Expresion ;'),
    (68, '}'): ('r', 'Sentencia -> identificador = Expresion ;'),
    (68, 'if'): ('r', 'Sentencia -> identificador = Expresion ;'),
    (68, 'while'): ('r', 'Sentencia -> identificador = Expresion ;'),
    (68, 'return'): ('r', 'Sentencia -> identificador = Expresion ;'),
    (68, 'else'): ('r', 'Sentencia -> identificador = Expresion ;'),
    (69, 'opSuma'): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (69, 'opMul'): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (69, 'opRelac'): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (69, 'opOr'): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (69, 'opAnd'): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (69, 'opIgualdad'): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (69, ';'): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (69, ','): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (69, ')'): ('r', 'LlamadaFunc -> identificador ( Argumentos )'),
    (70, ')'): ('r', 'Argumentos -> Expresion ListaArgumentos'),
    (71, 'identificador'): ('s', 46),
    (71, 'entero'): ('s', 47),
    (71, 'real'): ('s', 48),
    (71, 'cadena'): ('s', 49),
    (71, 'opSuma'): ('s', 42),
    (71, 'opNot'): ('s', 43),
    (71, '('): ('s', 41),
    (72, 'identificador'): ('s', 27),
    (72, '{'): ('s', 85),
    (72, 'if'): ('s', 28),
    (72, 'while'): ('s', 29),
    (72, 'return'): ('s', 30),
    (73, '{'): ('s', 85),
    (74, 'opSuma'): ('r', 'Expresion -> Expresion opMul Expresion'),
    (74, 'opMul'): ('r', 'Expresion -> Expresion opMul Expresion'),
    (74, 'opRelac'): ('r', 'Expresion -> Expresion opMul Expresion'),
    (74, 'opOr'): ('r', 'Expresion -> Expresion opMul Expresion'),
    (74, 'opAnd'): ('r', 'Expresion -> Expresion opMul Expresion'),
    (74, 'opIgualdad'): ('r', 'Expresion -> Expresion opMul Expresion'),
    (74, ';'): ('r', 'Expresion -> Expresion opMul Expresion'),
    (74, ','): ('r', 'Expresion -> Expresion opMul Expresion'),
    (74, ')'): ('r', 'Expresion -> Expresion opMul Expresion'),
    (75, 'opSuma'): ('r', 'Expresion -> Expresion opSuma Expresion'),
    (75, 'opMul'): ('s', 58),
    (75, 'opRelac'): ('r', 'Expresion -> Expresion opSuma Expresion'),
    (75, 'opOr'): ('r', 'Expresion -> Expresion opSuma Expresion'),
    (75, 'opAnd'): ('r', 'Expresion -> Expresion opSuma Expresion'),
    (75, 'opIgualdad'): ('r', 'Expresion -> Expresion opSuma Expresion'),
    (75, ';'): ('r', 'Expresion -> Expresion opSuma Expresion'),
    (75, ','): ('r', 'Expresion -> Expresion opSuma Expresion'),
    (75, ')'): ('r', 'Expresion -> Expresion opSuma Expresion'),
    (76, 'opSuma'): ('s', 59),
    (76, 'opMul'): ('s', 58),
    (76, 'opRelac'): ('r', 'Expresion -> Expresion opRelac Expresion'),
    (76, 'opOr'): ('r', 'Expresion -> Expresion opRelac Expresion'),
    (76, 'opAnd'): ('r', 'Expresion -> Expresion opRelac Expresion'),
    (76, 'opIgualdad'): ('r', 'Expresion -> Expresion opRelac Expresion'),
    (76, ';'): ('r', 'Expresion -> Expresion opRelac Expresion'),
    (76, ','): ('r', 'Expresion -> Expresion opRelac Expresion'),
    (76, ')'): ('r', 'Expresion -> Expresion opRelac Expresion'),
    (77, 'opSuma'): ('s', 59),
    (77, 'opMul'): ('s', 58),
    (77, 'opRelac'): ('s', 60),
    (77, 'opOr'): ('r', 'Expresion -> Expresion opIgualdad Expresion'),
    (77, 'opAnd'): ('r', 'Expresion -> Expresion opIgualdad Expresion'),
    (77, 'opIgualdad'): ('r', 'Expresion -> Expresion opIgualdad Expresion'),
    (77, ';'): ('r', 'Expresion -> Expresion opIgualdad Expresion'),
    (77, ','): ('r', 'Expresion -> Expresion opIgualdad Expresion'),
    (77, ')'): ('r', 'Expresion -> Expresion opIgualdad Expresion'),
    (78, 'opSuma'): ('s', 59),
    (78, 'opMul'): ('s', 58),
    (78, 'opRelac'): ('s', 60),
    (78, 'opOr'): ('r', 'Expresion -> Expresion opAnd Expresion'),
    (78, 'opAnd'): ('r', 'Expresion -> Expresion opAnd Expresion'),
    (78, 'opIgualdad'): ('s', 61),
    (78, ';'): ('r', 'Expresion -> Expresion opAnd Expresion'),
    (78, ','): ('r', 'Expresion -> Expresion opAnd Expresion'),
    (78, ')'): ('r', 'Expresion -> Expresion opAnd Expresion'),
    (79, 'opSuma'): ('s', 59),
    (79, 'opMul'): ('s', 58),
    (79, 'opRelac'): ('s', 60),
    (79, 'opOr'): ('r', 'Expresion -> Expresion opOr Expresion'),
    (79, 'opAnd'): ('s', 62),
    (79, 'opIgualdad'): ('s', 61),
    (79, ';'): ('r', 'Expresion -> Expresion opOr Expresion'),
    (79, ','): ('r', 'Expresion -> Expresion opOr Expresion'),
    (79, ')'): ('r', 'Expresion -> Expresion opOr Expresion'),
    (80, 'opSuma'): ('r', 'Expresion -> ( Expresion )'),
    (80, 'opMul'): ('r', 'Expresion -> ( Expresion )'),
    (80, 'opRelac'): ('r', 'Expresion -> ( Expresion )'),
    (80, 'opOr'): ('r', 'Expresion -> ( Expresion )'),
    (80, 'opAnd'): ('r', 'Expresion -> ( Expresion )'),
    (80, 'opIgualdad'): ('r', 'Expresion -> ( Expresion )'),
    (80, ';'): ('r', 'Expresion -> ( Expresion )'),
    (80, ','): ('r', 'Expresion -> ( Expresion )'),
    (80, ')'): ('r', 'Expresion -> ( Expresion )'),
    (81, 'opSuma'): ('s', 59),
    (81, 'opMul'): ('s', 58),
    (81, 'opRelac'): ('s', 60),
    (81, 'opOr'): ('s', 63),
    (81, 'opAnd'): ('s', 62),
    (81, 'opIgualdad'): ('s', 61),
    (81, ','): ('s', 71),
    (81, ')'): ('r', 33),
    (82, 'identificador'): ('r', 'Otro -> \e'),
    (82, 'tipo'): ('r', 'Otro -> \e'),
    (82, '}'): ('r', 'Otro -> \e'),
    (82, 'if'): ('r', 'Otro -> \e'),
    (82, 'while'): ('r', 'Otro -> \e'),
    (82, 'return'): ('r', 'Otro -> \e'),
    (82, 'else'): ('s', 89),
    (83, 'identificador'): ('r', 'SentenciaBloque -> Sentencia'),
    (83, 'tipo'): ('r', 'SentenciaBloque -> Sentencia'),
    (83, '}'): ('r', 'SentenciaBloque -> Sentencia'),
    (83, 'if'): ('r', 'SentenciaBloque -> Sentencia'),
    (83, 'while'): ('r', 'SentenciaBloque -> Sentencia'),
    (83, 'return'): ('r', 'SentenciaBloque -> Sentencia'),
    (83, 'else'): ('r', 'SentenciaBloque -> Sentencia'),
    (84, 'identificador'): ('r', 'SentenciaBloque -> Bloque'),
    (84, 'tipo'): ('r', 'SentenciaBloque -> Bloque'),
    (84, '}'): ('r', 'SentenciaBloque -> Bloque'),
    (84, 'if'): ('r', 'SentenciaBloque -> Bloque'),
    (84, 'while'): ('r', 'SentenciaBloque -> Bloque'),
    (84, 'return'): ('r', 'SentenciaBloque -> Bloque'),
    (84, 'else'): ('r', 'SentenciaBloque -> Bloque'),
    (85, 'identificador'): ('s', 27),
    (85, '}'): ('r', 'Sentencias -> \e'),
    (85, 'if'): ('s', 28),
    (85, 'while'): ('s', 29),
    (85, 'return'): ('s', 30),
    (86, 'identificador'): ('r', 'Sentencia -> while ( Expresion ) Bloque'),
    (86, 'tipo'): ('r', 'Sentencia -> while ( Expresion ) Bloque'),
    (86, '}'): ('r', 'Sentencia -> while ( Expresion ) Bloque'),
    (86, 'if'): ('r', 'Sentencia -> while ( Expresion ) Bloque'),
    (86, 'while'): ('r', 'Sentencia -> while ( Expresion ) Bloque'),
    (86, 'return'): ('r', 'Sentencia -> while ( Expresion ) Bloque'),
    (86, 'else'): ('r', 'Sentencia -> while ( Expresion ) Bloque'),
    (87, ')'): ('r', 'ListaArgumentos -> , Expresion ListaArgumentos'),
    (88, 'identificador'): ('r', 'Sentencia -> if ( Expresion ) SentenciaBloque Otro'),
    (88, 'tipo'): ('r', 'Sentencia -> if ( Expresion ) SentenciaBloque Otro'),
    (88, '}'): ('r', 'Sentencia -> if ( Expresion ) SentenciaBloque Otro'),
    (88, 'if'): ('r', 'Sentencia -> if ( Expresion ) SentenciaBloque Otro'),
    (88, 'while'): ('r', 'Sentencia -> if ( Expresion ) SentenciaBloque Otro'),
    (88, 'return'): ('r', 'Sentencia -> if ( Expresion ) SentenciaBloque Otro'),
    (88, 'else'): ('r', 'Sentencia -> if ( Expresion ) SentenciaBloque Otro'),
    (89, 'identificador'): ('s', 27),
    (89, '{'): ('s', 85),
    (89, 'if'): ('s', 28),
    (89, 'while'): ('s', 29),
    (89, 'return'): ('s', 30),
    (90, '}'): ('s', 93),
    (91, 'identificador'): ('s', 27),
    (91, '}'): ('r', 'Sentencias -> \e'),
    (91, 'if'): ('s', 28),
    (91, 'while'): ('s', 29),
    (91, 'return'): ('s', 30),
    (92, 'identificador'): ('r', 'Otro -> else SentenciaBloque'),
    (92, 'tipo'): ('r', 'Otro -> else SentenciaBloque'),
    (92, '}'): ('r', 'Otro -> else SentenciaBloque'),
    (92, 'if'): ('r', 'Otro -> else SentenciaBloque'),
    (92, 'while'): ('r', 'Otro -> else SentenciaBloque'),
    (92, 'return'): ('r', 'Otro -> else SentenciaBloque'),
    (93, 'identificador'): ('r', 'Bloque -> { Sentencias }'),
    (93, 'tipo'): ('r', 'Bloque -> { Sentencias }'),
    (93, '}'): ('r', 'Bloque -> { Sentencias }'),
    (93, 'if'): ('r', 'Bloque -> { Sentencias }'),
    (93, 'while'): ('r', 'Bloque -> { Sentencias }'),
    (93, 'return'): ('r', 'Bloque -> { Sentencias }'),
    (93, 'else'): ('r', 'Bloque -> { Sentencias }'),
    (94, '}'): ('r', 'Sentencias -> Sentencia Sentencias')
}

# (estado actual, No_terminal): nuevo_estado
goto_table = {
    (0, 'programa'): 1,
    (0, 'Definiciones'): 2,
    (0, 'Definicion'): 3,
    (0, 'DefVar'):4,
    (0, 'DefFunc'):6,
    (3, 'Definiciones'): 7,
    (3, 'Definicion'): 3,
    (3, 'DefVar'):4,
    (3, 'DefFunc'):6,
    (8, 'ListaVar'): 9,
    (11, 'Parametros'): 14,
    (13, 'ListaVar'): 16,
    (17, 'BloqFunc'): 19,
    (18, 'ListaParam'): 21,
    (20, 'DefVar'): 25,
    (20, 'DefLocales'): 23,
    (20, 'DefLocal'): 24,
    (20, 'Sentencia'): 26,
    (20, 'LlamadaFunc'): 31,
    (24, 'DefVar'): 25,
    (24, 'DefLocales'): 34,
    (24, 'DefLocal'): 24,
    (24, 'Sentencia'): 26,
    (24, 'LlamadaFunc'): 31,
    (30, 'ValorRegresa'): 39,
    (30, 'Termino'): 44,
    (30, 'LlamadaFunc'): 45,
    (30, 'Expresion'): 40,
    (35, 'Termino'): 44,
    (35, 'LlamadaFunc'): 45,
    (35, 'Expresion'): 52,
    (36, 'Argumentos'): 53,
    (36, 'Termino'): 44,
    (36, 'LlamadaFunc'): 45,
    (36, 'Expresion'): 54,
    (37, 'Termino'): 44,
    (37, 'LlamadaFunc'): 45,
    (37, 'Expresion'): 55,
    (38, 'Termino'): 44,
    (38, 'LlamadaFunc'): 45,
    (38, 'Expresion'): 56,
    (41, 'Termino'): 44,
    (41, 'LlamadaFunc'): 45,
    (41, 'Expresion'): 64,
    (42, 'Termino'): 44,
    (42, 'LlamadaFunc'): 45,
    (42, 'Expresion'): 65,
    (43, 'Termino'): 44,
    (43, 'LlamadaFunc'): 45,
    (43, 'Expresion'): 66,
    (51, 'ListaParam'): 67,
    (54, 'ListaArgumentos'): 70,
    (58, 'Termino'): 44,
    (58, 'LlamadaFunc'): 45,
    (58, 'Expresion'): 74,
    (59, 'Termino'): 44,
    (59, 'LlamadaFunc'): 45,
    (59, 'Expresion'): 75,
    (60, 'Termino'): 44,
    (60, 'LlamadaFunc'): 45,
    (60, 'Expresion'): 76,
    (61, 'Termino'): 44,
    (61, 'LlamadaFunc'): 45,
    (61, 'Expresion'): 77,
    (62, 'Termino'): 44,
    (62, 'LlamadaFunc'): 45,
    (62, 'Expresion'): 78,
    (63, 'Termino'): 44,
    (63, 'LlamadaFunc'): 45,
    (63, 'Expresion'): 79,
    (71, 'Termino'): 44,
    (71, 'LlamadaFunc'): 45,
    (71, 'Expresion'): 81,
    (72, 'Sentencia'): 83,
    (72, 'Bloque'): 84,
    (72, 'LlamadaFunc'): 31,
    (72, 'SentenciaBloque'): 82,
    (72, 'Bloque'): 86,
    (81, 'ListaArgumentos'): 87,
    (82, 'Otro'): 88,
    (85, 'Sentencias'): 90,
    (85, 'Sentencia'): 91,
    (85, 'LlamadaFunc'): 31,
    (89, 'Sentencia'): 83,
    (89, 'Bloque'): 84,
    (89, 'LlamadaFunc'): 31,
    (89, 'SentenciaBloque'): 92,
    (91, 'Sentencias'): 94,
    (91, 'Sentencia'): 91,
    (91, 'LlamadaFunc'): 31
}

# 'produccion': ('no_terminal', cantidad_de_elementos)
grammar_rules = {
    'programa -> Definiciones': ('programa', 1),
    'Definiciones -> \e': ('Definiciones', 0),
    'Definiciones -> Definicion Definiciones': ('Definiciones', 2),
    'Definicion -> DefVar': ('Definicion', 1),
    'Definicion -> DefFunc': ('Definicion', 1),
    'DefVar -> tipo identificador ListaVar ;': ('DefVar', 4),
    'ListaVar -> \e': ('ListaVar', 0),
    'ListaVar -> , identificador ListaVar': ('ListaVar', 3),
    'DefFunc -> tipo identificador ( Parametros ) BloqFunc': ('DefFunc', 6), #revisar
    'Parametros -> \e': ('Parametros', 0),
    'Parametros -> tipo identificador ListaParam': ('Parametros', 3),
    'ListaParam -> \e': ('ListaParam', 0),
    'ListaParam -> , tipo identificador ListaParam': ('ListaParam', 4),
    'BloqFunc -> { DefLocales }': ('BloqFunc', 3),
    'DefLocales -> \e': ('DefLocales', 0),
    'DefLocales -> DefLocal DefLocales': ('DefLocales', 2),
    'DefLocal -> DefVar': ('DefLocal', 1),
    'DefLocal -> Sentencia': ('DefLocal', 1),
    'Sentencias -> \e': ('Sentencias', 0),
    'Sentencias -> Sentencia Sentencias': ('Sentencias', 2),
    'Sentencia -> identificador = Expresion ;': ('Sentencia', 4),
    'Sentencia -> if ( Expresion ) SentenciaBloque Otro': ('Sentencia', 5),
    'Sentencia -> while ( Expresion ) Bloque': ('Sentencia', 5), #revisar
    'Sentencia -> return ValorRegresa ;': ('Sentencia', 3),
    'Sentencia -> LlamadaFunc ;': ('Sentencia', 2),
    'Otro -> \e': ('Otro', 0),
    'Otro -> else SentenciaBloque': ('Otro', 2),
    'Bloque -> { Sentencias }': ('Bloque', 3),
    'ValorRegresa -> \e': ('ValorRegresa', 0),
    'ValorRegresa -> Expresion': ('ValorRegresa', 1),
    'Argumentos -> \e': ('Argumentos', 0),
    'Argumentos -> Expresion ListaArgumentos': ('Argumentos', 2),
    'ListaArgumentos -> \e': ('ListaArgumentos', 0),
    'ListaArgumentos -> , Expresion ListaArgumentos': ('ListaArgumentos', 3),
    'Termino -> LlamadaFunc': ('Termino', 1),
    'Termino -> identificador': ('Termino', 1),
    'Termino -> entero': ('Termino', 1),
    'Termino -> real': ('Termino', 1),
    'Termino -> cadena': ('Termino', 1),
    'LlamadaFunc -> identificador ( Argumentos )': ('LlamadaFunc', 4),
    'SentenciaBloque -> Sentencia': ('SentenciaBloque', 1),
    'SentenciaBloque -> Bloque': ('SentenciaBloque', 1),
    'Expresion -> ( Expresion )': ('Expresion', 3),
    'Expresion -> opSuma Expresion': ('Expresion', 2),
    'Expresion -> opNot Expresion': ('Expresion', 2),
    'Expresion -> Expresion opMul Expresion': ('Expresion', 3),
    'Expresion -> Expresion opSuma Expresion': ('Expresion', 3),
    'Expresion -> Expresion opRelac Expresion': ('Expresion', 3),
    'Expresion -> Expresion opIgualdad Expresion': ('Expresion', 3),
    'Expresion -> Expresion opAnd Expresion': ('Expresion', 3),
    'Expresion -> Expresion opOr Expresion': ('Expresion', 3),
    'Expresion -> Termino': ('Expresion', 1), 
}

# Objeto ElementoPila y herencias

class ElementoPila:
    def __init__(self, simbolo=None, valor=None, numero=None):
        self.simbolo = simbolo
        self.valor = valor
        self.numero = numero

    def __repr__(self):
        return f"{self.simbolo} {self.valor} {self.numero}"

class Terminal(ElementoPila):
    def __init__(self, simbolo= None, valor= None, numero= None):
        super().__init__(simbolo, valor, numero)

class NoTerminal(ElementoPila):
    def __init__(self, simbolo= None, valor= None, numero= None):
        super().__init__(simbolo, valor, numero)

class Estado(ElementoPila):
    def __init__(self, simbolo= None, valor= None, numero= None):
        super().__init__(simbolo, valor, numero)

def es_letra(c):
    return c.isalpha()

def es_digito(c):
    return c.isdigit()

def es_identificador(input):
    if input[0].isalpha():
        for char in input[1:]:
            if not (char.isalpha() or char.isdigit()):
                return False
        return True
    return False

def es_entero(input):
    if input[0].isdigit():
        for char in input[1:]:
            if not char.isdigit():
                return False
        return True
    return False

def es_real(input):
    if not input[0].isdigit():
        return False
    elif input[0].isdigit:
        pos=1
        for char in input[1:]:
            if not (char.isdigit() or char == '.'):
                return False
            elif char == '.':
                if '.' in input[pos+1:]:
                    return False
            pos += 1
        if input[-1] == '.':
            return False
        return True

def es_cadena(input):
    if input[0] == '"' and input[-1] == '"':
        return True
    return False

def es_espacio(c):
    return c in ' \t\n\r'

def obtener_tokens(codigo):
    tokens = {
        ";": (";", ";", 12), ",": (",", ",", 13), "(": ("(", "(", 14), ")": (")", ")", 15),
        "{": ("{", "{", 16), "}": ("}", "}", 17), "=": ("=", "=", 18),
        "if": ("if", "if", 19), "while": ("while", "while", 20),
        "return": ("return", "return", 21), "else": ("else", "else", 22),
        "+": ("opSuma", "+", 5), "-": ("opSuma", "-", 5),
        "||": ("opOr", "||", 8), "&&": ("opAnd", "&&", 9), "!": ("opNot", "!", 10),
        "*": ("opMul", "*", 6), "/": ("opMul", "/", 6),
        "==": ("Operador Igualdad", "==", 11), "!=": ("opIgualdad", "!=", 11), "<": ("opRelac", "<", 7),
        "<=": ("opRelac", "<=", 7), ">": ("opRelac", ">", 7), ">=": ("opRelac", ">=", 7),
        "$": ("Fin de Archivo", "$", 23)
    }
    tipos_de_dato = ["int", "float", "void"]

    i = 0
    longitud = len(codigo)
    tokens_identificados = []

    while i < longitud:
        if es_espacio(codigo[i]):
            i += 1
            continue
        
        temp = ""
        
        if codigo[i] == '"':  # Inicio de cadena
            inicio_cadena = i
            i += 1
            while i < longitud and codigo[i] != '"':
                temp += codigo[i]
                i += 1
            if i < longitud and codigo[i] == '"':  # Cerrar cadena correctamente
                temp = codigo[inicio_cadena:i+1]
                token = Terminal("cadena", temp, 3)
                tokens_identificados.append(token)
                i += 1
            else:
                # Error: cadena no cerrada
                temp = codigo[inicio_cadena:i+1]
                token = Terminal("Error", temp, -1)
                tokens_identificados.append(token)
        
        elif es_letra(codigo[i]):  # Inicio de identificador o palabra reservada
            inicio_token = i
            while i < longitud and (es_letra(codigo[i]) or es_digito(codigo[i])):
                temp += codigo[i]
                i += 1
            
            if not es_identificador(temp):  # Si el identificador no es válido
                token = Terminal("Error", temp, -1)
                tokens_identificados.append(token)
            elif temp in tipos_de_dato:
                token = Terminal("tipo", temp, 4)
                tokens_identificados.append(token)
            elif temp in tokens:
                token = Terminal( tokens[temp][0], temp, tokens[temp][2])
                tokens_identificados.append(token)
            else:
                token = Terminal("identificador", temp, 0)
                tokens_identificados.append(token)
        
        elif es_digito(codigo[i]):  # Inicio de constante numérica
            inicio_numero = i
            while i < longitud and (es_digito(codigo[i]) or codigo[i] == '.'):
                temp += codigo[i]
                i += 1
            
            if not es_entero(temp) and not es_real(temp):  # Si el número no es válido
                token = Terminal("Error", temp, -1)
                tokens_identificados.append(token)
            elif es_entero(temp):
                token = Terminal("entero", temp, 1)
                tokens_identificados.append(token)
            elif es_real(temp):
                token = Terminal("real", temp, 2)
                tokens_identificados.append(token)
        
        else:  # Otros caracteres (operadores, delimitadores) o errores
            temp += codigo[i]
            if i + 1 < longitud:
                temp_doble = temp + codigo[i + 1]
                if temp_doble in tokens:  # Verificar operadores de dos caracteres
                    token = Terminal(tokens[temp_doble][0], temp_doble, tokens[temp_doble][2])
                    tokens_identificados.append(temp)
                    i += 2
                    continue
            if temp in tokens:
                token = Terminal(tokens[temp][0], temp, tokens[temp][2])
                tokens_identificados.append(token)
            else:
                # Error: caracter no reconocido
                token = Terminal("Error", temp, -1)
                tokens_identificados.append(token)
            i += 1

    return tokens_identificados

class Pila:
    def __init__(self):
        self.items = []

    def push(self, item):
        if isinstance(item, ElementoPila):
            self.items.append(item)
        else:
            raise TypeError("Solo los objetos de tipo ElementoPila pueden ser apilados en la pila.")

    def pop(self):
        if self.items:
            return self.items.pop()

    def top(self):
        if self.items:
            return self.items[-1]

    def __repr__(self):
        return str(self.items)

class SyntacticAnalyzer:
    def __init__(self, action_table, goto_table, grammar_rules):
        self.action = action_table
        self.goto = goto_table
        self.grammar = grammar_rules
        self.stack = Pila()
        self.stack.push(Estado(numero=0))  # Asumimos Estado(0) como estado inicial

    def parse(self, tokens):
        cursor = 0

        while True:
            top_state = self.stack.top()
            symbol = tokens[cursor] if cursor < len(tokens) else Terminal('$', '$', 23)
            print(f"Estado actual: {top_state}, Símbolo actual: {symbol}")
            action_entry = (top_state.numero, symbol.simbolo)

            if action_entry in self.action:
                action, value = self.action[action_entry]

                if action == 's':  # Acción de desplazamiento
                    self.stack.push(symbol)
                    self.stack.push(Estado(numero=value))
                    cursor += 1

                elif action == 'r':  # Acción de reducción
                    for _ in range(self.grammar[value][1] * 2):
                        self.stack.pop()
                    non_terminal = NoTerminal(simbolo=self.grammar[value][0])
                    self.stack.push(non_terminal)
                    goto_state = self.stack.items[-2].numero
                    goto_entry = (goto_state, non_terminal.simbolo)
                    self.stack.push(Estado(numero=self.goto[goto_entry]))

                    # Verificar si la pila está efectivamente vacía tras la reducción, lo cual indicaría aceptación
                    if len(self.stack.items) == 1:
                        print("La cadena de entrada es aceptada por la gramática.")
                        return True

            else:
                print("La cadena de entrada no es aceptada por la gramática.")
                return False


def main():
    codigo = """
    int main() {
        int a, b;
        a = 5;
        b = 3;
        if (a == b) {
            a = a + b;
        }
        else {
            a = a - b;
        }
        return a;
    }
    """

    tokens = obtener_tokens(codigo)
    print(tokens)

    syntactic_analyzer = SyntacticAnalyzer(action_table, goto_table, grammar_rules)
    syntactic_analyzer.parse(tokens)

if __name__ == "__main__":
    main()