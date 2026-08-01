# Classes Lab: Build a Planet Class and fulfill user stories
class Planet:
    def __init__(self, name, planet_type, star):
        self.name = name
        self.planet_type = planet_type
        self.star = star

        if not isinstance(self.name, str) or not isinstance(self.planet_type, str) or not isinstance(self.star, str):
            print(f"{self.name}, {self.planet_type}, and {self.star} must be strings")
            raise TypeError(f"name, planet type, and star must be strings")

        elif not self.name or not self.planet_type or not self.star:
            print(f"{self.name}, {self.planet_type}, and {self.star} must be non-empty strings")
            raise ValueError(f"name, planet_type, and star must be non-empty strings")
    
    def __str__(self):
        return f"Planet: {self.name} | Type: {self.planet_type} | Star: {self.star}"
        
    def orbit(self):
        return f"{self.name} is orbiting around {self.star}..."

'''    
planet_1 = Planet("mercury", "terrestrial", "Sun")
planet_2 = Planet("mars", "terrestrial", "Sun")
planet_3 = Planet("Earth", "terrestrial", "Sun")

print(planet_1)
print(planet_2)
print(planet_3)

print(planet_1.orbit())
print(planet_2.orbit())
print(planet_3.orbit())
'''
