"""Clase para creacion y administracion de un hotel.
    """
import json
import os


class Hotel:
    """Clase para representar un hotel.
    Esta clase contiene información sobre el hotel, como su nombre,
    la lista de habitaciones disponibles, las reservas realizadas, etc.
    """
    def __init__(self, name, location, rooms, reservations=None):
        """Inicializa una nueva instancia de la clase Hotel.
        """
        self.name = name
        self.location = location
        self.rooms = rooms
        self.reservations = reservations if reservations is not None else []

    def to_dict(self):
        """Conversion de un objeto a Diccionario.
        """
        return {
            "name": self.name,
            "location": self.location,
            "rooms": [room.to_dict() for room in self.rooms],
            "reservations": [reservation.to_dict()
                             for reservation in self.reservations]
        }

    @classmethod
    def from_dict(cls, data):
        """Inicializa de objetos apartir de diccionarios.
        """
        rooms = [Room(**room_data) for room_data in data['rooms']]
        reservations = [Reservation(**reservation_data)
                        for reservation_data in data.get('reservations', [])]
        return cls(data['name'], data['location'], rooms, reservations)


class Room:
    """Clase para representar una habitacion.
    Esta clase contiene información sobre la habitacion, como su capacidad,
    precio, numero de habitacion y tipo.
    """
    def __init__(self, number, room_type, capacity, price):
        """Inicializa una nueva instancia de la clase Room.
        """
        self.number = number
        self.room_type = room_type
        self.capacity = capacity
        self.price = price

    def to_dict(self):
        """Conversion de un objeto a Diccionario.
        """
        return {
            "number": self.number,
            "room_type": self.room_type,
            "capacity": self.capacity,
            "price": self.price
        }

    def __str__(self):
        """Objeto room to String.
        """
        return f"Habitación {self.number}: Tipo {self.room_type},\
              Capacidad {self.capacity}, Precio {self.price}"


class Reservation:
    """Clase para representar una reservacion.
    Esta clase contiene información sobre la reservacion, hotel
    habitacion, huesped.
    """
    def __init__(self, reservation_id, hotel, room, guest_name):
        """Inicializa una nueva instancia de la clase Reservation.
        """
        self.reservation_id = reservation_id
        self.hotel = hotel
        self.room = room
        self.guest_name = guest_name

    def to_dict(self):
        """Conversion de un objeto a Diccionario.
        """
        room_data = self.room.to_dict() if isinstance(self.room, Room)\
            else self.room
        return {
            "reservation_id": self.reservation_id,
            "hotel": {
                "name": self.hotel.name,
                "location": self.hotel.location
            },
            "room": room_data,
            "guest_name": self.guest_name
        }


class HotelManager:
    """Clase para representar la adminstracion del Hotel.
    """
    def __init__(self, filename):
        """Inicializa una nueva instancia de la clase Hotel Manager.
        """
        self.filename = filename
        self.hotels = self.load_hotels()
        self.reservations = []

    def load_hotels(self):
        """Metodo que abre el archivo Json con la informacion  guardada.
        """
        hotels = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                hotels_data = json.load(file)
                for hotel_data in hotels_data:
                    hotel = Hotel.from_dict(hotel_data)
                    hotels.append(hotel)
        return hotels

    def save_hotels(self):
        """Metodo que almacena Hoteles.
        """
        hotels_data = []
        for hotel in self.hotels:
            hotel_data = hotel.to_dict()
            hotel_data["reservations"] = [reservation.to_dict() for reservation in hotel.reservations]
            hotels_data.append(hotel_data)

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(hotels_data, file, indent=4)

    def create_hotel(self, name, location):
        """Metodo que crea un hotel.
        """
        hotel = Hotel(name, location, [])
        self.hotels.append(hotel)
        self.save_hotels()
        return hotel

    def display_all_hotels(self):
        """Metodo que consulta todos los hoteles.
        """
        for index, hotel in enumerate(self.hotels, start=1):
            print(f"{index}. {hotel.name} ({hotel.location})")

    def delete_hotel(self, index):
        """Metodo que elimina un hotel.
        """
        if 0 < index <= len(self.hotels):
            del self.hotels[index - 1]
            self.save_hotels()
            print("Hotel eliminado exitosamente.")
        else:
            print("Índice de hotel inválido.")

    def search_hotels_by_location(self, location):
        """Metodo que consulta hoteles por location.
        """
        found_hotels = [hotel for hotel in self.hotels if hotel.location == location]
        return found_hotels

    def get_hotel_by_index(self, index):
        """Metodo que consulta hoteles por index.
        """
        return self.hotels[index - 1]

    def create_reservation(self, hotel, room, guest_name):
        """Metodo que crea una reserbacion.
        """
        existing_reservation = self.find_reservation(hotel, room)
        if existing_reservation:
            print("Ya existe una reserva para esta habitación.")
            return existing_reservation
        else:
            reservation_id = len(hotel.reservations) + 1
            reservation = Reservation(reservation_id, hotel, room, guest_name)
            hotel.reservations.append(reservation)
            self.save_hotels()
            return reservation

    def find_reservation(self, hotel, room):
        """Metodo que consulta una reservacion.
        """
        for reservation in hotel.reservations:
            if reservation.room == room:
                return reservation
        return None

    def search_reservations_by_hotel(self, hotel):
        """Metodo que consulta reservacion por hotel.
        """
        return [reservations for reservations in hotel.reservations]

    def search_reservation_by_id(self, reservation_id):
        """Metodo que consulta reservaciones por id.
        """
        for hotel in self.hotels:
            for reservation in hotel.reservations:
                if reservation.reservation_id == reservation_id:
                    return reservation
        return None


