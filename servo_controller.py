import time
import Adafruit_PCA9685


class ServoController:
    
    """
    Winkel: 0-180°
    Tastverhältnis = Ausgang 5V / (Ausgang 5V + Ausgang 0)  <-- Nenner ist quasi Periodendauer
    Frequenz 50Hz --> eine Periode des Signals dauert 20ms 
    Tastverhältnis == Duty cycle

    2% Tastverhältnis 0° --> 0.4 ms Signallänge
    7% Tastverhältnis 90°--> 1.4 ms Signallänge
    11% Tastverhältnis 180° --> 2.2 ms Signallänge

    """

    def __init__(self, channel=7, frequency=50, homing_angle=90):
        self.channel = channel
        self.frequency = frequency
        self.homing_angle = homing_angle
        self.current_angle = self.homing_angle
        
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.frequency)


    def get_signal_length_for_degree(self, degree):
        """Returns signal length ins seconds."""
        # if not 0 <= degree <= 180: raise ValueError("Degree must be between 0 and 180°!")
        
        lower_bound =0.4e-3
        upper_bound =2.33e-3
        
        return lower_bound + (upper_bound - lower_bound)*degree/180 

    
    def move_servo_to_degree(self, degree):
        if degree == self.current_angle: return

        delta = abs(self.current_angle - degree)
        steps_per_degree = 6


        if degree > self.current_angle:
            #move in positive angle direction
            for i in range(self.current_angle*steps_per_degree, degree*steps_per_degree+1):
                self.pwm.set_pwm(
                    self.channel,
                    0,
                    int(4096*self.frequency * self.get_signal_length_for_degree(i/steps_per_degree))
                )
                time.sleep(.001)
        else:
            #move in negative angle direction
            for i in range(self.current_angle*steps_per_degree, degree*steps_per_degree, -1):
                self.pwm.set_pwm(
                    self.channel,
                    0,
                    int(4096*self.frequency * self.get_signal_length_for_degree(i/steps_per_degree))
                )
                time.sleep(.001)
        
        self.current_angle = degree

        
    
    def perform_homing(self):
        self.move_servo_to_degree(self.homing_angle)
    
    
    def run(self):
        self.move_servo_to_degree(0,self.channel)

        time.sleep(3)

        desired_angle = 180
        steps_per_degree = 4 

        for i in range(desired_angle * steps_per_degree + 1):
            self.move_servo_to_degree(i/steps_per_degree,self.channel)
            time.sleep(.001)





if __name__ == "__main__":
    controller = ServoController(channel=0)
    # controller.run()

    while True:
        try:
            value = input("Enter new angle or any other key to switch servo:\n")
            angle = int(value)

            controller.move_servo_to_degree(angle)

        except ValueError:
            value = input("Which servo do you want to choose? Pick between 0,1 and 7\n")
            servo = int(value)
            if servo in [0,1,7]:
                controller.channel = servo


        except KeyboardInterrupt:
            controller.perform_homing()
            break

    

        
        

    # controller.run()#