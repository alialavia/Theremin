import Leap
from helpers import cutoff
palm_offset = -60.0
palm_gain = 2.0


class LeapEventListener(Leap.Listener):
    '''Leap Event Listener'''
    def __init__(self):
        self.leftHandHandler = None
        self.rightHandHandler = None
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
                    if self.leftHandHandler is not None:
                        self.leftHandHandler(hand)
                else:
                    if self.rightHandHandler is not None:
                        self.rightHandHandler(hand)


class HandProcessor(object):
    '''Hand Processor

    Dispatches left hand and right hand events.
    '''
    def __init__(self):
        self.listener = LeapEventListener()
        self.controller = Leap.Controller()
        self.controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    def run(self):
        self.controller.add_listener(self.listener)

    def attach_left_event_handler(self, handler):
        self.listener.leftHandHandler = handler

    def attach_right_event_handler(self, handler):
        self.listener.rightHandHandler = handler


class HandState(object):
    '''Hand State

    Gets a hand object and store and convert its attributes of interest.
    '''

    def __init__(self, hand):
        self._hand = hand
        self.PalmPosition = self.find_highest_finger()
        self.Pinch = self.find_pinch()
        self.PalmState = self.find_palm_state()

    def get_hand(self):
        '''Get the hand object assigned to this HandState object.'''
        return self._hand

    def find_pinch(self):
        '''Find the pinching finger. Returns -1 if no pinch is found.'''
        iterfingers = iter(self._hand.fingers)
        thumb = self._hand.fingers[0]
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

    def find_highest_finger(self):
        '''Calculate distance of farthest finger tip.'''
        distances = []
        interaction_box = self._hand.frame.interaction_box
        vector = interaction_box.normalize_point(self._hand.palm_position)
        return vector.x, vector.y, vector.z

    def find_palm_state(self):
        """Returns a value in the range [0., 1.]. 0. being a closed and 1.
        being an open palm.
        """
        distance = 0
        validFingers = 0

        for finger in self._hand.fingers:
            fingerbone = finger.bone(Leap.Bone.TYPE_DISTAL)
            if (fingerbone.is_valid):
                distance += fingerbone.next_joint.distance_to(self._hand.palm_position)
                validFingers += 1

        val = (distance / validFingers + palm_offset) * palm_gain
        return cutoff(val, 0.0, 100.0) / 100.0
