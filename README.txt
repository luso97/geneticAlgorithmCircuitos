El c�digo fuente se puede ejecutar en un ordenador que contenga los paquetes numpy,DEAP y plotly de Python.
Si se tiene Windows se puede ejecutar el exe que es proporcionado por el instalador "instalador.exe" que instalar� el programa donde solo ejecutando program.exe se
podr� usar el programa.
El c�digo fuente est� estructurado en tres ficheros:
-funciones.py. Tiene todas las funciones del programa anidadas dentro de otra mayor llamada ejecutaPrograma. A parte de anidar todas las funciones ejecutaPrograma
	realiza los pasos de escribir por pantalla los resultados del experimento. Dentro de ejecutaPrograma se analizan los valores de configuraci�n del experimento y 
	dependiendo de ellos se ejecuta una funci�n u otra.

-program.py. Lee el fichero text.txt y lo ejecuta, adem�s llama a la funcion ejecutaPrograma de funciones. 
	Imprime por pantalla los resultados y crea un fichero html llamado basicline que muestra una gr�fica con la media 
	y los m�ximos por generaci�n para el experimento realizado.

-text.txt. Un fichero txt con c�digo Python inicializando todas las variables del problema. Si se cambia y se ejecuta program.exe el problema
	se ejecuta segun los nuevos datos del fichero. Como es c�digo Python es importante no cometer errores de sintaxis al cambiarlo, porqu esino el programa no funcionara.
	En caso de error es recomendable inciar el programa desde la consola y no desde el mismo archivo.
	
	----------------------------IMPORTANTE------------------------------------
		Cuando se guarde el text.txt guardar con codificaci�n ANSI
	----------------------------IMPORTANTE------------------------------------
	
	Si se quiere realizar un experimento con un circuito diferente se puede cambiar el circuito y el vectorEntradas 
	y el programa imprime un vectorSalidas por pantalla para ser copiado en el apartado vectorSalidas del text.txt
	
	El formato de cada variable debe ajustarse al problema. Aqu� un ejemplo de text.txt correspondiente al primer experimento.
#Copiar desde aqu�
m=3
n=3
circuito=[1,0, 0, 0, 1, 3, 0, 0, -1, 2, 3, -1, -1, 0, 1, 2, 1, 1, -1, 0, 4, 1, 1, 0, 0, 1, -1, 2, 1, 2, 5, 1, 2, 2, 0, 4, 1, 2, -1, 2, 1, 1, 0, 2, 1];
#Cada 5 elementos se crea una puerta, siendo el primero el tipo, el segundo la coordenada x de la entrada 0
#el tercero la coordenada y de la entrada 0 y 4 y 5 igual pero para la entrada 1. 
vectorEntradas=[[0,1,0],[1,0,1],[1,0,0]];#entradas y salidas del circuito del circuito 
vectorSalidas=[[1,1,1],[1,1,1],[1,1,1]];
entradasRotas=[[1,2,0],[2,2,0]];
#aqu? usamos tr?os de enteros que representan, primero que puerta tiene una entrada rota, y sregundo cual es
#por ejemplo [5,3,0] ser?a la entrada 1 de la puerta en 5,3 (sin tener en cuenta que en i=0 est?n las entradas)
puertasRotas=[[1,1],[0,2]];
#pares de enteros que representan la posici?n de la puerta que est? rota,sin tener en cuenta que en i=0 est?n las entradas


#?Qu? tipo de algoritmo quieres usar? (0 para eaSimple 1 para eaPlusLambda
algoritmo=0;
#?Que tipo de cruzamiento?(0 un punto, 1 dos puntos y 2 para uniforme)
cruzamiento=1;
#indpb de cruzamiento(Solo afecta en uniforme)
indpbCx=0.2;
#cxpbd entre 0.0 y 1.0
cxpbd=0.2
#?Qu? tipo de mutaci?n?(0 uniforme sin ajustar y 1 uniforme con low y up ajustados)
mutacion=1;
#indpb de mutaci?n
indpbMut=0.2;
#mutpbd entre 0.0 y 1.0
mutpbd=0.0
#lambda (solo para muplusLambda)
lam=15;
#mu (solo para muPlusLambda)
mu=15;
#numero de generaciones
ngen=20;
#poblacion inicial tama?o (en el problema hemos ajustado a 15 siempre)
pobTam=15;
		
		
	Ejemplo para experimento del circuito 4x4
