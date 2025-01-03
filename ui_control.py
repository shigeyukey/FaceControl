
from queue import Queue

from aqt import mw
from aqt.qt import QTimer

from aqt.utils import tooltip

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
    if mw is None:
        return
    if mw.state == "review":
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

            elif command == "space":
                mw.reviewer.onEnterKey()
            elif command == "undo":
                if mw.undo_actions_info().can_undo:
                    mw.undo()
            elif command == "scrollUp":
                scrollUp()
            elif command == "scrollDown":
                scrollDown()

    elif mw.state in ["deckBrowser", "overview"]:
        if not facecontrol_queue.empty():
            command = facecontrol_queue.get()
            if command not in ["scrollUp", "scrollDown"]:
                tooltip(f"{command} (test)")

facecontrol_timer = QTimer()
facecontrol_timer.timeout.connect(process_ui_queue)
facecontrol_timer.start(100)
