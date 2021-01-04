class Constants:
    LIGHT_OFF_PWM_VAL = 0.0
    LIGHT_DIM_PWM_VAL = 0.02
    LIGHT_BRIGHT_PWM_VAL = 1.0
    LIGHT_BLINK_DURATION_NS = pow(10, 9) / 2
    MOTOR_REV_GEAR_CHANGE_THROTTLE = -0.12
    MOTOR_REV_GEAR_CHANGE_DURATION_Secs = 0.04

    GPIO_PIN_I2C_SDA = 2                        #do not modify
    GPIO_PIN_I2C_SCL = 3                        #do not modify
    GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER = 12   #do not modify
    GPIO_PIN_STEERING_SERVO = 13                #do not modify

    # GPIO_PIN_HEADLIGHTS = 2
    # GPIO_PIN_FOGLIGHTS = 14
    # GPIO_PIN_LEFT_TURNSIGNAL = 4
    # GPIO_PIN_RIGHT_TURNSIGNAL = 3
    #
    # GPIO_PIN_LEFT_TAILLIGHT = 27
    # GPIO_PIN_RIGHT_TAILLIGHT = 17
    # GPIO_PIN_REVERSE_LIGHTS = 22

