import numpy;
import random;
import time;
import plotly as py
import plotly.graph_objs as go
import sys;

from deap import base, creator, tools, algorithms;


def bit_not(m, numbits=1):
    return (1 << numbits) - 1 - m
     #función para hacer una negación de bit, la de python es sobre 16 bits asi que no sale lo que nosotros queremos       
#Clase Puerta
class Puerta:
    def __init__(self,tipo,entrada00,entrada01,entrada10,entrada11,salida):
        #entrada0 y 1 se inician como dos pares de int que señalan a posiciones de la matriz del circuito
        self.entrada0=[entrada00,entrada01];
        self.entrada1=[entrada10,entrada11];
        self.tipo=tipo;
        #el valor salida solo sirve realmente para las puertas que en realidad son entradas
        #para las demás el valor se sobreescribe en la función salida()
        self.salida=salida;
    def setSalida(self,a):
        self.salida=a;
    def setTipo(self,tipo):
        self.tipo=tipo;
    def romperEntrada(self,i):
        if i==0:
            self.entrada0=[-1,-1];
        if i==1:
            self.entrada1=[-1,-1];
        
    def getSalida(self):
        #print(self,self.entrada1,self.entrada2);
        
        l=self.salida;
        #por defecto las entradas son 0, ya sea porque están sin usar o porque la entrada es una puerta defectuosa
        x=0;
        y=0;
        
        if self.entrada0 != -1:
            if isinstance(self.entrada0,int):
                #esto en este código creo que no sirve para nada
                x=self.entrada0;
            else:
                #la entrada es la salida de la puerta a la que hace referencia
                x=self.entrada0.getSalida();    
        if self.entrada1 != -1:
              
            if isinstance(self.entrada1,int):
                y=self.entrada1; 
            else:
                y=self.entrada1.getSalida();
         
        if self.tipo==0:
            #si la puerta esta defectuosa la salida es 0 siempre
            l=0;
        #si la puerta es una entrada la salida es el mismo valor que se introduce en init, véase defArray
        if self.tipo==-1:
            l=self.salida;
        #aquí calculamos los valores para cada tipo de puerta lógica
        if self.tipo==1:
            l=x|y;
        if self.tipo==2:
            l=x&y;
        if self.tipo==3:
            l=bit_not(x);
        if self.tipo==4:
            l=bit_not(x&y); 
        if self.tipo==5:
            l=(x&(bit_not(y)))|(bit_not(x) &y);
        self.salida=l;
        return self.salida;
    def setCircuito(self,circuito,i,j):
        #aquí se cambia el valor de entrada0 y 1 por las puertas a las que deberían hacer referencia.
        #para eso se mete un cirucito como par�metro y se cambia el valor de entrada por la puerta que 
        #se encuentra en el punto de la matriz entrada[0],entrada[1]
        
        if self.entrada0[0]!=-1 and self.entrada0[1]!=-1:
            self.entrada0=circuito.array[self.entrada0[0]][self.entrada0[1]];
        else:
            #si uno de los valores de entrada es None significa que no está conectada a nada
            self.entrada0=-1;
        if self.entrada1[0]!=-1 and self.entrada1[1]!=-1:
            self.entrada1=circuito.array[self.entrada1[0]][self.entrada1[1]];
        else:
            self.entrada1=-1;
    
    
        


# init inicia todos los parametros de la puerta. Salida se inicia pero solo sirve cuando la puerta es una entrada del circuito, 
#porque en otros casos los cálculos de salida sobreescribiran a ese valor.
# setCircuito cmabia el valor de entrada0 y entrada1 por puertas del circuito donde se encuentra la puerta.

# m son el m�mero de capas y n el m�mero de puertas por capa

# In[86]:

