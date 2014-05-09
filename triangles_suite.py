#-*-coding: utf8 -*-
from turtle import *
import math
import sys

DÉBOGUE = False #True
TOLÉRANCE = 1e-18

class Point() :
    def __init__(self, x=0, y=0) :
        self.x = x
        self.y = y
    def __repr__ (self) :
        return "({:.3g}, {:.3g})".format(self.x, self.y)
    def norm(self) :
        return math.sqrt( self.x**2 + self.y**2 )
    def angle(self) :
        return math.atan2(self.y, self.x)

def dist(A, B) :
    return math.sqrt( (A.x-B.x)**2 + (A.y-B.y)**2 )

def angle(A, B, C) :
    return math.acos( (-dist(A, C)**2 + dist(B, A)**2 + dist(C, B)**2)/
                      (2* dist(B, A)*dist(C, B)) )
def pente(A, B) :
    return (B.y-A.y) / (B.x-A.x)

def penteInv(A, B) :
    return -1/pente(A, B)

class Triangle() :
    def __init__(self, A, B, C) :  #corriger cela pour qu'il puisse prendre trois 2-tuples de nombres
        self.A = A
        self.B = B
        self.C = C
        self.a = dist(self.B, self.C)
        self.b = dist(self.C, self.A)
        self.c = dist(self.A, self.B)

        self._a_ = angle(C, A, B)
        self._b_ = angle(A, B, C)
        self._c_ = angle(B, C, A)

        if DÉBOGUE :
            self.vérif()

    def __repr__(self) :
        return "[{!r}, {!r}, {!r}]".format(self.A, self.B, self.C)

    def angles(self) :
        return (self._a_, self._b_, self._c_)
    def côtés(self) :
        return (self.a, self.b, self.c)
    def plusGrandCôté(self) :
        return max(x for x in self.côtés())

    def aire(self) :
        s = (self.a + self.b + self.c)/2
        return math.sqrt( s*(s-self.a)*(s-self.b)*(s-self.c) )

    def vérif(self):
        somme = 0
        for x in self.angles():
            somme += x
        return ("{!r} :\n    0, 1 =? {}, {}\n"
                .format(self, somme - math.pi, somme / math.pi))

    def minmaxAngles(self) :
        plusPetit = min(x for x in self.angles())
        plusGrand = max(x for x in self.angles())
        return (plusPetit, plusGrand)
    def triangledessin (self) :      #dessiner le triangle avec turtle
        up()
        color("blue")
        goto(self.A.x*100,self.A.y*100)
        down()
        goto(self.B.x*100,self.B.y*100)
        goto(self.C.x*100,self.C.y*100)
        goto(self.A.x*100,self.A.y*100) 

def sym(t):
    Aprime = Point()
    Bprime = Point()
    Cprime = Point()

    Asym = Point()
    Bsym = Point()
    Csym = Point()

    # Bprime est la projection orthogonale de B sur la droite AC
    Bprime.x = ( pente(t.A, t.C) * t.A.x - penteInv(t.A, t.C) * t.B.x
                 + t.B.y - t.A.y ) /\
               ( pente(t.A, t.C) - penteInv(t.A, t.C) )
    Bprime.y = penteInv (t.A, t. C) *( Bprime.x -t.B.x ) + t.B.y
    # Bsym est le symétrique de B par rapport à la droite AC
    Bsym.x = t.B.x + 2*( Bprime.x - t.B.x )
    Bsym.y = t.B.y + 2*( Bprime.y - t.B.y )

    if DÉBOGUE :
        print( Bprime.y,"=?", pente(t.A, t.C) * (Bprime.x-t.A.x) + t.A.y)

    Cprime.x = ( pente(t.B, t.A) * t.B.x - penteInv(t.B, t.A) * t.C.x
                 + t.C.y - t.B.y ) /\
               ( pente(t.B, t.A) - penteInv(t.B, t.A) )
    Cprime.y = penteInv (t.B, t. A) *( Cprime.x -t.C.x ) + t.C.y
    Csym.x = t.C.x + 2*( Cprime.x - t.C.x )
    Csym.y = t.C.y + 2*( Cprime.y - t.C.y )

    Aprime.x = ( pente(t.C, t.B) * t.C.x - penteInv(t.C, t.B) * t.A.x
                 + t.A.y - t.C.y ) /\
               ( pente(t.C, t.B) - penteInv(t.A, t.C) )
    Aprime.y = penteInv (t.C, t. B) *( Aprime.x -t.A.x ) + t.A.y
    Asym.x = t.A.x + 2*( Aprime.x - t.A.x )
    Asym.y = t.A.y + 2*( Aprime.y - t.A.y )

    tsym = Triangle(Asym, Bsym, Csym)

    if DÉBOGUE :
        print(" {!r} ---> {!r}". format(t, tsym))
    return tsym

def récurrenceSimple(t) :
    while True :
        try:
            tprime = sym(t)
        except OverflowError:  ## améliorer pour sortir de la boucle sans tuer
            sys.exit()
        récurrenceSimple( tprime )

