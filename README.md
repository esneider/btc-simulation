# Marco teórico

## Qué es bitcoin

Bitcoin es una moneda digital global con la que se pueden realizar transacciones sin la necesidad de una entidad central (ej. banco central) que la coordine. [1]

Esta moneda tiene propiedades similares al efectivo, permitiendo transacciones casi instantáneas y no reembolsables. Pero logra esto sin hacer distinciones entre distancias: es lo mismo realizar un pago a alguien que está parado en frente mío, que a alguien que esta en otro continente.

También comparte aspectos con el oro, al ser un recurso finito y escaso. Los bitcoins, al igual que el oro, entran en circulación tras ser minados y su precio es determinado puramente por la oferta y demanda del mercado. Sin embargo, los bitcoins son fácilmente divisibles, portables, y almacenables: es lo mismo almacenar un bitcoin, que mil.

Este conjunto de propiedades únicas introduce varias aplicaciones innovadores como propiedades inteligentes, micropagos, etc.

## Cómo funciona bitcoin

Tanto la generación de nuevos bitcoins, como el procesamiento y verificación de transacciones es llevado a cabo por la red de bitcoin. Esta red mantiene colectivamente un registro contable (**ledger**) con el balance de todas las cuentas del sistema.

La red bitcoin es una red p2p en la cual cada participante es un **nodo** de la red. Por esta red se transmiten dos tipos de información: **transacciones** y **bloques**. Las transacciones permiten transferir bitcoins entre cuentas, y los bloques son usados para sincronizar el estado a través de todos los nodos de la red.

Cada nodo de la red guarda una réplica completa del ledger. Es crucial que estas réplicas sean consistentes, ya que son utilizadas para verificar las transacciones.

### Nodo

Cada nodo tiene una lista de **vecinos** con los que se comunica, que es un subconjunto cuasi-aleatorio [2] del resto de los nodos. Los nodos son los encargados de verificar los bloques y las transacciones, y transmitirlos al resto de la red: cada nodo reenvía los bloques y transacciones a todos sus vecinos.

Existen nodos distinguidos llamados nodos **mineros**. Estos nodos son los encargados de crear nuevos bloques.

### Transacciones

Una transacción transfiere bitcoins de una o más **cuentas origen**, hacia una o más **cuentas destino**. Para que una transacción sea válida, las cuentas origen deben tener el dinero suficiente para cubrir la transacción.

Cuando un usuario desea transferir bitcoins de una o más cuentas suyas, crea una transacción, y se la envía al menos a un nodo de la red. Los nodos, al recibir una nueva transacción, la verifican, la agregan a su réplica del ledger, y la transmiten al resto de los nodos vecinos.

A lo largo del tiempo, las réplicas del ledger en diferentes nodos pueden hacerse inconsistentes:

* Un nodo puede recibir una transacción para transferir dinero de una cuenta, pero aún no recibió la transacción que enviaba el dinero a esa cuenta.

* Dos o más transacciones pueden intentar transferir el mismo dinero al mismo tiempo en nodos distintos. Esto es llamado **double spending attack**.

### Bloques

Para evitar estos problemas, todas las réplicas del ledger deben ser consistentes. Es decir, los nodos tienen que estar de acuerdo en el orden de todas las transacciones.

Para lograrlo, cada nodo minero intenta construir un bloque con las transacciones válidas que todavía no fueron confirmadas. Un bloque contiene una lista de transacciones, metadata, y un número llamado **nonce**. Para que el bloque sea válido, el minero debe encontrar un valor del nonce que cumpla con cierta propiedad matemática. Este proceso es conocido como **minado de bitcoins**: cada nuevo bloque tiene una transacción especial que crea bitcoins, y se los asigna al minero.

Una vez que un minero logra construir un bloque válido, lo envía a sus vecinos. Al recibir un nuevo bloque, cada nodo lo verifica y reenvía al resto de la red. Si el nodo es minero, borra todas las transacciones incluidas en el nuevo bloque de su lista de transacciones no confirmadas, y empieza a trabajar en el próximo bloque.

En este momento, todos los nodos están de acuerdo en la validez de las transacciones del nuevo bloque. Se dice que estas transacciones han sido **confirmadas**.

La dificultad del problema matemático que tienen que resolver los mineros se ajusta automáticamente para que, en promedio, se cree un bloque cada 10 minutos.

### Blockchain

Cada bloque contiene en su metadata una referencia al bloque inmediatamente anterior sobre el que fue construido, su **padre**. De esta manera, al encadenarse los bloques, se crea un orden cronológico de bloques, y por lo tanto, de las transacciones que contienen.

Este sistema en donde cada bloque apunta a su padre, genera un árbol dirigido de bloques. A la raíz del árbol, es decir el primer bloque jamás emitido, se lo llama **bloque génesis**.

La **blockchain** se define como la cadena más larga de bloques conectados entre sí, que termina en el bloque génesis. Al primer bloque de esta cadena, se lo llama **cabeza** de la blockchain.

![](https://github.com/esneider/btc-simulation/raw/master/images/blockchain.png)

Una transacción se considera válida y confirmada si aparece en algún bloque de la blockchain. Por lo tanto, al crear un bloque, un minero recibirá sus bitcoins minados sólo si este bloque pertenece a la blockchain, es decir, a la cadena más larga. En consecuencia, al minero siempre le convendrá construir sus bloques con el bloque cabeza como padre.

### Bifurcación de la blockchain

WORK IN PROGRESS!

# Generación del grafo de la red Bitcoin

Parámetros de la simulación:

* Número de nodos (6724 as of today [3])

Variables aleatorias:

* Por cada nodo, cantidad de conexiones (distribución a determinar [4])

* Por cada nodo, lista de conexiones (distribución uniforme)

* Por cada conexión, latencia (distribución a determinar)

* Por cada conexión, bandwidth (distribución a determinar)



[1]  Nakamoto, Satoshi. Bitcoin: A Peer-to-Peer Electronic Cash System. https://bitcoin.org/bitcoin.pdf, 2008

[2]  bitcoind peer discovery algorithms. https://en.bitcoin.it/wiki/Satoshi_Client_Node_Discovery

[3]  https://getaddr.bitnodes.io/

[4]  El máximo (default) es 125: bitcoind --help | grep maxconnections.

