import copy

def initialize_routing_table(nodes, edges):
    """
    Crea una tabella di routing iniziale per ciascun nodo, includendo i next hop.
    :param nodes: Lista di nodi nella rete
    :param edges: Lista di tuple (nodo1, nodo2, costo) rappresentanti i collegamenti
    :return: Dizionario con tabelle di routing per ciascun nodo
    """
    routing_table = {}
    for node in nodes:
        # Inizializza le distanze a infinito per tutti i nodi eccetto se stesso
        routing_table[node] = {n: {'cost': float('inf'), 'next_hop': None} for n in nodes}
        routing_table[node][node] = {'cost': 0, 'next_hop': node}  # Distanza a se stesso = 0

    for edge in edges:
        # Imposta il costo e il next hop per i collegamenti diretti tra i nodi
        nodo1, nodo2, costo = edge
        routing_table[nodo1][nodo2] = {'cost': costo, 'next_hop': nodo2}
        routing_table[nodo2][nodo1] = {'cost': costo, 'next_hop': nodo1}

    return routing_table

def print_routing_table(routing_table):
    """
    Stampa la tabella di routing per ciascun nodo, inclusi i next hop.
    :param routing_table: Dizionario con le tabelle di routing
    """
    for node, table in routing_table.items():
        print(f"Tabella di routing per il nodo {node}:")
        for dest, data in table.items():
            cost = data['cost']
            next_hop = data['next_hop']
            print(f"  {dest}: costo={cost}, next_hop={next_hop}")
        print("\n")

def distance_vector_routing(nodes, edges, max_iterations=10):
    """
    Simula il protocollo di routing Distance Vector con next hop.
    :param nodes: Lista di nodi nella rete
    :param edges: Lista di tuple (nodo1, nodo2, costo) rappresentanti i collegamenti
    :param max_iterations: Numero massimo di iterazioni da eseguire.
    :return: Tabella di routing finale
    """
    # Inizializza la tabella di routing
    routing_table = initialize_routing_table(nodes, edges)

    for iteration in range(max_iterations):
        print(f"Iterazione {iteration + 1}:")
        updated = False
        # Copia profonda della tabella per evitare modifiche simultanee
        new_table = copy.deepcopy(routing_table)

        for node in nodes:
            for neighbor in nodes:
                # Salta se il nodo corrente non è un vicino diretto
                if neighbor == node or routing_table[node][neighbor]['cost'] == float('inf'):
                    continue

                for dest in nodes:
                    # Salta se il nodo di destinazione è lo stesso nodo di partenza
                    if dest == node:
                        continue

                    # Calcola il nuovo costo passando attraverso il vicino
                    new_cost = routing_table[node][neighbor]['cost'] + routing_table[neighbor][dest]['cost']
                    if new_cost < routing_table[node][dest]['cost']:
                        # Aggiorna la tabella con il nuovo costo più basso e next hop
                        new_table[node][dest]['cost'] = new_cost
                        new_table[node][dest]['next_hop'] = routing_table[node][neighbor]['next_hop']
                        updated = True

        # Aggiorna la tabella di routing per la prossima iterazione
        routing_table = new_table
        print_routing_table(routing_table)

        # Termina se non ci sono stati aggiornamenti
        if not updated:
            print("Le tabelle di routing sono stabili. Fine della simulazione.")
            break

    return routing_table

if __name__ == "__main__":
    # Esempio di nodi e collegamenti
    nodes = ["Nodo A", "Nodo B", "Nodo C", "Nodo D"]
    edges = [
        ("Nodo A", "Nodo B", 1),
        ("Nodo B", "Nodo C", 2),
        ("Nodo A", "Nodo C", 4),
        ("Nodo C", "Nodo D", 1)
    ]

    print("Simulazione del protocollo Distance Vector Routing:\n")
    final_routing_table = distance_vector_routing(nodes, edges)

    print("Tabelle di routing finali:")
    print_routing_table(final_routing_table)
