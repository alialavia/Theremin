import Leap
from numpy import pi
from helpers import cutoff
palm_offset = -60.0
palm_gain = 2.0

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

""" Dispatches left hand and right hand events """
class HandProcessor(object):
    
    def __init__(self):
        self.listener = LeapEventListener() 
        self.controller = Leap.Controller()
        self.controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    def run(self): 
        self.controller.add_listener(self.listener)

    def attachLeftEventHandler(self, handler):
        self.listener.LeftHandHandler = handler;

    def attachRightEventHandler(self, handler):
        self.listener.RightHandHandler = handler;


""" Gets a hand object and store and convert its attributes of interest """
class HandState(object):
    
    def __init__(self, hand):
        self.__hand__ = hand        
        self.PalmPosition = self.findHighestFinger()
        self.Pinch = self.findPinch()
        self.PalmState = self.findPalmState()

    """ Get the hand object assigned to this object """
    def getHand(self):
        return self.__hand__

    """ Find the pinching finger. Returns -1 if no pinch is found """
    def findPinch(self):
        
        iterfingers = iter(self.__hand__.fingers)
        thumb = self.__hand__.fingers[0]
        thumbbone = thumb.bone(Leap.Bone.TYPE_DISTAL)
        
        distances = []           
        if (thumbbone.is_valid):
            next(iterfingers)
            distances = []
            for finger in iterfingers:
                fingerbone = finger.bone(Leap.Bone.TYPE_DISTAL)                                        
                if (fingerbone.is_valid):                        
                    distances += [fingerbone.next_joint.distance_to(thumbbone.next_joint)]
            minDistance = min(distances)
        
        if distances == [] or minDistance > 45:
            return -1
        
        return distances.index(minDistance)

    """ Calculate distance of farthest finger tip"""
    def findHighestFinger(self):
        distances = []
        interaction_box = self.__hand__.frame.interaction_box
        return interaction_box.normalize_point(self.__hand__.palm_position)

    """ Returns a value between 0 and 1, 0 being a closed and 1 being an open palm """
    def findPalmState(self):
        distance = 0
        valid_fingers = 0

        for finger in self.__hand__.fingers:
            fingerbone = finger.bone(Leap.Bone.TYPE_DISTAL)                                        
            if (fingerbone.is_valid):                        
                distance += fingerbone.next_joint.distance_to(self.__hand__.palm_position)
                valid_fingers += 1

        return cutoff((distance / valid_fingers + palm_offset) * palm_gain, 0.0, 100.0) / 100.0
