import Leap;


class HandProcessor:
    def __init__():
        self.controller = Leap.Controller()
        listener = LeapEventListener()
        listener.LeftHandHandler = LeftHandHandler
        listener.RightHandHandler = RightHandHandler
        controller.add_listener(listener)

    def LeftHandHandler(hand):
        print "Lefthand: ", hand.palm_position

    def RightHandHandler(hand):
        print "Righthand: ", hand.palm_position

    class LeapEventListener(Leap.Listener):

        def __init__():
            self.LeftHandHandler = None
            self.RightHandHandler = None

        def on_connect(self, controller):                
            controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
            
        def on_disconnect(self, controller):
            # Note: not dispatched when running in a debugger.
            print "Disconnected"

        def on_frame(self, controller):
            print "Frame available"
            frame = controller.frame()
            if not frame.hands.is_empty:
                for hand in frame.hands:
                    if hand.is_left:
                        LeftHandHandler(hand)
                    else:
                        RightHandHandler(hand)