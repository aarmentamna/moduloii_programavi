import unittest
from hotel import HotelManager, RoomManager


class TestHotel(unittest.TestCase):

    def test_load_hotels(self):
        # Configura el entorno de prueba
        self.hotel_manager = HotelManager("test_hotels.json")
        self.assertIsNotNone(self.hotel_manager.load_hotels())

    def test_create_hotel(self):
        # Configura el entorno de prueba
        self.hotel_manager = HotelManager("test_hotels.json")
        hotel_name = "Hotel Test"
        hotel_location = "Location Test"
        created_hotel = self.hotel_manager.create_hotel(hotel_name, hotel_location)
        self.assertIsNotNone(created_hotel)
        self.assertEqual(created_hotel.name, hotel_name)
        self.assertEqual(created_hotel.location, hotel_location)

    def test_display_all_hotels(self):
        # Configura el entorno de prueba
        self.hotel_manager = HotelManager("test_hotels.json")
        self.assertIsNone(self.hotel_manager.display_all_hotels())

    def test_search_hotels_by_location(self):
        # Configura el entorno de prueba
        self.hotel_manager = HotelManager("test_hotels.json")
        hotel_location = "Location Test"
        # Llama al método search_hotels_by_location usando la instancia de HotelManager
        found_hotels = self.hotel_manager.search_hotels_by_location(hotel_location)

        # Verifica que se hayan encontrado hoteles correctamente
        self.assertIsNotNone(found_hotels)
        self.assertTrue(isinstance(found_hotels, list))

    def test_get_hotel_by_index(self):
        # Configura el entorno de prueba
        self.hotel_manager = HotelManager("test_hotels.json")
        hotel_index = 1
        # Llama al método search_hotels_by_location usando la instancia de HotelManager
        found_hotels = self.hotel_manager.get_hotel_by_index(hotel_index)

        # Verifica que se hayan encontrado hoteles correctamente
        self.assertIsNotNone(found_hotels)

    def test_create_room(self):
        self.hotel_manager = HotelManager("test_hotels.json")
        self.room_manager = RoomManager()
        hotel_number = 1
        hotel_type = "Luxury"
        hotel_capacity = 3
        hotel_price = 4800
        hotel_index = 1
        # Llama al método search_hotels_by_location usando la instancia de HotelManager
        found_hotels = self.hotel_manager.get_hotel_by_index(hotel_index)
        room = self.room_manager.create_room(
            self.hotel_manager,  # instancia de HotelManager
            found_hotels,  # hotel en el que se creará la habitación
            hotel_number,  # número de la habitación
            hotel_type,  # tipo de la habitación
            hotel_capacity,  # capacidad de la habitación
            hotel_price  # precio de la habitación
        )

        self.assertIsNotNone(room)
        self.assertEqual(room.number, hotel_number)
        self.assertEqual(room.room_type, hotel_type)
        self.assertEqual(room.capacity, hotel_capacity)
        self.assertEqual(room.price, hotel_price)

    def test_search_rooms_by_hotel(self):
        self.hotel_manager = HotelManager("test_hotels.json")
        self.room_manager = RoomManager()
        hotel_index = 1
        # Llama al método search_hotels_by_location usando la instancia de HotelManager
        found_hotels = self.hotel_manager.get_hotel_by_index(hotel_index)
        rooms = self.room_manager.search_rooms_by_hotel(found_hotels)
        self.assertIsNotNone(rooms)

    def test_search_rooms_by_hotel_and_type(self):
        room_type = "Luxury"
        self.hotel_manager = HotelManager("test_hotels.json")
        self.room_manager = RoomManager()
        hotel_index = 1
        # Llama al método search_hotels_by_location usando la instancia de HotelManager
        found_hotels = self.hotel_manager.get_hotel_by_index(hotel_index)
        rooms = self.room_manager.search_rooms_by_hotel_and_type(found_hotels, room_type)
        self.assertIsNotNone(rooms)

    def test_search_rooms_by_hotel_type_and_price(self):
        room_type = "Luxury"
        room_price = 4800
        self.hotel_manager = HotelManager("test_hotels.json")
        self.room_manager = RoomManager()
        hotel_index = 1
        # Llama al método search_hotels_by_location usando la instancia de HotelManager
        found_hotels = self.hotel_manager.get_hotel_by_index(hotel_index)
        rooms = self.room_manager.search_rooms_by_hotel_type_and_price(found_hotels, room_type, room_price)
        self.assertIsNotNone(rooms)

    def test_display_all_rooms(self):
        self.hotel_manager = HotelManager("test_hotels.json")
        self.room_manager = RoomManager()
        hotel_index = 1
        # Llama al método search_hotels_by_location usando la instancia de HotelManager
        found_hotels = self.hotel_manager.get_hotel_by_index(hotel_index)
        self.room_manager.display_all_rooms(found_hotels)

    def test_get_room_by_number(self):
        self.hotel_manager = HotelManager("test_hotels.json")
        self.room_manager = RoomManager()
        hotel_index = 1
        room_number = 1
        # Llama al método search_hotels_by_location usando la instancia de HotelManager
        found_hotels = self.hotel_manager.get_hotel_by_index(hotel_index)
        room_exist = self.room_manager.get_room_by_number(found_hotels, room_number)
        self.assertIsNotNone(room_exist)


if __name__ == '__main__':
    unittest.main()
