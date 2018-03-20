from chatterbot.output import OutputAdapter
import subprocess

class LiepaTtsAdapter(OutputAdapter):
    """
    A adapter that allows ChatterBot to
    generate audio voice signal. It is used liepa TTS.
    """

    def process_response(self, statement, session_id=None):
        """
        Print the response to the user's input.
        """
        # this is liepa TTS on local box. I should compile it to be part of this sample
        subprocess.check_output(['tark-win-lt', statement.text])
        # Use logging instead!
        print("[LiepaTtsAdapter]Computer says: : " + statement.text)
        return statement.text
