# Marco teórico

## Qué es Bitcoin

Bitcoin es una moneda digital global con la que se pueden realizar transacciones sin la necesidad de una entidad central que la coordine (ej. banco central).

Esta moneda tiene propiedades similares al efectivo, permitiendo transacciones casi instantáneas y no reembolsables. Pero logra esto sin hacer distinciones entre distancias: es lo mismo realizar un pago a alguien que está parado en frente mío, que a alguien que esta en otro continente.

También comparte aspectos con el oro, al ser un recurso finito y escaso. Los bitcoins entran en circulación tras ser minados y su precio es determinado puramente por la oferta y demanda del mercado. Sin embargo, a diferencia del oro, son fácilmente divisibles, portables y almacenables: es lo mismo almacenar un bitcoin, que mil.

Este conjunto de propiedades únicas introduce varias aplicaciones innovadores como propiedades inteligentes, micropagos, etc.

## Cómo funciona la red de Bitcoin

Tanto la generación de nuevos bitcoins como el procesamiento y verificación de transacciones es llevado a cabo por la red de Bitcoin. Esta red mantiene colectivamente un registro contable (**ledger**) con el balance de todas las cuentas del sistema.

Los participantes de la red de Bitcoin (**nodos**) transmiten dos tipos de información: **transacciones** y **bloques**. Las transacciones permiten transferir bitcoins entre cuentas, y los bloques son usados para sincronizar el estado a través de todos los nodos de la red.

Cada nodo guarda una réplica completa del ledger. Es crucial que estas réplicas sean consistentes, ya que son utilizadas para verificar las transacciones.

### Nodos

Cada participante de la red de Bitcoin es un nodo de la red, y tiene una lista de **vecinos** con los que se comunica. Al recibir un mensaje, un nodo verifica su validez y lo retransmite a todos sus vecinos.

Existen nodos distinguidos llamados **mineros**, que son los encargados de crear nuevos bloques.

### Transacciones

Una transacción transfiere bitcoins de una o más **cuentas origen**, hacia una o más **cuentas destino**. Para que una transacción sea válida las cuentas origen deben tener dinero suficiente para cubrir el monto de la transacción.

Cuando un usuario desea transferir sus bitcoins, crea una transacción y la envía a algún nodo de la red. Los nodos, al recibir una nueva transacción, la verifican, la agregan a su réplica del ledger, y la transmiten al resto de la red.

A medida que las transacciones son transmitidas por la red, el estado de las réplicas del ledger cambia. Si distintas réplicas tienen transacciones en distinto orden, se dice que están en un estado **inconsistente**:

* Un nodo puede recibir una transacción que transfiere fondos de una cuenta, antes de recibir la transacción que enviaba los fondos hacia esa cuenta.

* Un atacante puede enviar distintas transacciones a distintos nodos, que usen los mismos fondos. Esto se llama **double spending attack**.

Para evitar estos problemas y mantener la consistencia, los nodos deben estar de acuerdo en un único orden de las transacciones.

### Bloques

Para sincronizar las distintas réplicas del ledger se introducen los bloques. Cada bloque contiene una lista de transacciones, metadata, y un número arbitrario llamado **nonce**. El trabajo de los nodos mineros consiste en construir bloques con las transacciones que no hayan sido incluidas en ningún bloque. Este proceso es conocido como **minado de bitcoins**.

Cuando un minero logra construir un bloque válido, lo envía a todos sus vecinos. Al recibir un nuevo bloque, cada nodo lo verifica y reenvía al resto de la red. Si el nodo es minero, además actualiza su lista de transacciones no incluidas en ningún bloque, y empieza a trabajar en el próximo bloque.

El minado de bitcoins es un proceso difícil: para que un bloque sea válido, el minero debe encontrar un valor del nonce que cumpla con cierta propiedad matemática. La dificultad de este problema matemático se ajusta automáticamente para que, en promedio, se cree un bloque cada 10 minutos.

De manera similar al oro, la única manera de crear bitcoins es minandolos. Los mineros tienen derecho a agregar una transacción especial en cada bloque que minen, llamada **coinbase**, que crea una cantidad prefijada de bitcoins y los envía a la cuenta del minero.

### Blockchain

Cada bloque contiene en su metadata una referencia al bloque inmediatamente anterior sobre el que fue construido, su **padre**. Al encadenarlos de esta manera, se crea un orden cronológico de bloques, y por lo tanto de las transacciones que contienen.

Este sistema en donde cada bloque apunta a su padre, genera un árbol dirigido de bloques. A la raíz del árbol, es decir el primer bloque jamás emitido, se lo llama **bloque génesis**. La **altura** de un bloque es su distancia al bloque génesis.

