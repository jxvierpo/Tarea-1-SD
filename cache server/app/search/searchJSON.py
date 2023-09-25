import grpc
import json
import time
import numpy as np
import cache_service_pb2
import cache_service_pb2_grpc
from find_car_by_id import find_car_by_id

class CacheClient:
    def __init__(self, host="master", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        

    def get(self, key, simulated=False):
        start_time = time.time()  # Inicio del temporizador

        if not simulated:
            # Simulamos un retraso aletorio de 1 a 3 segundos, con una distribución normal en 2
            delay = np.random.normal(2, 0.5)
            print(f"Waiting {delay:.5f} seconds...")
            time.sleep(delay)

        # busca en el JSON
        value = find_car_by_id(int(key))
        value = str(value)
        if value:
            print("Key found in JSON.")
                
                
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            print(f"Time taken (JSON + delay): {elapsed_time:.5f} seconds")          
            return value
        else:
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            print(f"Time taken: {elapsed_time:.5f} seconds")
            print("Key not found.")
            return None
            
    def simulate_searches(self, n_searches=100):
        keys_to_search = [f"{i}" for i in np.random.randint(1, 101, n_searches)]
        search_times = []  # Lista para almacenar los tiempos individuales de búsqueda

        # Métricas
        time_without_cache = 0
        

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
            search_times.append(elapsed_time)

        average_search_time = sum(search_times) / len(search_times) if search_times else 0  # Calcula el tiempo medio de búsqueda
        std_dev_search_time = np.std(search_times) if search_times else 0  # Desviación estándar del tiempo de búsqueda
                
        print(f"\nTotal time taken (JSON only): {time_without_cache:.2f} seconds")
        print(f"Average search time: {average_search_time:.5f} seconds")
        print(f"Standard deviation of search time: {std_dev_search_time:.5f} seconds")
        

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