class RoomManager:
    """Clase para representar la Administracion de una Habitacion.
    """
    def __init__(self):
        """Inicializa una nueva instancia de la clase Room Manager.
        """
        self.rooms = []

    def create_room(self, hotel_manager, hotel, number, room_type, capacity, price):
        """Metodo que crea una habitacion.
        """
        room = Room(number, room_type, capacity, price)
        hotel.rooms.append(room)
        hotel_manager.save_hotels()
        return room

    def search_rooms_by_hotel(self, hotel):
        """Metodo que consulta una habitacion por hotel.
        """
        return hotel.rooms

    def search_rooms_by_hotel_and_type(self, hotel, room_type):
        """Metodo que consulta una habitacion por hotel y tipo.
        """
        found_rooms = [room for room in hotel.rooms if room.room_type == room_type]
        return found_rooms

    def search_rooms_by_hotel_type_and_price(self, hotel, room_type, max_price):
        """Metodo que consulta una habitacion por hotel tipo y precio.
        """
        found_rooms = [room for room in hotel.rooms if room.room_type == room_type and room.price <= max_price]
        return found_rooms

    def display_all_rooms(self, hotel):
        """Metodo que consulta todas las habitaciones por hotel.
        """
        print(f"Habitaciones del hotel {hotel.name}:")
        for room in hotel.rooms:
            print(f"Número: {room.number}, Tipo: {room.room_type},  \
                  Capacidad: {room.capacity}, Precio: {room.price}")

    def get_room_by_number(self, hotel, room_number):
        """Metodo que consulta habitaciones por numero.
        """
        for room in hotel.rooms:
            if room.number == room_number:
                return room
        return None


