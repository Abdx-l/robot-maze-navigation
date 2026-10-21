; HCS12 control-loop scaffold. Board-specific I/O addresses are placeholders.
; Bits in SENSOR_PORT: 0 front wall, 1 left wall, 2 right wall.
; Motor codes: 0 stop, 1 forward, 2 left pivot, 3 right pivot, 4 reverse.
; A real board must wait for completed turns and debounce sensor input.
SENSOR_PORT EQU $1000
MOTOR_PORT  EQU $1001
GOAL_PORT   EQU $1002
STOP_CMD    EQU $00
FWD_CMD     EQU $01
LEFT_CMD    EQU $02
RIGHT_CMD   EQU $03
REVERSE_CMD EQU $04

            ORG $2000
START       LDS #$3FFF
LOOP        LDAA GOAL_PORT
            BITA #$01
            BNE DONE
            LDAA SENSOR_PORT
            BITA #$02
            BEQ TURN_LEFT
            BITA #$01
            BEQ GO_FORWARD
            BITA #$04
            BEQ TURN_RIGHT
            LDAA #REVERSE_CMD
            STAA MOTOR_PORT
            BRA LOOP
TURN_LEFT   LDAA #LEFT_CMD
            STAA MOTOR_PORT
            BRA LOOP
GO_FORWARD  LDAA #FWD_CMD
            STAA MOTOR_PORT
            BRA LOOP
TURN_RIGHT  LDAA #RIGHT_CMD
            STAA MOTOR_PORT
            BRA LOOP
DONE        LDAA #STOP_CMD
            STAA MOTOR_PORT
            BRA DONE

