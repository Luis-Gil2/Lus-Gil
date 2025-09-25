class Temperature():
    def __init__(self):
        self.temperatures = []
    def _add_temperature(self,temp):
        self.temperatures.append(temp)
    
    def _average_temperature(self):
        return round((sum(self.temperatures) / len(self.temperatures)), 2)
    
    def _get_max_temperature(self):
        return max(self.temperatures)
    
    def _get_min_temperature(self):
        return min(self.temperatures)
    
    def _above_average(self):
        average = self._average_temperature()
        above_average = [temp for temp in self.temperatures if temp > average]
        return  len(above_average)
    
    def _add_week_temperature(self):
        for _ in range(7):
            temp = round(float(input("Ingrese la temperatura (ejemplo 10): ")), 2)
            self._add_temperature(temp)

    def _get_info(self):
        print(f"Temperatura promedio: {self._average_temperature()}")
        print(f"Temperatura maxima: {self._get_max_temperature()}")
        print(f"Temperatura minima: {self._get_min_temperature()}")
        print(f"Dias con temperaturas mayores al promedio: {self._above_average()}")
    
    def main(self):
        self._add_week_temperature()
        self._get_info()

merida_week_temperatures = Temperature()
merida_week_temperatures.main()