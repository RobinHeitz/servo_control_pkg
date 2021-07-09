#!/usr/bin/env python
#-*- coding:UTF-8 -*-(add)

import time
import Adafruit_PCA9685

class ServoControllerFinishedMovementException(Exception):
    pass

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

    def __init__(self, frequency=50, homing_angle=90):
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

    
    def move_servo_to_degree(self, goal_degree, channel):

        def _set_pwm(angle, channel):
            self.pwm.set_pwm(
                    channel,
                    0,
                    int(4096*self.frequency * self.get_signal_length_for_degree(angle))
                )
            time.sleep(.01)


        if goal_degree == self.current_angle: return

        increment = 0.4
        cur_angle = self.current_angle


        if goal_degree > self.current_angle:
            #move in positive angle direction

            while cur_angle <= goal_degree:
                cur_angle += increment
                _set_pwm(cur_angle, channel)
        else:
            #move in negative angle direction
            while cur_angle >= goal_degree:
                cur_angle -= increment
                _set_pwm(cur_angle, channel)
        

        self.current_angle = cur_angle
        raise ServoControllerFinishedMovementException("Finished Movement for servo at channel {} with goal of {} degrees.".format(channel, self.current_angle))

        
    
    def perform_homing(self):
        self.move_servo_to_degree(self.homing_angle)
    

if __name__ == "__main__":
    controller = ServoController(channel=0)

    def switch_channel():
        value = input("Which servo do you want to choose? Pick between 0,1 and 7\n")
        servo = int(value)
        if servo in [0,1,7]:
            controller.channel = servo



    while True:
        try:
            value = input("Enter new angle or any other key to switch servo:\n")
            angle = int(value)

            controller.move_servo_to_degree(angle)
        
        except ServoControllerFinishedMovementException as e:
            print(e)

        except NameError:
           switch_channel()

        except ValueError:
           switch_channel()





        except KeyboardInterrupt:
            controller.perform_homing()
            break
