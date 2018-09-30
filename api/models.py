from django.db import models

# Create your models here.
class Interest(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class InterestGroup(models.Model):
    interests = models.ManyToManyField(Interest)
    start_seat = models.ForeignKey('Seat', on_delete=models.CASCADE, related_name='start_seat')
    end_seat = models.ForeignKey('Seat', on_delete=models.CASCADE, related_name='end_seat')

    def add_to_interest_group(self, interests, seats):
        for i in interests:
            interest, created = Interest.objects.get_or_create(name=i)
            self.interests.add(interest)
        if max([seat.number for seat in seats]) > self.end_seat.number:
            self.end_seat = Seat.objects.get(number=max([seat.number for seat in seats]))
        elif min([seat.number for seat in seats]) < self.start_seat.number:
            self.start_seat =  Seat.objects.get(number=min([seat.number for seat in seats]))
        interest.save()

    def find_matches(self, interests):
        match = 0
        for i in interests:
            if i in [interest.name for interest in self.interests.all()]:
                match += 1
        return match            

    def check_if_next_seats_are_empty(self, number_of_seats):
        seat = self.end_seat.next_seat()
        for n in range(number_of_seats):
            if seat.is_booked == True:
                return False
            seat = seat.next_seat()
        return True

    def check_if_prev_seats_are_empty(self, number_of_seats):
        seat = self.start_seat.next_seat()
        for n in range(number_of_seats):
            if seat.is_booked == True:
                return False
            seat = seat.prev_seat()
        return True

    @staticmethod
    def find_most_compatible(interests, number_of_seats):
        interest_groups = InterestGroup.objects.all()
        max_matches = 1
        max_matched_interest_group = None
        for ig in interest_groups:
            matches = ig.find_matches(interests)
            if matches > max_matches and (ig.check_if_next_seats_are_empty(number_of_seats) \
            or ig.check_if_prev_seats_are_empty(number_of_seats)):
                max_matches =  matches
                max_matched_interest_group = ig
        return max_matched_interest_group

    @staticmethod
    def get_seats(interests, number_of_seats):
        ig = InterestGroup.find_most_compatible(interests, number_of_seats)
        seats = []
        if ig is None:
            if not Seat.objects.get(number='1A').is_booked:
                s = Seat.objects.get(number='1A')
                for n in range(number_of_seats):
                    seats.append(s)
                    s = s.next_seat()
            elif not Seat.objects.get(number='1D').is_booked:
                s = Seat.objects.get(number='1D')
                for n in range(number_of_seats):
                    seats.append(s)
                    s = s.next_seat()
            elif not Seat.objects.get(number='9C').is_booked:
                s = Seat.objects.get(number='9C')
                for n in range(number_of_seats):
                    seats.append(s)
                    s = s.prev_seat()
            elif not Seat.objects.get(number='9F').is_booked:
                s = Seat.objects.get(number='9F')
                for n in range(number_of_seats):
                    seats.append(s)
                    s = s.prev_seat()
            ig = InterestGroup(start_seat=(seats[0] if seats[0].number < seats[-1].number else seats[-1]), \
            end_seat=(seats[0] if seats[0].number > seats[-1].number else seats[-1]))
            ig.save()
            for interest in interests:
                interest, created = Interest.objects.get_or_create(name=interest)
                ig.interests.add(interest)
        else:
            if ig.check_if_next_seats_are_empty(number_of_seats):
                s = ig.end_seat
                for n in range(number_of_seats):
                    s = s.next_seat()
                    seats.append(s)
            else:
                s =ig.prev_seat
                for n in range(number_of_seats):
                    s = s.prev_seat()
                    seats.append(s)
            ig.add_to_interest_group(interests, seats)
        
        ig.save()
        for seat in seats:
            seat.book()
            seat.save()
        return seats

class Seat(models.Model):
    number = models.CharField(max_length=4)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.number

    def book(self):
        self.is_booked = True
        self.save()

    def next_seat(self):
        seat_number = list(self.number)
        if self.number[-1] != 'C' and self.number[-1] != 'F':
            seat_number[-1] = chr(ord(self.number[-1]) + 1) 
        elif self.number[-1] == 'C' or self.number[-1] == 'F':
            seat_number[-1] = chr(ord(self.number[-1]) - 2)
            seat_number[-2] = chr(ord(self.number[-2]) + 1) 
        seat_number = "".join(seat_number)
        return Seat.objects.get(number=seat_number)

    def prev_seat(self):
        seat_number = list(self.number)
        if self.number[-1] != 'A' and self.number[-1] != 'D':
            seat_number[-1] = chr(ord(self.number[-1]) - 1) 
        else:
            seat_number[-1] = chr(ord(self.number[-1]) + 2) 
            seat_number[-2] = chr(ord(self.number[-2]) - 1) 
        seat_number = "".join(seat_number)
        return Seat.objects.get(number=seat_number)
        

    



