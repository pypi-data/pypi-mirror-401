from sympy import Rational, Integer, Float, sympify
from .utilitaires import preparer_coef, execute_dans_google_colab, envelopper_latex_dans_balises_align
from typing_extensions import Self
from math import isclose

class Polynome:

    def __init__(self, tab: list[int|float|Rational|Integer|Float], module=None) -> None:
        assert isinstance(tab, list), 'tab doit être du type list !'
        if tab == []:
            tab == [0]
        if module != None:
            assert isinstance(module, int), f"module doit être du type int pas {type(module)} !"
            assert module > 1, "module doit être supérieur ou égal à 2 !"
        self.module = module
        for elt in tab:
            if self.module == None:
                message = f'Chaque élément de tab doit être un nombre pas un {type(elt)} !'
                assert isinstance(elt, (int, float, Rational, Integer, Float)), message
            else:
                message = f'Chaque élément de tab doit être un nombre entier pas un {type(elt)} !'
                assert isinstance(elt, (int, Integer)), message
        self.tab = tab
        if self.module != None:
            self._modulo()
        self._retrait_zeros_a_gauche()
        self.ensemble = self._ensemble()
        self.latex = self._creer_latex()
        self.deg = self._deg()

    def _retrait_zeros_a_gauche(self):
        # sauf le dernier zéros qui permet de représenter le polynôme nul !
        while self.tab[0] == 0 and len(self.tab) > 1:
            self.tab.pop(0)

    def est_nul(self) -> bool:
        return self.tab == [0]
    
    def _deg(self):
        if self.est_nul():
            return float('-inf')
        else:
            return len(self.tab)
        
    def termes(self):
        if self.est_nul():
            return [Polynome([0], module=self.module)]
        else:
            res = []
            for i in range(len(self.tab)):
                if self.tab[i] != 0:
                    tab = [self.tab[i]] + [0] * (len(self.tab) - i - 1)
                    res.append(Polynome(tab, module=self.module))
            return res
    
    def _modulo(self) -> None:
        assert self.module != None, "Le polynome doit être à coefficients d'un ensemble quotient !"
        for i in range(len(self.tab)):
            self.tab[i] = self.tab[i] % self.module

    def _ensemble(self) -> str:
        if self.module == None:
            return 'ℝ[X]'
        elif self.module == 2:
            return '𝔽[X]'
        else:
            return f'ℤ/{self.module}ℤ[X]'       

    def _creer_latex(self) -> str:
        if self.est_nul():
            res = '0_{' + self.ensemble + '}'
        else:
            res = ''
            for i in range(len(self.tab)):
                if self.tab[i] != 0:
                    if i == 0:
                        en_tete = True    
                    else:
                        en_tete = False
                    coeff = preparer_coef(self.tab[i], en_tete=en_tete)
                    puissance = len(self.tab) - i - 1
                    if puissance == 0: # constante
                        if self.tab[i] in (-1, 1):
                            res += coeff + '1'
                        else:
                            res += coeff
                    elif puissance == 1:
                        res += coeff + 'X'
                    elif puissance < 10:
                        res += coeff + 'X^' + str(len(self.tab) - i - 1)
                    else:
                        res += coeff + 'X^{' + str(len(self.tab) - i - 1) + '}'
        return res
    
    def _repr_latex_(self) -> str:
        if not execute_dans_google_colab():
            return envelopper_latex_dans_balises_align(self.latex)
        else:
            return self.latex
    
    def __str__(self) -> str:
        return self.latex
    
    def __repr__(self) -> str:
        return self.latex
    
    def __eq__(self, autre: Self) -> bool:
        if self.deg != autre.deg:
            return False
        else:
            for i in range(len(self.tab)):
                if self.tab[i] != autre.tab[i]:
                    return False
            return True
    
    def __neg__(self) -> str:
        return Polynome([-coeff for coeff in self.tab], self.module)
    
    def __add__(self, autre: Self) -> Self:
        assert isinstance(autre, Polynome), f"On ne peux pas additionner un Polynome avec un {type(autre)} mais seulement avec un autre polynome !"
        assert self.module == autre.module, "Les polynômes à sommer doivent appartenir au même ensemble !"
        if len(self.tab) > len(autre.tab):
            tab1 = self.tab
            tab2 = autre.tab
        else:
            tab1 = autre.tab
            tab2 = self.tab
        tab = [0] * len(tab1)
        i1 = len(tab1) - 1
        i2 = len(tab2) - 1
        while i2 >= 0:
            tab[i1] = tab1[i1] + tab2[i2]
            i1 -= 1
            i2 -= 1
        while i1 >= 0:
            tab[i1] = tab1[i1]
            i1 -= 1
        return Polynome(tab, self.module)
    
    def __sub__(self, autre: Self) -> Self:
        assert isinstance(autre, Polynome), f"On ne peux pas soustraire à un Polynome un {type(autre)} mais seulement un autre Polynome !"
        return self + (-autre)
    
    def __mul__(self, autre: Self) -> Self:
        assert isinstance(autre, Polynome), f"On ne peux pas multiplier un Polynome avec un {type(autre)} mais seulement avec un autre polynome !"
        assert self.module == autre.module, "Les polynômes à sommer doivent appartenir au même ensemble !"
        res = Polynome([0], module=self.module)
        for iself in range(len(self.tab)):
            prod = [0] * (len(self.tab) + len(autre.tab))
            for iautre in range(len(autre.tab)):
                puissance_self = len(self.tab) - iself - 1
                puissance_autre = len(autre.tab) - iautre - 1
                iprod = len(prod) - puissance_self - puissance_autre - 1
                prod[iprod] = self.tab[iself] * autre.tab[iautre]
            res += Polynome(prod, module=self.module)
        return res
    
    def __pow__(self, puissance: int) -> Self:
        assert isinstance(puissance, (int, Integer)), f"puissance doit être un entier et pas un {type(puissance)}!"
        assert puissance >= 0, "Puissance doit être un entier positif ou nul !"
        if puissance == 0:
            return Polynome([0], module=self.module)
        elif puissance == 1:
            return self
        else:
            res = self
            for _ in range(puissance - 1):
                res *= self
            return res
        
    def puissance_min(self) -> int:
        if self.est_nul():
            return 0
        else:
            i = len(self.tab) - 1
            while isclose(self.tab[i], 0) and i >= 0:
                i -= 1
            puissance = len(self.tab) - i - 1
        return puissance
        
    def __len__(self) -> int:
        if self.est_nul():
            return 1
        else:
            return len(self.tab) - self.puissance_min()
        