def main():
    """
    Función principal que ejecuta el programa.
    """
    hotel_manager = HotelManager("hotels.json")
    room_manager = RoomManager()

    while True:
        print("\nMenú de opciones:")
        print("1. Crear hotel")
        print("2. Mostrar todos los hoteles")
        print("3. Buscar hoteles por ubicación")
        print("4. Eliminar hotel")
        print("5. Crear habitación")
        print("6. Buscar habitaciones por hotel")
        print("7. Buscar habitaciones por hotel y tipo")
        print("8. Buscar habitaciones por hotel, tipo y precio")
        print("9. Crear reserva")
        print("10. Buscar reservaciones por hotel")
        print("11. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            name = input("Ingrese el nombre del hotel: ")
            location = input("Ingrese la ubicación del hotel: ")
            hotel = hotel_manager.create_hotel(name, location)
            print(f"Hotel '{hotel.name}' creado exitosamente en '{hotel.location}'.")

        elif choice == "2":
            print("\nLista de hoteles:")
            hotel_manager.display_all_hotels()

        elif choice == "3":
            location = input("Ingrese la ubicación a buscar: ")
            found_hotels = hotel_manager.search_hotels_by_location(location)
            if found_hotels:
                print("\nHoteles encontrados:")
                for hotel in found_hotels:
                    print(f"- {hotel.name} ({hotel.location})")
            else:
                print("No se encontraron hoteles en esa ubicación.")

        elif choice == "4":
            hotel_manager.display_all_hotels()
            index = input("Seleccione el número del hotel a eliminar: ")
            hotel_manager.delete_hotel(int(index))

        elif choice == "5":
            hotel_manager.display_all_hotels()
            index = int(input("Seleccione el número del hotel para agregar la habitación: "))
            hotel = hotel_manager.get_hotel_by_index(index)
            if hotel:
                number = input("Ingrese el número de la habitación: ")
                room_type = input("Ingrese el tipo de habitación: ")
                capacity = int(input("Ingrese la capacidad de la habitación: "))
                price = float(input("Ingrese el precio de la habitación por noche: "))
                room = room_manager.create_room(hotel_manager, hotel, number, room_type, capacity, price)
                print(f"Habitación {room.number} creada exitosamente.")
            else:
                print("Hotel no encontrado.")

        elif choice == "6":
            hotel_manager.display_all_hotels()
            index = int(input("Seleccione el número del hotel para buscar habitaciones: "))
            hotel = hotel_manager.get_hotel_by_index(index)
            if hotel:
                found_rooms = room_manager.search_rooms_by_hotel(hotel)
                if found_rooms:
                    print("\nHabitaciones encontradas:")
                    for room in found_rooms:
                        print(room)
                else:
                    print("No se encontraron habitaciones para este hotel.")
            else:
                print("Hotel no encontrado.")

        elif choice == "7":
            hotel_manager.display_all_hotels()
            index = int(input("Seleccione el número del hotel para buscar habitaciones: "))
            hotel = hotel_manager.get_hotel_by_index(index)
            if hotel:
                room_type = input("Ingrese el tipo de habitación a buscar: ")
                found_rooms = room_manager.search_rooms_by_hotel_and_type(hotel, room_type)
                if found_rooms:
                    print("\nHabitaciones encontradas:")
                    for room in found_rooms:
                        print(room)
                else:
                    print("No se encontraron habitaciones de ese tipo para este hotel.")
            else:
                print("Hotel no encontrado.")

        elif choice == "8":
            hotel_manager.display_all_hotels()
            index = int(input("Seleccione el número del hotel para buscar habitaciones: "))
            hotel = hotel_manager.get_hotel_by_index(index)
            if hotel:
                room_type = input("Ingrese el tipo de habitación a buscar: ")
                max_price = float(input("Ingrese el precio máximo por noche: "))
                found_rooms = room_manager.search_rooms_by_hotel_type_and_price(hotel, room_type, max_price)
                if found_rooms:
                    print("\nHabitaciones encontradas:")
                    for room in found_rooms:
                        print(room)
                else:
                    print("No se encontraron habitaciones de ese tipo y precio para este hotel.")
            else:
                print("Hotel no encontrado.")

        if choice == "9":
            hotel_manager.display_all_hotels()
            hotel_index = int(input("Seleccione el número del hotel: "))
            hotel = hotel_manager.get_hotel_by_index(hotel_index)
            if hotel:
                room_manager.display_all_rooms(hotel)
                room_number = input("Ingrese el número de la habitación: ")
                room = room_manager.get_room_by_number(hotel, room_number)
                if room:
                    guest_name = input("Ingrese el nombre del huésped: ")
                    reservation = hotel_manager.create_reservation(hotel, room, guest_name)
                    print(f"Reserva creada con éxito. ID de reserva: {reservation.reservation_id}")
                else:
                    print("¡Habitación no encontrada!")
            else:
                print("¡Hotel no encontrado!")

        elif choice == "10":
            hotel_manager.display_all_hotels()
            hotel_index = int(input("Seleccione el número del hotel: "))
            hotel = hotel_manager.get_hotel_by_index(hotel_index)
            if hotel:
                reservations = hotel_manager.search_reservations_by_hotel(hotel)
                if reservations:
                    print("\nReservaciones encontradas:")
                    for reservation in reservations:
                        print(f"ID: {reservation.reservation_id},  \
                              Huésped: {reservation.guest_name}")
                else:
                    print("No se encontraron reservaciones para este hotel.")
            else:
                print("¡Hotel no encontrado!")

        elif choice == "11":
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
