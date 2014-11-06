# Marco teórico

## Qué es Bitcoin

Bitcoin es una moneda digital global con la que se pueden realizar transacciones sin la necesidad de una entidad central que la coordine (ej. banco central).

Esta moneda tiene propiedades similares al efectivo, permitiendo transacciones casi instantáneas y no reembolsables. Pero logra esto sin hacer distinciones entre distancias: es lo mismo realizar un pago a alguien que está parado en frente mío, que a alguien que esta en otro continente.

También comparte aspectos con el oro, al ser un recurso finito y escaso. Los bitcoins entran en circulación tras ser minados y su precio es determinado puramente por la oferta y demanda del mercado. Sin embargo, a diferencia del oro, son fácilmente divisibles, portables y almacenables: es lo mismo almacenar un bitcoin, que mil.

Este conjunto de propiedades únicas introduce varias aplicaciones innovadores como propiedades inteligentes, micropagos, etc.

## Cómo funciona Bitcoin

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

De manera similar al oro, la única manera de crear bitcoins es minandolos. Los mineros tienen derecho a agregar una transacción especial en cada bloque que minen. Esta transacción, llamada **coinbase**, crea una cantidad prefijada de bitcoins y los envía a la cuenta del minero.

### Blockchain

Cada bloque contiene en su metadata una referencia al bloque inmediatamente anterior sobre el que fue construido, su **padre**. Al encadenarlos de esta manera, se crea un orden cronológico de bloques, y por lo tanto de las transacciones que contienen.

Este sistema en donde cada bloque apunta a su padre, genera un árbol dirigido de bloques. A la raíz del árbol, es decir el primer bloque jamás emitido, se lo llama **bloque génesis**. La **altura** de un bloque es su distancia al bloque génesis.

![](https://github.com/esneider/btc-simulation/raw/master/images/blockchain.png)

La **blockchain** se define como la cadena más larga de bloques conectados entre sí, que termina en el bloque génesis. Al primer bloque de esta cadena se lo llama **cabeza** de la blockchain.

Una transacción se considera **confirmada** únicamente si aparece en algún bloque de la blockchain. Es decir, la blockchain forma un registro ordenado cronológicamente de todas las transacciones realizadas desde la creación de Bitcoin hasta el presente.

Al crear un bloque, un minero recibirá sus bitcoins minados sólo si este bloque pertenece a la cadena más larga, la blockchain, sino la transacción coinbase nunca será confirmada. Por lo tanto, al minero siempre le convendrá construir sus bloques con el bloque cabeza como padre.

### Bifurcaciones de la blockchain

Los mensajes entre nodos de la red de Bitcoin se transmiten tan rápido como las conexiones de Internet entre ellos lo permiten. Como los bloques son encontrados independientemente de forma aleatoria por los nodos mineros, puede llegar a encontrarse un bloque mientras otro bloque en conflicto está siendo propagado por la red.

Como ambos bloques son válidos y tienen la misma altura, ambos son potenciales cabezas de la blockchain, y esta se **bifurca**: los nodos que hayan recibido antes el primer bloque, lo marcarán como cabeza de la blockchain, y el resto de los nodos tendrá como cabeza al último bloque. Tras este evento, diferentes nodos ven diferentes historias, y el sistema deja de ser consistente.

![](https://github.com/esneider/btc-simulation/raw/master/images/fork.png)

En la imagen se puede apreciar el proceso recién mencionado. En la etapa 1, todos los nodos tienen la misma cabeza `P`. En la etapa 2, el nodo `a` construye un nuevo bloque `A` que tiene como padre a `P`. En la etapa 3, mientras el bloque `A` se propaga por la red, el nodo `b` construye un nuevo bloque `B` que tiene como padre a `P`, ya que el nodo `b` aún no está enterado de la existencia del bloque `A`. Finalmente, en la etapa 4, los nodos quedan particionados en dos subconjuntos, los que tienen a `A` como cabeza y los que tienen a `B` como cabeza.

La bifurcación puede prolongarse si ambas particiones de la red siguen encontrando bloques que construyan sobre sus respectivas cabezas de blockchain, formando dos ramas. Pero eventualmente alguna de las ramas será más larga y se resolverá la bifurcación, ya que cuando un nodo recibe un nuevo bloque y su altura es mayor a todos los bloques previos, lo tomará como la nueva cabeza de la blockchain. Por este motivo, se dice que Bitcoin es un sistema con **consistencia eventual**.

### Double spending attack

[...] dos o más transacciones pueden intentar transferir el mismo dinero al mismo tiempo en nodos distintos. Esto es llamado **double spending attack**.

## Topología de la red

