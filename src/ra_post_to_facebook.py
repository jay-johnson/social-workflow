import sys, uuid
from datetime                       import datetime, date, timedelta

sys.path.append("/flowstacks/public-cloud-src")
from logger.logger import Logger
from modules.base_api.fs_web_tier_base_work_item     import FSWebTierBaseWorkItem
from connectors.redis.redis_pickle_application       import RedisPickleApplication
import facebook

class RA_PostToFacebook(FSWebTierBaseWorkItem):

    def __init__(self, json_data):
        FSWebTierBaseWorkItem.__init__(self, "RA_PTF", json_data)

        # INPUTS:
        self.m_user_token                       = str(json_data['User Token'])
        self.m_post_text                        = str(json_data['Post Text'])
        
        # OUTPUTS:
        self.m_results["Status"]                = "FAILED"

    # end of  __init__


###############################################################################
#
# Request Handle Methods
#
###############################################################################


    def handle_startup(self):

        self.lg("Start Handle Startup", 5)

        self.handle_post_to_facebook()

        self.lg("Done Startup State(ENDING)", 5)

        return None
    # end of handle_startup

    def handle_post_to_facebook(self):
        self.lg("Starting handle_posting_to_facebook", 5)
        user_token = self.m_user_token
        post_text = self.m_post_text
        graph = facebook.GraphAPI(user_token)
        graph.put_object('me', 'feed', message=post_text)

        self.lg("Done handle_posting_to_facebook", 5)
        self.m_status['Results'] = 'SUCCESS'
        
    
###############################################################################
#
# Helpers
#
###############################################################################


###############################################################################
#
# Request State Machine
#
###############################################################################


    # Needs to be state driven:
    def perform_task(self):

        if  self.m_state == "Startup":

            self.handle_startup()

            # found in the base
            self.lg("Result Cleanup", 5)
            self.base_handle_results_and_cleanup(self.m_result_details, self.m_completion_details)

        else:
            if self.m_log:
                self.lg("UNKNOWN STATE FOUND IN OBJECT(" + self.m_name + ") State(" + self.m_state + ")", 0)
            self.m_state = "Startup"

        # end of State Loop
        return self.m_is_done
    # end of perform_task

# end of RA_PostStatusToFacebook


