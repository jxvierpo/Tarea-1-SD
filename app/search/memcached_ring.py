import uhashring
import memcache
import json
import time
import numpy as np
from find_car_by_id import find_car_by_id

class CacheClient:
    def __init__(self):
        # Configura el cliente Memcached con los nombres de host de los contenedores
        nodes = ["memcached-master:11211", "memcached-slave:11211"]
        self.ring = uhashring.HashRing(nodes)
        
    def get_mc_client(self, key):
        server = self.ring.get_node(key)
        return memcache.Client([server])

    def get(self, key, simulated=False):
        start_time = time.time()  # Inicio del temporizador

        # Obtiene el cliente Memcached correcto basado en el hashing consistente
        mc = self.get_mc_client(key)

        # Realiza la operación de obtener en el cliente Memcached
        value = mc.get(key)

        if value:
            print("Key found in Memcached.")
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            print(f"Time taken (Memcached + delay): {elapsed_time:.5f} seconds")
            return value
        else:
            if not simulated:
                # Simula un retraso aleatorio (puedes mantener esta parte)
                delay = np.random.normal(2, 0.5)
                print(f"Waiting {delay:.5f} seconds...")
                time.sleep(delay)
            # Si no se encuentra en Memcached, busca en el JSON y almacena en Memcached
            value = find_car_by_id(int(key))
            value = str(value)
            if value:
                print("Key found in JSON. Adding to Memcached...")
                # Almacena el valor en Memcached para futuras consultas
                mc.set(key, value)
                elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                if simulated:
                    # Añade el retraso al tiempo
                    elapsed_time += delay
                print(f"Time taken (JSON + delay): {elapsed_time:.5f} seconds")
                return value
            else:
                elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                print(f"Time taken: {elapsed_time:.5f} seconds")
                print("Key not found.")
                return None

    def simulate_searches(self, n_searches=100):
        keys_to_search = [f"{i}" for i in np.random.randint(1, 101, n_searches)]

        # Métricas
        time_without_cache = 0
        time_with_cache = 0
        avoided_json_lookups = 0

        count = 0
        for key in keys_to_search:
            # clear console
            count += 1
            print("\033[H\033[J")
            print(f"Searching : {count}/{n_searches}")
            start_time = time.time()
            time_without_cache += 3 + 0.001  # Estimado de tiempo de búsqueda en JSON
            self.get(key)
            elapsed_time = time.time() - start_time
            time_with_cache += elapsed_time

            if elapsed_time < 1:
                avoided_json_lookups += 1

        time_saved = time_without_cache - time_with_cache
        print(f"\nTime saved thanks to cache: {time_saved:.2f} seconds")
        print(f"Number of times JSON lookup was avoided: {avoided_json_lookups}")

# La implementación del resto de los métodos y el código principal permanecerían esencialmente iguales.

if __name__ == '__main__':
    client = CacheClient()

    while True:
        print("\nChoose an operation:")
        print("1. Get")
        print("2. Simulate Searches")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            key = input("Enter key: ")
            value = client.get(key)
            if value is not None:
                print(f"Value: {value}")
        elif choice == "2":
            n_searches = int(input("Enter the number of searches you want to simulate: "))
            client.simulate_searches(n_searches)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
