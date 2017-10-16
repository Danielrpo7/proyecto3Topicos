# proyecto3Topicos
Proyecto3 de la materia Tópicos Especiales en Telemática. 

Autores:

Pablo Quijano - pquijano@eafit.edu.co

Daniel Restrepo -

Introducción:

El proyecto 3 consistió en diseñar e implementar un algoritmo paralelo que permitiera agrupar (clustering) un conjunto de documentos utilizando el algoritmo de k–means y una métrica de similaridad entre documentos. El dataset utilizado para las pruebas fue el de Gutenberg, que cuenta con al rededor de 3000 documentos. En este repositorio se encuentran 2 programas, uno con el programa realizado en serial y el otro en paralelo.

Algoritmos empleados:

Básicamente se emplearon 2 algoritmos, el kMeans para agupar los documentos, y el Jaccard para medir la similaridad entre estos. A continuación se explica el funcionamiento de cada uno.

Jaccard:

El índice de Jaccard ( IJ ) o coeficiente de Jaccard ( IJ ) mide el grado de similitud entre dos conjuntos, sea cual sea el tipo de elementos.

La formulación es la siguiente:

J(A,B) = |A ∩ B| / |A ∪ B|

K-means:

El algoritmo K-means es uno de los algoritmos de aprendizaje no supervisado más simples para resolver el problema de la clusterización. El procedimiento aproxima por etapas sucesivas un cierto número (prefijado) de clusters haciendo uso de los centroides de los puntos que deben representar.
El algoritmo se compone de los siguientes pasos:

-Sitúa KK puntos en el espacio en el que "viven" los objetos que se quieren clasificar. Estos puntos representan los centroides iniciales de los grupos.

-Asigna cada objeto al grupo que tiene el centroide más cercano.

-Tras haber asignado todos los objetos, recalcula las posiciones de los KK centroides.

-Repite los pasos 2 y 3 hasta que los centroides se mantengan estables. Esto produce una clasificación de los objetos en grupos que permite dar una métrica entre ellos.

Ejecución programas:

Para correr el programa serial, se debe ejecutar el sifuiente comando: <python2.7 serial.py ./(Carpeta del dataset)/

Para el paralelo, el comando es: <mpiexec -np (número de nucleos) python2.7 paraleloF.py ./(Carpeta del dataset)/

Bibliografía:

https://www.gutenberg.org/
https://goo.gl/LL4CgA
http://dataconomy.com/2015/04/implementing-the-five-most-popular-similarity-measures-in-python/
https://es.wikipedia.org/wiki/%C3%8Dndice_Jaccard
http://www.cs.us.es/~fsancho/?e=43