#Clase Circuito
class Circuito:
    def __init__(self,m,n,vector):
        #aquí creamos un array que tenga m+1 capas(las m capas de puertas y una más  para las entradas)
        #n puertas posibles por capa
        self.array=[[0]*(n) for _ in range(m+1)];
        self.array[0]=vector;#la primera capa son el vector 
        self.n=n;
        self.m=m;
    def defArray(self,array):
        x=1;
        
        self.array[1:]=array;
        
        
        for i in range(self.m+1):
            for j in range(self.n):
                
                if isinstance(self.array[i][j],Puerta):
                
                    #aquí se hace que la puerta que está en i,j en vez de tener como referencia de entradas dos [int,int]
                    #tenga una puerta
                    self.array[i][j].setCircuito(self,i,j);
                if isinstance(self.array[i][j],int):
                    
                    #si la entrada es un int significa que es una entrada del circuito por lo que creamos
                    #una puerta de tipo -1 y nos aseguramos que su salida sea la entrada que se le de
                    self.array[i][j]=Puerta(-1,-1,-1,-1,-1,self.array[i][j]);
                    #aquí hay un error 24/6/18 13:00
                    self.array[i][j].setCircuito(self,i,j);   
                
    def getArray(self):
        return self.array;
    def setEntrada(self,vector):
        for i in range(self.n):
            self.array[0][i].setSalida(vector[i]);
    def getSalida(self):
        vector=[];
        for i in range (self.n):
            
            
            vector.append(self.array[self.m][i].getSalida());
           
        return vector;


def representaCircuitos3(individuo,entrada,m,n):
    print("n->",end='');
    for p in range(n):
        print("|         ",p,"         ",end='');
    print("|");      
    print("m| ",end='');              
    #for p in range(n):
       # print(" --",end=' ');
    print("");
    print("0 ",end=' ');
    for k in range(n):
        print("|         ",entrada[k],"        |",end='');
    print("|",end='');
    for i in range(0,n*m*5,5):
        if i%(5*n)==0:
            print("");
            print("     ", end='');
            for d in range(n):            
                print("-------------------  ", end=' ');
            print("");
            print(int(i/(5*n))+1," ||",end='');
        
        if individuo[i]==-1:
            print(" na ",end=' ');
        if individuo[i]==1:
            print(" OR ",end=' ');
        if individuo[i]==2:
            print("AND ",end=' ');
        if individuo[i]==3:
            print("NOT ",end=' ');
        if individuo[i]==4:
            print("NAND",end=' ');
        if individuo[i]==5:
            print("XOR ",end=' ');
        print("(",individuo[i+1] if individuo[i+1]!=-1 else "X"
              ,",",individuo[i+2] if individuo[i+2]!=-1 else "X",")"
              ," , ", "(",individuo[i+3] if individuo[i+3]!=-1 else "X"
              ,",",individuo[i+4] if individuo[i+4]!=-1 else "X" ,")",sep='',end=' || ');
    print("")
    print("     ", end='');
    for l in range(n):
            print("-------------------  ", end=' ');
    print("");
