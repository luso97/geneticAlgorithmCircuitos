#!/usr/bin/env python
# -*- coding: utf-8 -*-


from source.funciones import Circuito, Puerta, representaCircuitos3,ejecutaPrograma
file=open("text.txt",'r');
exec(file.read());
#Escribe aqui los datos de tu circuito



ejecutaPrograma(circuito,m,n,vectorEntradas,vectorSalidas,entradasRotas,puertasRotas,algoritmo,cruzamiento,indpbCx,mutacion,indpbMut,cxpbd,mutpbd,lam,mu,ngen,pobTam);
input("Escribe algo para salir del programa");