#Copiar desde aqu�
circuito=[1, 0, 2, -1, 1, 1, 0, 1, 0, 0, 5, 0, 1, 0, 2, 3, 0, 3, 0, 2, 1, 0, 2, 0, -1, 5, 1, 0, 1, 0, 5, -1, 2, 1, 2, 1, 0, 1, 1, 1, 4, 1, 2, 2, 3, 2, 2, 0, 2, 0, 3, 2, 0, 2, 1, 4, 1, 3, 1, 3, 1, 2, 0, 2, 2, 2, 3, 3, 3, 2, 4, 3, 0, 3, -1, 2, 2, 1, 3, 1];
vectorEntradas=[[0,1,0,0],[1,0,1,1],[1,0,0,1],[0,1,0,1]];
vectorSalidas=[[1,0,1,0],[1,0,1,0],[0,1,1,0],[1,1,1,0]];
puertasRotas=[[1,1],[0,3],[2,3],[2,0]];
entradasRotas=[[2,0,1],[2,2,1],[0,1,0],[3,0,1],[3,3,0]];
n=4;
m=4;
algoritmo=0;		
cruzamiento=1;		
indpbCx=0.2;
cxpbd=0.2
mutacion=1;
indpbMut=0.2;
mutpbd=0.0
lam=15;
mu=15;
ngen=20;
pobTam=15;
#Copiar hasta aqu�
	Ejemplo para experimento del circuito 5x6 
#Copiar desde aqu�
circuito=[5, 0, 1, 0, 4, 1, 0, 2, 0, 4, 5, 0, 5, 0, 1, 2, -1, 3, 0, 0, 1, 0, 3, 0, 5, 3, -1, 5, -1, 1, 2, 1, 3, 0, 3, 2, 0, 5, 1, 2, 5, 1, 1, 1, 5, 4, 0, 4, 1, 2, 3, 1, 2, 0, 4, 5, -1, -1, 1, 1, 5, 2, 1, 1, 1, 1, 1, 4, 1, 5, 2, 2, 4, 1, 0, 3, 1, 1, -1, 2, 4, 1, 5, 2, 2, 4, 2, 5, 2, 0, 1, 3, 0, 3, 3, 4, 2, 1, 3, 5, 5, 2, 1, 2, 5, 1, -1, 3, 3, 1, 1, -1, 1, 2, 4, 4, 2, 2, 2, 0, 4, 3, 5, -1, 3, 2, 3, 1, 4, 0, 2, 4, 2, 4, 5, 3, 3, 1, 3, 1, 2, 4, 1, -1, 3, 5, 4, 1, 4, 3]
vectorEntradas=[[0,1,0,1,0,0],[1,0,1,0,0,0],[0,0,0,0,1,1],[0,1,0,0,0,1],[0,0,0,0,0,0],[1,1,1,1,1,1]]
vectorSalidas=[[1,1,0,0,0,0],[1,1,1,0,0,0],[1,0,0,0,0,1],[1,1,0,0,0,0],[1,1,0,0,0,0],[1,1,1,0,0,0]]
puertasRotas=[[1,1],[1,3],[2,2]]
entradasRotas=[[2,0,1],[2,3,1],[0,1,0],[3,0,1]];
n=6;
m=5;
algoritmo=0;		
cruzamiento=1;		
indpbCx=0.2;
cxpbd=0.2
mutacion=1;
indpbMut=0.2;
mutpbd=0.0
lam=15;
mu=15;
ngen=20;
pobTam=15;
#Copiar hasta aqu�
	