#funciónPrincipal que ejecuta el programa entero
def ejecutaPrograma(circuito,m,n,vectorEntradas,vectorSalidas,entradasRotas,puertasRotas,algoritmo,cruzamiento,indpbCx,mutacion,indpbMut,cxpbd,mutpbd,lam,mu,ngen,pobTam):
    #La ejecución del programa está al final de la función

    def validateVariables():
        if algoritmo!=0 and algoritmo!=1:
            print("algoritmo debe valer 0 ó 1");
            return 1;
        if cruzamiento not in range(0,3):
            print("cruzamiento debe valer 0,1 ó 2");
            return 1;
        if indpbCx>1.0 or indpbCx<0.0:
            print("indpbCx es un entero de 0 a 1");
            return 1;
        if mutacion not in range(0,2):
            print("mutacion debe valer 0 ó 1");
            return 1;
        if indpbMut>1.0 or indpbMut<0.0:
            print("indpbMut es un entero de 0 a 1");
            return 1;
        if cxpbd>1.0 or cxpbd<0.0:
            print("cxpbd es un entero de 0 a 1");
            return 1;
        if mutpbd>1.0 or mutpbd<0.0:
            print("mutpbd es un entero de 0 a 1");
            return 1;
        if mutpbd+cxpbd>1:
            print("La suma de cxpbd y mupbd debe ser menor o igual a 1.0");
        if lam<1:
            print("lam debe ser 1 o mayor");
            return 1;
        if mu<1:
            print("mu debe ser 1 o mayor");
            return 1;
        if ngen<1:
            print("ngen debe ser 1 o mayor");
            return 1;
        if pobTam<1:
            print("pobTam debe ser 1 o mayor");
            return 1;
    def circuitoCorrecto():
        vector=[1,1,0,1];
        individuo=circuito;
        
        P3=fenotipo2(individuo);
        
        if P3!=(float(len(vectorEntradas)*n),):
            return 0;
        else:
            return 1;
    
    
    def fenotipo(individuo):
        
        
        vector=[1,1,0,1,1,1];
        cir=Circuito(m,n,vector);
        cir.array;
        error=0;
        array=[[0]*(n) for _ in range(m)];
        
        for i in range(0,n*m*5,5):
            l=max(int((i/5)/n)-1,0);
            t=range(l,int((i/5)/n)+1);
            t2=range(-1,n);
            t3=range(-1,6);
            if individuo[i] not in t3:
                error=1;
                
            if individuo[i+1] not in t and individuo[i+1]!=-1:
                error=1;
        
            if  individuo[i+2] not in t2:
                error=1;
        
            if individuo[i+3] not in t and individuo[i+3 ]!=-1:
                error=1;
        
            if individuo[i+4] not in t2:
                error=1;
            if [individuo[i+1],individuo[i+2]]==[int((i/5)/n)+1,int((i/5)%n)]:
                error=1;
            
            if [individuo[i+3],individuo[i+4]]==[int((i/5)/n)+1,int((i/5)%n)]:
                error=1;
                #miramos si hay entradas vacías
            
                
            #aquí hacemos una puerta por cada entrada del array y calculamos con n y m en que posición del array estarían
            puertax=Puerta(individuo[i],individuo[i+1],individuo[i+2],individuo[i+3],individuo[i+4],0)
            #print(puertax);
            #print((i/5)/n,(i/5)%n);
            array[int((i/5)/n)][int((i/5)%n)]=Puerta(individuo[i],individuo[i+1],individuo[i+2],individuo[i+3],individuo[i+4],0);
        #miramos puertas y entradas rotas    
        for k in range (len(entradasRotas)):
            res=entradasRotas[k];
            if res[0]<m and res[1]<n:
                array[res[0]][res[1]].romperEntrada(res[2]);
                #miramos si el valor está dentro del array y rompemos la entrada que nos digan
        for l in range (len(puertasRotas)):
            res=puertasRotas[l];
            if res[0]<m and res[1]<n:
                array[res[0]][res[1]].setTipo(0);
            
                    #al cambiar el tipo a 0 la puerta pasa a devolver 0 siempre ya que está rota
        
        P3=0;
        if error==0:
            savedArray=array.copy();
            cir.defArray(array);
    
            #print(cir.array);
            #print("---------------------")
            #a=cir.getSalida();
            #print(a);
            #print(a)
            b=[1,1,1,1];
            P3=0;
            for x in range(len(vectorEntradas)):
                cir.setEntrada(vectorEntradas[x]);
    
                a=cir.getSalida()
                for i in range(n):
                #mira cada uno de los pares entrada salida y compara la salida del circuito con esa entrada con la salida ideal
                    if a[i]==vectorSalidas[x][i]:
                        P3=P3+1;
        else:
            P3=0;
        return (float(P3),);
    def fenotipo2(individuo):
        
        
        vector=[1,1,0,1,1,1];
        cir=Circuito(m,n,vector);
        cir.array;
        error=0;
        array=[[0]*(n) for _ in range(m)];
        
        for i in range(0,n*m*5,5):
            l=max(int((i/5)/n)-1,0);
            t=range(l,int((i/5)/n)+1);
            t2=range(-1,n);
            t3=range(-1,6);
            if individuo[i] not in t3:
                error=1;
                
            if individuo[i+1] not in t and individuo[i+1]!=-1:
                error=1;
        
            if  individuo[i+2] not in t2:
                error=1;
        
            if individuo[i+3] not in t and individuo[i+3 ]!=-1:
                error=1;
        
            if individuo[i+4] not in t2:
                error=1;
            if [individuo[i+1],individuo[i+2]]==[int((i/5)/n)+1,int((i/5)%n)]:
                error=1;
            
            if [individuo[i+3],individuo[i+4]]==[int((i/5)/n)+1,int((i/5)%n)]:
                error=1;
                #miramos si hay entradas vacías
            
                
            #aquí hacemos una puerta por cada entrada del array y calculamos con n y m en que posición del array estarían
            puertax=Puerta(individuo[i],individuo[i+1],individuo[i+2],individuo[i+3],individuo[i+4],0)
            #print(puertax);
            #print((i/5)/n,(i/5)%n);
            array[int((i/5)/n)][int((i/5)%n)]=Puerta(individuo[i],individuo[i+1],individuo[i+2],individuo[i+3],individuo[i+4],0);
        #miramos puertas y entradas rotas    
        for k in range (len(entradasRotas)):
            res=entradasRotas[k];
            if res[0]<m and res[1]<n:
                array[res[0]][res[1]].romperEntrada(res[2]);
                #miramos si el valor está dentro del array y rompemos la entrada que nos digan
        for l in range (len(puertasRotas)):
            res=puertasRotas[l];
            if res[0]<m and res[1]<n:
                array[res[0]][res[1]].setTipo(0);
            
                    #al cambiar el tipo a 0 la puerta pasa a devolver 0 siempre ya que está rota
        
        P3=0;
        if error==0:
            savedArray=array.copy();
            cir.defArray(array);
    
            #print(cir.array);
            #print("---------------------")
            #a=cir.getSalida();
            #print(a);
            #print(a)
            b=[1,1,1,1];
            P3=0;
            resolr=[];
            for x in range(len(vectorEntradas)):
                cir.setEntrada(vectorEntradas[x]);
    
                a=cir.getSalida()
                print("entrada=",vectorEntradas[x],"salida=",a,"salida esperada",vectorSalidas[x]);
                resolr.append(a);
                
                for i in range(n):
                #mira cada uno de los pares entrada salida y compara la salida del circuito con esa entrada con la salida ideal
                    if a[i]==vectorSalidas[x][i]:
                        P3=P3+1;
            print("Vector salidas para uso experimental",resolr);          
        else:
            P3=0;
            print("Hay un error en la configuración del circuito")
        return (float(P3),);
    def compErroresCircuito():
        error=0;
        if len(circuito)!=m*n*5:
            print("El array circuito debe de tener una logitud de m*n*5");
            error=1;
            return 1;
        individuo=circuito;
        for i in range(0,n*m*5,5):
            l=max(int((i/5)/n)-1,0);
            t=range(l,int((i/5)/n)+1);
            t2=range(-1,n);
            t3=range(-1,6);
            if individuo[i] not in t3:
                print("el elemento",i,"del array debe estar en el rango",t3);
                error=1;
                return 1;
            if individuo[i+1] not in t and individuo[i+1]!=-1:
                print("el elemento",i,"del array debe estar en el rango",t,"o valer -1");
                error=1;
                return 1;
        
            if  individuo[i+2] not in t2:
                print("el elemento",i,"del array debe estar en el rango",t2);
                error=1;
                return 1;
            if individuo[i+3] not in t and individuo[i+3 ]!=-1:
                print("el elemento",i,"del array debe estar en el rango",t,"o valer -1");
                error=1;
                return 1;
            if individuo[i+4] not in t2:
                print("el elemento",i,"del array debe estar en el rango",t2);
                error=1;
                return 1;
            if [individuo[i+1],individuo[i+2]]==[int((i/5)/n)+1,int((i/5)%n)]:
                print("el array en la posición",int((i/5)/n),",",int((i/5)%n),"tiene una entrada que apunta hacia si misma creando un bucle infinito","véase posición",i,"y en adelante");
                error=1;
                return 1;
            if [individuo[i+3],individuo[i+4]]==[int((i/5)/n)+1,int((i/5)%n)]:
                print("el array en la posición",int((i/5)/n),",",int((i/5)%n),"tiene una entrada que apunta hacia si misma creando un bucle infinito","véase posición",i,"y en adelante");
                error=1;
                return 1;
                #miramos si hay entradas vacías
    
    #Función gen
    def gen():
        #con esta función creamos un array que representa los valores de un circuito aleatorio
        x=creator.Individuo();
        #este error no importa porque cuando gen se ejecuta Individuo ya se ha creado
        #
        for i in range(m*n):
            y=random.randint(1,5)
            #por cada espacio del circuito creamos una pueta con unos par�metros al azar
            #y es el tipo de puerta
            x.append(y);
            ih=int(i/n);#con ih calculamos calculamos en que capa estamos ya que si dividimosi entre n y sacamos la parte
            #entera tenemos la capa m
            for j in range(1):
                #esto no tiene sentido hacer un for pero ya esta hecho as�
                # el min es la capa más lejos a la que puede estar una entrada
                min=ih-1;
                #miramos que la cpa mínima no sea -1
                if min<0:
                    min=0;
                #aquí ponemos ih y no ih-1 por que hay que pensar que la primera capa es de entradas por lo 
                #que todo sube un puesto
                #ponemos min-1 porque los valores que están en min-1 vamos a tomarlos como si esa conexión no fuera usada
                d=random.randint(min-1,ih);
                if d==min-1:
                    d=-1;
                x.append(d);
                x.append(random.randint(-1,n-1));
                e=random.randint(min-1,ih);
                if e==min-1:
                    e=-1;
                x.append(e);
                x.append(random.randint(-1,n-1));
            
        return x;
    def generateLowAndMax():
        x=[];
        y=[];
        for i in range(m*n):
            
            x.append(1);
            y.append(5);
            ih=int(i/n);#con ih calculamos calculamos en que capa estamos ya que si dividimosi entre n y sacamos la parte
            #entera tenemos la capa m
            for j in range(1):
                #esto no tiene sentido hacer un for pero ya esta hecho as�
                # el min es la capa más lejos a la que puede estar una entrada
                min=ih-1;
                #miramos que la cpa mínima no sea -1
                if min<0:
                    min=0;
                #aquí ponemos ih y no ih-1 por que hay que pensar que la primera capa es de entradas por lo 
                #que todo sube un puesto
                #ponemos min-1 porque los valores que están en min-1 vamos a tomarlos como si esa conexión no fuera usada
                
                x.append(min);
                y.append(ih);
                x.append(0);
                y.append(n-1);
                x.append(min);
                y.append(ih);
                x.append(0);
                y.append(n-1);
            
        return x,y;


    def ejecutaEaSimple():
        INT_MIN, INT_MAX = 0, 5
        FLT_MIN, FLT_MAX= 0, 1
        print("Datos de ejecución");
        print("-------------------------------------------------------");
        print("Algoritmo usado: eaSimple")
        creator.create('Fitness', base.Fitness, weights=(1.0,))
        creator.create("Individuo", list, fitness=creator.Fitness);
        toolbox1 = base.Toolbox()
        toolbox1.register("attr_int",random.randint,  INT_MIN, INT_MAX)
        toolbox1.register("attr_flt", random.randint, FLT_MIN, FLT_MAX)
        toolbox1.register("individuo", gen);#un individuo es un circuito al azar
        print(toolbox1.individuo());
        toolbox1.register('poblacion', tools.initRepeat,
            container=list, func=toolbox1.individuo, n=pobTam)#una poblacion es un conjunto de individuos
        toolbox1.register('evaluate',fenotipo);
        if cruzamiento==0:
            print("Cruzamiento: Un punto")
            toolbox1.register('mate', tools.cxOnePoint);
        elif cruzamiento==1:
            print("Cruzamiento: Dos puntos")
            toolbox1.register('mate', tools.cxTwoPoint);
        elif cruzamiento==2:
            print("Cruzamiento: Uniforme con idpbd=",indpbCx);
            toolbox1.register('mate', tools.cxUniform,indpb=indpbCx);
        if mutacion==1:
            low,up=generateLowAndMax()
            print("Mutación: Uniforme con idpbd=",indpbMut);
            toolbox1.register('mutate', tools.mutUniformInt, low=low, up=up,  indpb=indpbMut)
        if mutacion==0:
            print("Mutación: Uniforme sin ajustar con idpbd=",indpbMut);
            toolbox1.register('mutate', tools.mutUniformInt, low=1, up=5,  indpb=indpbMut)
        toolbox1.register('select', tools.selTournament, tournsize=3)
        print("Probabilidad de cruzamiento:",cxpbd);
        print("Probabilidad de mutación:",mutpbd);
        print("Selección: Selección por torneo de tamaño 3");
        print("Tamaño de población inicial=",pobTam);
        print("Número de generaciones:",ngen);
        salon_fama = tools.HallOfFame(5);
        estadisticas = tools.Statistics(key=lambda ind: ind.fitness.values)
        estadisticas.register("mínimo", numpy.min)
        estadisticas.register("media", numpy.mean)
        estadisticas.register("máximo", numpy.max)
        random.seed(12345)
        sys.setrecursionlimit(922);
        poblacion_inicial = toolbox1.poblacion()
        startTime=time.time();
        poblacion_final, registro = algorithms.eaSimple(poblacion_inicial,
                                                        toolbox1,
                                                        cxpb=cxpbd,  # Probabilidad de cruzamiento
                                                        mutpb=mutpbd
                                                        ,  # Probabilidad de mutaci�m
                                                        ngen=ngen
                                                        ,  # m�mero de generaciones
                                                        verbose=False,
                                                        stats=estadisticas,
                                                        halloffame=salon_fama)
        print("Tiempo de ejecución:", time.time()-startTime);
        generarResultados(registro,salon_fama,ngen,toolbox1);
    def generarResultados(registro,salon_fama,ngen,toolbox1):
        maximos=registro.select("máximo");
        minimos=registro.select("mínimo");
        medias=registro.select("media");
        print("Para este caso el valor máximo de acierto obtenido por el algoritmo es:",max(maximos));
        media=0.0;
        print("Las 5 mejores soluciones son:")
        for individuo in salon_fama:
            d=toolbox1.evaluate(individuo);
            print(individuo,d);
            media=media+d[0];
        print("media de las 5 mejores soluciones=",media/5
          );    
        #gráficas
        
        data = [x / (len(vectorEntradas)*n) for x in maximos];
        
        data2 = [x / (len(vectorEntradas)*n) for x in medias];
        print(data2);
        xaxis=list(range(ngen));
        trace0=go.Scatter(x=xaxis,y=data,name="máximo");
        trace1=go.Scatter(x=xaxis,y=data2,name="media");
        datos=[trace0,trace1];
        layout = go.Layout(
            title='Máximos y media por generación',
            xaxis=dict(
                title='Generaciones',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='% de reparación',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
        fig = go.Figure(data=datos, layout=layout)
        py.offline.plot(fig, filename = 'basicline.html', auto_open=True);
    def ejecutaEaMuPlusLambda():
        INT_MIN, INT_MAX = 0, 5
        FLT_MIN, FLT_MAX= 0, 1
        print("Datos de ejecución");
        print("-------------------------------------------------------");
        print("Algoritmo usado: eaMuPlusLambda")
        creator.create('Fitness', base.Fitness, weights=(1.0,))
        creator.create("Individuo", list, fitness=creator.Fitness);
        toolbox1 = base.Toolbox()
        toolbox1.register("attr_int",random.randint,  INT_MIN, INT_MAX)
        toolbox1.register("attr_flt", random.randint, FLT_MIN, FLT_MAX)
        toolbox1.register("individuo", gen);#un individuo es un circuito al azar
        print(toolbox1.individuo());
        toolbox1.register('poblacion', tools.initRepeat,
            container=list, func=toolbox1.individuo, n=pobTam)#una poblacion es un conjunto de individuos
        toolbox1.register('evaluate',fenotipo);
        if cruzamiento==0:
            print("Cruzamiento: Un punto")
            toolbox1.register('mate', tools.cxOnePoint);
        elif cruzamiento==1:
            print("Cruzamiento: Dos puntos")
            toolbox1.register('mate', tools.cxTwoPoint);
        elif cruzamiento==2:
            print("Cruzamiento: Uniforme con idpbd=",indpbCx);
            toolbox1.register('mate', tools.cxUniform,indpb=indpbCx);
        if mutacion==1:
            low,up=generateLowAndMax()
            print("Mutación: Uniforme con idpbd=",indpbMut);
            toolbox1.register('mutate', tools.mutUniformInt, low=low, up=up,  indpb=indpbMut)
        if mutacion==0:
            print("Mutación: Uniforme sin ajustar con idpbd=",indpbMut);
            toolbox1.register('mutate', tools.mutUniformInt, low=1, up=5,  indpb=indpbMut)
        toolbox1.register('select', tools.selTournament, tournsize=3)
        print("Probabilidad de cruzamiento:",cxpbd);
        print("Probabilidad de mutación:",mutpbd);
        print("Selección: Selección por torneo de tamaño 3");
        print("Tamaño de lambda=",lam);
        print("Tamaño de lambda=",mu);
        print("Número de generaciones:",ngen)
        salon_fama = tools.HallOfFame(5);
        estadisticas = tools.Statistics(key=lambda ind: ind.fitness.values)
        estadisticas.register("mínimo", numpy.min)
        estadisticas.register("media", numpy.mean)
        estadisticas.register("máximo", numpy.max)
        random.seed(12345)
        sys.setrecursionlimit(922);
        poblacion_inicial = toolbox1.poblacion()
        print("Si ngen es alto es posible que tarde en seguir imprimendo en pantalla")
        startTime=time.time();
        poblacion_final, registro = algorithms.eaMuPlusLambda(poblacion_inicial,
                                                        toolbox1,
                                                        lam, mu,
                                                        cxpb=cxpbd,
                                                        mutpb=mutpbd,
                                                        ngen=ngen,
                                                        stats=estadisticas,
                                                        halloffame=salon_fama, verbose=False)
        print("Tiempo de ejecución:", time.time()-startTime);
        generarResultados(registro,salon_fama,ngen,toolbox1);
    #Nos aseguramos que todas las variables están en los límites aceptados
    val=validateVariables();
    if val==1:
        return 1;
    comp=compErroresCircuito();
    if comp==1:
        print("Hay un error en el circuito");
        return 1;
    circCorr=circuitoCorrecto();
    if circCorr==1:
        print("El circuito funciona correctamente, no necesita arreglo");
        return 1;
    else:
        print("El circuito no produce la salida esperada, procedemos a la autoconfiguración");
    
    print("Esta es una representación de tu circuito");
    representaCircuitos3(circuito, vectorEntradas[0], m, n);
    #Una vez nos hemos asegurado de que todos los valores son correctos vamos a ejecutar los algoritmos de evolución
    if algoritmo==0:
        ejecutaEaSimple()
    if algoritmo==1:
        ejecutaEaMuPlusLambda();
    