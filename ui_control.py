
from queue import Queue

from aqt import mw
from aqt.qt import QTimer

facecontrol_queue = Queue()

def scrollUp():
    mw.web.eval("""
        var currentOffset = window.pageYOffset;
        var newOffset = Math.max(0, currentOffset - 100);
        window.scrollTo({ top: newOffset, behavior: 'smooth' });
    """)

def scrollDown():
    mw.web.eval("""
        var currentOffset = window.pageYOffset;
        var newOffset = currentOffset + 100;
        window.scrollTo({ top: newOffset, behavior: 'smooth' });
    """)

def process_ui_queue():
    if mw is not None and mw.state == "review":
        if not facecontrol_queue.empty():
            command = facecontrol_queue.get()
            if command in ["Again", "Hard", "Good", "Easy"]:
                if mw.reviewer.state == "question":
                    mw.reviewer.onEnterKey()
                else:
                    if command == "Again":
                        mw.reviewer._answerCard(1)
                    elif command == "Hard":
                        mw.reviewer._answerCard(2)
                    elif command == "Good":
                        mw.reviewer._answerCard(3)
                    elif command == "Easy":
                        mw.reviewer._answerCard(4)

            elif command[0] == "space":
                mw.reviewer.onEnterKey()
            elif command[0] == "undo":
                if mw.undo_actions_info().can_undo:
                    mw.undo()
            elif command[0] == "scrollUp":
                scrollUp()
            elif command[0] == "scrollDown":
                scrollDown()

facecontrol_timer = QTimer()
facecontrol_timer.timeout.connect(process_ui_queue)
facecontrol_timer.start(100)
