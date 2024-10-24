import azure.functions as func
import logging
import mimetypes
import json
from utils.models import *
from src.apis import *


global token_instance
token_instance = TokenManager()


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="zohotrigger")
def zohotrigger(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # Returns /projectRoot/functionName/static/index.html
    carrierID = req.params.get('carrierID')
    jobID = req.params.get('jobID')
    carriername = req.params.get('carriername')
    filename = f"{context.function_directory}/static/index.html"
    try:
            with open(filename, 'r') as f:
                html_content = f.read()
            
            # Replace placeholders with actual values
            html_content = html_content.replace("{{carrierID}}", carrierID)
            html_content = html_content.replace("{{jobID}}", jobID)
            html_content = html_content.replace("{{carriername}}", carriername)
            
            # Return the modified HTML
            mimetype = mimetypes.guess_type(filename)
            return func.HttpResponse(html_content, mimetype=mimetype[0])
        
    except Exception as e:
        logging.error(f"Error reading or processing the HTML file: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)

@app.route(route="create-quotes")
def zohoquotes(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    token = token_instance.get_access_token()
    logging.info(req.get_json())

    data = req.get_json()

    quotes = Quotes(
        Estimated_Amount = data.get('estimatedAmount'),
        Delivery_Date_Range = data.get('deliveryDate'),
        Dropoff_Location = data.get('dropoffLocation'),
        pickup_location = data.get('pickupLocation'),
        pickup_date_range = data.get('estimatedPickup'),
        Carriers = data.get('carrierid'),
        Transport_Job_in_Deal = data.get('jobid'),
        Name = data.get('carrierid'),
    )
    logging.info(dict(quotes))

    response = create_quotes(dict(quotes), token)
    logging.info(response.json())

    try:
        if response.status_code == 201:
            # Instead of returning HTML here, we return a simple JSON response.
            return func.HttpResponse(
                json.dumps({"message": "Quote created successfully", "redirect_url": f"https://crm.zohocloud.ca/crm/org110000402423/tab/Deals/{data.get('jobid')}"}),
                mimetype="application/json",
                status_code=200
            )
        else:
            return func.HttpResponse(
                json.dumps({"error": "Something went wrong, please try again."}),
                mimetype="application/json",
                status_code=400
            )

    except Exception as e:
        logging.error(f"Error creating the quote: {e}")
        error_data = {"error": str(e)}
        return func.HttpResponse(json.dumps(error_data), mimetype="application/json", status_code=500)