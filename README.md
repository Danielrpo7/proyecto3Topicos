# proyecto3Topicos
Proyecto Tópocos telemática 

Autores:
Pablo Quijano - pquijano@eafit.edu.co
Daniel Restrepo -

Introducción:
En éste repositorio se encuentran dos programas (uno en serial y otro en paralelo) que sirven para encontrar la similitud que existe entre documentos, basicamente utiliza dos algoritmos principales, Jaccard y Kmeans (que serán explicados a continuación), con los cuales agrupamos en diferentes clusters los documentos que más se parecen debido a una serie de palabras relevantes. El dataset se obtuvo de Gutenberg por medio del siguiente link, https://goo.gl/LL4CgA, en este dataset se encuentran al rededor de 3000 documentos con los cuáles se pueden correr los programas.

Algoritmos empleados:
Para empezar con los programas se decidió gracias a la lectura de varios papers, escoger una cantidad 10 términos de cada documento para poder hacer la comparación entre ellos, entonces lo que se hace es que después de eliminar las 'stopwords' se buscan las 10 palabras más usadas en los documentos, estas palabras se ingresan en una lista que posteriormente será utilizada por el Jaccard para encontrar la similitud de los documentos, cuando obtenemos esta similitud también obtenemos la distancia entre archivos y esto lo ingresamos en una matriz que será procesada por el Kmeans donde finalmente agruparemos los documentos con sus respectivos centroides. Los algoritmos que se utilizaron fueron Jaccard para obtener las distancias entre los documentos y KMeans para agrupar los documentos en sus respectivos centros

Jaccard:
*El índice de Jaccard ( IJ ) o coeficiente de Jaccard ( IJ ) mide el grado de similitud entre dos conjuntos, sea cual sea el tipo de elementos.

La formulación es la siguiente:
J(A,B) = |A ∩ B| / |A ∪ B|* Éste algoritmo se obtuvo de la siguiente página donde se explicaba de muy buena manera su funcionamiento, http://dataconomy.com/2015/04/implementing-the-five-most-popular-similarity-measures-in-python/

KMeans:
K-means es un método de agrupamiento, que tiene como objetivo la partición de un conjunto de n observaciones en k grupos en el que cada observación pertenece al grupo cuyo valor medio es más cercano. Es un método utilizado en minería de datos. El código para el Kmeans se obtuvo de varios links y repositorios de dónde se trató de entender su funcionamiento y gracias a los cuáles se pudo realizar el KMeans que se encuentra en los programas realizados.

Ejecución programas:
Para correr el programa serial, se debe ejecutar el sifuiente comando: <python2.7 serial.py ./(Carpeta del dataset)/
Para el paralelo, el comando es: <mpiexec -np (número de nucleos) python2.7 paraleloF.py ./(Carpeta del dataset)/
