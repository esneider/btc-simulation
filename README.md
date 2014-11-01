# Marco teórico

## Qué es Bitcoin

Bitcoin es una moneda digital global con la que se pueden realizar transacciones sin la necesidad de una entidad central (ej. banco central) que la coordine.

Esta moneda tiene propiedades similares al efectivo, permitiendo transacciones casi instantáneas y no reembolsables. Pero logra esto sin hacer distinciones entre distancias: es lo mismo realizar un pago a alguien que está parado en frente mío, que a alguien que esta en otro continente.

También comparte aspectos con el oro, al ser un recurso finito y escaso. Los bitcoins, al igual que el oro, entran en circulación tras ser minados y su precio es determinado puramente por la oferta y demanda del mercado. Sin embargo, los bitcoins son fácilmente divisibles, portables, y almacenables: es lo mismo almacenar un bitcoin, que mil.

Este conjunto de propiedades únicas introduce varias aplicaciones innovadores como propiedades inteligentes, micropagos, etc.

## Cómo funciona Bitcoin

Tanto la generación de nuevos bitcoins, como el procesamiento y verificación de transacciones es llevado a cabo por la red de Bitcoin. Esta red mantiene colectivamente un registro contable (**ledger**) con el balance de todas las cuentas del sistema.

La red bitcoin es una red p2p en la cual cada participante es un **nodo** de la red. Por esta red se transmiten dos tipos de información: **transacciones** y **bloques**. Las transacciones permiten transferir bitcoins entre cuentas, y los bloques son usados para sincronizar el estado a través de todos los nodos de la red.

Cada nodo de la red guarda una réplica completa del ledger. Es crucial que estas réplicas sean consistentes, ya que son utilizadas para verificar las transacciones.

### Nodo

Cada participante de la red de Bitcoin es llamado nodo, y tiene una lista de **vecinos** con los que se comunica. Los nodos son los encargados de verificar los bloques y las transacciones, y transmitirlos al resto de la red: cada nodo reenvía los bloques y transacciones a todos sus vecinos.

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

Este sistema en donde cada bloque apunta a su padre, genera un árbol dirigido de bloques. A la raíz del árbol, es decir el primer bloque jamás emitido, se lo llama **bloque génesis**. La **altura** de un bloque es su distancia al bloque génesis.

La **blockchain** se define como la cadena más larga de bloques conectados entre sí, que termina en el bloque génesis. Al primer bloque de esta cadena, se lo llama **cabeza** de la blockchain.

![](https://github.com/esneider/btc-simulation/raw/master/images/blockchain.png)

La blockchain forma un registro de todas las transacciones desde la creación de Bitcoin hasta el presente, es decir, el llamado ledger. Una transacción se considera válida y confirmada si aparece en algún bloque de la blockchain.

Al crear un bloque, un minero recibirá sus bitcoins minados sólo si este bloque pertenece a la cadena más larga, la blockchain. Por lo tanto al minero siempre le convendrá construir sus bloques con el bloque cabeza como padre (hay algunas excepciones a esto, como selfish mining [1] y freeze attack [2]).

### Bifurcación de la blockchain

Los mensajes entre nodos de la red de Bitcoin se transmiten tan rápido como las conexiones de Internet entre ellos lo permiten. Dado que los bloques son encontrados al azar independientemente por los nodos mineros, puede llegar a encontrarse un bloque mientras otro bloque en conflicto está siendo propagado por la red.

Como ambos bloques son válidos y tienen la misma altura, ambos son potenciales cabezas de la blockchain, y esta se bifurca: una parte de los nodos tendrá como cabeza de la blockchain a este nuevo nodo, mientras que el resto de los nodos tendrá como cabeza al primer bloque. En consecuencia, diferentes nodos ven diferentes historias, y el sistema deja de ser consistente.

La bifurcación puede prolongarse si las particiones de la red siguen encontrando bloques que construyen sobre sus respectivas cabezas de blockchain, formando dos (o más) ramas. Pero eventualmente alguna de las ramas será más larga que el resto y se resolverá la bifurcación, ya que cuando un nodo recibe un nuevo bloque y su altura es mayor a todos los bloques previos, lo tomará como la nueva cabeza de la blockchain.

## Topología de la red



[1]  Eyal, Ittay, and Emin Gün Sirer. "Majority is not enough: Bitcoin mining is vulnerable". http://arxiv.org/abs/1311.0243 (2013)

[2]  Lerner, Sergio. “The Bitcoin Freeze on Transaction Attack (FRONT)”. http://sourceforge.net/p/bitcoin/mailman/message/32899645/ (2014)