![](https://github.com/esneider/btc-simulation/raw/master/images/blockchain.png)

La **blockchain** se define como la cadena más larga de bloques conectados entre sí, que termina en el bloque génesis. Al primer bloque de esta cadena se lo llama **cabeza** de la blockchain.

Una transacción se considera **confirmada** únicamente si aparece en algún bloque de la blockchain. Es decir, la blockchain forma un registro ordenado cronológicamente de todas las transacciones realizadas desde la creación de Bitcoin hasta el presente.

Al crear un bloque, un minero recibirá sus bitcoins minados sólo si este bloque pertenece a la cadena más larga, la blockchain, sino la transacción coinbase nunca será confirmada. Por lo tanto, al minero siempre le convendrá construir sus bloques con el bloque cabeza como padre.

### Bifurcaciones de la blockchain

Los mensajes entre nodos de la red de Bitcoin se transmiten tan rápido como las conexiones de Internet entre ellos lo permiten. Dado que el proceso de creación de bloques es aleatorio, puede llegar a encontrarse un bloque mientras otro bloque en conflicto está siendo propagado por la red.

Como ambos bloques son válidos y tienen la misma altura, ambos son potenciales cabezas de la blockchain, y esta se **bifurca**: los nodos que hayan recibido antes el primer bloque, lo marcarán como cabeza de la blockchain, y el resto de los nodos tendrá como cabeza al último bloque. Tras este evento, diferentes nodos ven diferentes historias, y el sistema deja de ser consistente.

![](https://github.com/esneider/btc-simulation/raw/master/images/fork.png)

En la imagen se puede apreciar el proceso recién mencionado. **(1)** Todos los nodos tienen la misma cabeza `P`. **(2)** El nodo `a` construye un nuevo bloque `A` que tiene como padre a `P`. **(3)** Mientras el bloque `A` se propaga por la red, el nodo `b` construye un nuevo bloque `B` que tiene como padre a `P`, ya que el nodo `b` aún no está enterado de la existencia del bloque `A`. **(4)** Finalmente los nodos quedan particionados en dos subconjuntos, los que tienen a `A` como cabeza y los que tienen a `B` como cabeza.

Tras una bifurcación, ambas particiones competirán para encontrar el próximo bloque y decidir que versión de la historia será la definitiva. Si se encuentra un bloque en una partición y antes de distribuirse por toda la red se encuentra otro bloque en la partición opuesta, la bifurcación se prolongará, formando dos ramas.

![](https://github.com/esneider/btc-simulation/raw/master/images/fork_resolution.png)

Eventualmente alguna de las ramas será más larga y se resolverá la bifurcación, ya que cuando un nodo recibe un nuevo bloque cuya altura es mayor a la de todos los bloques previos, lo tomará como la nueva cabeza de la blockchain. Por este motivo se dice que Bitcoin es un sistema con **consistencia eventual**.

### Double spending attack

[...] dos o más transacciones pueden intentar transferir el mismo dinero al mismo tiempo en nodos distintos. Esto es llamado **double spending attack**.

# Modelo de la red de Bitcoin

Modelamos la red de Bitcoin como un grafo dirigido `G = (V,􏰋E)` en donde cada nodo `v` tiene una fracción `pᵥ ≥ 0` del poder computacional de la red.

<p align="center">
    <img src="http://latex.codecogs.com/png.latex?%5Cdpi%7B150%7D%20%5Csum_%7Bv%20%5C%2C%5Cin%20V%7Dp_v%20%3D%201"></img>
</p>

Cada nodo `v` de la red genera bloques mediante un proceso de Poisson, con una velocidad `pᵥ · λ`, y la red entera combinada genera bloques mediante un proceso de Poisson con velocidad `λ`.

Cuando un bloque es generado por un nodo, es inmediatamente enviado a todos sus vecinos en la red, que continúan propagando el bloque a sus vecinos hasta que eventualmente todos los nodos lo hayan recibido. Cada arista `e ∈ E` tiene una latencia `lₑ`, que es el tiempo que tarda en transmitirse una unidad mínima de información por esa arista, y que cada nodo `v` tiene una velocidad de subida `sᵥ` y una velocidad de bajada `bᵥ`. Si `e` es la arista de `u` a `v`, entonces el tiempo de transmisión de un bloque `b` por la arista `e` es:

<p align="center">
    <img src="http://latex.codecogs.com/png.latex?%5Cdpi%7B150%7D%20t_e%28b%29%20%3D%20%5Cmin%5Cleft%28s_u%2C%20b_v%5Cright%29%20%5Ccdot%20%5Cleft%7Cb%5Cright%7C%20&plus;%20l_e"></img>
</p>

Donde `|b|` es el tamaño del bloque `b`.