def normalize(t) :
    maximum = t.plusGrandCôté()
    if DÉBOGUE:
        print(t, "\nLongueur du plus grand côté =", maximum)
    Anorm = Point( t.A.x/maximum , t.A.y/maximum )
    Bnorm = Point( t.B.x/maximum , t.B.y/maximum )
    Cnorm = Point( t.C.x/maximum , t.C.y/maximum )
    tnorm = Triangle( Anorm , Bnorm, Cnorm )
    if DÉBOGUE:
        print(tnorm, "\nLongueur du plus grand côté =", tnorm.plusGrandCôté())
    return tnorm

def récurrenceNormalisée(t) :
    while True :
        tprime = sym(t)
        tpprime = normalize( tprime )
        if DÉBOGUE :
            anglest   = sorted(t.minmaxAngles())
            anglestpp = sorted(tpprime.minmaxAngles())
        if not DÉBOGUE :
            anglest   = sorted(t.angles())
            anglestpp = sorted(tpprime.angles())
        print(anglestpp)
        if abs(anglestpp[0] - anglest[0]) < TOLÉRANCE and \
           abs(anglestpp[1] - anglest[1]) < TOLÉRANCE and \
           abs(anglestpp[2] - anglest[2]) < TOLÉRANCE :
            print( "\n¡ Convergence !\n sur angles :", tpprime.angles(),
                   "\nTriangle final    :", tpprime,
                   "\nTriangle précédent:", t,
                   "\navec angles :", t.angles())
            print("\nTolérance =",TOLÉRANCE)
            sys.exit()       # à faire plus joli
        récurrenceNormalisée( tpprime )

if __name__ == "__main__" :

    P = Point(1/3, math.pi)
#    print(P)
#    print("Norme =", P.norm(), "; Angle =", P.angle())

    Q = Point(2/7, -4/7)
    R = Point(11/9, 23/9)

    t = Triangle (P, Q, R)
#    print ("\nTriangle t = ", t)
#    print(t.a, t.b, t.c)
#    print(t.vérif())
#    print("Côtés t = ", t.côtés())
#    print(t._a_, t._b_, t._c_)
#    print("Angles t = ", t.angles())
#    print("Aire t = ", t.aire())

    p = Point(0, 1)
    q = Point(1, 2)
    r = Point(3, 0)

    T = Triangle (p, q, r)
#    print ("\nTriangle T = ", T)
#    print(t.vérif())
#    print("Côtés T = ", T.côtés())
#    print("Angles T = ", T.angles())
#    print("Aire T = ", T.aire())

#    print("\nEnfant de t =", sym(t))
#    print("Enfant de T =", sym(T), "\n")

#    normalize(t)
#    normalize(T)

#    récurrenceSimple(T)

    print("\nTriangle de départ :", T,
          "\n       avec angles :", t.angles())
    récurrenceNormalisée(T)
    récurrenceNormalisée(t) # n'y arrive jamais à cause du sys.exit()


'''Problèmes:

Vérifer á la main avec deux ou trois exemples simples
 que les résultats de sym(Triangle) sont justes.

Écrire des programmes séparés qui appellent triangles_suite
 et étudient les cas des triangles
- équilatéraux ;
- isocèles ;
- rectangles.


Adresser les pentes zéro et infinie,
 à l'aide des valeurs de float "inf" ou "infinity".
The math module has been updated with six new functions
inspired by the C99 standard.

The isfinite() function provides a reliable and
 fast way to detect special values.
 It returns True for regular numbers and False for Nan or Infinity:

>>> [isfinite(x) for x in (123, 4.56, float('Nan'), float('Inf'))]
[True, True, False, False]


Permettre que l'utilisateur interactif change
 les valeurs de TOLÉRANCE et de DÉBOGUE,
 sans pour autant enlever les valeurs par défaut
 et sans qu'il soit requis de les spécifier.

Employer l'aire pour normaliser ?
 Probablement pas bon, mais à tester.

Afficher suite des angles minmax pour après la
 graphiquer ?

Améliorer la sortie des boucles sans appel à sys.exit() ?

Changer la notation A, B, C... en
 sommets = [A, B, C] et faire des boucles
 sur x in sommets, cycliquement ?

Commenter chacune des fonctions et classes
 avec un """...""" juste après la
 déclaration initiale pour avoir de l'aide sous la souris ?

Rajouter des commentaires succincts sur les intentions ?

Adresser les demandes d'amélioration
 qui sont en commentaire # ?

Augmenter la précision pour atteindre
 TOLÉRANCE beaucoup plus petite... module décimal ?

Écrire un programme interactif qui guide l'élève ?

Employer le module doctest beaucoup de fois pour
 intégrer des tests (en lieu de "DÉBOGUE = True" ?


ENSUITE :

Parcourir tous les triangles possibles de départ
pour voir lesquels convergent, et où.

Intéger ce programme dans turtle ou tkinter.ttk
 pour voir de jolis dessins.


PROJET github :
 tout le monde login
 prénomN   avec N la ou des initiales du nom
Auparavant :
 tout le monde gmail avec prénom.nom ...

Puis à la maison, commit, clone, ...

'''

