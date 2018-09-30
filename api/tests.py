from django.test import TestCase
from .models import *

# Create your tests here.
class SeatTestCase(TestCase):
    def setUp(self):
        for n in range(1, 10):
            for ch in ['A', 'B', 'C', 'D', 'E', 'F']:
                seat = Seat(number=str(n)+ch)
                seat.save()
    
    def test_next_seat(self):
        seat = Seat.objects.get(number='1C')
        self.assertEqual(seat.next_seat().number, '2A')
        seat = Seat.objects.get(number='1D')
        self.assertEqual(seat.next_seat().number, '1E')

    def test_prev_seat(self):
        seat = Seat.objects.get(number='9F')
        self.assertEqual(seat.prev_seat().number, '9E')
        seat = Seat.objects.get(number='9A')
        self.assertEqual(seat.prev_seat().number, '8C')

class InterestGroupTestCase(TestCase):
    def setUp(self):
        for n in range(1, 10):
            for ch in ['A', 'B', 'C', 'D', 'E', 'F']:
                seat = Seat(number=str(n)+ch)
                seat.save()

    def test_get_seats(self):
        seats = InterestGroup.get_seats(['a', 'b', 'c'], 2)
        print(seats)
        seats = InterestGroup.get_seats(['a', 'd', 'e'], 2)
        print(seats)
        seats = InterestGroup.get_seats(['a', 'c', 'd'], 1)
        print(seats)
        seats = InterestGroup.get_seats(['a', 'b', 'c'], 1)
        print(seats)
        seats = InterestGroup.get_seats(['a', 'd', 'e'], 1)
        print(seats)
