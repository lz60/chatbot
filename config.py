

#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from dotenv import load_dotenv

# For local development, load the environment variables stored in the (not distributed) .env file
# For deployment on Azure, environment variables are loaded automatically from app settings

load_dotenv()

class DefaultConfig:
    """ Bot Configuration """
    # Port 
    PORT = 3978  
    
    # Azure bot ID (if you are deploying with Azure Bot resource)
    APP_ID = os.environ.get("MicrosoftAppId", "")  
    
    # Azure bot password (if you are deploying with Azure Bot resource)
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")  
    
    # LUIS app ID
    LUIS_APP_ID = os.environ.get("LuisAppId", "871ac5ee-9231-4e07-bbdd-9b3038148ca1")  
    
    # Authoring or prediction LUIS app key
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "d936015d362f443dab9e07de619ee3d6")  
    
    # Authoring or prediction LUIS app endpoint
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "https://chatbotvoyage-authoring.cognitiveservices.azure.com/")
    APP_PASSWORD = os.environ.get("LuisAPIHostName", " ")
    APP_ID = os.environ.get("LuisAPIHostName", " ")
	 
    
    # Application Insights instrumentation key
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY", "b0c4a284-4666-42f1-9c69-827b6e186019")