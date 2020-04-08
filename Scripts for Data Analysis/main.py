import os
import analyzer


def data_elaboration(path, scenario_name, scenarios_results):
    # list all the folders in the current directory
    folders = []

    for entry in os.listdir(path):
        if os.path.isdir(os.path.join(path, entry)):
            folders.append(entry)

    # if this directory doesn't have any subdirectory then we're in the .sca and .vec folder
    if len(folders) == 0:
        print("path = " + path + ", scenario = " + scenario_name)

        # run the scenario analysis for the current scenario and then exit
        scenarios_results.append([scenario_name, analyzer.analyze_scenario(path + "\\" + scenario_name)])
        return

    # browse through the tiers of folders and convert the path into the scenario_name
    for folder in folders:
        # first tier - policy
        if folder == "P1":
            data_elaboration(path + "\\" + folder, ",1" + scenario_name, scenarios_results)
        if folder == "P2":
            data_elaboration(path + "\\" + folder, ",2" + scenario_name, scenarios_results)

        # second tier - distribution for service times
        if folder == "exp":
            data_elaboration(path + "\\" + folder, "-0" + scenario_name, scenarios_results)
        if folder == "logn":
            data_elaboration(path + "\\" + folder, "-1" + scenario_name, scenarios_results)
        if folder == "normal":
            data_elaboration(path + "\\" + folder, "-2" + scenario_name, scenarios_results)

        # third tier - workload
        if folder == "high":
            data_elaboration(path + "\\" + folder, "high_load*" + scenario_name, scenarios_results)
        if folder == "low":
            data_elaboration(path + "\\" + folder, "low_load*" + scenario_name, scenarios_results)
        if folder == "med":
            data_elaboration(path + "\\" + folder, "med_load*" + scenario_name, scenarios_results)
        if folder == "high_low_delta":
            data_elaboration(path + "\\" + folder, "high_load*_closeTills" + scenario_name[:-2], scenarios_results)
        if folder == "low_low_delta":
            data_elaboration(path + "\\" + folder, "low_load*_closeTills" + scenario_name[:-2], scenarios_results)
        if folder == "med_low_delta":
            data_elaboration(path + "\\" + folder, "med_load*_closeTills" + scenario_name[:-2], scenarios_results)

        # fourth tier - number of tills
        if folder == "few":
            scenario_name_parts = scenario_name.split("*")
            data_elaboration(path + "\\" + folder, scenario_name_parts[0] + "_1" + scenario_name_parts[1],
                             scenarios_results)
        if folder == "many":
            scenario_name_parts = scenario_name.split("*")
            data_elaboration(path + "\\" + folder, scenario_name_parts[0] + "_2" + scenario_name_parts[1],
                             scenarios_results)

def main():
    # create output folder if it does not exists
    if not os.path.exists("out"):
        os.makedirs("out")

    # create output folder for correlograms if it does not exists
    if not os.path.exists("correlograms"):
        os.makedirs("correlograms")
        
    # create one file per performance index per metric in which C.I. and name of the scenario will be put as .csv records
    response_time_mean_value_file = open(".\\out\\response_time_mean_value.csv", "a+")
    response_time_lcg_file = open(".\\out\\response_time_lcg.csv", "a+")
    response_time_median_file = open(".\\out\\response_time_median.csv", "a+")
    response_time_1st_quartile_file = open(".\\out\\response_time_1st_quartile.csv", "a+")
    response_time_3rd_quartile_file = open(".\\out\\response_time_3rd_quartile.csv", "a+")
    response_time_98th_percentile_file = open(".\\out\\response_time_98th_percentile.csv", "a+")

    wait_time_mean_value_file = open(".\\out\\wait_time_mean_value.csv", "a+")
    wait_time_lcg_file = open(".\\out\\wait_time_lcg.csv", "a+")
    wait_time_median_file = open(".\\out\\wait_time_median.csv", "a+")
    wait_time_1st_quartile_file = open(".\\out\\wait_time_1st_quartile.csv", "a+")
    wait_time_3rd_quartile_file = open(".\\out\\wait_time_3rd_quartile.csv", "a+")
    wait_time_98th_percentile_file = open(".\\out\\wait_time_98th_percentile.csv", "a+")
    
    num_customers_mean_value_file = open(".\\out\\num_customers_mean_value.csv", "a+")
    
    # start the data analysis
    scenarios_results = []
    data_elaboration("..\\Simulations", "", scenarios_results)

    # write data in the correct file to be displayed
    # scenario[0]               : name of the scenario
    # scenario[1]               : confidence intervals
    #   - scenario[1][x]        : confidence intervals for performance index 'x'
    #       - scenario[1][x][0] : lower boundary
    #       - scenario[1][x][1] : upper boundary

    for scenario in scenarios_results:
        response_time_mean_value_file.write(str(scenario[0]) + ";" + str(scenario[1][0][0]) + ";" + str(scenario[1][0][1]) + "\n")
        response_time_lcg_file.write(str(scenario[0]) + ";" + str(scenario[1][1][0]) + ";" + str(scenario[1][1][1]) + "\n")
        response_time_median_file.write(str(scenario[0]) + ";" + str(scenario[1][2][0]) + ";" + str(scenario[1][2][1]) + "\n")
        response_time_1st_quartile_file.write(str(scenario[0]) + ";" + str(scenario[1][3][0]) + ";" + str(scenario[1][3][1]) + "\n")
        response_time_3rd_quartile_file.write(str(scenario[0]) + ";" + str(scenario[1][4][0]) + ";" + str(scenario[1][4][1]) + "\n")
        response_time_98th_percentile_file.write(str(scenario[0]) + ";" + str(scenario[1][5][0]) + ";" + str(scenario[1][5][1]) + "\n")

        wait_time_mean_value_file.write(str(scenario[0]) + ";" + str(scenario[1][6][0]) + ";" + str(scenario[1][6][1]) + "\n")
        wait_time_lcg_file.write(str(scenario[0]) + ";" + str(scenario[1][7][0]) + ";" + str(scenario[1][7][1]) + "\n")
        wait_time_median_file.write(str(scenario[0]) + ";" + str(scenario[1][8][0]) + ";" + str(scenario[1][8][1]) + "\n")
        wait_time_1st_quartile_file.write(str(scenario[0]) + ";" + str(scenario[1][9][0]) + ";" + str(scenario[1][9][1]) + "\n")
        wait_time_3rd_quartile_file.write(str(scenario[0]) + ";" + str(scenario[1][10][0]) + ";" + str(scenario[1][10][1]) + "\n")
        wait_time_98th_percentile_file.write(str(scenario[0]) + ";" + str(scenario[1][11][0]) + ";" + str(scenario[1][11][1]) + "\n")
        num_customers_mean_value_file.write(str(scenario[0]) + ";" + str(scenario[1][12][0]) + ";" + str(scenario[1][12][1]) + "\n")


if __name__ == "__main__":
    main()
