import Leap

class LeapEventListener(Leap.Listener):
    def __init__(self):
        self.LeftHandHandler = None
        self.RightHandHandler = None        
        super(LeapEventListener, self).__init__()

    def on_connect(self, controller): 
        print "Connected"               
        
        
    def on_disconnect(self, controller):
        pass
        # Note: not dispatched when running in a debugger.
        #sys.stderr.writeln("Disconnected\r\n");

    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty:
            for hand in frame.hands:
                if hand.is_left:
                    if self.LeftHandHandler != None:
                        self.LeftHandHandler(hand)
                else:
                    if self.RightHandHandler != None:
                        self.RightHandHandler(hand)
class HandProcessor:
    
    def __init__(self):
        self.listener = LeapEventListener() 
        self.controller = Leap.Controller()
        #self.controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    def run(self):       
        self.controller.add_listener(self.listener)

    def attachLeftEventHandler(self, handler):
        self.listener.LeftHandHandler = handler;

    def attachRightEventHandler(self, handler):
        self.listener.RightHandHandler = handler;

    



    