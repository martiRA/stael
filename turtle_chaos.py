#-*-coding: utf8 -*-
# GPL
# Gregor Lingl 2009-06-24
# nettoyé avril 2014 martiRA chez github.com

'''Les bifurcations qu'on connait, mais
pour r proche de 4, attention au chaos.

Trois façons apparemment équivalentes pour
calculer la suite récursive x -> r x (1-x) 
donnent des résultats différents après un
certain nombre d'itérations, comme quoi les
résultats dépendent d'arrondis ridiculement
petits.
'''

from turtle import *
from decimal import Decimal, getcontext
import random

r = Decimal('3.93')
N = 200  # ou aute, au moins 160 pour voir quelque chose
getcontext().prec = 30  # ou 50

def f(x):
  x = Decimal(str(x))
  return r*x*(1-x)

def g(x):
  x = Decimal(str(x))
  return r*(x-x**2)

def h(x):
  x = Decimal(str(x))
  return r*x-r*x*x

def saute(x, y):
  penup()
  goto(x, y)

def ligne(x1, y1, x2, y2):
  saute(x1, y1)
#  pendown() # pour relier les points d'une évolution
  goto(x2, y2)

def axes():
  ligne(-1, 0, N+1, 0)
  ligne(0, -0.1, 0, 1.1)

def dessine(fonction, départ, couleur):
  pencolor(couleur)
  x = départ
  saute(0, x)
  pendown()
  dot(5)
  penup()
  for i in range(N):
      x = fonction(x)
      goto(i+1, float(x))
      dot(5)

def chaotine():
  reset()
  setworldcoordinates(-1, -0.1, N+1, 1.1)
  speed(0)
  hideturtle()
  axes()
#  début = float(Decimal(str(random.random())))
  début = random.random()
  
  print(début)
  dessine(f, début, (1, 0, 0))
  dessine(g, début, (0, 1, 0))
  dessine(h, début, (0, 0, 1))
  # Agrandissons la fin :
  for s in range(0, 3*N//4, 11):
      setworldcoordinates(s, -0.1, N+1, 1.1)
  return "Voilà !"

if __name__ == "__main__":
  chaotine()
  mainloop()