class DivEucPolynomes:

    def __init__(self, dividende: Polynome, diviseur: Polynome, module: int = None) -> None:
        assert isinstance(dividende, (Polynome, list)), f"dividende doit être du type list ou Polynome pas du type {type(dividende)} !"
        assert isinstance(diviseur, (Polynome, list)), f"diviseur doit être du type list ou Polynome pas du type {type(diviseur)} !"
        if module != None:
            assert isinstance(module, int), f"module doit être du type int pas {type(module)} !"
        if isinstance(dividende, list):
            dividende = Polynome(dividende, module=module)
        if isinstance(diviseur, list):
            diviseur = Polynome(diviseur, module=module)
        assert dividende.module == diviseur.module, "dividende et diviseur doivent appartenir au même ensemble !"
        assert not diviseur.est_nul(), "diviseur ne doit pas être le polynôme nul !"
        self.module = module
        self.dividende = dividende
        self.diviseur = diviseur
        self.restes = []
        self.produits = []
        self.quotient, self.reste = self._div_euclidienne()
        self.latex = self._latex()

    def _div_euclidienne(self) -> tuple[Polynome]:
        polynome_nul = Polynome([0], module=self.module)
        quotient = polynome_nul
        reste = self.dividende
        while reste.deg >= self.diviseur.deg:
            deg_terme_quotient = reste.deg - self.diviseur.deg
            if isclose(reste.tab[0], self.diviseur.tab[0]):
                coeff_terme_quotient = 1
            elif isinstance(reste.tab[0], int) and isinstance(self.diviseur.tab[0], int):
                coeff_terme_quotient = Rational(reste.tab[0], self.diviseur.tab[0])
            else:
                coeff_terme_quotient = reste.tab[0]/self.diviseur.tab[0]
            terme_quotient = Polynome([coeff_terme_quotient] + [0] * deg_terme_quotient, module=self.module)
            produit = self.diviseur * terme_quotient
            self.produits.append(produit)
            reste = reste - produit
            self.restes.append(reste)
            quotient += terme_quotient
        return (quotient, reste)
    
    def _pol_vers_ligne_tab_latex(self, pol: Polynome, puiss_min: int, puiss_max: int) -> str:
        assert isinstance(puiss_min, int), f"puiss_min doit être du type int et non du type {type(puiss_min)} !"
        assert puiss_min >= 0, "puiss_min doit être positif ou nul !"
        assert isinstance(puiss_max, int), f"puiss_max doit être du type int et non du type {type(puiss_min)} !"
        assert puiss_max >= 0, "puiss_max doit être positif ou nul !"
        assert puiss_max >= puiss_min, "puiss_max doit être supérieur ou égal à puiss_min !"
        assert puiss_min <= pol.puissance_min(), "puiss_min trop élevée : impossible de représenter tous les termes du polynôme !"
        assert puiss_max >= len(pol.tab) - 1, "puiss_max trop faible : impossible de représenter tous les termes du polynôme !"
        nbtermes = puiss_max - puiss_min + 1
        if pol.est_nul():
            return (nbtermes - 1) * ' &  & ' + ' & 0'
        else:
            res = ''
            ipol = len(pol.tab) - puiss_min - 1
            while ipol >= 0:
                if isclose(pol.tab[ipol], 0):
                    if ipol == len(pol.tab) - puiss_min - 1:
                        res = ' & ' + res
                    else:
                        res = ' &  & ' + res
                else:
                    if ipol == 0:
                        if pol.tab[ipol] < 0:
                            signe = '-'
                        else:
                            signe = ''
                    else:
                        if pol.tab[ipol] < 0:
                            signe = '-'
                        else:
                            signe = '+'
                    puissance = len(pol.tab) - ipol - 1
                    if puissance == 0: # constante
                        abs_terme = str(abs(pol.tab[ipol]))
                    else:
                        if isclose(abs(pol.tab[ipol]), 1):
                            abs_coeff = ''
                        else:
                            abs_coeff = str(abs(pol.tab[ipol]))
                        if puissance == 1:
                            abs_terme = abs_coeff + 'X'
                        elif puissance < 10:
                            abs_terme = abs_coeff + 'X^' + str(puissance)
                        else:
                            abs_terme = abs_coeff + 'X^{' + str(puissance) + '}'
                    if ipol == len(pol.tab) - puiss_min - 1:
                        res = signe  + ' & ' + abs_terme + res
                    else:
                        res = signe  + ' & ' + abs_terme + ' & ' + res
                ipol -= 1
            res = (nbtermes - (len(pol.tab) - puiss_min)) * ' &  & ' + res
        return res            
    
    def _latex(self) -> str:
        puiss_max = len(self.dividende.tab) - 1
        puiss_min = self.dividende.puissance_min()
        for reste in self.restes:
            if len(reste.tab) - 1 > puiss_max:
                puiss_max = len(reste.tab) - 1
            if reste.puissance_min() < puiss_min:
                puiss_min = reste.puissance_min()
        nbre_termes_a_gauche = puiss_max - puiss_min + 1
        res = '\\text{Division euclidienne dans } ' + self.dividende.ensemble + ' \\\\\n'
        res += '\\\\\n'
        res += '\\text{\\phantom{0}}\\\\\n'
        if self.dividende.deg >= self.diviseur.deg:
            res += '\\begin{array}{cc' + 'cr' * (nbre_termes_a_gauche) + 'c|}\n'
            res += '     &  & ' + self._pol_vers_ligne_tab_latex(self.dividende, puiss_min, puiss_max) + ' &  \\\\\n'
            for i in range(len(self.restes)):
                prod = self.produits[i]
                reste = self.restes[i]
                res += '    - & ( & ' + self._pol_vers_ligne_tab_latex(prod, puiss_min, puiss_max) + ' & ) \\\\' + '\n'
                res += '    \\hline\n'
                res += '     &  & ' + self._pol_vers_ligne_tab_latex(reste, puiss_min, puiss_max) + ' &  \\\\' + '\n'
            res += '\\end{array}\n'
            res += '\\begin{array}{l}\n'
            res += '    ' + self.diviseur.latex + ' \\\\\n'
            res += '    \hline\n'
            if self.dividende.deg < self.diviseur.deg:
                res += '    0\\\\\n'
            else:
                if len(self.restes) == 1:
                    ajout = 0
                else:
                    ajout = 1
                for i in range(len(self.reste) + ajout):
                    if i == 0:
                        res += '    ' + self.quotient.latex + ' \\\\\n'
                    else:
                        res += '     \\\\\n'
                    res += '     \\\\\n'
            res += '\\end{array}\n'
            res += '\\\\\n'
            res += '\\text{\\phantom{0}}\\\\\n'
        res += self.dividende.latex + ' = B(X)Q(X) + R(X)'
        if self.reste.est_nul():
            reste = ''
        else:
            reste = ' + (' + self.reste.latex + ')'
        res += ' = (' + self.diviseur.latex + ')(' + self.quotient.latex + ')' + reste + '\n' 
        return res

    def _repr_latex_(self) -> str:
        if not execute_dans_google_colab():
            return envelopper_latex_dans_balises_align(self.latex)
        else:
            return self.latex
    
    def __str__(self) -> str:
        return self.latex
    
    def __repr__(self) -> str:
        return self.latex

    