from flask import Flask, render_template, abort, jsonify
import requests


app = Flask(__name__)

#address of my webservice where the statistics are obtained from.
STATISTICS_PATH = "http://127.0.0.1:5001"


@app.route('/statistics', methods=['GET'])
def stats_all():

    #TODO: logic for actually getting the user_id over here and checking whether the user is loggedin.
    #can be taken from the original file
    user_id = 1

    #perform a request to the statistics web server

    try:
        stats_request = requests.get(url=STATISTICS_PATH + "/users/" + str(user_id) + "/statistics")
        if (stats_request.status_code == 404):
            return abort(404, "User not found for the user ID supplied.")

    except requests.exceptions.RequestException:
        return abort(503, "The 'statistics' microservice on which this application depends on is not available. Please, try again later.")

    #Fine, we managed to get the statistics successfully. We now need to return them to the HTML page
    #just a dictionary, can get elements from it
    stats_response = stats_request.json()

    distance_array = stats_response["distance_array"]
    average_speed_array = stats_response["average_speed_array"]
    average_heart_rate_array = stats_response["average_heart_rate_array"]
    elevation_gain_array = stats_response["elevation_gain_array"]
    elapsed_time_array = stats_response["elapsed_time_array"]
    run_names_array = stats_response["run_names_array"]
    run_ids_array = stats_response["run_ids_array"]

    run_names_concatenated = concatenate_run_name_id(run_names_array, run_ids_array)


    return render_template("statistics_js.html", distance_array=distance_array, average_speed_array=average_speed_array, average_heart_rate_array=average_heart_rate_array,
                    elevation_gain_array=elevation_gain_array, elapsed_time_array=elapsed_time_array, run_names_concatenated=run_names_concatenated)


def concatenate_run_name_id(run_names, run_ids):
    run_names_concatenated = []
    for run_id, run_name in zip(run_ids, run_names):
        run_names_concatenated.append(str(run_id) + "_" + run_name)
    return run_names_concatenated




if __name__ == '__main__':
    app.run()
