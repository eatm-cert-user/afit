##
# Input class.
# Get Input techniques and method to refresh result.
#
class Input:
    techniques = []
    refresh_result = lambda x: x

    ##
    # Input set_techniques static method.
    # Set input technique list.
    #
    @staticmethod
    def set_techniques(list_view):
        Input.techniques = list_view

    ##
    # Input get_techniques static method.
    # Return input technique list.
    # @return ListView
    @staticmethod
    def get_techniques():
        return Input.techniques
